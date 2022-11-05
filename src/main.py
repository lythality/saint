from sys import argv

from fixer import Fixer
from rule_checker import RuleChecker
from ui import open_gui

with_gui = False


def start_saint(srcfile: str):
    trav = RuleChecker()
    trav.add_file(srcfile)
    trav.start_trav()
    trav.post_check()
    trav.print_violations()
    # for f in trav.function:
    #     print(f.get_control_flow_graph_info())

    fixer = Fixer()
    for vio in trav.violations:
        fixer.fix(vio)
    return trav.violations


# the main function
if __name__ == '__main__':
    # remove former processed result
    from os import listdir
    from os import remove

    for f in list(filter(lambda f: str(f).endswith("_saved.c"), listdir('../test_res/'))):
        remove('../test_res/' + f)

    # process files in argv
    if len(argv) > 1:
        for arg in argv[1:]:
            print(arg)
            start_saint(arg)
    elif with_gui:
        open_gui()
    else:
        # violations = start_saint('../test_res/test_array.c')
        # violations = start_saint('../test_res/test_bitfield.c')
        # violations = start_saint('../test_res/test_cfg.c')
        # violations = start_saint('../test_res/test_comments.c')
        # violations = start_saint('../test_res/test_control.c')
        # violations = start_saint('../test_res/test_expr.c')
        # violations = start_saint('../test_res/test_goto_15_1.c')
        # violations = start_saint('../test_res/test_goto_15_3.c')
        # violations = start_saint('../test_res/test_func_decl.c')
        # violations = start_saint('../test_res/test_multi001.c')
        # violations = start_saint('../test_res/test_multi002.c')
        # violations = start_saint('../test_res/test_switch.c')
        # violations = start_saint('../test_res/test_typedef.c')
        # violations = start_saint('../test_res/test_string.c')
        # violations = start_saint('../test_res/test_bitfield.c')
        violations = start_saint('../test_res/test_value.c')
        open_gui(violations)
