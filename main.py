import os

from dial_dbpath import DbPathWindow
from my_sql import My_Sql
from window_main import LogistReportWindow
from PyQt5 import QtWidgets, QtSql
import sys  # sys нужен для передачи argv в QApplication

def main():


    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = LogistReportWindow()  # Создаём объект класса ReportWindow
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    # TODO рахунки



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
