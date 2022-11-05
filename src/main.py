from sys import argv
from rule_checker import RuleChecker

from mydiff import MyDifference
from mydiff import Common, Differ

from fixer import Fixer

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


from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtCore

import sys
from PyQt5 import QtGui, QtWidgets
from ui.main_view import Ui_MainWindow


def open_gui(violations=[]):
    # basic gui open - start
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = My_MainWindow()

    # setting style
    app.setStyle('Fusion')
    print(QtWidgets.QStyleFactory.keys())

    # set violations
    MainWindow.show_violations(violations)

    # basic gui open - end
    MainWindow.show()
    app.exec_()

COMMON = QtGui.QColor(100, 100, 150)
HARD_GREEN = QtGui.QColor(0, 250, 0)
LIGHT_GREEN = QtGui.QColor(200, 255, 200)
HARD_RED = QtGui.QColor(250, 0, 0)
LIGHT_RED = QtGui.QColor(255, 200, 200)


class My_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # codeview scroll synchronized
        self.ui.codeWidgetLeft.verticalScrollBar().valueChanged.connect(self.__set_codeviewright_scroll)
        self.ui.codeWidgetRight.verticalScrollBar().valueChanged.connect(self.__set_codeviewleft_scroll)

    # for test purpose
    def button_clicked(self):
        print("pressed")

    def __set_codeviewleft_scroll(self, value):
        self.ui.codeWidgetLeft.verticalScrollBar().setValue(value)

    def __set_codeviewright_scroll(self, value):
        self.ui.codeWidgetRight.verticalScrollBar().setValue(value)

    # called by UI
    # row is violation row
    def show_code(self, row, __unused):
        # getting file name and show line num
        orig_file_name = self.ui.vioWidget.item(row, 1).text()
        fixed_file_name = orig_file_name + "_saved.c"
        line_number = int(self.ui.vioWidget.item(row, 2).text().split(":")[0])

        # get code text
        orig_code = open(orig_file_name, 'r').read()
        fixed_code = open(fixed_file_name, 'r').read()

        # diff check of the code text
        diff_record = MyDifference().get_diff(orig_code, fixed_code)

        # show it to the widget
        if diff_record:
            self.show_code_deletion(self.ui.codeWidgetLeft, diff_record, line_number)
            self.show_code_addition(self.ui.codeWidgetRight, diff_record, line_number)
        else:
            self.show_code_itself(self.ui.codeWidgetLeft, orig_code)
            self.show_code_itself(self.ui.codeWidgetRight, fixed_code)

    def show_code_itself(self, code_widget, code_text):
        line_num = 1
        for line in code_text.split("\n"):
            # insert row
            code_widget.insertRow(code_widget.rowCount())
            # adding line number
            line_number = QTableWidgetItem(str(line_num))
            line_number.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignTop)
            code_widget.setItem(code_widget.rowCount() - 1, 0, line_number)
            # adding color
            line_color = QTableWidgetItem()
            code_widget.setItem(code_widget.rowCount() - 1, 1, line_color)
            # adding line content
            line_content = QTableWidgetItem(line)
            line_content.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
            code_widget.setItem(code_widget.rowCount() - 1, 2, line_content)

            line_num += 1

        code_widget.resizeColumnsToContents()

    def show_code_deletion(self, code_widget, diff_record, show_line):
        # Remove all lines
        while code_widget.rowCount() > 0:
            code_widget.removeRow(0)

        line_num = 1
        for diff in diff_record:
            if type(diff) == Common:
                contents = diff.codes
            else:
                contents = diff.deletion

            for line in contents:
                # insert row
                code_widget.insertRow(code_widget.rowCount())
                # adding line number
                line_number = QTableWidgetItem(str(line_num))
                line_number.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignTop)
                if type(diff) == Differ:
                    line_number.setBackground(LIGHT_RED)
                code_widget.setItem(code_widget.rowCount()-1, 0, line_number)
                # adding color
                line_color = QTableWidgetItem()
                if type(diff) == Differ:
                    line_color.setBackground(HARD_RED)
                else:
                    line_color.setBackground(COMMON)
                code_widget.setItem(code_widget.rowCount()-1, 1, line_color)
                # adding line content
                line_content = QTableWidgetItem(line)
                line_content.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
                if type(diff) == Differ:
                    line_content.setBackground(LIGHT_RED)
                code_widget.setItem(code_widget.rowCount()-1, 2, line_content)

                line_num += 1

            if type(diff) == Differ:
                for _ in range(diff.size-len(diff.deletion)):
                    code_widget.insertRow(code_widget.rowCount())

        code_widget.resizeColumnsToContents()

        # line number
        code_widget.selectRow(show_line - 1)
        code_widget.scrollTo(code_widget.model().index(show_line - 1, 1))

    def show_code_addition(self, code_widget, diff_record, show_line):
        # Remove all lines
        while code_widget.rowCount() > 0:
            code_widget.removeRow(0)

        line_num = 1
        for diff in diff_record:

            if type(diff) == Common:
                contents = diff.codes
            else:
                contents = diff.addition

            for line in contents:
                # insert row
                code_widget.insertRow(code_widget.rowCount())
                # adding line number
                line_number = QTableWidgetItem(str(line_num))
                line_number.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignTop)
                if type(diff) == Differ:
                    line_number.setBackground(LIGHT_GREEN)
                code_widget.setItem(code_widget.rowCount()-1, 0, line_number)
                # adding color
                line_color = QTableWidgetItem()
                if type(diff) == Differ:
                    line_color.setBackground(HARD_GREEN)
                else:
                    line_color.setBackground(COMMON)
                code_widget.setItem(code_widget.rowCount()-1, 1, line_color)
                # adding line content
                line_content = QTableWidgetItem(line)
                line_content.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
                if type(diff) == Differ:
                    line_content.setBackground(LIGHT_GREEN)
                code_widget.setItem(code_widget.rowCount()-1, 2, line_content)

                line_num += 1

            if type(diff) == Differ:
                for _ in range(diff.size-len(diff.addition)):
                    code_widget.insertRow(code_widget.rowCount())

        code_widget.resizeColumnsToContents()

        # line number
        code_widget.selectRow(show_line - 1)
        code_widget.scrollTo(code_widget.model().index(show_line - 1, 1))

    def show_code_at(self, code_widget, code_str, show_line):
        # test - start
        lines = code_str.split("\n")
        while code_widget.rowCount() > 0:
            code_widget.removeRow(0)
        for i in range(len(lines)):
            code_widget.insertRow(code_widget.rowCount())
            # adding line number
            line_number = QTableWidgetItem(str(code_widget.rowCount()))
            line_number.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignTop)
            code_widget.setItem(code_widget.rowCount()-1, 0, line_number)
            # adding color
            line_color = QTableWidgetItem()
            line_color.setBackground(QtGui.QColor(100, 100, 150))
            code_widget.setItem(code_widget.rowCount()-1, 1, line_color)
            # adding line content
            line_content = QTableWidgetItem(lines[code_widget.rowCount()-1])
            line_content.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
            code_widget.setItem(code_widget.rowCount()-1, 2, line_content)

        code_widget.resizeColumnsToContents()

        # line number
        code_widget.selectRow(show_line - 1)
        code_widget.scrollTo(code_widget.model().index(show_line - 1, 1))


    def show_violations(self, violations):
        for i in range(len(violations)):
            self.ui.vioWidget.insertRow(self.ui.vioWidget.rowCount())
            # adding rule_id
            rule_id = QTableWidgetItem(str(violations[i].rule_id) + ", " + str(violations[i].sub_id))
            rule_id.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
            self.ui.vioWidget.setItem(i, 0, rule_id)
            if violations[i].location is not None:
                # adding file
                file_name = QTableWidgetItem(str(violations[i].location.file))
                file_name.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
                self.ui.vioWidget.setItem(i, 1, file_name)
                # adding location
                code_loc = QTableWidgetItem(str(violations[i].location.line) + ":" + str(violations[i].location.column))
                code_loc.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
                self.ui.vioWidget.setItem(i, 2, code_loc)
            # adding comment
            comment = QTableWidgetItem(violations[i].get_message())
            comment.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
            self.ui.vioWidget.setItem(i, 3, comment)
        self.ui.vioWidget.resizeColumnsToContents()


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
