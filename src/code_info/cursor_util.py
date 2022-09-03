from clang.cindex import CursorKind


def get_if_condition(n):
    if n.kind != CursorKind.IF_STMT:
        return None

    # states
    IF_CONDITION = 0

    # state machine based traverse
    state = IF_CONDITION
    for c in n.get_children():
        if state == IF_CONDITION:
            return c

    # shall not reachable
    return None


def get_if_body(n):
    if n.kind != CursorKind.IF_STMT:
        return None

    # states
    IF_CONDITION = 0
    IF_TRUE_STATEMENT = 1
    IF_FALSE_STATEMENT = 2
    IF_FULLY_ITERATED = 3

    # state machine based traverse
    state = IF_CONDITION
    for c in n.get_children():
        if state == IF_CONDITION:
            state = IF_TRUE_STATEMENT
        elif state == IF_TRUE_STATEMENT:
            state = IF_FALSE_STATEMENT
            return c
        elif state == IF_FALSE_STATEMENT:
            state = IF_FULLY_ITERATED

    # shall not reachable
    return None


def get_else_body(n):
    if n.kind != CursorKind.IF_STMT:
        return None

    # states
    IF_CONDITION = 0
    IF_TRUE_STATEMENT = 1
    IF_FALSE_STATEMENT = 2
    IF_FULLY_ITERATED = 3

    # state machine based traverse
    state = IF_CONDITION
    for c in n.get_children():
        if state == IF_CONDITION:
            state = IF_TRUE_STATEMENT
        elif state == IF_TRUE_STATEMENT:
            state = IF_FALSE_STATEMENT
        elif state == IF_FALSE_STATEMENT:
            state = IF_FULLY_ITERATED
            return c

    # shall not reachable
    return None


def get_while_condition(n):
    if n.kind != CursorKind.WHILE_STMT:
        return None

    # states
    WHILE_CONDITION = 0

    # state machine based traverse
    state = WHILE_CONDITION
    for c in n.get_children():
        if state == WHILE_CONDITION:
            return c

    # shall not reachable
    return None


def get_while_body(n):
    if n.kind != CursorKind.WHILE_STMT:
        return None

    # states
    WHILE_CONDITION = 0
    WHILE_BODY = 1
    WHILE_FULLY_ITERATED = 2

    # state machine based traverse
    state = WHILE_CONDITION
    for c in n.get_children():
        if state == WHILE_CONDITION:
            state = WHILE_BODY
        elif state == WHILE_BODY:
            return c

    # shall not reachable
    return None


def get_switch_condition(n):
    if n.kind != CursorKind.SWITCH_STMT:
        return None

    # states
    SWITCH_CONDITION = 0

    # state machine based traverse
    state = SWITCH_CONDITION
    for c in n.get_children():
        if state == SWITCH_CONDITION:
            return c

    # shall not reachable
    return None


def get_switch_body(n):
    if n.kind != CursorKind.SWITCH_STMT:
        return None

    # states
    SWITCH_CONDITION = 0
    SWITCH_BODY = 1
    SWITCH_FULLY_ITERATED = 2

    # state machine based traverse
    state = SWITCH_CONDITION
    for c in n.get_children():
        if state == SWITCH_CONDITION:
            state = SWITCH_BODY
        elif state == SWITCH_BODY:
            return c

    # shall not reachable
    return None


def get_case_condition(n):
    if n.kind != CursorKind.CASE_STMT:
        return None

    # states
    CASE_CONDITION = 0

    # state machine based traverse
    state = CASE_CONDITION
    for c in n.get_children():
        if state == CASE_CONDITION:
            return c

    # shall not reachable
    return None


def get_case_body(n):
    if n.kind != CursorKind.CASE_STMT:
        return None

    # states
    CASE_CONDITION = 0
    CASE_BODY = 1
    CASE_FULLY_ITERATED = 2

    # state machine based traverse
    state = CASE_CONDITION
    for c in n.get_children():
        if state == CASE_CONDITION:
            state = CASE_BODY
        elif state == CASE_BODY:
            return c

    # shall not reachable
    return None


def get_default_body(n):
    if n.kind != CursorKind.DEFAULT_STMT:
        return None

    # states
    DEFAULT_BODY = 0
    DEFAULT_FULLY_ITERATED = 1

    # state machine based traverse
    state = DEFAULT_BODY
    for c in n.get_children():
        if state == DEFAULT_BODY:
            return c

    # shall not reachable
    return None


def get_bin_lhs(n):
    if n.kind != CursorKind.BINARY_OPERATOR:
        return None

    # states
    BIN_LHS = 0

    # state machine based traverse
    state = BIN_LHS
    for c in n.get_children():
        if state == BIN_LHS:
            return c

    # shall not reachable
    return None


def get_bin_rhs(n):
    if n.kind != CursorKind.BINARY_OPERATOR:
        return None

    # states
    BIN_LHS = 0
    BIN_RHS = 1

    # state machine based traverse
    state = BIN_LHS
    for c in n.get_children():
        if state == BIN_LHS:
            state = BIN_RHS
        elif state == BIN_RHS:
            return c

    # shall not reachable
    return None


def get_unary_operand(n):
    if n.kind != CursorKind.UNARY_OPERATOR:
        return None

    # states
    UNARY_OPERAND = 0

    # state machine based traverse
    state = UNARY_OPERAND
    for c in n.get_children():
        if state == UNARY_OPERAND:
            return c

    # shall not reachable
    return None


def get_array_operand(n):
    if n.kind != CursorKind.ARRAY_SUBSCRIPT_EXPR:
        return None

    # states
    ARRAY_OPERAND = 0

    # state machine based traverse
    state = ARRAY_OPERAND
    for c in n.get_children():
        if state == ARRAY_OPERAND:
            return c

    # shall not reachable
    return None


def get_array_subscript(n):
    if n.kind != CursorKind.ARRAY_SUBSCRIPT_EXPR:
        return None

    # states
    ARRAY_OPERAND = 0
    ARRAY_SUBSCRIPT = 1

    # state machine based traverse
    state = ARRAY_OPERAND
    for c in n.get_children():
        if state == ARRAY_OPERAND:
            state = ARRAY_SUBSCRIPT
        elif state == ARRAY_SUBSCRIPT:
            return c

    # shall not reachable
    return None


def get_condop_cond(n):
    if n.kind != CursorKind.CONDITIONAL_OPERATOR:
        return None

    # states
    CONDOP_CONDITION = 0

    # state machine based traverse
    state = CONDOP_CONDITION
    for c in n.get_children():
        if state == CONDOP_CONDITION:
            return c

    # shall not reachable
    return None


def get_condop_true_expr(n):
    if n.kind != CursorKind.CONDITIONAL_OPERATOR:
        return None

    # states
    CONDOP_CONDITION = 0
    CONDOP_TRUE_EXPR = 1

    # state machine based traverse
    state = CONDOP_CONDITION
    for c in n.get_children():
        if state == CONDOP_CONDITION:
            state = CONDOP_TRUE_EXPR
        elif state == CONDOP_TRUE_EXPR:
            return c

    # shall not reachable
    return None


def get_condop_false_expr(n):
    if n.kind != CursorKind.CONDITIONAL_OPERATOR:
        return None

    # states
    CONDOP_CONDITION = 0
    CONDOP_TRUE_EXPR = 1
    CONDOP_FALSE_EXPR = 2

    # state machine based traverse
    state = CONDOP_CONDITION
    for c in n.get_children():
        if state == CONDOP_CONDITION:
            state = CONDOP_TRUE_EXPR
        elif state == CONDOP_TRUE_EXPR:
            state = CONDOP_FALSE_EXPR
        elif state == CONDOP_FALSE_EXPR:
            return c

    # shall not reachable
    return None


def get_type_name(n):
    if n.kind == CursorKind.UNEXPOSED_EXPR:
        if n.get_children():
            return get_type_name(n.get_children().__next__())
    return n.type.spelling
