from webbrowser import get

import clang.cindex
from clang.cindex import TypeKind, CursorKind

from code_info import SWorkspace
from code_info.util import getTokenString

import re

from rule_checker.array_init_check import check_array_init, is_array, get_array_size_list


ARCHITECTURE_BITS = 16


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


# trigraph ??' may used in C code as ??\', we take care of it
trigraph_strings = ['??=', '??(', '??/', '??)', '??\\\'', '??<', '??!', '??>', '??-']



def get_bitfield_size(n):
    for c in n.get_children():
        if c.kind == CursorKind.INTEGER_LITERAL:
            text = ""
            for t in c.get_tokens():
                text = text + t.spelling
            return int(text)
    return None




def collect_decl_var_names(n, names):
    if n.kind == CursorKind.VAR_DECL:
        names.append(n.spelling)

    # iterate recursively
    for c in n.get_children():
        if c.kind == CursorKind.COMPOUND_STMT:
            continue
        collect_decl_var_names(c, names)


var_names_scope = []


external_vars = []


names_typedef = []
names_external_vars = []
names_internal_vars = []
names_local_vars = []
names_field_names = []
names_tags = []


# name : token_string
found_tag = {}



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
        try: new_dict[e] += 1
        except: new_dict[e] = 1
    return new_dict


class RuleChecker(SWorkspace):

    def hook_enter_comp_stmt(self, n: CursorKind, var_names_inside_comp_stmt):
        global var_names_scope
        collect_decl_var_names(n, var_names_inside_comp_stmt)
        # check intersection
        intersection = list(set(var_names_scope) & set(var_names_inside_comp_stmt))
        if intersection:
            print(" > same var name is used in inner scope")
            var_names_inside_comp_stmt = list(set(var_names_inside_comp_stmt) - set(intersection))
        var_names_scope.extend(var_names_inside_comp_stmt)

        collect_decl_var_names(n, var_names_inside_comp_stmt)
        var_names_scope.extend(var_names_inside_comp_stmt)

    def hook_exit_comp_stmt(self, n: CursorKind, var_names_inside_comp_stmt):
        global var_names_scope
        var_names_scope = list(set(var_names_scope) - set(var_names_inside_comp_stmt))

    def post_visit(self, n):
        global names_typedef
        global names_external_vars
        global names_internal_vars
        global names_local_vars
        global names_field_names
        global names_tags
        global external_vars

        if n.kind == CursorKind.TYPEDEF_DECL:
            names_typedef.append(n.type.spelling)
        elif n.kind == CursorKind.VAR_DECL:
            if is_global_var(n) and not is_static_var(n):
                names_external_vars.append(n.spelling)
                external_vars.append(n)
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

    def post_check(self):
        global names_typedef
        global names_external_vars
        global names_internal_vars
        global names_local_vars
        global names_field_names
        global names_tags
        global external_vars

        print(names_typedef)
        print(names_external_vars)
        print(names_internal_vars)
        print(names_local_vars)
        print(names_field_names)
        print(names_tags)
        print(external_vars)

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

        # linkage check
        for i in range(0,len(external_vars)):
            for j in range(i+1, len(external_vars)):
                if i == j:
                    continue
                elif external_vars[i].mangled_name == external_vars[j].mangled_name:
                    print(" >>> SAME var " + str(external_vars[i].mangled_name) + " " + str(external_vars[i].spelling) + " :: " + external_vars[j].spelling)

        # checking rule 3.[1,2] - no_in_comments, no_in_comments_2
        for c in self.comments:
            comment_text = c.spelling
            if comment_text.startswith("//"):
                comment_text = comment_text[2:]
                if "\\" in comment_text:
                    print(" > line splicing shall not be used in one-line comment: " + comment_text)
            elif comment_text.startswith("/*"):
                comment_text = comment_text[2:-2]
            else:
                print(" > unknown comment")

            if "/*" in comment_text or "//" in comment_text:
                print(" > /* or // shall not be used within comment: " + comment_text)

        # checking rule 4.2 - no_trigraph
        global trigraph_strings
        for tri in trigraph_strings:
            for s in self.string_literal:
                if tri in getTokenString(s):
                    print(" > trigraph " + tri + " shall not be used")

        # checking rule 6.1 - bit_field_type are restricted
        for n in self.field_decl:
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

        # checking rule 6.2 - signed_bit_field shall have more than 1 bit
        for n in self.field_decl:
            if "signed" in getTokenString(n) and get_bitfield_size(n) == 1:
                print(" > The size of signed bit-field shall be greater than 1")

        # checking rule 7.1 - no octal
        for n in self.integer_literal:
            print(" > OCTET IS USED\n" if isOctet(getTokenString(n)) else "", end="")

        # checking rule 7.2 - put u to all non-obvious signed integer
        for n in self.integer_literal:
            print(" > non-obvious signed int is used\n" if is_non_obvious_sign(getTokenString(n)) else "", end="")

        # checking rule 7.3 - no_lower_long_char
        for n in self.integer_literal:
            print(" > LOWER CASE LONG CHAR L IS USED\n" if isLowerLongCharUsed(getTokenString(n)) else "", end="")

        # checking rule 7.4 - string only can be const char*
        for n in self.expression:
            if is_assignment(n):
                if not isConstCharType(n):
                    if hasConstCharTypeConstants(n):
                        print(" > const char is assigned on non const char type")

        # checking rule 8.10 - static inline
        for n in self.function_decl:
            signature = getTokenString(n)
            if signature.startswith("inline") or signature.startswith("externinline"):
                print(" > an inline function shall be declared as static inline")

        # checking rule 8.11 - extern array should have size
        for n in self.var_decl:
            signature = getTokenString(n)
            if signature.startswith("extern") and is_array(n):
                dimension = n.type.spelling.count("[")
                if dimension != len(get_array_size_list(n)):
                    print(" > extern array should have all size: "+n.spelling)

        # checking rule 8.12 - enum check
        for n in self.enum_decl:
            enum_dict_implicit = {}
            enum_dict_explicit = {}
            enum_prev_value = 0
            # iterate constant
            for c in n.get_children():
                enum_const_text = getTokenString(c)
                if "=" in enum_const_text:
                    enum_name = enum_const_text.split("=")[0]
                    enum_value = int(enum_const_text.split("=")[1])
                    enum_dict_explicit[enum_name] = enum_value
                else:
                    enum_name = enum_const_text
                    enum_value = enum_prev_value+1
                    enum_dict_implicit[enum_name] = enum_value
                enum_prev_value = enum_value
            for key_ex, value_ex in enum_dict_explicit.items():
                print(key_ex)
                for key_im, value_im in enum_dict_implicit.items():
                    if value_ex == value_im:
                        print(" > enum contains duplicated constant for "+key_ex+" = "+key_im+" = "+str(value_im))

        # checking rule 9.[2,3,4,5] - array init check
        internal_array_vars = list(filter(lambda v: is_array(v) and not getTokenString(v).startswith("extern"),
                                          self.var_decl))
        check_array_init(internal_array_vars)
