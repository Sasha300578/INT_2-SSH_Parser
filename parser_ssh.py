import ipaddress
import logging
from paramiko import AutoAddPolicy, AuthenticationException, SSHClient, ssh_exception

from db import Database

class Parser:
    def __init__(self, db):
        # Данные для подключения по SSH
        self.host = None
        self.connection = None
        self.log_file()
        self.db = db
        self.data_from_Linux = None


    # Проверка корректности введенных данных для GUI
    def check_correct_data(self, host, port, username, password):
        if ipaddress.IPv4Address(host):
            if 1 <= port <= 65535:
                if username and password:
                    return True
        return False


    # Ввод данных для подключения
    def host_info_gui(self, host, port, username, password):
        self.host = (host, port, username, password)


    # Лог выполненных команд
    def log_file(self):
        logging.basicConfig(filename='cmd_log.txt', level=logging.INFO, format='Time: %(asctime)s; info about command: %(message)s')


    # Подключение по SSH
    def ssh_connect(self):
        ssh_client = SSHClient()
        # Установка политики хоста
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            ssh_client.connect(hostname=self.host[0], port=self.host[1], username=self.host[2], password=self.host[3], banner_timeout=300)
            # Запись данных в лог
            self.connection = ssh_client
            logging.info(f"Connection established to {self.host[0]} with username={self.host[2]} and password={self.host[3]}")
            print(f"Connection established to {self.host[0]} with username={self.host[2]} and password={self.host[3]}")
        except AuthenticationException:
            logging.warning(f"Authentication failed for {self.host[0]} with username={self.host[2]} and password={self.host[3]}")

        except ssh_exception.SSHException:
            logging.error(f"Failed to connect to {self.host[0]} - Rate limiting on server")


    # Закрытие подключения
    def do_close(self):
        self.connection.close()
        logging.info(f"Connection closed: {self.connection}")


    # Выполнение команд
    def execute_command(self, connect, command, host):
        stdin, stdout, stderr = connect.exec_command(command)
        stdin.close()
        output = stdout.read().decode('utf-8').strip()
        logging.info(f'Command executed on {host}: {command}')
        return output


    # Управление запуском команд
    def do(self):
        try:
            os_name_cmd = "uname -s"
            os_version_cmd = "uname -r"
            os_arch_cmd = "uname -m"
            os_core_cmd = 'uname -a'
            lsb_release_cmd = 'lsb_release -a'

            os_name = self.execute_command(self.connection, os_name_cmd, self.host[0])
            os_version = self.execute_command(self.connection, os_version_cmd, self.host[0])
            os_arch = self.execute_command(self.connection, os_arch_cmd, self.host[0])
            os_core = self.execute_command(self.connection, os_core_cmd, self.host[0])
            lsb_release = self.execute_command(self.connection, lsb_release_cmd, self.host[0])

            self.data_from_Linux = f"Host: {self.host[0]}\n"
            self.data_from_Linux += f"Port: {self.host[1]}\n"
            self.data_from_Linux += f"User: {self.host[2]}\n"
            self.data_from_Linux += f"Password: {self.host[3]}\n"
            self.data_from_Linux += f"OS: {os_name}\n"
            self.data_from_Linux += f"Version: {os_version}\n"
            self.data_from_Linux += f"Architecture: {os_arch}\n"
            self.data_from_Linux += f"Core: {os_core}\n"
            self.data_from_Linux += f"Common information: {lsb_release}\n"
            self.data_from_Linux += f"log of commands in file: cmd_log.txt\n"
            self.data_from_Linux += "\n"
            print(self.data_from_Linux)
            self.db.fetch_all_data()

            # Запись полученной информации в БД
            data = (self.host[0], self.host[1], self.host[2], self.host[3], os_name, os_version, os_arch, os_core, lsb_release)
            self.db.insert_data(data)

        except Exception as err:
            print(f'Error: {str(err)}')

        self.do_close()