import re

from clang.cindex import CursorKind

from code_info.cursor_util import get_default_body
from code_info.util import getTokenString

from rule_checker.violation import Violation

# Not initialized first.
rule_checker = None


def check_switch(checker, functions):
    global rule_checker
    rule_checker = checker

    for f in functions:
        # 16.2 - case shall used immediately below switch
        for c in f.function_decl.get_children():
            check_case_used_below_switch(c, [])

        # 16.4 - all switch shall have default
        for c in f.function_decl.get_children():
            check_default_for_switch(c)


def check_case_used_below_switch(n, parent_stack):
    # report violation
    if n.kind == CursorKind.CASE_STMT:
        switch_parents = []

        while parent_stack:
            parent = parent_stack.pop()
            switch_parents.append(parent)

            if parent.kind == CursorKind.SWITCH_STMT:
                # good
                break
            elif parent.kind == CursorKind.COMPOUND_STMT:
                # try one more time
                continue
            elif parent.kind == CursorKind.CASE_STMT:
                # try one more time
                continue
            else:
                rule_checker.add_violation(Violation(16, 2, getTokenString(n)))
                break

        while switch_parents:
            parent_stack.append(switch_parents.pop())

    # iterate recursively
    parent_stack.append(n)
    for c in n.get_children():
        check_case_used_below_switch(c, parent_stack)
    parent_stack.pop()


def check_default_for_switch(n):
    # report violation
    if n.kind == CursorKind.SWITCH_STMT:
        if get_default_body(n) is None:
            rule_checker.add_violation(Violation(16, 4, getTokenString(n)))

    # iterate recursively
    for c in n.get_children():
        check_default_for_switch(c)
