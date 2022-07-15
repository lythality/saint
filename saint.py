import clang.cindex

import re


ARCHITECTURE_BITS = 16


def getTokenString(n):
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
    print(getTokenString(n), end="")
    print("")


def hook_integer_literal(n: clang.cindex.CursorKind):
    text = ""
    for t in n.get_tokens():
        text = text + t.spelling
    print(" > OCTET IS USED\n" if isOctet(text) else "", end="")
    print(" > LOWER LONG IS USED\n" if isLowerLongCharUsed(text) else "", end="")
    print(" > non-obvious signed int is used\n" if is_non_obvious_sign(text) else "", end="")


def hook_expression(n: clang.cindex.CursorKind):
    if is_assignment(n):
        if not isConstCharType(n):
            if hasConstCharTypeConstants(n):
                print(" > const char is assigned on non const char type")


def collect_decl_var_names(n, names):
    if n.kind == clang.cindex.CursorKind.VAR_DECL:
        names.append(n.spelling)

    # iterate recursively
    for c in n.get_children():
        if c.kind == clang.cindex.CursorKind.COMPOUND_STMT:
            continue
        collect_decl_var_names(c, names)


var_names_scope = []


def traverse(n, i=0):
    global var_names_scope
    print_info(n, i)

    var_names_inside_comp_stmt = []
    if n.kind == clang.cindex.CursorKind.COMPOUND_STMT:
        collect_decl_var_names(n, var_names_inside_comp_stmt)
        # check intersection
        intersection = list(set(var_names_scope) & set(var_names_inside_comp_stmt))
        if intersection:
            print(" > same var name is used in inner scope")
            var_names_inside_comp_stmt = list(set(var_names_inside_comp_stmt) - set(intersection))
        var_names_scope.extend(var_names_inside_comp_stmt)

    if n.kind == clang.cindex.CursorKind.COMPOUND_STMT:
        collect_decl_var_names(n, var_names_inside_comp_stmt)
        var_names_scope.extend(var_names_inside_comp_stmt)

    if n.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        hook_integer_literal(n)

    if n.kind.is_expression():
        hook_expression(n)

    # iterate recursively
    for c in n.get_children():
        traverse(c, i+1)

    if n.kind == clang.cindex.CursorKind.COMPOUND_STMT:
        var_names_scope = list(set(var_names_scope) - set(var_names_inside_comp_stmt))


def start_saint(srcfile: str):
    clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')

    index = clang.cindex.Index.create()
    translation_unit = index.parse(srcfile, ['-x', 'c++'])
    traverse(translation_unit.cursor)
