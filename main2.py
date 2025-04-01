
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QStandardItem, QStandardItemModel
import sys
from autorization import Ui_Vhod
from menu import Ui_Menu
from db import Database
from zakaz import Ui_Zakaz
from mainWindow import Ui_MainWIndow
from check import Ui_Check

class Vhod(QMainWindow, Ui_Vhod):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Авторизация")
        self.db = Database()
        self.pushButton.clicked.connect(self.vhod)

    def vhod(self):
        login = str(self.lineEdit.text().strip()) # Удаляем лишние пробелы
        password = str(self.lineEdit_2.text().strip())

        data = self.db.autorization(login, password)
        if data:
            print("Успешный вход!")  # Отладка
            self.menu = MainWindow()
            self.menu.show()
            self.hide()
        else:
            print("Ошибка входа!")  # Отладка
            self.label.setText("Неверный логин или пароль!")

class MainWindow(QMainWindow, Ui_MainWIndow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Главное окно")
        self.db = Database()
        self.pushButton.clicked.connect(self.zakaz)
        self.pushButton_2.clicked.connect(self.check)
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton_5.clicked.connect(self.menu)
        self.zakazi_now()

    def zakazi_now(self):
        data = self.db.zakazi_now()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Номер стола", "Блюдо","Кол.персон", "Цена"])
        for row in data:
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)
        self.tableView.setModel(model)

    def zakaz(self):
        self.zakaz = NewZakaz()
        self.zakaz.show()
        self.hide()
    def menu(self):
        self.menuu = FoodMenu()
        self.menuu.show()
        self.hide()
    def back(self):
        self.backk = Vhod()
        self.backk.show()
        self.hide()
    def check(self):
        self.checkk = NewCheck()
        self.checkk.show()
        self.hide()

class NewCheck(QMainWindow, Ui_Check):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Новый чек")
        self.db = Database()
        self.pushButton.clicked.connect(self.poisk)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.new_check)

    def poisk(self):
        namber = str(self.lineEdit.text().strip())
        data = self.db.zakazi_check(namber)

        if data:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["Номер стола", "Блюдо","Кол.персон", "Цена"])
            for row in data:
                items = [QStandardItem(str(item)) for item in row]
                model.appendRow(items)
            self.tableView.setModel(model)
        else:
            self.label.setText("Ошибка!")

    def new_check(self):
        stol = str(self.lineEdit.text().strip())
        data = self.db.new_check(stol)  # Предполагается, что это ваш метод для обращения к БД
        if data:
            self.label_3.setText(f"Сумма: {data}")  # Устанавливаем текст в QLabel
        else:
            self.label_3.setText("Ошибка!")

    def back(self):
        self.backk = MainWindow()
        self.backk.show()
        self.hide()


class FoodMenu(QMainWindow, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Наше меню")
        self.db = Database()

        self.nextList = 0
        self.backList = 3
        self.food = self.db.get_menu() or []

        self.update_labels()
        self.pushButton_2.clicked.connect(self.next)
        self.pushButton.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.mainWindow)

    def update_labels(self):
        self.name.setText("")
        self.name_3.setText("")
        self.name_5.setText("")
        self.description.setText("")
        self.description_3.setText("")
        self.description_5.setText("")
        self.sale.setText("")
        self.sale_3.setText("")
        self.sale_5.setText("")

        try:
            if self.nextList < len(self.food):
                food1 = self.food[self.nextList]
                self.name.setText(f'{food1[0]}')
                self.description.setText(f'{food1[1]}')
                self.sale.setText(f'{food1[2]} рублей')

            if self.nextList +1 < len(self.food):
                food2 = self.food[self.nextList+1]
                self.name_3.setText(f'{food2[0]}')
                self.description_3.setText(f'{food2[1]}')
                self.sale_3.setText(f'{food2[2]} рублей')

            if self.nextList + 2 < len(self.food):
                food3 = self.food[self.nextList+2]
                self.name_5.setText(f'{food3[0]}')
                self.description_5.setText(f'{food3[1]}')
                self.sale_5.setText(f'{food3[2]} рублей')

        except IndexError as e:
            print(f"Ошибка:, {e}")


    def next(self):
        if self.backList >= len(self.food):
            return
        self.nextList += 3
        self.backList += 3
        self.update_labels()

    def back(self):
        if self.nextList == 0:
            return
        self.nextList -= 3
        self.backList -= 3
        self.update_labels()

    def mainWindow(self):
        self.main= MainWindow()
        self.main.show()
        self.hide()


class NewZakaz(QMainWindow,Ui_Zakaz):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Окно официанта")
        self.db = Database()
        self.pushButton.clicked.connect(self.zakaz)
        self.pushButton_2.clicked.connect(self.back)

        self.menu()

    def back(self):
        self.backk = MainWindow()
        self.backk.show()
        self.hide()

    def menu(self):
        data = self.db.get_menu()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Наименование", "Состав", "Цена"])
        for row in data:
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)

            self.tableView.setModel(model)

    def zakaz(self):
        id_stol = str(self.lineEdit.text().strip())
        id_b = str(self.lineEdit_2.text().strip())
        count_p = str(self.lineEdit_3.text().strip())
        try:

            data = self.db.zakaz(id_stol,id_b,count_p )
            if data:
                self.label.setText("Заказ не создан!")
            else:
                self.label.setText("Заказ создан!")


        except Exception as e:

            print(f"Ошибка при создании заказа: {e}")

            self.label.setText("Произошла ошибка!")




if __name__ == "__main__":
    app = QApplication([])
    main = Vhod()
    main.show()
    sys.exit(app.exec())

