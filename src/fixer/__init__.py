import re
from os.path import exists

class Fixer:
    def fix(self, violation):
        target_file_name = str(violation.location.file)
        fixed_file_name = target_file_name + "_saved.c"

        if not exists(fixed_file_name):
            code_line_list = open(target_file_name, "r").read().split("\n")
        else:
            code_line_list = open(fixed_file_name, "r").read().split("\n")

        line_str = violation.location.line
        col = violation.location.column
        fix_target = violation.supplementary

        # fix
        if violation.rule_id == 4 and violation.sub_id == 1:
            code_line_list[line_str - 1] = self.fix_4_1(code_line_list[line_str - 1], col, fix_target)
        elif violation.rule_id == 4 and violation.sub_id == 2:
            code_line_list[line_str - 1] = self.fix_4_2(code_line_list[line_str - 1], col, fix_target)

        open(fixed_file_name, "w").write("\n".join(code_line_list))

    def fix_4_1(self, line_str, col, fix_target):
        replaced = fix_target
        print(replaced)
        # replace hex with double quote and quote
        replaced = re.sub(r'(".*)(\\x[0-9A-F]+)(.*")', r'\1\2" "\3', replaced)
        replaced = re.sub(r"('.*)(\\x[0-9A-F]+)(.*')", r"\1\2' '\3", replaced)
        # replace oct with double quote and quote
        replaced = re.sub(r'(".*)(\\[0-7]+)(.*")', r'\1\2" "\3', replaced)
        replaced = re.sub(r"('.*)(\\[0-7]+)(.*')", r"\1\2' '\3", replaced)
        return line_str[:col - 1] + replaced + line_str[col - 1 + len(fix_target):]

    def fix_4_2(self, line_str, col, fix_target):
        return line_str[:col - 1] + fix_target.replace(r"??", "?\\?") + line_str[col - 1 + len(fix_target):]
