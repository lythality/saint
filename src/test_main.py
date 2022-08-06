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

