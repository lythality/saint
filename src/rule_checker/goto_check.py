import re

from clang.cindex import CursorKind

from code_info.util import getTokenString

from rule_checker.violation import Violation

# Not initialized first.
rule_checker = None


def check_goto(checker, functions):
    global rule_checker
    rule_checker = checker

    # checking rule 15.* - goto check
    for f in functions:
        find_and_report_goto_usage(f.function_decl)


def find_and_report_goto_usage(n):
    # report goto usage
    if n.kind == CursorKind.GOTO_STMT:
        rule_checker.add_violation(Violation(15, 1, getTokenString(n)))

    # iterate recursively
    for c in n.get_children():
        find_and_report_goto_usage(c)
