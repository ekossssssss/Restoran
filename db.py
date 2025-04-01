import pymysql

class Database():
    def __init__(self):
        self.connection = pymysql.connect(
            host='MySQL-8.2',
            user='root',
            password='',
            db='stolovaia'
        )
        self.connection.autocommit(True)
        self.cursor = self.connection.cursor()
        print('Успешное подключение к БД')

    def get_menu(self):
        sql = "SELECT name_food, ingridienti, sale FROM food"
        try:
            self.cursor.execute(sql)
            menu = self.cursor.fetchall()
            print("Меню из БД:", menu)  # Для отладки
            return menu  # Возвращаем данные
        except Exception as e:
            print(f"Ошибка при получении меню: {e}")
            return []  # Возвращаем пустой список в случае ошибки


    def autorization(self, login, pasword):
        sql = "SELECT * FROM custom WHERE login = %s AND pasword = %s"
        self.cursor.execute(sql, (login, pasword))
        procedure = self.cursor.fetchall()
        return procedure

    def zakaz(self, id_stol, id_bluda, count_pers):
        sql = "call zakaz(%s, %s, %s)"
        self.cursor.execute(sql, (id_stol, id_bluda, count_pers))
        procedure = self.cursor.fetchall()
        return procedure

    def zakazi_now(self):
        sql = ("""select z.id_stol,
         f.name_food,z.count_person,
         z.count_zakaz
         from zakaz z
         inner join food f on f.id = z.id_food 
         where date(z.date_zakaz) = curdate()""")
        self.cursor.execute(sql,)
        procedure = self.cursor.fetchall()
        return procedure

    def zakazi_check(self, id_stol):
        sql = """ select z.id_stol,
         f.name_food,z.count_person,
         z.count_zakaz
         from zakaz z
         inner join food f on f.id = z.id_food 
         where date(z.date_zakaz) = curdate() and z.id_stol = %s"""
        self.cursor.execute(sql, (id_stol,))
        procedure = self.cursor.fetchall()
        return procedure
    def new_check(self, id_stol):
        sql = 'CALL chek(%s)'
        self.cursor.execute(sql, (id_stol,))
        procedure = self.cursor.fetchall()
        return procedure

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Соединение с БД закрыто")