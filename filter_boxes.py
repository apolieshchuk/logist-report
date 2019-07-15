from PyQt5 import QtGui, QtCore, QtWidgets
from collections import OrderedDict

DEBUG = True


class FilterBoxes(QtWidgets.QMainWindow):

    def __init__(self, filter_view, table_view, focused_box=-1):
        # from my_sql import My_Sql
        # self.DB = My_Sql.connect_db(str(self))

        super().__init__()
        self.filter_model = QtGui.QStandardItemModel()  # модель фильтра
        self.filter_view = filter_view  # вид фильтра
        self.table_view = table_view  # tableView по которому делаем фильтр
        self.origin_table_model = table_view.model()  # таблица по которой делаем фильтр
        try:
            self.origin_table_model.fetchTable()
        except:
            pass

        self.filter_root = FilterNode(None,table_view.model())
        self.current_filter_node = self.filter_root
        # self.active_filters = OrderedDict()  # очередь фильтров
        # self.active_filters['root'] = self.origin_table_model  # корень, основная таблица под фильтрацию

        self.create_filter_model()
        self.create_filter_view(focused_box)
        from window_main import mysql
        table = self.origin_table_model.tableName()
        self.sql_table_header = mysql.getHeader_sql(table)
        # print(self.sql_table_header)
        self.last_filter = ""
        # TODO фильтры выбора

    def create_filter_model(self):
        # создаем рядок со сзначений StandartItemModel
        self.filter_model.appendRow([QtGui.QStandardItem(0) for _ in range(self.origin_table_model.columnCount())])

    def create_filter_view(self, focused_box):
        # вставляем модель в tableview
        self.filter_view.setModel(self.filter_model)

        # забираем значения колонок/строк/хедеров с исходной таблицы
        self.copy_view_settings(self.table_view, self.filter_view)

        # убираем  горизонтальный скролбар (для комфортной работы при малом окне)
        self.filter_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # убираем горизонтальную шапку
        self.filter_view.horizontalHeader().hide()
        # стираем вертикальную шапку
        self.filter_model.setHeaderData(0, QtCore.Qt.Vertical, " ")

        # TODO очистка полей инпута при переходе на новое поле фильтра
        # поля инпута(фильтры)
        for col in range(self.filter_model.columnCount()):  # bc checkbox "CHECKBOX_INDEX" col
            filter_text = MyLineEdit(self.table_view.window(), 0, col)

            filter_text.setMinimumWidth(1)  # для чекбокса поля CHk
            # добавляем его в таблицу
            self.filter_view.setIndexWidget(self.filter_model.index(0, col), filter_text)
            # меняем значение фильтра по Умолчанию под название колонок
            filter_text.filter_default_viewset(self.table_view)
            # включаем слушатель изменения текста
            filter_text.textEdited.connect(self.filter_text_edited)

            # автофокус в диалоге
            if col == focused_box:
                filter_text.setFocusPolicy(QtCore.Qt.StrongFocus)
                filter_text.setFocus()

    def copy_view_settings(self, giver_view, taker_view):

        # расширяем колонки
        for col in range(giver_view.model().columnCount()):
            taker_view.setColumnWidth(col, giver_view.columnWidth(col))

        # расширяем строки по содержимому
        # ВАЖНО для того ччтоб ввод не обрезало
        taker_view.resizeRowsToContents()

        # уравниваем ширину верхней и нижней таблиц
        tabl_head_width = giver_view.verticalHeader().width()
        taker_view.verticalHeader().setMinimumWidth(tabl_head_width)
        taker_view.verticalHeader().setMaximumWidth(tabl_head_width)

    def filter_text_edited(self):

        # Если фильтр ещё неактивен - добавить в очередь активности фильтров
        if not self.active_filters.get(self.sender()):
            self.active_filters[self.sender()] = None

        if DEBUG: print("Text change event (filter_text_edited)")
        text = self.sender().text()

        # TODO Сделать нодами
        # если текст удаляется - удаляем и фильтр в очереди активности
        if text == "":
            ord_list = list(self.active_filters.items())
            ind = ord_list.index(self.sender())


        if len(self.active_filters) > 2:
            # предпоследний фильтр
            val = list(self.active_filters.items())[-2][0]
            # модель предпоследнего фильтра
            model_for_filter = self.active_filters[val]

        # если текст предыдущего фильтра есть в текущем,
        # не нужно перебирать всю таблицу снова\
        if self.last_filter in text:
            model_for_filter = self.table_view.model()
        self.last_filter = text

        # # фильтруем модель СПОСОБ №1
        # model_for_filter.setFilter(f"{self.sql_table_header[self.sender().col]} LIKE '%{text}%'")
        # self.table_view.resizeRowsToContents()  # расширяем строки по содержимому

        # фильтруем модель СПОСОБ №2
        # делаем реджекс выражение
        regex = ""
        for c in text:
            regex += f"[{c.lower()}{c.upper()}]"
        # строим модель прокси фильтра
        proxy_model = QtCore.QSortFilterProxyModel()
        proxy_model.setFilterRegExp(regex)
        proxy_model.setFilterKeyColumn(self.sender().col)
        proxy_model.setSourceModel(model_for_filter)  # что фильтруем?
        self.table_view.setModel(proxy_model)  # Вот вам отфильтрованное

        self.active_filters[self.sender()] = proxy_model

    def clearFilters(self):
        self.active_filters = []
        # убираем фильтр с колонок
        for col in range(2, self.filter_model.columnCount()):
            pos = (0, col)
            item = self.filter_model.item(pos[0], pos[1])  # Берём QStandartItem в tableModel
            index = self.filter_model.indexFromItem(item)  # Берём QModelIndex в tableModel
            widg = self.filter_view.indexWidget(index)  # Берём Widget из QModelIndex
            widg.filter_default_viewset(self.table_view)


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
            self.filter_default_viewset(self.window.table_view)
        super(MyLineEdit, self).focusOutEvent(event)

    def filter_default_viewset(self, table_view):
        # Устанавливаем дефолтные настройки поля фильтра
        # Берем название колонки с шапки TABLE MODEL
        head = table_view.model().headerData(self.col, QtCore.Qt.Horizontal)
        # Установливаем текст поля таким же как в соответсвующей колонке шапки
        self.setText(str(head))
        # Устанавливаем цвет текста в поле, серым
        self.setStyleSheet("color: #A9A9A9")

class FilterNode():

    def __init__(self,box,model,next_node=None):
        self.filter_box = box
        self.filter_model = model
        self.next_node = next_node
