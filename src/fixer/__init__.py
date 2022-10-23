from os.path import exists

class Fixer:
    def fix(self, violation):
        target_file_name = str(violation.location.file)
        fixed_file_name = target_file_name + "_saved.c"

        if not exists(fixed_file_name):
            code_line_list = open(target_file_name, "r").read().split("\n")
        else:
            code_line_list = open(fixed_file_name, "r").read().split("\n")

        line = violation.location.line
        col = violation.location.column
        fix_target = violation.supplementary

        # fix
        if violation.rule_id == 4 and violation.sub_id == 2:
            code_line_list[line - 1] = self.fix_4_2(code_line_list[line - 1], col, fix_target)

        open(fixed_file_name, "w").write("\n".join(code_line_list))

    def fix_4_2(self, line, col, fix_target):
        return line[:col-1] + fix_target.replace(r"??", "?\\?") + line[col - 1 + len(fix_target):]
