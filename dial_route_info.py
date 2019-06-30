import csv
import operator

from files.ui import design_route_info
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from static import TITLE_FONT, ROUTE_INFO_PATTERN, COLUMNS_ROUTE_INFO, MANAGERS, CROPS

DEBUG = True


class RouteInfo(QtWidgets.QDialog, design_route_info.Ui_Dialog):

    def __init__(self, id_set, route):
        # from my_sql import My_Sql
        # self.DB = My_Sql.connect_db(str(self))

        super().__init__()
        self.id_set = id_set
        self.setupUi(self)
        self.route = route

        self.create_table_model()
        self.create_table_view()

        self.date_edit.setDate(QtCore.QDate.currentDate())

        self.manager_box.addItems(sorted(MANAGERS))
        # устанавливаем значение основного менеджера
        try:
            manager = self.most_used_on_route("manager")
            ind = self.manager_box.findText(manager)
            if ind != -1:
                self.manager_box.setCurrentIndex(ind)
        except:
            print("PASS Except!")

        self.crop_box.addItems(CROPS)
        # устанавливаем значение основной культуры на маршруте
        try:
            crop = self.most_used_on_route("crop")
            ind = self.crop_box.findText(crop)
            if ind != -1:
                self.crop_box.setCurrentIndex(ind)
        except:
            print("PASS Except!")

    def create_table_model(self):

        # ------------- МОДЕЛЬ---------------------
        # создаем модель таблицы
        self.table_model = QtGui.QStandardItemModel()

        # создаем горизонтальную шапку
        self.table_model.setHorizontalHeaderLabels(COLUMNS_ROUTE_INFO)

        # заполняем таблицу базой данных
        for id in self.id_set:
            # формируем sql запрос

            from window_main import DB
            sql = DB.exec(f"SELECT * FROM auto WHERE id = {id}")
            # берем первый (и единственный) вывод с sql
            sql.next()

            # формируем колонки которые заданы шаблоном
            row = []
            for el in ROUTE_INFO_PATTERN:
                item = QtGui.QStandardItem(sql.value(el))
                # item.setEditable(False) # неизменяемость елементов в окне
                row.append(item)
            self.table_model.appendRow(row)

    def create_table_view(self):
        # ------------- ВИЗУАЛИЗАЦИЯ---------------------

        # вставляем модель в tableview
        self.table_view.setModel(self.table_model)

        # расширяем строки и колонки по содержимому
        self.table_view.resizeRowsToContents()
        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(COLUMNS_ROUTE_INFO.index("ТР"), 50)  # Трансформация

        # Скрываем колонку ID
        self.table_view.hideColumn(0)
        self.table_view.hideColumn(4)

        # вставляем виджеты
        # инпут филды
        text_inputs = []
        text_inputs.append(COLUMNS_ROUTE_INFO.index("ф1"))
        text_inputs.append(COLUMNS_ROUTE_INFO.index("ф2"))
        text_inputs.append(COLUMNS_ROUTE_INFO.index("Прим."))
        for col in text_inputs:  # bc checkbox "CHECKBOX_INDEX" col
            for row in range(self.table_model.rowCount()):
                inp_text = MyLineEdit(self, row, col)
                inp_text.setFixedWidth(self.table_view.columnWidth(col))
                inp_text.setFixedHeight(self.table_view.rowHeight(row))
                if col == COLUMNS_ROUTE_INFO.index("ф1"):
                    inp_text.setText(str(self.most_used_on_route('f1', 5)))
                elif col == COLUMNS_ROUTE_INFO.index("ф2"):
                    inp_text.setText(str(self.most_used_on_route('f2', 5)))
                # добавляем его в таблицу
                self.table_view.setIndexWidget(self.table_model.index(row, col), inp_text)

        # лист
        col = COLUMNS_ROUTE_INFO.index("ТР")
        for row in range(self.table_model.rowCount()):
            lst_widg = QtWidgets.QComboBox()
            lst_widg.addItem("НІ")
            lst_widg.addItem("ТАК")
            # устанавливаем значение трансформации на маршруте
            tr = self.most_used_on_route("tr", 10)
            ind = lst_widg.findText(tr)
            if ind != -1:
                lst_widg.setCurrentIndex(ind)
            lst_widg.setFixedWidth(self.table_view.columnWidth(col))
            lst_widg.setFixedHeight(self.table_view.rowHeight(row))
            # добавляем его в таблицу
            self.table_view.setIndexWidget(self.table_model.index(row, col), lst_widg)

        # меняем шрифт шапки
        self.table_view.horizontalHeader().setFont(TITLE_FONT)

    def most_used_on_route(self, item, limit=18446744073709551615):

        # limit - количество ПОСЛЕДНИХ по ID записей
        from window_main import DB
        sql = DB.exec(f"SELECT {item} FROM reptable WHERE route = '{self.route}'"
                           f" ORDER BY id DESC LIMIT {limit} ")
        dict = {}
        while sql.next():
            val = sql.value(item)
            if dict.get(val):
                dict[val] += 1
            else:
                dict[val] = 1
        sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        if DEBUG: print(sorted_dict)
        if len(sorted_dict) > 0:
            return sorted_dict[0][0]
        return ""


class MyLineEdit(QtWidgets.QLineEdit):

    def __init__(self, QWindow, row, col):
        super().__init__()
        self.window = QWindow
        self.row = row
        self.col = col
