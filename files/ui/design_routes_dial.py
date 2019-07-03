# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_routes_dial.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(403, 484)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.filter_view = QtWidgets.QTableView(Dialog)
        self.filter_view.setMinimumSize(QtCore.QSize(0, 0))
        self.filter_view.setMaximumSize(QtCore.QSize(16777215, 23))
        self.filter_view.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.filter_view.setObjectName("filter_view")
        self.verticalLayout.addWidget(self.filter_view)
        self.table_view = QtWidgets.QTableView(Dialog)
        self.table_view.setObjectName("table_view")
        self.verticalLayout.addWidget(self.table_view)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit = QtWidgets.QLineEdit(Dialog)
        self.line_edit.setObjectName("line_edit")
        self.horizontalLayout.addWidget(self.line_edit)
        self.add_route_but = QtWidgets.QPushButton(Dialog)
        self.add_route_but.setObjectName("add_route_but")
        self.horizontalLayout.addWidget(self.add_route_but)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_route_but.setText(_translate("Dialog", "Добавить маршрут"))

