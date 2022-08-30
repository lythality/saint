import clang.cindex
from clang.cindex import TypeKind, CursorKind, TokenKind

import code_info.cfg
from code_info.cfg import CFG
from code_info.cursor_util import get_if_condition, get_while_condition, get_switch_condition, get_case_condition
from code_info.cursor_util import get_if_body, get_else_body, get_while_body, get_switch_body, get_case_body, get_default_body
from code_info.cursor_util import get_bin_lhs, get_bin_rhs, get_unary_operand, get_array_operand, get_array_subscript
from code_info.cursor_util import get_condop_cond, get_condop_true_expr, get_condop_false_expr

from code_info.util import getTokenString


class ASTTraverser:

    def __init__(self, _node):
        self.expr_list = self.extract_expr(_node)

    def extract_expr(self, node):
        if node.kind == CursorKind.IF_STMT:
            return [get_if_condition(node)]
        elif node.kind == CursorKind.WHILE_STMT:
            return [get_while_condition(node)]
        elif node.kind == CursorKind.SWITCH_STMT:
            return [get_switch_condition(node)]
        elif node.kind == CursorKind.CASE_STMT:
            return [get_case_condition(node)]
        elif node.kind == CursorKind.BINARY_OPERATOR:
            return [node]
        elif node.kind == CursorKind.UNARY_OPERATOR:
            return [node]
        elif node.kind == CursorKind.CONDITIONAL_OPERATOR:
            return node.get_children()
        elif node.kind == CursorKind.DECL_STMT:
            return node.get_children()
        elif node.kind == CursorKind.RETURN_STMT:
            return node.get_children()
        elif node.kind == CursorKind.COMPOUND_STMT:
            return []
        elif node.kind == CursorKind.DEFAULT_STMT:
            return []
        elif node.kind == CursorKind.BREAK_STMT:
            return []
        elif node.kind == CursorKind.CONTINUE_STMT:
            return []
        elif node.kind == CursorKind.GOTO_STMT:
            return []
        elif node.kind == CursorKind.LABEL_STMT:
            return []
        elif node.kind == CursorKind.NULL_STMT:
            return []
        elif type(node) == code_info.cfg.DummyNode:
            return []
        return [node]

    def traverse(self):
        if not self.expr_list:
            return
        for expr in self.expr_list:
            self._traverse(expr)

    def _traverse(self, expr):
        # 1. visit binary operator
        if expr.kind == CursorKind.BINARY_OPERATOR:
            lhs = get_bin_lhs(expr)
            rhs = get_bin_rhs(expr)
            op = getTokenString(expr).replace(getTokenString(lhs), "", 1)
            op = "".join(op.rsplit(getTokenString(rhs), 1))
            self.hook_binary_operator(expr, lhs, rhs, op)
        elif expr.kind == CursorKind.UNARY_OPERATOR:
            operand = get_unary_operand(expr)
            self.hook_unary_operator(expr, operand, getTokenString(expr).replace(getTokenString(operand), ""))
        elif expr.kind == CursorKind.ARRAY_SUBSCRIPT_EXPR:
            self.hook_array_subscript_expr(expr, get_array_operand(expr), get_array_subscript(expr))
        elif expr.kind == CursorKind.CONDITIONAL_OPERATOR:
            self.hook_conditional_operator(expr, get_condop_cond(expr), get_condop_true_expr(expr),
                                           get_condop_false_expr(expr))
        elif expr.kind == CursorKind.UNEXPOSED_EXPR:
            self.hook_unexposed_expr(expr)
        elif expr.kind == CursorKind.DECL_REF_EXPR:
            self.hook_decl_ref_expr(expr)
        elif expr.kind == CursorKind.INTEGER_LITERAL:
            self.hook_integer_literal(expr)
        elif expr.kind == CursorKind.CHARACTER_LITERAL:
            self.hook_character_literal(expr)
        elif expr.kind == CursorKind.STRING_LITERAL:
            self.hook_string_literal(expr)
        elif expr.kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
            self.hook_bool_literal(expr)
        elif expr.kind == CursorKind.VAR_DECL:
            self.hook_var_decl(expr)
        elif expr.kind == CursorKind.TYPE_REF:
            pass
        elif type(expr) == code_info.cfg.DummyNode:
            self.hook_dummy_node(expr)
        else:
            raise Exception('unknown type: ' + str(expr.kind))

        self.hook_each_node(expr)

        # 2. visit children
        for c in expr.get_children():
            self._traverse(c)

    def hook_binary_operator(self, n, lhs, rhs, operator):
        pass

    def hook_array_subscript_expr(self, n, array, subscript):
        pass

    def hook_unary_operator(self, n, operand, operator):
        pass

    def hook_conditional_operator(self, n, cond, true_expr, false_expr):
        pass

    def hook_unexposed_expr(self, n):
        pass

    def hook_decl_ref_expr(self, n):
        pass

    def hook_integer_literal(self, n):
        pass

    def hook_character_literal(self, n):
        pass

    def hook_string_literal(self, n):
        pass

    def hook_bool_literal(self, n):
        pass

    def hook_var_decl(self, n):
        pass

    def hook_dummy_node(self, n):
        pass

    # called by every visit of node
    def hook_each_node(self, n):
        pass
