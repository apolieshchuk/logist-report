# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Auto(object):
    def setupUi(self, Auto):
        Auto.setObjectName("Auto")
        Auto.resize(678, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Auto.sizePolicy().hasHeightForWidth())
        Auto.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(Auto)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.copy_checked_but = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_checked_but.sizePolicy().hasHeightForWidth())
        self.copy_checked_but.setSizePolicy(sizePolicy)
        self.copy_checked_but.setMinimumSize(QtCore.QSize(120, 30))
        self.copy_checked_but.setMaximumSize(QtCore.QSize(75, 16777215))
        self.copy_checked_but.setObjectName("copy_checked_but")
        self.verticalLayout.addWidget(self.copy_checked_but)
        self.add_row_but = QtWidgets.QPushButton(self.centralwidget)
        self.add_row_but.setMinimumSize(QtCore.QSize(120, 30))
        self.add_row_but.setObjectName("add_row_but")
        self.verticalLayout.addWidget(self.add_row_but, 0, QtCore.Qt.AlignTop)
        self.go_but = QtWidgets.QPushButton(self.centralwidget)
        self.go_but.setMinimumSize(QtCore.QSize(120, 30))
        self.go_but.setObjectName("go_but")
        self.verticalLayout.addWidget(self.go_but)
        self.report_but = QtWidgets.QPushButton(self.centralwidget)
        self.report_but.setMinimumSize(QtCore.QSize(120, 30))
        self.report_but.setObjectName("report_but")
        self.verticalLayout.addWidget(self.report_but)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filter_view = QtWidgets.QTableView(self.centralwidget)
        self.filter_view.setEnabled(True)
        self.filter_view.setMaximumSize(QtCore.QSize(16777215, 23))
        self.filter_view.setObjectName("filter_view")
        self.verticalLayout_2.addWidget(self.filter_view)
        self.table_view = QtWidgets.QTableView(self.centralwidget)
        self.table_view.setEnabled(True)
        self.table_view.setObjectName("table_view")
        self.verticalLayout_2.addWidget(self.table_view)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        Auto.setCentralWidget(self.centralwidget)

        self.retranslateUi(Auto)
        QtCore.QMetaObject.connectSlotsByName(Auto)

    def retranslateUi(self, Auto):
        _translate = QtCore.QCoreApplication.translate
        Auto.setWindowTitle(_translate("Auto", "MainWindow"))
        self.copy_checked_but.setText(_translate("Auto", "Копировать"))
        self.add_row_but.setText(_translate("Auto", "Добавить авто"))
        self.go_but.setText(_translate("Auto", "Отправить на\n"
"маршрут"))
        self.report_but.setText(_translate("Auto", "Отчет"))

