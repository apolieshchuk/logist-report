from PyQt5 import QtGui, QtCore, QtWidgets

debug = True


class FilterBoxes(QtWidgets.QMainWindow):

    def __init__(self, filter_view, table_view):
        super().__init__()
        self.filter_model = QtGui.QStandardItemModel()  # модель фильтра
        self.filter_view = filter_view  # вид фильтра
        self.table_view = table_view  # tableView по которому делаем фильтр
        self.table_model = table_view.model()  # таблица по которой делаем фильтр
        self.create_filter_model()
        self.create_filter_view()

        # TODO фильтры выбора

    def create_filter_model(self):
        # создаем рядок со сзначений StandartItemModel
        self.filter_model.appendRow([QtGui.QStandardItem(0) for _ in range(self.table_model.columnCount())])

    def create_filter_view(self):
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

        # поля инпута(фильтры)
        for col in range(self.filter_model.columnCount()):  # bc checkbox "CHECKBOX_INDEX" col
            filter_text = MyLineEdit(self.table_view.window(), 0, col)
            # добавляем его в таблицу
            self.filter_view.setIndexWidget(self.filter_model.index(0, col), filter_text)
            # меняем значение фильтра по Умолчанию под название колонок
            filter_text.filter_default_viewset(self.table_view)
            # включаем слушатель изменения текста
            filter_text.textEdited.connect(self.filter_text_edited)

    def copy_view_settings(self, giver_view, taker_view):

        # расширяем колонки
        for col in range(giver_view.model().columnCount()):
            taker_view.setColumnWidth(col, giver_view.columnWidth(col))
        # расширяем строки по содержимому
        taker_view.resizeRowsToContents()
        # уравниваем ширину верхней и нижней таблиц
        tabl_head_width = giver_view.verticalHeader().width()
        taker_view.verticalHeader().setMinimumWidth(tabl_head_width)
        taker_view.verticalHeader().setMaximumWidth(tabl_head_width)

    def filter_text_edited(self):
        if debug: print("Text change event (filter_text_edited)")

        # делаем реджекс выражение
        text = self.sender().text()
        # print(text)
        regex = ""
        for c in text:
            regex += f"[{c.lower()}{c.upper()}]"
        # строи модель прокси фильтра
        proxy_model = QtCore.QSortFilterProxyModel()
        proxy_model.setFilterRegExp(regex)
        proxy_model.setFilterKeyColumn(self.sender().col)

        # прокручиваем к низу все данные в модели
        while self.table_model.canFetchMore():
            self.table_model.fetchMore()

        proxy_model.setSourceModel(self.table_model)  # что фильтруем?
        self.table_view.setModel(proxy_model)  # Вот вам отфильтрованное
        self.table_view.resizeRowsToContents()  # расширяем строки по содержимому




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
