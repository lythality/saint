

class Violation:

    def __init__(self, rule_id, sub_id, supplementary):
        self.rule_id = rule_id
        self.sub_id = sub_id
        self.supplementary = supplementary

    def get_message(self):
        message = "Not defined"
        if self.rule_id == 9:
            if self.sub_id == 2:
                message = "non-array is assigned to array %s" % self.supplementary
            elif self.sub_id == 3:
                message = "array is partially defined on %s" % self.supplementary
            elif self.sub_id == 4:
                message = "re-initialize the array %s" % self.supplementary
            elif self.sub_id == 5:
                message = "array size is not given on index based initialized array %s" % self.supplementary

        return "(%d,%d) %s" % (self.rule_id, self.sub_id, message)

    def print(self):
        print(" > "+self.get_message())
