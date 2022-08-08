from unittest import TestCase

from main import start_saint
from rule_checker import RuleChecker
from rule_checker.violation import Violation


def get_violations(srcfile):
    trav = RuleChecker()
    trav.add_file(srcfile)
    trav.start_trav()
    trav.post_check()
    trav.print_violations()
    return trav.violations


def get_control_flow_graph(srcfile):
    trav = RuleChecker()
    trav.add_file(srcfile)
    trav.start_trav()
    trav.post_check()
    trav.print_violations()
    return [f.get_control_flow_graph_info() for f in trav.function]


class Test(TestCase):
    def test_array(self):
        violations = get_violations('../test_res/test_array.c')

        if len(violations) != 10:
            self.fail("missing violation")

        for vio in violations:
            print("%2d,%2d,%20s : %s" % (vio.rule_id, vio.sub_id, vio.supplementary, vio.get_message()))

        oracle = [Violation(9,  2,  "(1)"),
                Violation(9,  3,  "dead_arr"),
                Violation(9,  3,  "arr_indexed"),
                Violation(9,  4,  ""),
                Violation(9,  3,  "t"),
                Violation(9,  2,  "(2)"),
                Violation(9,  3,  "arr_2d_linear"),
                Violation(9,  4,  ""),
                Violation(9,  5,  "arr_no_size_2"),
                Violation(9,  3,  "arr_2d_some_idx_def")]

        for vio in oracle:
            if vio not in violations:
                self.fail("missing violation: "+vio.get_message())

    def test_control_flow(self):
        cfg_infos = get_control_flow_graph('../test_res/test_control.c')

        oracle = ['''=== nested_compound ===
0 [1]
1 [2]
2 [3] intn;
3 [4]
4 [5]
5 [6]
6 [7] n=1
7 [8]
8 [9]
9 [10]
10 [11]
11 []
''', '''=== main ===
0 [1]
1 [2]
2 [3] inta;
3 [4] a=3+4+5+6+7
4 [6, 8] if(a==3){}elseif(a==4){}
5 [14]
6 [7]
7 [5]
8 [10, 12] if(a==4){}
9 [5]
10 [11]
11 [9]
12 [13]
13 [9]
14 [15] return0
15 [16]
16 []
''']
        for cfg in oracle:
            self.assertTrue(cfg in cfg_infos, "missing cfg: "+cfg)


