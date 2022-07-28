from rule_checker import RuleChecker


def start_saint(srcfile: str):
    trav = RuleChecker()
    trav.start_trav(srcfile)
    trav.post_check()


# the main function
if __name__ == '__main__':
    start_saint('./test_res/test_multi001.c')
    start_saint('./test_res/test_multi002.c')