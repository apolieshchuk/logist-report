from files.ui import design_addauto
from PyQt5 import QtWidgets


class AddAutoWindow(QtWidgets.QDialog, design_addauto.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
