# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_route_info.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(609, 427)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.date_edit = QtWidgets.QDateEdit(Dialog)
        self.date_edit.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setObjectName("date_edit")
        self.horizontalLayout_2.addWidget(self.date_edit)
        self.manager_box = QtWidgets.QComboBox(Dialog)
        self.manager_box.setObjectName("manager_box")
        self.horizontalLayout_2.addWidget(self.manager_box)
        self.crop_box = QtWidgets.QComboBox(Dialog)
        self.crop_box.setObjectName("crop_box")
        self.horizontalLayout_2.addWidget(self.crop_box)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table_view = QtWidgets.QTableView(Dialog)
        self.table_view.setObjectName("table_view")
        self.horizontalLayout.addWidget(self.table_view)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

