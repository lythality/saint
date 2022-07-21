from webbrowser import get

import clang.cindex
from clang.cindex import TypeKind, CursorKind

import re


ARCHITECTURE_BITS = 16


def getTokenString(n):
    if n is None:
        return "NONE"
    ret = ""
    for token in n.get_tokens():
        ret += token.spelling
    return ret


def isConstCharType(n):
    typename = n.type.spelling
    return "const" in typename and "char" in typename and \
        ("*" in typename or "[" in typename)


def hasConstCharTypeConstants(n):
    if n.kind.name == "STRING_LITERAL":
        return True
    for c in n.get_children():
        if hasConstCharTypeConstants(c):
            return True
    return False


def is_assignment(n):
    return "=" in getTokenString(n)


def is_non_obvious_sign(name):
    global ARCHITECTURE_BITS
    try:
        return int(name, 0) > 2 ** (ARCHITECTURE_BITS - 1) - 1
    except ValueError:
        pass


def isOctet(text: str) -> bool:
    return re.match(r"^0[0-7]+$", text)


def isLowerLongCharUsed(text: str) -> bool:
    return "l" in text


def print_info(n, tab: int):
    print('\t' * tab, end="")
    print(n.kind, end="")
    print(" : ", end="")
    print(n.type.spelling, end="")
    print(" :: ", end="")
    print(n.spelling, end="")
    print(" :: ", end="")
    print(is_global_var(n), end="")
    print(" - ", end="")
    print(is_static_var(n), end="")
    print(" :: ", end="")
    print(getTokenString(n), end="")
    print("")


def hook_integer_literal(n: CursorKind):
    text = ""
    for t in n.get_tokens():
        text = text + t.spelling
    print(" > OCTET IS USED\n" if isOctet(text) else "", end="")
    print(" > LOWER LONG IS USED\n" if isLowerLongCharUsed(text) else "", end="")
    print(" > non-obvious signed int is used\n" if is_non_obvious_sign(text) else "", end="")


# trigraph ??' may used in C code as ??\', we take care of it
trigraph_strings = ['??=', '??(', '??/', '??)', '??\\\'', '??<', '??!', '??>', '??-']


def hook_char_literal(n):
    global trigraph_strings
    for tri in trigraph_strings:
        if tri in getTokenString(n):
            print(" > trigraph " + tri + " shall not be used")


def hook_string_literal(n):
    global trigraph_strings
    for tri in trigraph_strings:
        if tri in getTokenString(n):
            print(" > trigraph " + tri + " shall not be used")


def hook_expression(n: CursorKind):
    if is_assignment(n):
        if not isConstCharType(n):
            if hasConstCharTypeConstants(n):
                print(" > const char is assigned on non const char type")


def get_bitfield_size(n):
    for c in n.get_children():
        if c.kind == CursorKind.INTEGER_LITERAL:
            text = ""
            for t in c.get_tokens():
                text = text + t.spelling
            return int(text)
    return None


def hook_field_decl(n: CursorKind):
    kind_of_type = n.type.get_canonical().kind

    # checking whether it has correct type
    if kind_of_type == TypeKind.UINT or kind_of_type == TypeKind.UCHAR \
            or kind_of_type == TypeKind.CHAR_U or kind_of_type == TypeKind.USHORT \
            or kind_of_type == TypeKind.BOOL:
        # other types shall be a problem
        pass
    elif kind_of_type == TypeKind.INT or kind_of_type == TypeKind.CHAR16 \
            or kind_of_type == TypeKind.CHAR32 or kind_of_type == TypeKind.SHORT:
        if "signed" not in getTokenString(n):
            print(" > bit-field does not allow just int short char .... use signed keyword")
    else:
        print(" > bit-field only allows limited types (int, uint, short, ushort, char, uchar, bool)")

    # checking whether it does not have signed 1 bit
    if "signed" in getTokenString(n) and get_bitfield_size(n) == 1:
        print(" > The size of signed bit-field shall be greater than 1")


def collect_decl_var_names(n, names):
    if n.kind == CursorKind.VAR_DECL:
        names.append(n.spelling)

    # iterate recursively
    for c in n.get_children():
        if c.kind == CursorKind.COMPOUND_STMT:
            continue
        collect_decl_var_names(c, names)


var_names_scope = []


def traverse(n, i=0):
    global var_names_scope
    print_info(n, i)

    var_names_inside_comp_stmt = []
    if n.kind == CursorKind.COMPOUND_STMT:
        collect_decl_var_names(n, var_names_inside_comp_stmt)
        # check intersection
        intersection = list(set(var_names_scope) & set(var_names_inside_comp_stmt))
        if intersection:
            print(" > same var name is used in inner scope")
            var_names_inside_comp_stmt = list(set(var_names_inside_comp_stmt) - set(intersection))
        var_names_scope.extend(var_names_inside_comp_stmt)

    if n.kind == CursorKind.COMPOUND_STMT:
        collect_decl_var_names(n, var_names_inside_comp_stmt)
        var_names_scope.extend(var_names_inside_comp_stmt)

    if n.kind == CursorKind.INTEGER_LITERAL:
        hook_integer_literal(n)

    if n.kind == CursorKind.FIELD_DECL:
        hook_field_decl(n)

    if n.kind == CursorKind.CHARACTER_LITERAL:
        hook_char_literal(n)

    if n.kind == CursorKind.STRING_LITERAL:
        hook_string_literal(n)

    if n.kind.is_expression():
        hook_expression(n)

    # iterate recursively
    for c in n.get_children():
        traverse(c, i+1)

    if n.kind == CursorKind.COMPOUND_STMT:
        var_names_scope = list(set(var_names_scope) - set(var_names_inside_comp_stmt))

    post_visit(n)


names_typedef = []
names_external_vars = []
names_internal_vars = []
names_local_vars = []
names_field_names = []
names_tags = []


# name : token_string
found_tag = {}


def post_visit(n):
    global names_typedef
    global names_external_vars
    global names_internal_vars
    global names_local_vars
    global names_field_names
    global names_tags

    if n.kind == CursorKind.TYPEDEF_DECL:
        names_typedef.append(n.type.spelling)
    elif n.kind == CursorKind.VAR_DECL:
        if is_global_var(n) and not is_static_var(n):
            names_external_vars.append(n.spelling)
        elif is_global_var(n) and is_static_var(n):
            names_internal_vars.append(n.spelling)
        else:
            names_local_vars.append(n.spelling)
    elif n.kind == CursorKind.STRUCT_DECL:
        tag = n.type.spelling
        definition = getTokenString(n)
        if "unnamed struct at " in tag:
            print(" > duplicated tag name in " + definition)
        elif tag in found_tag and found_tag[tag] == definition:
            pass
        else:
            found_tag[tag] = definition
            names_tags.append(tag)
    elif n.kind == CursorKind.FIELD_DECL:
        names_field_names.append(n.spelling)


def is_global_var(n):
    if n.semantic_parent is None:
        return False
    elif n.semantic_parent.kind == CursorKind.TRANSLATION_UNIT:
        return True
    return False


def is_static_var(n):
    return "static" in getTokenString(n.get_definition())


def get_dict_from_list(my_list):
    new_dict = {}
    for e in my_list:
        try: new_dict[e] +=1
        except: new_dict[e] = 1
    return new_dict


def post_check():
    global names_typedef
    global names_external_vars
    global names_internal_vars
    global names_local_vars
    global names_field_names
    global names_tags

    print(names_typedef)
    print(names_external_vars)
    print(names_internal_vars)
    print(names_local_vars)
    print(names_field_names)
    print(names_tags)

    names_vars = list(set(names_external_vars) | set(names_internal_vars) | set(names_local_vars)
                      | set(names_field_names))

    # checking rule 5.6 (typedef name - unique)
    for v in list(set(names_typedef) & set(names_vars)):
        print(" > typedef name " + v + " is not unique")

    # checking rule 5.7 (tag name - unique)
    for key in get_dict_from_list(names_tags).keys():
        if get_dict_from_list(names_tags)[key] > 1:
            print(" > tag name " + key + " is not unique")

    # checking rule 5.8 (external var name - unique)
    for v in list(set(names_external_vars) & set(names_internal_vars)):
        print(" > extern var name " + v + " is not unique")
    for v in list(set(names_external_vars) & set(names_local_vars)):
        print(" > extern var name " + v + " is not unique")

    # checking rule 5.9 (internal var name - unique)
    for v in list(set(names_internal_vars) & set(names_local_vars)):
        print(" > static var name " + v + " is not unique")


def start_saint(srcfile: str):
    clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')

    index = clang.cindex.Index.create()
    translation_unit = index.parse(srcfile, ['-x', 'c++'])
    traverse(translation_unit.cursor)

    print(dir(translation_unit.cursor))

    post_check()
