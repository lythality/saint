import re

from clang.cindex import CursorKind

from code_info.util import getTokenString

from rule_checker.violation import Violation

# Not initialized first.
rule_checker = None


def check_array_init(checker, internal_array_vars):
    global rule_checker
    rule_checker = checker

    # checking rule 9.[2,3,4,5] - array init check
    for n in internal_array_vars:
        dimension = n.type.spelling.count("[")
        arr_size_list = list(reversed(get_array_size_list(n)))
        if dimension != len(arr_size_list):
            if getTokenString(n).count("=") > 1:
                rule_checker.add_violation(Violation(9,5,n.spelling))
            continue

        none_array = get_none_array_of(arr_size_list, 0)
        initializer = get_array_initializer(n)
        assigned_array = assign_initializer_to(none_array, initializer)

        print(n.spelling, assigned_array)

        if has_undefined_element(assigned_array):
            rule_checker.add_violation(Violation(9,3,n.spelling))


def has_undefined_element(assigned_array):
    if type(assigned_array) != list:
        return assigned_array is None
    for element in assigned_array:
        if has_undefined_element(element):
            return True
    return False


def is_array(n:CursorKind):
    return "[" in n.type.spelling


# array size is a list as there are more than one size for n-array
def get_array_size_list(n: CursorKind):
    if not is_array(n):
        return None
    ret = []
    for c in n.get_children():
        if c.kind == CursorKind.INTEGER_LITERAL:
            ret.append(int(getTokenString(c)))
    return ret


def parse_array_initializer(n: CursorKind):
    if n.kind != CursorKind.INIT_LIST_EXPR:
        return getTokenString(n)

    ret = []
    for c in n.get_children():
        ret.append(parse_array_initializer(c))
    return ret


def get_array_initializer(n: CursorKind):
    if not is_array(n):
        return None

    for c in n.get_children():
        if c.kind == CursorKind.INIT_LIST_EXPR:
            return parse_array_initializer(c)

    return None


def check_arr_size(component, arr_size_list, idx):
    if idx >= len(arr_size_list):
        return True

    # not defined item found
    if component is None:
        return False

    if len(component) != arr_size_list[idx]:
        return False

    for element in component:
        if not check_arr_size(element, arr_size_list, idx+1):
            return False
    return True


def get_none_array_of(arr_size_list, idx):
    if idx >= len(arr_size_list):
        return None
    return [get_none_array_of(arr_size_list, idx+1) for _ in range(arr_size_list[idx])]


# The initializer is an array where elements are string. Dimension depend on the array variable.
def assign_initializer_to(none_array, initializer):
    if type(initializer) != list:
        rule_checker.add_violation(Violation(9,2,"(1)"))
        return None

    idx = 0
    for init in initializer:
        if type(init) != list:
            if "=" in init:
                (index, value) = init.split("=")[0], init.split("=")[1]
                index_array = re.split(r"\[|\]", index)
                index_array = list(filter(None, index_array))
                index_array = list(map(lambda x: int(x), index_array))
                assign_at(none_array, index_array, value)
                pass
            else:
                if idx >= len(none_array):
                    print(" > initializer is bigger than the array")
                    break
                elif type(none_array[idx]) == list:
                    rule_checker.add_violation(Violation(9, 2, "(2)"))
                    break
                if none_array[idx]:
                    rule_checker.add_violation(Violation(9, 4, ""))
                none_array[idx] = init
                idx += 1
        else:
            if idx >= len(none_array):
                print(" > initializer is bigger than the array")
                break
            assign_initializer_to(none_array[idx], init)
            idx += 1
    return none_array


def assign_at(none_array, index_array, value):
    if len(index_array) == 1:
        if type(none_array[index_array[0]]) == list:
            rule_checker.add_violation(Violation(9, 2, "(3)"))
            return
        elif none_array[index_array[0]]:
            rule_checker.add_violation(Violation(9, 4, ""))
        none_array[index_array[0]] = value
    else:
        none_array = none_array[index_array[0]]
        index_array = index_array[1:]
        assign_at(none_array, index_array, value)


def check_arr_size(component, arr_size_list, idx):
    if idx >= len(arr_size_list):
        return True

    # not defined item found
    if component is None:
        return False

    if len(component) != arr_size_list[idx]:
        return False

    for element in component:
        if not check_arr_size(element, arr_size_list, idx+1):
            return False
    return True


def get_none_array_of(arr_size_list, idx):
    if idx >= len(arr_size_list):
        return None
    return [get_none_array_of(arr_size_list, idx+1) for _ in range(arr_size_list[idx])]


# The initializer is an array where elements are string. Dimension depend on the array variable.
def assign_initializer_to(none_array, initializer):
    if type(initializer) != list:
        rule_checker.add_violation(Violation(9, 2, "(1)"))
        return None

    idx = 0
    for init in initializer:
        if type(init) != list:
            if "=" in init:
                (index, value) = init.split("=")[0], init.split("=")[1]
                index_array = re.split(r"\[|\]", index)
                index_array = list(filter(None, index_array))
                index_array = list(map(lambda x: int(x), index_array))
                assign_at(none_array, index_array, value)
                pass
            else:
                if idx >= len(none_array):
                    print(" > initializer is bigger than the array")
                    break
                elif type(none_array[idx]) == list:
                    rule_checker.add_violation(Violation(9, 2, "(2)"))
                    break
                if none_array[idx]:
                    rule_checker.add_violation(Violation(9, 4, ""))
                none_array[idx] = init
                idx += 1
        else:
            if idx >= len(none_array):
                print(" > initializer is bigger than the array")
                break
            assign_initializer_to(none_array[idx], init)
            idx += 1
    return none_array


def assign_at(none_array, index_array, value):
    if len(index_array) == 1:
        if type(none_array[index_array[0]]) == list:
            rule_checker.add_violation(Violation(9, 2, "(3)"))
            return
        elif none_array[index_array[0]]:
            rule_checker.add_violation(Violation(9, 4, ""))
        none_array[index_array[0]] = value
    else:
        none_array = none_array[index_array[0]]
        index_array = index_array[1:]
        assign_at(none_array, index_array, value)
