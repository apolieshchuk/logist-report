# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_report.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReportWindow(object):
    def setupUi(self, ReportWindow):
        ReportWindow.setObjectName("ReportWindow")
        ReportWindow.resize(1119, 634)
        self.centralwidget = QtWidgets.QWidget(ReportWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_3.addWidget(self.dateEdit)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.verticalLayout.addWidget(self.dateEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.filter_view = QtWidgets.QTableView(self.centralwidget)
        self.filter_view.setMaximumSize(QtCore.QSize(16777215, 23))
        self.filter_view.setObjectName("filter_view")
        self.verticalLayout_2.addWidget(self.filter_view)
        self.table_view = QtWidgets.QTableView(self.centralwidget)
        self.table_view.setObjectName("table_view")
        self.verticalLayout_2.addWidget(self.table_view)
        ReportWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ReportWindow)
        QtCore.QMetaObject.connectSlotsByName(ReportWindow)

    def retranslateUi(self, ReportWindow):
        _translate = QtCore.QCoreApplication.translate
        ReportWindow.setWindowTitle(_translate("ReportWindow", "MainWindow"))
        self.label_2.setText(_translate("ReportWindow", "От"))
        self.label.setText(_translate("ReportWindow", "До"))

