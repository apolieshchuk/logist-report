from PyQt5 import QtSql, QtCore
from PyQt5.QtGui import QFont



DEBUG = True
LOCAL_SERVER = False
RECONNECT_TIME_MYSQL = 55 #seconds

TITLE_FONT = QFont("Helvetica", 10, QFont.Bold)  # Шрифт заголовка

# COPY_BUFFER_PATTERN = "name,code,mark,auto_num,trail_num,dr_dr_surn,dr_name,dr_fath,tel,notes"
COLUMNS_AUTO = ["id", "v", "Назва", "ЄДРПОУ", "Марка", "№ авто", "№ прич", "Прізвище",
                "Ім`я", "По-батькові", "Телефон", "Замітки","v2"]
COPY_BUFFER_PATTERN = [2, 4, 5, 6, 7, 8, 9, 10, 11]  # шаблон копирования авто в буфер (номера колонок)

COLUMNS_ROUTE_INFO = ["id", "Перевозчик", "Авто", "Вод", "Тел","ф2", "ф1", "ТР", "Прим."]
ROUTE_INFO_PATTERN = ["id", "name", "auto_num", "dr_surn","tel"]  # шаблон для внесения инфы по загрузке согласно ID авто

COLUMNS_REPORT = ["id", "Дата", "Менеджер",  "Культура", "Маршрут", "Перевозчик","гос.№", "Водитель", "Тел",
                     "ф2", "ф1", "ТР","Примітка"]

MANAGERS = ["ДемченкоВП","СалюкС","ЦыбенкоМВ","ГулинЛА","СкворцоваВН","ТютюнникЮ",
            "ПолещукАИ","ЗаливнойМ","БуртникР","КОММЕРЦИЯ","ШарпакВ","РудаО","KSG"]
CROPS = ["соняшник","пшениця","кукуруза","соя","висівки","ячмінь"]



def table_size(table_view):
    # ширина колонок таблицы
    head = table_view.horizontalHeader()
    head_sections = head.count()
    table_width = 0
    for i in range(head_sections):
        table_width += head.sectionSize(i)
    # ширина вертикальнгго хедера
    vert_head_width = table_view.verticalHeader().width()
    # скрол бар
    scroll = 45
    return table_width + vert_head_width + scroll

def create_table_model(DB,table):

    # создаем модель таблицы
    table_model = MySqlTableModel(None, DB, table)
    table_model.setTable(table)
    table_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
    table_model.select()

    # создаем горизонтальную шапку
    head = None
    if table == 'auto': head = COLUMNS_AUTO
    if table == 'reptable': head = COLUMNS_REPORT
    if table == 'routes': head = ['id', 'Маршрут']
    for col in range(table_model.columnCount()):
        table_model.setHeaderData(col, QtCore.Qt.Horizontal, head[col])

    return table_model

class MySqlTableModel(QtSql.QSqlTableModel):

    def __init__(self, *args, **kwargs):
        QtSql.QSqlTableModel.__init__(self, args[0], args[1])
        self.table = args[2] # таблица с которой будем работать
        self.checkeable_data = {}

    def flags(self, index):
        if self.table == 'auto':
            if index.column() == COLUMNS_AUTO.index("v") or \
                    index.column() == COLUMNS_AUTO.index("v2"):
                return QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        return QtSql.QSqlTableModel.flags(self, index)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.CheckStateRole and (self.flags(index)&
                                                 QtCore.Qt.ItemIsUserCheckable !=
                                                 QtCore.Qt.NoItemFlags):
            if index.row() not in self.checkeable_data.keys():
                self.setData(index, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
            return self.checkeable_data[index.row()]
        else:
            return QtSql.QSqlTableModel.data(self, index, role)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.CheckStateRole and (self.flags(index)&
                                                 QtCore.Qt.ItemIsUserCheckable !=
                                                 QtCore.Qt.NoItemFlags):
            self.checkeable_data[index.row()] = value
            self.dataChanged.emit(index, index, (role,))
            return True
        return QtSql.QSqlTableModel.setData(self, index, value, role)

