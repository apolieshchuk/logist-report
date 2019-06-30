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
        Auto.resize(678, 700)
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
        spacerItem = QtWidgets.QSpacerItem(20, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.copy_checked_but = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_checked_but.sizePolicy().hasHeightForWidth())
        self.copy_checked_but.setSizePolicy(sizePolicy)
        self.copy_checked_but.setMinimumSize(QtCore.QSize(120, 30))
        self.copy_checked_but.setMaximumSize(QtCore.QSize(75, 16777215))
        self.copy_checked_but.setStyleSheet("Text-align:left")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_checked_but.setIcon(icon)
        self.copy_checked_but.setIconSize(QtCore.QSize(32, 32))
        self.copy_checked_but.setObjectName("copy_checked_but")
        self.verticalLayout.addWidget(self.copy_checked_but)
        self.add_row_but = QtWidgets.QPushButton(self.centralwidget)
        self.add_row_but.setMinimumSize(QtCore.QSize(120, 30))
        self.add_row_but.setStyleSheet("Text-align:left")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/addauto.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_row_but.setIcon(icon1)
        self.add_row_but.setIconSize(QtCore.QSize(32, 32))
        self.add_row_but.setObjectName("add_row_but")
        self.verticalLayout.addWidget(self.add_row_but, 0, QtCore.Qt.AlignTop)
        self.go_but = QtWidgets.QPushButton(self.centralwidget)
        self.go_but.setMinimumSize(QtCore.QSize(120, 30))
        self.go_but.setStyleSheet("Text-align:left")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/goauto.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.go_but.setIcon(icon2)
        self.go_but.setIconSize(QtCore.QSize(32, 32))
        self.go_but.setObjectName("go_but")
        self.verticalLayout.addWidget(self.go_but)
        self.report_but = QtWidgets.QPushButton(self.centralwidget)
        self.report_but.setMinimumSize(QtCore.QSize(120, 30))
        self.report_but.setAutoFillBackground(False)
        self.report_but.setStyleSheet("Text-align:left")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.report_but.setIcon(icon3)
        self.report_but.setIconSize(QtCore.QSize(32, 32))
        self.report_but.setObjectName("report_but")
        self.verticalLayout.addWidget(self.report_but)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.path_but = QtWidgets.QPushButton(self.centralwidget)
        self.path_but.setObjectName("path_but")
        self.verticalLayout.addWidget(self.path_but)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/mylogo(24x24).ico"))
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
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
        self.copy_checked_but.setText(_translate("Auto", "Копіювати"))
        self.add_row_but.setText(_translate("Auto", "Додати авто"))
        self.go_but.setText(_translate("Auto", "Відправити на\n"
"     маршрут"))
        self.report_but.setText(_translate("Auto", "   Звіт"))
        self.path_but.setText(_translate("Auto", "Путь к базе"))
        self.label_2.setText(_translate("Auto", "   БАЗА ДАНИХ ГК \"ФОРМУЛА СМАКУ\""))

import qtimg_rc
