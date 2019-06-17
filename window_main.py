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
import os

from files.ui import design

debug = True
DB = None


class LogistReportWindow(QtWidgets.QMainWindow, design.Ui_Auto):

    def __init__(self):

            global DB
            DB = My_Sql().connect_db()

            # РАССКОМИТИТЬ ЕСЛИ НУЖНО ЗАГРУЗИТЬ ОТЧЕТ С CSV!
            # My_Sql.add_report_from_csv("files/sql/report.csv", DB)

            # РАССКОМИТИТЬ ЕСЛИ НУЖНО ИЗМЕНИТЬ ФОРМАТ ДАТЫ
            # My_Sql.data_format_in_db(DB)

            # Это здесь нужно для доступа к переменным, методам
            # и т.д. в файле design.py
            super().__init__()
            self.setupUi(self)  # Это нужно для инициализации нашего дизайна
            # self.report_window = ReportWindow()

            self.checked_ids = set()  # переменная для хранения выделенных рядков

            self.create_table_model()  # Функция которая вносит базу данных в QStandartItemModel
            self.create_table_view()  # Создаем обзорную модель(QTableView) на основании TableModel

            self.filter_box = FilterBoxes(self.filter_view, self.table_view)  # создаем фильтр-боксы
            self.create_deselect()

            self.clear_check_and_filters()  # Очищаем все флажки и фильтры базы при запуске
            self.copy_checked_but.clicked.connect(self.copy_in_bufer)  # слушаем нажатие кнопки "КОПИРОВАТЬ"
            self.add_row_but.clicked.connect(self.add_auto)  # слушаем нажатие кнопки "ДОБАВИТЬ АВТО"
            self.go_but.clicked.connect(self.go_auto)  # слушаем нажатие кнопки "Отправить на маршрут"
            self.report_but.clicked.connect(self.do_report)
            # self.db.close()

    def create_deselect(self):
        # кнопка деселект
        deselect_but = QtWidgets.QPushButton("DEL")
        deselect_but.setFixedSize(35, 20)
        deselect_but.clicked.connect(self.clear_check_and_filters)
        self.filter_box.filter_view.setIndexWidget(self.filter_box.filter_model.index(0, COLUMNS_MAIN.index("V")),
                                                   deselect_but)

    # НИЖНЯЯ ТАБЛИЦА ГЛАВНОГО ОКНА
    def create_table_model(self):

        # сортируем базу данных по алфавиту
        # TODO сортировка украинских букв

        # создаем модель таблицы
        self.table_model = QtSql.QSqlTableModel(None, DB)
        self.table_model.setTable("mytable")
        self.table_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.table_model.select()

        # создаем горизонтальную шапку
        for col in range(self.table_model.columnCount()):
            self.table_model.setHeaderData(col, QtCore.Qt.Horizontal, COLUMNS_MAIN[col])

    def create_table_view(self):
        # ------------- ВИЗУАЛИЗАЦИЯ---------------------

        # вставляем модель в tableview
        self.table_view.setModel(self.table_model)

        # расширяем колонки
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("V"), 1)  # чекбокс
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("Назва"), 230)  # перевоз
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("ЄДРПОУ"), 70)  # инд код
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("Марка"), 85)  # Марка
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("№ авто"), 80)  # гн Авто
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("№ прич"), 80)  # гн Прицепа
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("Телефон"), 90)  # тел
        self.table_view.setColumnWidth(COLUMNS_MAIN.index("Замітки"), 150)  # вод удостовер

        # Скрываем колонку ID
        self.table_view.hideColumn(0)

        # меняем колонки местами (чекбокс вперед)
        # self.table_view.horizontalHeader().moveSection(CHECKBOX_COLUMN, 0)

        # создаем чекбокс
        delegate = CheckBoxDelegate(None)
        self.table_view.setItemDelegateForColumn(COLUMNS_MAIN.index("V"), delegate)

        # делаем слушатели tableview
        self.table_view.clicked.connect(self.table_clicked)

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
        self.table_view.sortByColumn(COLUMNS_MAIN.index("Назва"), QtCore.Qt.AscendingOrder)


        # расширяем строки по содержимому
        self.table_view.resizeRowsToContents()


    def table_clicked(self, index_in_view):
        # ПРОРАБОТАТЬ ЕСЛИ КОЛОНКА УДАЛИТСЯ!!
        # При клике на флажок добавляет рядок в "отмеченные"
        if index_in_view.column() == COLUMNS_MAIN.index("V"):  # если кликают на колонку checkbox
            # берем текущую VIEW модель (на случай фильтра в том числе)
            model = self.table_view.model()
            # берем нужную клетку с уникальным полем "id"
            cell = model.index(index_in_view.row(), 0)
            # считываем уникальный ID
            id = cell.data()

            if index_in_view.data():  # если колонка чекбокса - НЕ 0
                self.checked_ids.add(id)
            else:
                self.checked_ids.remove(id)
            if debug: print("Checked rows", self.checked_ids)

    # КНОПКИ ГЛАВНОГО ОКНА
    def clear_check_and_filters(self):

        # Убираем выделение с строк
        DB.exec("UPDATE mytable SET chk=0 WHERE chk = 1")

        # убираем фильтр с колонок
        for col in range(2, self.filter_box.filter_model.columnCount()):
            pos = (0, col)
            item = self.filter_box.filter_model.item(pos[0], pos[1])  # Берём QStandartItem в tableModel
            index = self.filter_box.filter_model.indexFromItem(item)  # Берём QModelIndex в tableModel
            widg = self.filter_box.filter_view.indexWidget(index)  # Берём Widget из QModelIndex
            widg.filter_default_viewset(self.table_view)

        # пересоздаем окно и обнуляем список выделения
        self.checked_ids = set()
        self.table_model.select()
        self.table_view.setModel(self.table_model)

    def copy_in_bufer(self,*info):
        buf = ""
        c = 1
        for id in self.checked_ids:
            # формируем sql запрос
            sql = DB.exec(f"SELECT * FROM mytable WHERE id = {id}")
            # берем первый (и единственный) вывод с sql
            sql.next()
            # формируем колонки которые заданы шаблоном
            row = [sql.value(i) for i in COPY_BUFFER_PATTERN]
            buf += str(c) + ") " + " ".join(row) + "\n"
            c += 1

        if len(info) == 2: # если заданны дополнительные данные
            info_str = f"{info[0]} {info[1]}" + "\n"
            buf = info_str + buf

        pyperclip.copy(buf)

    def add_auto(self):
        self.dialog = AddAutoWindow()
        self.dialog.show()
        # При нажатие ОК на диалоге вытаскивает введенные значения и вставляет в таблицу
        row = []
        if self.dialog.exec_():
            DB.exec(f"""INSERT INTO mytable(chk,name,code,mark,auto_num,trail_num,dr_surn,dr_name,dr_fath,tel,notes) VALUES (
                              '0',
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
            DB.commit()
            self.table_model.select()

    def go_auto(self):

        if self.checked_ids:  # если выбран хоть один авто
            # Окно с выбором маршрута
            self.dial_routes = RoutesWindow()
            if self.dial_routes.exec_(): # если выбран маршрут
                route = self.dial_routes.choice  # МАРШРУТ
                if debug: print(route)

                # Окно с доп.инфой к маршруту
                info = []

                # TODO если инфо нажмут КЕНСЕЛ, вернутся к окну маршрутов
                # Запрашиваем инфо по загрузке
                self.dial_route_info = RouteInfo(self.checked_ids,route)
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

                    # if debug:
                        # for el in info: print(el)

                # Ячейка добавленния в базу REPTABLE
                selected_date = self.dial_route_info.date_edit.date()
                date = selected_date.toString("yyyy-MM-dd")
                manager = self.dial_route_info.manager_box.currentText()
                crop = self.dial_route_info.crop_box.currentText()
                go_report = []
                for el in info:
                    go_report.append([date] + [manager] + [route] + [crop] + el)  # создаем строку в базу reptable
                if debug: [print(i) for i in go_report]

                # дополнительно копируем в буфер инфо по загрузке
                self.copy_in_bufer(date,route) # Дата и маршрут

                # вставляем в БД строку
                for el in go_report:
                    # format go_report:
                    # 0-date, 1-manager, 2-rout, 3-crop, 4-carrier, 5-auto_num, 6-surname
                    # 7- f2, 8-f1, 9-tr,

                    DB.exec(f"""INSERT INTO reptable(route_date,manager,route,crop,carrier,auto_num,surname,f2,f1,tr) VALUES (
                                      '{el[0]}',
                                      '{el[1]}',
                                      '{el[2]}',
                                      '{el[3]}',
                                      '{el[4]}',
                                      '{el[5]}',
                                      '{el[6]}',
                                      '{el[7]}',
                                      '{el[8]}',
                                      '{el[9]}'
                                  )""")
                    DB.commit()

    def do_report(self):
        self.report_window = ReportWindow()
        self.report_window.show()

    # ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ

    def copy_view_settings(self, giver_view, taker_view):

        # расширяем колонки
        for col in range(self.table_model.columnCount()):
            taker_view.setColumnWidth(col, giver_view.columnWidth(col))
        # расширяем строки по содержимому
        taker_view.resizeRowsToContents()
        # меняем колонки местами (чекбокс вперед)
        taker_view.horizontalHeader().moveSection(COLUMNS_MAIN.index("V"), 0)
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

# class for fix out events
class MyLineEdit(QtWidgets.QLineEdit):

    def __init__(self, QWindow, row, col):
        super().__init__()
        self.window = QWindow
        self.row = row
        self.col = col

    def focusInEvent(self, event):
        if debug: print("Focus in ivent (MyLineEdit Class)")
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
            if debug: print(" Focus out event (MyLineEdit Class)")
            self.window.filter_default_viewset(self)
        super(MyLineEdit, self).focusOutEvent(event)

class CheckBoxDelegate(QtWidgets.QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """

    def __init__(self, parent):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawCheck(painter, option, option.rect,
                       QtCore.Qt.Unchecked if int(index.data()) == 0 else QtCore.Qt.Checked)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        '''
        if not int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False

        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True

        return False

    def setModelData(self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        model.setData(index, 1 if int(index.data()) == 0 else 0, QtCore.Qt.EditRole)