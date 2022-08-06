from sys import argv
from rule_checker import RuleChecker

def start_saint(srcfile: str):
    trav = RuleChecker()
    trav.add_file(srcfile)
    trav.start_trav()
    trav.post_check()
    trav.print_violations()


# the main function
if __name__ == '__main__':
    # process files in argv
    if len(argv) > 1:
        for arg in argv[1:]:
            print(arg)
            start_saint(arg)
    else:
        # start_saint('../test_res/test.c')
        start_saint('../test_res/test_array.c')
        # start_saint('../test_res/test_comments.c')
        # start_saint('../test_res/test_func_decl.c')
        # start_saint('../test_res/test_multi001.c')
        # start_saint('../test_res/test_multi002.c')
        # start_saint('../test_res/test_typedef.c')
        # start_saint('../test_res/test_string.c')
        # start_saint('../test_res/test_bitfield.c')
