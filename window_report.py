from PyQt5 import QtWidgets, QtSql, QtCore
from files.ui import design_report
from filter_boxes import FilterBoxes
from openpyxl import Workbook

from static import COLUMNS_AUTO, TITLE_FONT, COLUMNS_REPORT, table_size, create_table_model


class ReportWindow(QtWidgets.QMainWindow, design_report.Ui_ReportWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        # from my_sql import My_Sql
        # self.DB = My_Sql.connect_db(str(self))

        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # меняем титл окна
        self.setWindowTitle("Отчет")

        # Создаем таблицу
        from window_main import DB
        self.table_model = create_table_model(DB, 'reptable')
        self.create_table_view()

        # TODO вынести в функцию
        # устанавливаем диапазон дат по умолчанию
        date1 = QtCore.QDate.currentDate().addMonths(-6)
        date2 = QtCore.QDate.currentDate().addDays(+1)
        self.dateEdit.setDate(date1)
        self.dateEdit_2.setDate(date2)
        # слушатели диапазона дат
        self.dateEdit.dateChanged.connect(self.start_date_edit)
        self.dateEdit_2.dateChanged.connect(self.start_date_edit)
        # фильтруем по установленному диапазону дат
        self.start_date_edit()

        # создаем фильтр боксы
        self.filter_box = FilterBoxes(self.filter_view, self.table_view)

        # сортировка таблицы
        # self.table_model.setSort(1,QtCore.Qt.DescendingOrder)
        # self.table_model.setSort(3, QtCore.Qt.DescendingOrder)
        # self.table_model.select()

        # двигаем колонки на фильтрах и в основной табилце
        # self.move_view_columns(self.table_view,self.filter_box.filter_view)

        # слушатель кнопки
        self.excel_but.clicked.connect(self.export_to_excel)
        # слушатель клика таблицы
        self.table_view.clicked.connect(self.table_clicked)

        # TODO вывод в иксель даті в правильном формате

    def create_table_view(self):
        # ------------- ВИЗУАЛИЗАЦИЯ---------------------

        # вставляем модель в tableview
        self.table_view.setModel(self.table_model)

        # Скрываем колонку ID
        self.table_view.hideColumn(0)

        # меняем шрифт шапки
        self.table_view.horizontalHeader().setFont(TITLE_FONT)

        # включаем сортировку
        # Недостаток - только по одной колонке
        # self.table_view.sortByColumn(COLUMNS_REPORT.index("Дата"), QtCore.Qt.DescendingOrder)


        # Форматируем вывод даты на экран отчета
        # self.table_view.setItemDelegateForColumn(COLUMNS_REPORT.index("Дата"),
        #                                          DateFormatDelegate('dd/MMM/yyyy'))

        # расширяем строки и столбцы
        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Тел"), 95)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Перевозчик"), 200)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Маршрут"), 240)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Примітка"), 180)

        # Расширяем окно, согласно длинны таблицы
        table_width = table_size(self.table_view)
        # устанавливаем ширину окна
        self.setFixedWidth(table_width)

    def move_view_columns(self, *views):
        pass
        # # TODO автоматическое подтягивание индекса колонки с SQL
        # for el in views:
        #     el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Менеджер"), 2)
        #     el.horizontalHeader().moveSection(COLUMNS_REPORT.index("гос.№"), 5)
        #     el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Культура"), 3)
        #     el.horizontalHeader().moveSection(COLUMNS_REPORT.index("Тел"), 8)

    def start_date_edit(self):
        self.date1 = self.dateEdit.date().toString("yyyy-MM-dd")
        self.date2 = self.dateEdit_2.date().toString("yyyy-MM-dd")

        # ФИЛЬТРАЦИЯ И СОРТИРОВКА МОДЕЛИ!
        self.table_model.setFilter(f"route_date BETWEEN '{self.date1}' AND '{self.date2}' "
                                   f" ORDER BY route_date DESC, id DESC")

        # self.table_view.resizeRowsToContents()

    def export_to_excel(self):
        # create blank Workbook

        wb = Workbook()
        sheet = wb['Sheet']

        # шапка отчета
        sheet.append(COLUMNS_REPORT[1:])

        # отчет
        for row in range(self.table_view.model().rowCount()):
            # TODO проверка значений в ROW, QDate не добавит
            sheet.append(self.get_row_from_view(row))

        # расширяем колонки по значению
        for col in sheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if cell.coordinate in sheet.merged_cells:  # not check merge_cells
                    continue
                try:  # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = max_length + 2
            sheet.column_dimensions[column].width = adjusted_width

        try:
            filename = QtWidgets.QFileDialog().getSaveFileName()
            wb.save(filename[0] + '.xlsx')
        except:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setText("ОШИБКА при сохранении файла")
            messageBox.setFixedSize(500, 200)
            messageBox.exec_()

    def get_row_from_view(self, row_num):
        row = []
        # TODO какую-то нормальную синхронизацию колонок с ВЬЮ И МУСКУЛОМ
        for col in COLUMNS_REPORT[1:]:
            data = self.table_view.model().index(row_num, COLUMNS_REPORT.index(col)).data()
            if type(data).__name__ == 'QDate':
                data = data.toString('dd.MMM.yyyy')
            row.append(data)
        return row

    def table_clicked(self):
        row, column = None, None
        # код который определяет на кукую строку был сделан клик
        for idx in self.table_view.selectionModel().selectedIndexes():
            row = idx.row()
            column = idx.column()

        # сохраняем ID выбранного поля
        self.choice = self.table_view.model().index(row, 0).data()  # выбранный ID при дабл клике
        print(self.choice)

    def mousePressEvent(self,event):
        print("OK!!")
        super().mousePressEvent(event)


class DateFormatDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, date_format):
        QtWidgets.QStyledItemDelegate.__init__(self)
        self.date_format = date_format

    def displayText(self, value, locale):
        date = QtCore.QDate().fromString(value, 'yyyy-MM-dd')
        return date.toString(self.date_format)
