import os
import ctypes
from ctypes import wintypes

from dial_dbpath import DbPathWindow
from window_main import LogistReportWindow
from PyQt5 import QtWidgets, QtSql, QtGui, QtCore
import sys  # sys нужен для передачи argv в QApplication


def main():
    # Для того что бы иконка менялась в трее
    myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = LogistReportWindow()  # Создаём объект класса ReportWindow

    # Меняем иконку проекта
    app_icon = QtGui.QIcon()
    # app_icon.addFile('files/icons/mylogo(16x16).ico', QtCore.QSize(16, 16))
    # app_icon.addFile('files/icons/mylogo(24x24).ico', QtCore.QSize(24, 24))
    # app_icon.addFile('files/icons/mylogo(32x32).ico', QtCore.QSize(32, 32))
    # app_icon.addFile('files/icons/mylogo(48x48).ico', QtCore.QSize(48, 48))
    app_icon.addFile('files/icons/mylogo(256x256).ico', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    window.setWindowIcon(app_icon)

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    # TODO рахунки



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
