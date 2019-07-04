import csv
import re

from files.ui import design_routes_dial
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql

from filter_boxes import FilterBoxes
from static import TITLE_FONT, table_size, create_table_model


class RoutesWindow(QtWidgets.QDialog, design_routes_dial.Ui_Dialog):

    def __init__(self):
        # from my_sql import My_Sql
        # self.DB = My_Sql.connect_db(str(self))

        super().__init__()
        self.setupUi(self)
        from window_main import mysql
        self.table_model = create_table_model(mysql.DB,'routes')
        self.create_table_view()
        self.filter_box = FilterBoxes(self.filter_view, self.table_view, 1) # фокусим для ввода
        self.table_view.doubleClicked.connect(self.double_clicked)  # слушаем дабл клик
        self.add_route_but.clicked.connect(self.add_route)  # слушаем кнопку добавить маршрут


    def create_table_view(self):
        # ------------- ВИЗУАЛИЗАЦИЯ---------------------

        # вставляем модель в tableview
        self.table_view.setModel(self.table_model)

        # прячем ID
        self.table_view.hideColumn(0)

        # меняем шрифт шапки
        self.table_view.horizontalHeader().setFont(TITLE_FONT)

        # расширяем столбцы по содержимому
        self.table_view.resizeColumnsToContents()
        # расширяем строки по содержимому
        self.table_view.resizeRowsToContents()

        # Расширяем окно, согласно длинны таблицы
        # поле таблицы
        table_width = table_size(self.table_view)
        # устанавливаем ширину окна
        self.setFixedWidth(table_width)

        # включаем сортировку
        self.table_view.sortByColumn(1, QtCore.Qt.AscendingOrder)

    def double_clicked(self):

        row, column = None, None
        # код который определяет на кукую строку был сделан клик
        for idx in self.table_view.selectionModel().selectedIndexes():
            row = idx.row()
            column = idx.column()

        # сохраняем выбранное поле
        self.choice = self.table_view.model().index(row, column).data()  # выбранное поле при дабл клике

        # закрываем окно
        self.accept()

    def add_route(self):

        txt = self.line_edit.text()
        if re.match(r".*-.*",txt): # если вводимый текст совпадает формату ".... - ...."
            from window_main import mysql
            mysql.DB.exec(f"""INSERT INTO routes(route) VALUES ('{txt}')""")
            mysql.DB.commit()
            self.table_model.select()

    def csv_to_sql(self, path):
        # Считываем с файла CSV всё во внутреннюю базу данных
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            return [r for r in reader]
