import re

from clang.cindex import CursorKind

from code_info.ast_traverse_util import ASTTraverser
from code_info.cfg_traverse_util import CFGTraverser
from code_info.cursor_util import get_type_name
from code_info.util import getTokenString

from rule_checker.violation import Violation

# Not initialized first.
rule_checker = None


def check_type(checker, functions):
    global rule_checker
    rule_checker = checker

    for f in functions:
        # 10.1 -
        for c in f.function_decl.get_children():
            checker = NodeVisitor(f.cfg)
            checker.traverse()


class NodeVisitor(CFGTraverser):
    def hook_each_node(self, curr_node_id):
        checker = ASTVisitor(self.CFG.node_map[curr_node_id])
        checker.traverse()


def is_bool_type(expr):
    return get_type_name(expr) == "bool"


def is_char_type(expr):
    return get_type_name(expr) == "char"


def is_signed_type(expr):
    return get_type_name(expr) == "signed char" \
            or get_type_name(expr) == "signed short" or get_type_name(expr) == "short" \
            or get_type_name(expr) == "signed int" or get_type_name(expr) == "int" \
            or get_type_name(expr) == "signed long" or get_type_name(expr) == "long" \
            or get_type_name(expr) == "signed long long" or get_type_name(expr) == "long long"


def is_unsigned_type(expr):
    return get_type_name(expr) == "unsigned char" \
            or get_type_name(expr) == "unsigned short" \
            or get_type_name(expr) == "unsigned int" \
            or get_type_name(expr) == "unsigned long" \
            or get_type_name(expr) == "unsigned long long"


def is_unsigned_type(expr):
    return get_type_name(expr) == "unsigned char" \
            or get_type_name(expr) == "unsigned short" \
            or get_type_name(expr) == "unsigned int" \
            or get_type_name(expr) == "unsigned long" \
            or get_type_name(expr) == "unsigned long long"


def is_enum_type(expr):
    # raise Exception("need implementation")
    return False


def is_floating_type(expr):
    return get_type_name(expr) == "float" \
            or get_type_name(expr) == "double" \
            or get_type_name(expr) == "long double"


class ASTVisitor(ASTTraverser):

    def hook_binary_operator(self, n, lhs, rhs, operator):
        global rule_checker
        if operator == "+" or operator == "-":
            if is_bool_type(lhs) or is_bool_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary +- 3 @ " + getTokenString(n)))
        elif operator == "*" or operator == "/":
            if is_bool_type(lhs) or is_bool_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary */ 3 @ " + getTokenString(n)))
            elif is_char_type(lhs) or is_char_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary */ 4 @ " + getTokenString(n)))
        elif operator == "%":
            if is_bool_type(lhs) or is_bool_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary % 3 @ " + getTokenString(n)))
            elif is_char_type(lhs) or is_char_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary % 4 @ " + getTokenString(n)))
            elif is_floating_type(lhs) or is_floating_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary % 1 @ " + getTokenString(n)))
        elif operator == "<" or operator == ">" or operator == "<=" or operator == ">=":
            if is_bool_type(lhs) or is_bool_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary < > <= >= 3 @ " + getTokenString(n)))
        elif operator == "!" or operator == "&&" or operator == "||":
            if is_char_type(lhs) or is_char_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary ! && || 2 @ " + getTokenString(n)))
            elif is_signed_type(lhs) or is_signed_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary ! && || 2 @ " + getTokenString(n)))
            elif is_unsigned_type(lhs) or is_unsigned_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary ! && || 2 @ " + getTokenString(n)))
            elif is_floating_type(lhs) or is_floating_type(rhs):
                rule_checker.add_violation(Violation(10, 1, "binary ! && || 2 @ " + getTokenString(n)))

    def hook_array_subscript_expr(self, n, array, subscript):
        global rule_checker
        if is_bool_type(subscript):
            rule_checker.add_violation(Violation(10, 1, "arr-sub 3 @ " + getTokenString(n)))
        elif is_char_type(subscript):
            rule_checker.add_violation(Violation(10, 1, "arr-sub 4 @ " + getTokenString(n)))
        elif is_floating_type(subscript):
            rule_checker.add_violation(Violation(10, 1, "arr-sub 1 @ " + getTokenString(n)))

    def hook_unary_operator(self, n, operand, operator):
        global rule_checker
        if is_bool_type(operand):
            rule_checker.add_violation(Violation(10, 1, "unary 3 @ " + getTokenString(n)))
        elif is_char_type(operand):
            rule_checker.add_violation(Violation(10, 1, "unary 4 @ " + getTokenString(n)))
        elif is_enum_type(operand):
            rule_checker.add_violation(Violation(10, 1, "unary 5 @ " + getTokenString(n)))
        elif is_unsigned_type(operand) and operator == "-":
            rule_checker.add_violation(Violation(10, 1, "unary 8 @ " + getTokenString(n)))

    def hook_conditional_operator(self, n, cond, true_expr, false_expr):
        pass
