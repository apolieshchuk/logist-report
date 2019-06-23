import csv
import os

from PyQt5 import QtSql
from dial_dbpath import DbPathWindow

class My_Sql():

    def connect_db(self,path):
        DB = QtSql.QSqlDatabase().addDatabase('QSQLITE')  # Чем читаем Sql. QSQLITE- для sqlite
        # DB.setDatabaseName("files/auto.db")  # Путь к базе данных
        DB.setDatabaseName(path)  # Путь к базе данных
        DB.open()  # Открываем базу данных
        return DB
        # # Открываем базу данных
        # pathWindow = DbPathWindow()
        # DB = None
        # # достаем последний путь к файлу
        # try:
        #     with open("files/sql/path.txt") as f:
        #         path = f.readline()
        #     pathWindow.line_edit.setText(path)
        # except:
        #     pass
        # if pathWindow.exec_():
        #     path = pathWindow.line_edit.text()
        #     if not os.path.isfile(path): return None # Проверяем наличие файла
        #
        #     # Сохраняем путь к файлу
        #     with open("files/sql/path.txt", 'w') as f:
        #         f.write(path)
    @staticmethod
    def add_report_from_csv(csv,db):
        report = My_Sql.csv_to_list(csv)
        print(report[1])
        for el in report:
            db.exec(f"""INSERT INTO reptable(route_date,manager,route,crop,carrier,auto_num,surname,f2,f1,tr) VALUES (
                                                  '{el['route_date']}',
                                                  '{el['manager']}',
                                                  '{el['route']}',
                                                  '{el['crop']}',
                                                  '{el['carrier']}',
                                                  '{el['auto_num']}',
                                                  '{el['surname']}',
                                                  '{el['f2']}',
                                                  '{el['f1']}',
                                                  '{el['tr']}'
                                              )""")
            db.commit()

    @staticmethod
    def data_format_in_db(db):
        sql = None

        # 1
        # sql = [
        #     "UPDATE reptable SET route_date = REPLACE(route_date,'янв','01')",
        #     "UPDATE reptable SET route_date = REPLACE(route_date,'фев','02')",
        #     "UPDATE reptable SET route_date = REPLACE(route_date,'апр','04')",
        #     "UPDATE reptable SET route_date = REPLACE(route_date,'май','05')",
        #     "UPDATE reptable SET route_date = REPLACE(route_date,'июн','06')",
        #     "UPDATE reptable SET route_date = REPLACE(route_date,'мар','03')",
        #     "UPDATE reptable SET route_date = '20'||substr(route_date,7,2)||'-'||substr(route_date,4,2)||'-'||substr(route_date,1,2)"
        # ]

        # 2
        # sql = ["UPDATE reptable SET route_date = strftime('%Y-%m-%d',route_date)"]

        # 3
        # sql = [
        #     f"UPDATE reptable SET route_date = REPLACE(route_date,'июнь','июн')",
        #     f"UPDATE reptable SET route_date = REPLACE(route_date,'февр','фев')",
        #     f"UPDATE reptable SET route_date = REPLACE(route_date,'март','мар')"
        # ]


        for el in sql:
            db.exec(el)
        db.commit()

    @staticmethod
    def csv_to_list(path):
        # Считываем с файла CSV всё во внутреннюю базу данных
        with open(path) as f:
            reader = csv.DictReader(f, delimiter=";")
            return [r for r in reader]

    @staticmethod
    def replace_val_in_col(db):
        sql = f"UPDATE mytable SET chk = ''"
        db.exec(sql)
        db.commit()
