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
0 [1] INIT_node
1 [2] COMP-START-{intn;{{{n=1;}}}}
2 [3] intn;
3 [4] COMP-START-{{{n=1;}}}
4 [5] COMP-START-{{n=1;}}
5 [6] COMP-START-{n=1;}
6 [7] n=1
7 [8] COMP-END-{n=1;}
8 [9] COMP-END-{{n=1;}}
9 [10] COMP-END-{{{n=1;}}}
10 [11] COMP-END-{intn;{{{n=1;}}}}
11 [] EXIT_node
''', '''=== basic_if ===
0 [1] INIT_node
1 [2] COMP-START-{inta;a=3+4+5+6+7;if(a==3){}elseif(a==4){}}
2 [3] inta;
3 [4] a=3+4+5+6+7
4 [6, 8] if(a==3){}elseif(a==4){}
5 [14] MERGE-if(a==3){}elseif(a==4){}
6 [7] COMP-START-{}
7 [5] COMP-END-{}
8 [10, 12] if(a==4){}
9 [5] MERGE-if(a==4){}
10 [11] COMP-START-{}
11 [9] COMP-END-{}
12 [13] COMP-START-{}
13 [9] COMP-END-{}
14 [15] COMP-END-{inta;a=3+4+5+6+7;if(a==3){}elseif(a==4){}}
15 [] EXIT_node
''', '''=== basic_while ===
0 [1] INIT_node
1 [2] COMP-START-{while(g==3){}}
2 [5, 4] while(g==3){}
3 [2] MERGE-while(g==3){}
4 [7] WHILE-NEXT-while(g==3){}
5 [6] COMP-START-{}
6 [3] COMP-END-{}
7 [8] COMP-END-{while(g==3){}}
8 [] EXIT_node
''', '''=== break_while ===
0 [1] INIT_node
1 [2] COMP-START-{while(g==1){g==2;break;}g==5;}
2 [5, 4] while(g==1){g==2;break;}
3 [2] MERGE-while(g==1){g==2;break;}
4 [9] WHILE-NEXT-while(g==1){g==2;break;}
5 [6] COMP-START-{g==2;break;}
6 [7] g==2
7 [4] break
8 [3] COMP-END-{g==2;break;}
9 [10] g==5
10 [11] COMP-END-{while(g==1){g==2;break;}g==5;}
11 [] EXIT_node
''', '''=== cont_while ===
0 [1] INIT_node
1 [2] COMP-START-{while(g==1){g==2;continue;}g==5;}
2 [5, 4] while(g==1){g==2;continue;}
3 [2] MERGE-while(g==1){g==2;continue;}
4 [9] WHILE-NEXT-while(g==1){g==2;continue;}
5 [6] COMP-START-{g==2;continue;}
6 [7] g==2
7 [2] continue
8 [3] COMP-END-{g==2;continue;}
9 [10] g==5
10 [11] COMP-END-{while(g==1){g==2;continue;}g==5;}
11 [] EXIT_node
''', '''=== main ===
0 [1] INIT_node
1 [2] COMP-START-{inta;a=3+4+5+6+7;if(a==3){}elseif(a==4){}return0;}
2 [3] inta;
3 [4] a=3+4+5+6+7
4 [6, 8] if(a==3){}elseif(a==4){}
5 [14] MERGE-if(a==3){}elseif(a==4){}
6 [7] COMP-START-{}
7 [5] COMP-END-{}
8 [10, 12] if(a==4){}
9 [5] MERGE-if(a==4){}
10 [11] COMP-START-{}
11 [9] COMP-END-{}
12 [13] COMP-START-{}
13 [9] COMP-END-{}
14 [15] return0
15 [16] COMP-END-{inta;a=3+4+5+6+7;if(a==3){}elseif(a==4){}return0;}
16 [] EXIT_node
''']
        print(cfg_infos)
        for cfg in oracle:
            self.assertTrue(cfg in cfg_infos, "missing cfg: "+cfg)


