import csv

from PyQt5.QtSql import *

import mysql.connector

class My_Sql():

    def connect_db(self):
        #SQLITE
        # DB = QSqlDatabase().addDatabase('QSQLITE')  # Чем читаем Sql. QSQLITE- для sqlite
        # DB.setDatabaseName(path)  # Путь к базе данных
        # DB = QSqlDatabase().addDatabase('QODBC','odbc connection')
        # DB.setDatabaseName("Driver={MySQL ODBC 8.0 Unicode Driver};SERVER = 10.12.1.240;"
        #                    "DATABASE=logist_report;UID=logist;PWD=1cjDaw4RNjhMp7")

        # MYSQL
        # DB = QSqlDatabase().addDatabase('QMYSQL','mysql connection')
        # DB.setHostName("10.12.1.240")
        # DB.setDatabaseName("auto")
        # DB.setUserName("logist")  # Путь к базе данных
        # DB.setPassword("1cjDaw4RNjhMp7")

        # ODBC
        DB = QSqlDatabase().addDatabase('QODBC', 'odbc connection')
        DB.setDatabaseName("Driver={MySQL ODBC 8.0 Unicode Driver};SERVER = 10.12.1.240;"
                           "DATABASE=logist_report;UID=logist;PWD=1cjDaw4RNjhMp7")

        if DB.open():  # Открываем базу данных
            print("BD OPENING!!")
        return DB

    @staticmethod
    def add_report_from_csv(csv,db):
        report = My_Sql.csv_to_list(csv)
        print(report[1])
        for el in report:
            db.exec(f"""INSERT INTO reptable(route_date,manager,route,crop,carrier,auto_num,dr_surn,f2,f1,tr) VALUES (
                                                  '{el['route_date']}',
                                                  '{el['manager']}',
                                                  '{el['route']}',
                                                  '{el['crop']}',
                                                  '{el['carrier']}',
                                                  '{el['auto_num']}',
                                                  '{el['dr_surn']}',
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
    def sqlite_to_mysql(db_mysql,path_to_sqlite):
        db_sqlite = QSqlDatabase().addDatabase('QSQLITE', 'sqlite connection')  # Чем читаем Sql. QSQLITE- для sqlite
        db_sqlite.setDatabaseName(path_to_sqlite)  # Путь к базе данных

        # DEBUG for opening
        if (db_sqlite.open()):
            print('SQLITE OPENED')
        if(db_mysql.open()):
            print('MYSQL OPENED')


        # insert auto
        # sql = db_sqlite.exec_("SELECT * FROM auto")
        # # print(sql.size())
        # while sql.next():
        #     row = []
        #     for col in range(12):
        #         row.append(sql.value(col))
        #     sql2 = f"""INSERT INTO auto(chk, name, code, mark, auto_num,
        #                                 trail_num, dr_surn, dr_name, dr_fath, tel, notes)
        #               VALUES ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}',
        #               '{row[8]}','{row[9]}','{row[10]}','{row[11]}')"""
        #     db_mysql.exec_(sql2)

        # insert Reptable
        # sql = db_sqlite.exec_("SELECT * FROM reptable")
        # while sql.next():
        #     row = []
        #     for col in [0,1,8,10,2,3,9,4,11,5,6,7]:
        #         row.append(sql.value(col))
        #     row.append("")
        #     print(row)
        #     sql2 = f"INSERT INTO reptable(route_date, manager, crop, route,carrier, auto_num, dr_surn, tel, f2, f1, tr, notes)" \
        #            f" VALUES ('{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}','{row[7]}','{row[8]}','{row[9]}'," \
        #            f"'{row[10]}','{row[11]}','{row[12]}')"
        #     db_mysql.exec_(sql2)

        # insert routes
        # sql = db_sqlite.exec_("SELECT * FROM routes")
        # while sql.next():
        #     row = []
        #     for col in [0,1]:
        #         row.append(sql.value(col))
        #     row.append("")
        #     print(row)
        #     sql2 = f"INSERT INTO routes(route) VALUES ('{row[1]}')"
        #     db_mysql.exec_(sql2)

    @staticmethod
    def replace_val_in_col(db):
        sql = f"UPDATE auto SET chk = ''"
        db.exec(sql)
        db.commit()
