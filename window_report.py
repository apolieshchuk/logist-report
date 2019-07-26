import operator

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

        # TODO вынести в функцию
        # устанавливаем диапазон дат по умолчанию
        date1 = QtCore.QDate.currentDate().addMonths(-2)
        date2 = QtCore.QDate.currentDate().addDays(+1)
        self.dateEdit.setDate(date1)
        self.dateEdit_2.setDate(date2)
        # слушатели диапазона дат
        self.dateEdit.dateChanged.connect(self.start_date_edit)
        self.dateEdit_2.dateChanged.connect(self.start_date_edit)

        # Создаем таблицу
        from window_main import mysql
        self.table_model = create_table_model(mysql.DB, 'reptable')
        self.create_table_view()
        self.table_model.select()


        # создаем фильтр боксы
        self.filter_box = FilterBoxes(self.filter_view, self.table_view)
        self.table_view.setFilterBox(self.filter_box)



        # сортировка таблицы
        # self.table_model.setSort(1,QtCore.Qt.DescendingOrder)
        # self.table_model.setSort(3, QtCore.Qt.DescendingOrder)
        # self.table_model.select()

        # двигаем колонки на фильтрах и в основной табилце
        # self.move_view_columns(self.table_view,self.filter_box.filter_view)

        # слушатель кнопок
        self.excel_but.clicked.connect(self.export_to_excel)
        self.autoInTime_but.clicked.connect(self.autoInTime_report)
        self.autoToday_but.clicked.connect(lambda : self.autoInTime_report(True))
        self.clear_filer_but.clicked.connect(lambda : self.filter_box.clearFilters())

        # TODO вывод в иксель даті в правильном формате

    def create_table_view(self):

        # Закрываем созданый в конструкторе класс и создаем вместо него другой
        self.table_view.close()
        self.table_view = MyTableView(self.centralwidget)
        self.table_view.setSortingEnabled(False)
        self.table_view.setObjectName("table_view")
        self.verticalLayout_2.addWidget(self.table_view)

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
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Дата"), 70)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Менеджер"), 80)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Культура"), 70)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Тел"), 95)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("ф2"), 5)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("ф1"), 5)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("ТР"), 5)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Перевозчик"), 200)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Маршрут"), 240)
        self.table_view.setColumnWidth(COLUMNS_REPORT.index("Примітка"), 180)

        # Расширяем окно, согласно длинны таблицы
        table_width = table_size(self.table_view)
        # устанавливаем ширину окна #TODO +30плохо
        self.setFixedWidth(table_width+30)

        # фильтруем по установленному диапазону дат
        self.start_date_edit()

    def start_date_edit(self):
        self.date1 = self.dateEdit.date().toString("yyyy-MM-dd")
        self.date2 = self.dateEdit_2.date().toString("yyyy-MM-dd")


        # ФИЛЬТРАЦИЯ И СОРТИРОВКА МОДЕЛИ!
        self.table_model.setFilter(f"route_date BETWEEN '{self.date1}' AND '{self.date2}' "
                                   f" ORDER BY route_date DESC, id DESC")

        # self.table_view.resizeRowsToContents()э

    def autoInTime_report(self,today = False):

        if today:
            # Создаем модель для фильтрации по сегодняшнему дню
            model = QtCore.QSortFilterProxyModel()
            model.setFilterKeyColumn(COLUMNS_REPORT.index("Дата"))
            model.setSourceModel(self.table_model)  # что фильтруем?
            today = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
            model.setFilterRegExp(f"{today}")
        else:
            model = self.table_view.model()

        # TODO ошибка в случае если таблица уже отфильртована (QSortFilterModel)
        try:
            while model.canFetchMore():
                model.fetchMore()
        except:
            pass

        # считаем авто на загрузках
        rows = model.rowCount()
        d = dict()
        col = COLUMNS_REPORT.index('Маршрут')
        for row in range(rows):
            route = model.index(row, col).data()
            if route in d:
                d[route] += 1
            else:
                d[route] = 1

        # Сортируем словарь
        sorted_dict = sorted(d.items(), key=operator.itemgetter(0))

        s = ''
        # Основное поле сообщения
        summy = 0
        for k,v in sorted_dict:
            temp = f'{k}: {v} авто \n'
            s += temp
            summy += v

        # Итог
        s += '\n'
        s += f"Всего: {summy}"

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(s)
        msgBox.exec()

    def export_to_excel(self):
        # create blank Workbook

        wb = Workbook()
        sheet = wb['Sheet']

        # шапка отчета
        head = COLUMNS_REPORT[1:]
        # специально для трансформации TODO
        head[7:7] = ["Ім`я","По-батьк","Посв"]
        sheet.append(head)

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

        # специально для трансформации TODO
        auto_num = self.table_view.model().index(row_num, COLUMNS_REPORT.index("гос.№")).data()
        dr_surn = self.table_view.model().index(row_num, COLUMNS_REPORT.index("Водитель")).data()
        from window_main import mysql
        sql = mysql.DB.exec(f"SELECT dr_name,dr_fath, notes FROM auto"
                            f" WHERE auto_num='{auto_num}' AND dr_surn = '{dr_surn}'")
        sql.next()
        row[7:7] = [sql.value(i)for i in range(3)]
        return row


class DateFormatDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, date_format):
        QtWidgets.QStyledItemDelegate.__init__(self)
        self.date_format = date_format

    def displayText(self, value, locale):
        date = QtCore.QDate().fromString(value, 'yyyy-MM-dd')
        return date.toString(self.date_format)


        # переписываем клик ивент
class MyTableView(QtWidgets.QTableView):
    def __init__(self,*args):
        self.filter_box = None
        super().__init__(*args)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        delAction = menu.addAction("Удалить")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == delAction:
            id = self.id_clicked(event)
            from window_main import mysql
            mysql.DB.exec(f"DELETE FROM reptable WHERE id = {id};")
            # TODO в случае фильтрации - еррор
            # self.model().select()  # при фильтрации еррор?
            try:
                # TODO в случае фильтрации - еррор
                self.model().select() # при фильтрации еррор?
            except:
                # в случае с фильтром - добираемся до самой глубокой модели MySQLTable
                rootModel = self.model().sourceModel()
                while type(rootModel).__name__ != 'MySqlTableModel':
                    rootModel = rootModel.sourceModel()
                rootModel.select()
                self.setModel(rootModel)
                self.filter_box.clearFilters()

    def id_clicked(self,event):
        pos = event.pos()
        ind = self.indexAt(pos)
        row = ind.row()
        # сохраняем ID выбранного поля
        id = self.model().index(row, 0).data()  # выбранный ID при дабл клике
        return id

    def setFilterBox(self,filter_box):
        self.filter_box = filter_box