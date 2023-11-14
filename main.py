import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from db import Database
from parser_ssh import Parser
import ipaddress


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ssh = Parser(None)

        # Создание виджетов
        self.host_label = QLabel('Host:')
        self.host_input = QLineEdit()
        self.port_label = QLabel('Port:')
        self.port_input = QLineEdit()
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.parse_button = QPushButton('Parse data from Linux')
        self.search_by_ip = QPushButton('Search for data in the database by IP')
        self.output_text = QTextEdit()

        # Размещение виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_input)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.search_by_ip)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

        # Добавление нажатий на кнопки
        self.parse_button.clicked.connect(self.button_parse_clicked)
        self.search_by_ip.clicked.connect(self.button_search_clicked)

        # Параметры формы
        self.setWindowTitle('SSH_parser')
        self.setGeometry(100, 200, 800, 600)


    def button_parse_clicked(self):
        try:
            try:
                fl_ip = 0
                host = self.host_input.text()
                ip = ipaddress.IPv4Address(host)
            except:
                self.output_text.setPlainText("Host is invalid.")
                fl_ip = 1

            try:
                fl_port = 0
                port = int(self.port_input.text())
            except:
                fl_port = 1
                self.output_text.setPlainText("Port is invalid.")

            username = self.username_input.text()
            password = self.password_input.text()

            db = Database()
            self.ssh.db = db

            if fl_port == 0 and fl_ip == 0:
                # Данные для подключения
                self.ssh.host_info_gui(host, port, username, password)

                # Подключение SSH
                self.ssh.ssh_connect()

                # Выполнение метода do_run
                self.ssh.do()

                # Вывод результатов в текстовое поле
                self.output_text.setPlainText(self.ssh.data_from_Linux)
        except:
            self.output_text.setPlainText("Check the correctness of the entered data.")


    def button_search_clicked(self):
        try:
            try:
                host = self.host_input.text()
                ip = ipaddress.IPv4Address(host)
            except:
                self.output_text.setPlainText("Host is invalid.")

            db = Database()
            self.ssh.db = db

            data =  self.ssh.db.search_by_ip(host)
            if data != "":
                self.output_text.setPlainText(data)
            else:
                1 / 0
        except:
            self.output_text.setPlainText("No data found")


def __main__():
    try:
        app = QApplication(sys.argv)
        gui = GUI()
        gui.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


__main__()
