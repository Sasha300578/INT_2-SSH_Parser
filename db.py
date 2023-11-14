import sqlite3

class Database():
    def __init__(self):
        # Подключение к базе данных SQL Lite
        self.conn = sqlite3.connect('parser_ssh.db')
        self.create_table()
        self.data_from_db = None


     # Создание таблицы в БД
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parser_ssh (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                port INTEGER NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                os_name TEXT,
                os_version TEXT,
                os_arch TEXT,
                os_core TEXT,
                lsb_release TEXT
            )
        ''')
        self.conn.commit()


    # Добавление данных в БД
    def insert_data(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO parser_ssh (host, port, username, password, os_name, os_version, os_arch, os_core, lsb_release)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()


    # Вывод данных из БД (консоль)
    def fetch_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM parser_ssh')
        all_data = cursor.fetchall()

        for data in all_data:
            print("ID:", data[0])
            print("Host:", data[1])
            print("Port:", data[2])
            print("Username:", data[3])
            print("Password:", data[4])
            print("OS Name:", data[5])
            print("OS Version:", data[6])
            print("OS Architecture:", data[7])
            print("OS Core:", data[8])
            print("LSB Release:", data[9])
            print("_"*100)

    # Поиск по IP
    def search_by_ip(self, target_ip):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM parser_ssh WHERE host = ?", (target_ip,))
        result = cursor.fetchall()
        self.data_from_db = ""

        if result:
            for data in result:
                self.data_from_db += f"ID: {data[0]}\n"
                self.data_from_db += f"Host: {data[1]}\n"
                self.data_from_db += f"Port: {data[2]}\n"
                self.data_from_db += f"User: {data[3]}\n"
                self.data_from_db += f"Password: {data[4]}\n"
                self.data_from_db += f"OS: {data[5]}\n"
                self.data_from_db += f"Version: {data[6]}\n"
                self.data_from_db += f"Architecture: {data[7]}\n"
                self.data_from_db += f"Core: {data[8]}\n"
                self.data_from_db += f"Common information: {data[9]}\n"
                self.data_from_db += "\n"
        else:
            print(f"No data found for the IP: {target_ip}")

        print(self.data_from_db)
        return self.data_from_db

    # Закрытие SQL Lite подключения
    def __del__(self):
        self.conn.close()