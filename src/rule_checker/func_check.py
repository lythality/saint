import re

from clang.cindex import CursorKind

from code_info.cfg_traverse_util import PathVisitor
from code_info.cursor_util import get_if_body, get_else_body, get_while_body, get_switch_body, get_case_body, get_default_body
from code_info.util import getTokenString

from rule_checker.violation import Violation

# Not initialized first.
rule_checker = None


def check_func(checker, functions):
    global rule_checker
    rule_checker = checker

    # checking rule 17.* - func check
    for f in functions:
        # 17.4
        if f.function_decl.type.spelling != "void ()":
            checker = PathChecker(f.cfg)
            checker.traverse()

        # 17.6
        no_static_keyword(f.function_decl)


def no_static_keyword(n):
    params = get_params(n)

    # check each param
    for p in params:
        text = getTokenString(p)

        # not array
        if "[" not in text:
            continue

        index_texts = text.split("[")[1:]
        for index_text in index_texts:
            if "static" in index_text:
                rule_checker.add_violation(Violation(17, 6, getTokenString(p)))
                break


class PathChecker(PathVisitor):
    def hook_each_path(self, path):
        for n in path:
            if self.CFG.node_map[n].kind == CursorKind.RETURN_STMT:
                return
        rule_checker.add_violation(Violation(17, 4, self.CFG.func_name))


def get_params(n):
    ret = []
    for c in n.get_children():
        if c.kind == CursorKind.PARM_DECL:
            ret.append(c)
    return ret
