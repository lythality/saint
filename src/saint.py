from rule_checker import RuleChecker


def start_saint(srcfile: str):
    trav = RuleChecker()
    trav.start_trav(srcfile)
    trav.post_check()
