from PyQt5 import QtWidgets, QtSql, QtCore
from files.ui import design_report
from filter_boxes import FilterBoxes
from static import COLUMNS_MAIN, TITLE_FONT, COLUMNS_REPORT, table_size


class ReportWindow(QtWidgets.QMainWindow, design_report.Ui_ReportWindow):


    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна


        # Создаем таблицу
        self.create_table_model()
        self.create_table_view()

        # TODO вынести в функцию
        # устанавливаем диапазон дат по умолчанию
        date1 = QtCore.QDate.currentDate().addMonths(-3)
        date2 = QtCore.QDate.currentDate().addDays(+1)
        self.dateEdit.setDate(date1)
        self.dateEdit_2.setDate(date2)
        # слушатели диапазона дат
        self.dateEdit.dateChanged.connect(self.start_date_edit)
        self.dateEdit_2.dateChanged.connect(self.start_date_edit)
        # фильтруем по установленному диапазону дат
        self.start_date_edit()



        # создаем фильтр боксы
        self.filter_box = FilterBoxes(self.filter_view,self.table_view)

        # двигаем колонки на фильтрах и в основной табилце
        self.move_view_columns(self.table_view,self.filter_box.filter_view)



        #TODO вывод в иксель
        #TODO отчет выводится за диапазон


    def create_table_model(self):
        from window_main import DB

        # фильтруем модель за период
        # sql_model = DB.exec(f"SELECT * FROM reptable WHERE route_date BETWEEN"
        #                     f" '{self.date1}' AND '{self.date2}'")

        # создаем модель таблицы
        # self.table_model = QtSql.QSqlQueryModel()
        # self.table_model.setQuery(sql_model)
        self.table_model = QtSql.QSqlTableModel(None)
        self.table_model.setTable("reptable")
        self.table_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.table_model.select()



        # DB.exec("UPDATE reptable SET route_date = CONVERT(varchar,route_date,106) WHERE id = 2190")

        # создаем горизонтальную шапку
        for col in range(self.table_model.columnCount()):
            self.table_model.setHeaderData(col, QtCore.Qt.Horizontal, COLUMNS_REPORT[col])

    def create_table_view(self):
        # ------------- ВИЗУАЛИЗАЦИЯ---------------------

        # вставляем модель в tableview
        self.table_view.setModel(self.table_model)

        # Скрываем колонку ID
        self.table_view.hideColumn(0)

        # меняем шрифт шапки
        self.table_view.horizontalHeader().setFont(TITLE_FONT)


        # включаем сортировку
        # TODO сортировка по дате
        self.table_view.sortByColumn(COLUMNS_REPORT.index("Дата"), QtCore.Qt.DescendingOrder)
        # self.table_view.sortByColumn(COLUMNS_REPORT.index("Дата"), QtCore.Qt.DescendingOrder)

        # расширяем строки
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()

        # Расширяем окно, согласно длинны таблицы
        table_width = table_size(self.table_view)
        # устанавливаем ширину окна
        self.setFixedWidth(table_width)

    def move_view_columns(self,*views):
        # TODO автоматическое подтягивание индекса колонки с SQL
        for el in views:
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Менеджер"), 2)
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("гос.№"), 5)
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Культура"), 3)
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Тел"), 8)

    def start_date_edit(self):
        self.date1 = self.dateEdit.date().toString("yyyy-MM-dd")
        self.date2 = self.dateEdit_2.date().toString("yyyy-MM-dd")

        # ФИЛЬТРАЦИЯ МОДЕЛИ!
        self.table_model.setFilter(f"route_date BETWEEN '{self.date1}' AND '{self.date2}'")
        self.table_view.resizeRowsToContents()


