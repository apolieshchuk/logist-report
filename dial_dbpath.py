from PyQt5 import QtWidgets
from files.ui import design_dbpath


class DbPathWindow(QtWidgets.QDialog, design_dbpath.Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)