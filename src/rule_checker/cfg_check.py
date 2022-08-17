import re

from clang.cindex import CursorKind

from code_info.cursor_util import get_if_body, get_else_body, get_while_body, get_switch_body, get_case_body, get_default_body
from code_info.util import getTokenString

from rule_checker.violation import Violation

# Not initialized first.
rule_checker = None


def check_cfg(checker, functions):
    global rule_checker
    rule_checker = checker

    # checking rule 15.* - cfg check
    for f in functions:
        cfg = f.cfg
        # 15.5 check single point of exit
        num = num_of_point_of_exit(cfg.init_node_id, cfg, [])
        print(cfg.get_control_flow_graph_info())
        print(cfg.func_name + " :: " + str(num))
        if num != 1:
            rule_checker.add_violation(Violation(15, 5, cfg.func_name + ", " + str(num)))


def num_of_point_of_exit(curr_node_id, cfg, visited):
    # 1. check visited
    if curr_node_id in visited:
        return 0
    visited.append(curr_node_id)

    # 2. get next nodes
    next_node_ids = cfg.next(curr_node_id)

    # 3. visit next nodes
    num = 0
    for next_node_id in next_node_ids:
        num += num_of_point_of_exit(next_node_id, cfg, visited)

    # 4. return num of exit node
    return num + 1 if cfg.exit_node_id in next_node_ids else num
