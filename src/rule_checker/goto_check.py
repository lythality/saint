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
        # 15.1 - goto is used
        find_and_report_goto_usage(f.function_decl)

        # 15.2 - goto label only appear upper block
        check_goto_label_only_appear_upper_block(f.function_decl, [])


def find_and_report_goto_usage(n):
    # report goto usage
    if n.kind == CursorKind.GOTO_STMT:
        rule_checker.add_violation(Violation(15, 1, getTokenString(n)))

    # iterate recursively
    for c in n.get_children():
        find_and_report_goto_usage(c)


def check_goto_label_only_appear_upper_block(n, found_labels):
    # identify found labels
    for c in n.get_children():
        if c.kind == CursorKind.LABEL_STMT:
            goto_name = c.spelling
            found_labels.append(goto_name)

    # report jump to an un-found label
    for c in n.get_children():
        if c.kind == CursorKind.GOTO_STMT:
            goto_name = getTokenString(c).removeprefix("goto")
            if goto_name not in found_labels:
                rule_checker.add_violation(Violation(15, 3, "%s @ %d:%d" % (goto_name, c.location.line, c.location.column)))

    # iterate recursively
    for c in n.get_children():
        check_goto_label_only_appear_upper_block(c, found_labels)
