from PyQt5 import QtSql
from PyQt5.QtGui import QFont

TITLE_FONT = QFont("Helvetica", 10, QFont.Bold)  # Шрифт заголовка

# COPY_BUFFER_PATTERN = "name,code,mark,auto_num,trail_num,dr_surname,dr_name,dr_fath,tel,notes"
COLUMNS_MAIN = ["id", "V", "Назва", "ЄДРПОУ", "Марка", "№ авто", "№ прич", "Прізвище",
                "Ім`я", "По-батькові", "Телефон", "Замітки"]
COPY_BUFFER_PATTERN = [2, 4, 5, 6, 7, 8, 9, 10, 11]  # шаблон копирования авто в буфер (номера колонок)

COLUMNS_ROUTE_INFO = ["id", "Перевозчик", "Авто", "Вод", "ф2", "ф1", "ТР"]
ROUTE_INFO_PATTERN = ["id", "name", "auto_num", "dr_surn"]  # шаблон для внесения инфы по загрузке согласно ID авто

COLUMNS_REPORT = ["id", "Дата", "Маршрут", "Перевозчик", "Водитель", "ф2", "ф1",
                  "Трансф", "Менеджер","гос.№", "Культура","Тел"]  # INSQL!

MANAGERS = ["ДемченкоВП","СалюкС","ЦыбенкоМВ","ГулинЛА","СкворцоваВН","ТютюнникЮ",
            "ПолещукАИ","ЗаливнойМ","БуртникР","КОММЕРЦИЯ","ШарпакВ"]
CROPS = ["соняшник","пшениця","кукуруза","соя","висівки"]


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
    scroll = 50
    return table_width + vert_head_width + scroll
