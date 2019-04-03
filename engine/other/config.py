import configparser
import os
import sys
from engine.other import console


class Config:
    def __init__(self, name):
        self.config = configparser.ConfigParser()
        self.name = "{}.ini".format(name)
        if not os.path.exists(self.name):
            self.create_config()
        self.config.read(self.name)

    def create_config(self):
        console.log("Создание конфигурационного файла...")
        self.config.add_section("bot")
        self.config.set("bot", "access_token", "YOUR_TOKEN")
        self.config.set("bot", "group_id", "YOUR_ID")
        self.config.set("bot", "workers_count", "COUNT")
        self.config.set("bot", "mysql_host", "HOST")
        self.config.set("bot", "mysql_user", "USER")
        self.config.set("bot", "mysql_pass", "PASSWORD")
        self.config.set("bot", "mysql_base", "DATABASE")
        self.config.add_section('binds')
        self.save_config()
        console.process("Был создан новый конфигурационный файл. Пожалуйста,\
 настройте его перед началом использования бота")
        sys.exit(0)

    def save_config(self):
        with open(self.name, "w") as file:
            self.config.write(file)
        console.log("Конфигурационный файл \"{}\" успешно сохранён!".format(self.name))

    def get_bind(self, key):
        if key not in self.config['binds']:
            console.error("Ключ \"{}\" не найден в конфигурационном файле".format(key))
            return None
        else:
            return self.config['binds'][key]

    def set_bind(self, key, value):
        if value == "":
            self.config.remove_option('binds', key)
        else:
            self.config.set('binds', key, value)
        self.save_config()

    def get_bot(self):
        return self.config['bot']
