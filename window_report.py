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

        # устанавливаем диапазон дат
        date1 = QtCore.QDate.currentDate().addMonths(-1)
        date2 = QtCore.QDate.currentDate()
        self.dateEdit.setDate(date1)
        self.dateEdit_2.setDate(date2)





        # Создаем таблицу за определенную дату
        self.create_table_model()
        self.create_table_view()

        # создаем фильтр боксы
        self.filter_box = FilterBoxes(self.filter_view,self.table_view)

        # двигаем колонки на фильтрах и в основной табилце
        self.move_view_columns(self.table_view,self.filter_box.filter_view)



        #TODO вывод в иксель
        #TODO отчет выводится за диапазон


    def create_table_model(self):

        # ------------- МОДЕЛЬ---------------------

        # создаем модель таблицы
        from window_main import DB
        self.table_model = QtSql.QSqlTableModel(None, DB)
        self.table_model.setTable("reptable")
        self.table_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.table_model.select()

        !!!sql = DB.exec("SELECT route_date FROM reptable WHERE route_date > date('now')")
        print("OK!!!")
        while sql.next():
            print(f"{sql.value(0)}")

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

        # Расширяем окно, согласно длинны таблицы
        table_width = table_size(self.table_view)
        # устанавливаем ширину окна
        # TODO непонятно почему узко считает ширину окна
        self.setFixedWidth(table_width+30)

        # включаем сортировку
        # TODO сортировка по дате
        self.table_view.sortByColumn(COLUMNS_REPORT.index("id"), QtCore.Qt.DescendingOrder)

        # расширяем строки
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()

    def move_view_columns(self,*views):
        # TODO автоматическое подтягивание индекса колонки с SQL
        for el in views:
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Менеджер"), 2)
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("гос.№"), 5)
            el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Культура"), 3)

