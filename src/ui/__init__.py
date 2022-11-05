import sys

from PyQt5 import QtWidgets

from ui.MainWindow import MainWindow
from ui.UI_MainWindow import UI_MainWindow


def open_gui(violations=[]):
    # basic gui open - start
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()

    # setting style
    app.setStyle('Fusion')

    # set violations
    main_window.show_violations(violations)

    # basic gui open - end
    main_window.show()
    app.exec_()
