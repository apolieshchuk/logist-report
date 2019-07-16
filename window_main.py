import threading

import pyperclip  # copy in bufer
from PyQt5 import QtWidgets, QtCore, QtSql
from dial_addauto import AddAutoWindow
from dial_dbpath import DbPathWindow
from dial_route_info import RouteInfo
from filter_boxes import FilterBoxes
from my_sql import My_Sql
from window_report import ReportWindow
from dial_routes import RoutesWindow
from static import *


from files.ui import design

mysql = None

class LogistReportWindow(QtWidgets.QMainWindow, design.Ui_Auto):

    def __init__(self):
        # DB = My_Sql.connect_db("Auto connect")
        # from my_sql import My_Sql
        global mysql
        mysql = My_Sql()
        # global DB
        # DB = mysql.DB

        mysql.backup()
        # ПЕРЕНОС С SQLITE В MYSQL
        # My_Sql.sqlite_to_mysql(DB,"files/sql/auto.db")

        # РАССКОМИТИТЬ ЕСЛИ НУЖНО ЗАГРУЗИТЬ ОТЧЕТ С CSV!
        # My_Sql.add_report_from_csv("files/sql/2018.csv", DB)

        # РАССКОМИТИТЬ ЕСЛИ НУЖНО ИЗМЕНИТЬ ФОРМАТ ДАТЫ
        # My_Sql.data_format_in_db

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.stopThread = False
        self.reconnect_to_mysql()

        # отключаем кнопку настроек сервера
        self.path_but.hide()

        # меняем титл окна
        self.setWindowTitle("База авто")
        self.table_model = create_table_model(mysql.DB,'auto')  # Функция которая вносит базу данных в QStandartItemModel
        self.create_table_view()  # Создаем обзорную модель(QTableView) на основании TableModel
        self.filter_box = FilterBoxes(self.filter_view, self.table_view)  # создаем фильтр-боксы

        # двигаем колонки на фильтрах и в основной табилце
        self.move_view_columns(self.table_view, self.filter_box.filter_view)

        self.create_deselect_but()
        self.buttons_listeners()

    def closeEvent(self, event):
        # TODO Остановить поток сразу при закрытии
        self.stopThread = True
        super(LogistReportWindow, self).closeEvent(event)

    def create_deselect_but(self):
        # кнопка деселект
        deselect_but = QtWidgets.QPushButton("DEL")
        deselect_but.setFixedSize(35, 20)
        deselect_but.clicked.connect(self.clear_check_and_filters)
        self.filter_box.filter_view.setIndexWidget(self.filter_box.filter_model.index(0, COLUMNS_AUTO.index("v")),
                                                   deselect_but)

    def create_table_view(self):

        # вставляем модель в tableview
        self.table_view.setModel(self.table_model)

        # расширяем колонки
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("v"), 1)  # чекбокс
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("v2"), 1)  # чекбокс2
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("Назва"), 230)  # перевоз
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("ЄДРПОУ"), 70)  # инд код
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("Марка"), 60)  # Марка
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("№ авто"), 80)  # гн Авто
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("№ прич"), 80)  # гн Прицепа
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("Телефон"), 90)  # тел
        self.table_view.setColumnWidth(COLUMNS_AUTO.index("Замітки"), 150)  # вод удостовер

        # Скрываем колонку ID
        self.table_view.hideColumn(0)

        # меняем колонки местами (чекбокс вперед)
        # self.table_view.horizontalHeader().moveSection(CHECKBOX_COLUMN, 0)

        # создаем чекбокс Делегат
        # delegate = CheckBoxDelegate(None)
        # self.table_view.setItemDelegateForColumn(COLUMNS_MAIN.index("v"), delegate)

        # делаем слушатели tableview
        # self.table_view.clicked.connect(self.table_clicked)

        # меняем шрифт шапки
        self.table_view.horizontalHeader().setFont(TITLE_FONT)

        # Расширяем окно, согласно длинны таблицы
        # поле таблицы
        table_width = table_size(self.table_view)
        # лейаут кнопок
        but_width = self.copy_checked_but.width()
        # устанавливаем ширину окна
        self.setFixedWidth(table_width + but_width)

        # включаем сортировку
        self.table_view.sortByColumn(COLUMNS_AUTO.index("Назва"), QtCore.Qt.AscendingOrder)

        # удлиняем строки по содержимому
        # self.table_view.resizeRowsToContents()

    def move_view_columns(self, *views):
        for el in views:
            el.horizontalHeader().moveSection(COLUMNS_AUTO.index("v2"), 7)


    def table_clicked(self, index_in_view):
        pass
        # if index_in_view.column() == COLUMNS_MAIN.index("v"):
        #     print(self.table_model.checkeable_data)
        # if index_in_view.column() == COLUMNS_MAIN.index("v"):
        #     print(self.table_model.checkeable_data)
        #     # берем текущую VIEW модель (на случай фильтра в том числе)
        #     model = self.table_view.model()
        #     # берем нужную клетку с уникальным полем "id"
        #     cell = model.index(index_in_view.row(), 0)
        #     # считываем уникальный ID
        #     id = cell.data()
        #     print(id)
        # ПРОРАБОТАТЬ ЕСЛИ КОЛОНКА УДАЛИТСЯ!!
        # При клике на флажок добавляет рядок в "отмеченные"
        # if index_in_view.column() == COLUMNS_MAIN.index("v"):  # если кликают на колонку checkbox
        #     # берем текущую VIEW модель (на случай фильтра в том числе)
        #     model = self.table_view.model()
        #     # берем нужную клетку с уникальным полем "id"
        #     cell = model.index(index_in_view.row(), 0)
        #     # считываем уникальный ID
        #     id = cell.data()
        #
        #     if index_in_view.data():  # если колонка чекбокса - НЕ 0
        #         self.checked_ids.add(id)
        #     else:
        #         self.checked_ids.remove(id)
        #     if DEBUG: print("Checked rows", self.checked_ids)

    # КНОПКИ ГЛАВНОГО ОКНА
    def clear_check_and_filters(self):

        # Убираем выделение с строк
        # DB.exec("UPDATE auto SET chk=0 WHERE chk = 1")
        # TODO проходит весь словарь, желательно точечно
        for k,v in self.table_model.checkeable_data.items():
            self.table_model.checkeable_data[k] = 0

        # убираем фильтр с колонок
        self.filter_box.clearFilters()

        # self.table_model.setFilter("")
        # пересоздаем окно и обнуляем список выделения
        # self.table_model.select()
        # TODO Долго ресайзит роус ту контентс
        # self.table_view.setModel(self.table_model)
        # self.table_view.resizeRowsToContents()

    def copy_in_bufer(self,*info):
        buf = ""
        c = 1
        for id in self.get_checked_ids():
            # формируем sql запрос
            sql = mysql.DB.exec(f"SELECT * FROM auto WHERE id = {id}")
            # берем первый (и единственный) вывод с sql
            sql.next()
            # формируем колонки которые заданы шаблоном
            row = [sql.value(i) for i in COPY_BUFFER_PATTERN]
            buf += str(c) + ") " + " ".join(row) + "\n"
            c += 1

        if len(info) == 2: # если заданны дополнительные данные
            # конвертируем дату
            qdate = QtCore.QDate().fromString(info[0],"yyyy-MM-dd")
            date = qdate.toString('dd/MMM/yyyy')

            info_str = f"{date} {info[1]}" + "\n"
            buf = info_str + buf

        pyperclip.copy(buf)

    def add_auto(self):
        self.dialog = AddAutoWindow()
        self.dialog.show()
        # При нажатие ОК на диалоге вытаскивает введенные значения и вставляет в таблицу
        # Обязательно заполнение поля CHK!
        if self.dialog.exec_():
            mysql.DB.exec(f"""INSERT INTO auto(name,code,mark,auto_num,trail_num,dr_surn,dr_name,dr_fath,tel,notes) VALUES (
                              '{self.dialog.line_carrier.text()}',
                              '{self.dialog.line_kod.text()}',
                              '{self.dialog.line_mark.text()}',
                              '{self.dialog.line_autonum.text()}',
                              '{self.dialog.line_trailernum.text()}',
                              '{self.dialog.line_driver_secname.text()}',
                              '{self.dialog.line_driver_name.text()}',
                              '{self.dialog.line_driver_thirdname.text()}',
                              '{self.dialog.line_tel.text()}',
                              '{self.dialog.line_note.text()}'
                          )""")
            mysql.DB.commit()

            self.table_model.select()
            # self.table_view.setModel(self.table_model)

    def go_auto(self):
        # TODO Укоротить функцию

        checked_ids = self.get_checked_ids()

        if checked_ids:  # если выбран хоть один авто
            # Окно с выбором маршрута
            self.dial_routes = RoutesWindow()
            if self.dial_routes.exec_(): # если выбран маршрут
                route = self.dial_routes.choice  # МАРШРУТ
                if DEBUG: print(route)

                # Окно с доп.инфой к маршруту
                info = []

                # TODO если инфо нажмут КЕНСЕЛ, вернутся к окну маршрутов
                # Запрашиваем инфо по загрузке
                self.dial_route_info = RouteInfo(checked_ids,route)
                if self.dial_route_info.exec_():  # Только если нажимаем ОК
                    info_table = self.dial_route_info.table_view
                    for row in range(info_table.model().rowCount()):
                        el = []  # разбиваем данные с каждой строки на отдельные
                        for col in range(1, info_table.model().columnCount()):  # без ID
                            item = info_table.model().item(row, col)
                            if not item:
                                index = info_table.model().index(row,
                                                                 col)  # Берём QModelIndex колонки Widgetов в tableModel
                                item = info_table.indexWidget(index)  # Берём Widget из QModelIndex
                            el += [self.text_from_obj(item)]
                        info.append(el)

                    # if DEBUG:
                        # for el in info: print(el)

                    # Ячейка добавленния в базу REPTABLE
                    selected_date = self.dial_route_info.date_edit.date()
                    date = selected_date.toString("yyyy-MM-dd")
                    manager = self.dial_route_info.manager_box.currentText()
                    crop = self.dial_route_info.crop_box.currentText()
                    go_report = []
                    for el in info:
                        go_report.append([date] + [manager] + [route] + [crop] + el)  # создаем строку в базу reptable
                    if DEBUG: [print(i) for i in go_report]

                    # дополнительно копируем в буфер инфо по загрузке
                    self.copy_in_bufer(date,route) # Дата и маршрут

                    # вставляем в БД строку
                    for el in go_report:
                        # format go_report:
                        # 0-date, 1-manager, 2-rout, 3-crop, 4-carrier, 5-auto_num, 6-dr_surn
                        # 7-tel 8- f2, 9-f1, 10-tr,

                        mysql.DB.exec(f"""INSERT INTO reptable(route_date,manager,route,crop,carrier,auto_num,dr_surn,tel,f2,f1,tr,notes) VALUES (
                                          '{el[0]}',
                                          '{el[1]}',
                                          '{el[2]}',
                                          '{el[3]}',
                                          '{el[4]}',
                                          '{el[5]}',
                                          '{el[6]}',
                                          '{el[7]}',
                                          '{el[8]}',
                                          '{el[9]}',
                                          '{el[10]}',
                                          '{el[11]}'
                                      )""")
                        mysql.DB.commit()
                    self.clear_check_and_filters()

    def do_report(self):
        self.report_window = ReportWindow()
        self.report_window.show()

    def bdserver(self):
        try:
            with open("files/sql/bdserver.txt") as f:
                return f.readline().rstrip()
        except:
            print("Error! Don't find path-file to BD")
        return None

    def set_bdserver(self):
        pathWindow = DbPathWindow()
        pathWindow.line_edit.setText(self.bdserver())
        if pathWindow.exec_():
            server = pathWindow.line_edit.text()
            # Сохраняем адресс сервера в файл
            with open("files/sql/bdserver.txt", 'w') as f:
                f.write(server)

    # ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
    def reconnect_to_mysql(self):
        if self.stopThread: return
        threading.Timer(55.0, self.reconnect_to_mysql).start()
        mysql.DB.exec("SELECT id FROM auto WHERE id = 1")
        if DEBUG: print(f"DB reconnected!")

    def get_checked_ids(self):
        s = set()
        data_in_checkbox = self.table_model.checkeable_data.items()
        for row,checked in data_in_checkbox:
            if checked:
                id = self.table_model.index(row, 0).data()
                s.add(id)
        return s

    def copy_view_settings(self, giver_view, taker_view):

        # расширяем колонки
        for col in range(self.table_model.columnCount()):
            taker_view.setColumnWidth(col, giver_view.columnWidth(col))
        # расширяем строки по содержимому
        taker_view.resizeRowsToContents()
        # меняем колонки местами (чекбокс вперед)
        taker_view.horizontalHeader().moveSection(COLUMNS_AUTO.index("v"), 0)
        # taker_view.setColumnWidth(CHECKBOX_INDEX, 1)
        # уравниваем ширину верхней и нижней таблиц
        tabl_head_width = giver_view.verticalHeader().width()
        taker_view.verticalHeader().setMinimumWidth(tabl_head_width)
        taker_view.verticalHeader().setMaximumWidth(tabl_head_width)

    def text_from_obj(self, obj):
        name = type(obj).__name__
        if name == "MyLineEdit" or name == "QStandardItem":
            return obj.text()
        elif name == "QComboBox":
            return obj.currentText()
        return 0

    def buttons_listeners(self):
        self.copy_checked_but.clicked.connect(self.copy_in_bufer)  # слушаем нажатие кнопки "КОПИРОВАТЬ"
        self.add_row_but.clicked.connect(self.add_auto)  # слушаем нажатие кнопки "ДОБАВИТЬ АВТО"
        self.go_but.clicked.connect(self.go_auto)  # слушаем нажатие кнопки "Отправить на маршрут"
        self.path_but.clicked.connect(self.set_bdserver)  # слушаем нажатие кнопки "Найстройки"
        self.report_but.clicked.connect(self.do_report)  # слушаем нажатие кнопки "отчет"

# class for fix out events
class MyLineEdit(QtWidgets.QLineEdit):

    def __init__(self, QWindow, row, col):
        super().__init__()
        self.window = QWindow
        self.row = row
        self.col = col

    def focusInEvent(self, event):
        if DEBUG: print("Focus in ivent (MyLineEdit Class)")
        # проверяем, если текст в фильтре - это название фильтра - стираем
        if self.text() == self.window.table_model.headerData(self.col, QtCore.Qt.Horizontal):
            self.setText("")
            self.setStyleSheet("color: #000000")
        super(MyLineEdit, self).focusInEvent(event)

    def focusOutEvent(self, event):
        # ставим пометку для того, что бы поле не фильтровалось когда в него вносится
        # название фильтра
        if not self.text():
            # self.setProperty("StopFilter", True)
            if DEBUG: print(" Focus out event (MyLineEdit Class)")
            self.window.filter_default_viewset(self)
        super(MyLineEdit, self).focusOutEvent(event)
