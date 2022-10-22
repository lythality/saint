import difflib


class MyDiferrence:
    def __init__(self):
        self.code_before = ""
        self.code_after = ""
        self.diff_record = []

    def get_diff(self, code_before, code_after):
        self.code_before = code_before
        self.code_after = code_after
        self.diff_record.clear()

        curr_record = None
        for diff in difflib.unified_diff(self.code_before.split("\n"), self.code_after.split("\n"), lineterm=""):
            if diff.startswith("---") or diff.startswith("+++") or diff.startswith("@@"):
                pass
            elif diff.startswith(" "):
                if curr_record is None:
                    curr_record = Common()
                elif type(curr_record) != Common:
                    self.diff_record.append(curr_record)
                    curr_record = Common()
                curr_record.add(diff.removeprefix(" "))
            elif diff.startswith("-") or diff.startswith("+"):
                if curr_record is None:
                    curr_record = Differ()
                elif type(curr_record) != Differ:
                    self.diff_record.append(curr_record)
                    curr_record = Differ()

                if diff.startswith("-"):
                    curr_record.add_deletion(diff.removeprefix("-"))
                elif diff.startswith("+"):
                    curr_record.add_addition(diff.removeprefix("+"))
            else:
                print("??"+diff)

        if curr_record is not None:
            self.diff_record.append(curr_record)

        return self.diff_record


class Record:
    pass


class Common(Record):
    def __init__(self):
        self.codes = []

    def add(self, code):
        self.codes.append(code)


class Differ(Record):
    def __init__(self):
        self.deletion = []
        self.addition = []
        self.size = 0

    def add_deletion(self, code):
        self.deletion.append(code)
        self.size = max(len(self.deletion), len(self.addition))

    def add_addition(self, code):
        self.addition.append(code)
        self.size = max(len(self.deletion), len(self.addition))


if __name__ == '__main__':
    str1 = "start\nAAB apple\nAAD\nend"
    str2 = "start\nAAC apple\nAAD\nend"

    for diff in MyDiferrence().get_diff(str1, str2):
        if type(diff) == Common:
            print("COMMON: "+str(diff.codes))
        elif type(diff) == Differ:
            print(" SIZE : " + str(diff.size))
            print("DELETE: " + str(diff.deletion))
            print("APPEND: " + str(diff.addition))

