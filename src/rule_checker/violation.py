class Violation:

    def __init__(self, rule_id, sub_id, supplementary):
        self.rule_id = rule_id
        self.sub_id = sub_id
        self.supplementary = supplementary

    def __eq__(self, other):
        if not hasattr(other, "rule_id") \
                or not hasattr(other, "sub_id") \
                or not hasattr(other, "supplementary"):
            return False
        return self.rule_id == other.rule_id and \
                self.sub_id == other.sub_id and \
                self.supplementary == other.supplementary

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

        elif self.rule_id == 15:
            if self.sub_id == 1:
                message = "goto (%s) is used" % self.supplementary
            elif self.sub_id == 2:
                message = "jump to nested label from goto: %s" % self.supplementary
            elif self.sub_id == 5:
                message = "there are more than 1 exit in : %s" % self.supplementary
            elif self.sub_id == 7:
                message = "all if shall have else statement: %s" % self.supplementary

        elif self.rule_id == 16:
            if self.sub_id == 2:
                message = "case is not directly connected to switch: %s" % self.supplementary
            elif self.sub_id == 4:
                message = "default is not placed in switch: %s" % self.supplementary

        elif self.rule_id == 17:
            if self.sub_id == 1:
                message = "stdarg.h is included in: %s" % self.supplementary

        return "(%d,%d) %s" % (self.rule_id, self.sub_id, message)

    def print(self):
        print(" >  " + self.get_message())
