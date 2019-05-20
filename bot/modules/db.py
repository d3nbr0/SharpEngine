from engine.other import console
from contextlib import closing
import MySQLdb
import MySQLdb.cursors as cursors
import threading
from copy import deepcopy


connections = {}


def init():
    global connections
    connections = {}
    console.log("Подключение к MySQL серверу...")
    bot_config = module.config.get_bot()
    for i in range(1, int(bot_config['workers_count']) + 1):
        connections['Thread-{}'.format(i)] = Connection(
            host=bot_config['mysql_host'],
            user=bot_config['mysql_user'],
            passwd=bot_config['mysql_pass'],
            db=bot_config['mysql_base'],
            use_unicode=True,
            charset="utf8",
            cursorclass=cursors.DictCursor
        )
    connections['MainThread'] = Connection(
        host=bot_config['mysql_host'],
        user=bot_config['mysql_user'],
        passwd=bot_config['mysql_pass'],
        db=bot_config['mysql_base'],
        use_unicode=True,
        charset="utf8",
        cursorclass=cursors.DictCursor
    )


def query(line):
    global connections
    conn = connections[threading.current_thread().name]
    try:
        conn.cursor.execute(line)
        result = conn.cursor.fetchall()
        conn.db.commit()
    except Exception as ex:
        init()
        console.error("MySQL ошибка: {}".format(str(ex)))
        result = query(line)
    return result


def query_one(line):
    global connections
    conn = connections[threading.current_thread().name]
    try:
        conn.cursor.execute(line)
        result = conn.cursor.fetchone()
        conn.db.commit()
    except Exception as ex:
        init()
        console.error("MySQL ошибка: {}".format(str(ex)))
        result = query_one(line)
    return result


def check_table(name, **args):
    tables = query("SHOW TABLES")
    if tables is None:
        tables = ()
    bot_config = module.config.get_bot()
    for item in tables:
        if item['Tables_in_{}'.format(bot_config['mysql_base'])] == name:
            return True
    create_table(name, **args)


def create_table(name, **args):
    console.process("Создание таблицы \"{}\"...".format(name))
    unpacked_args = []
    for item in args.keys():
        unpacked_args.append("{} {}".format(item, args[item]))
    query("CREATE TABLE IF NOT EXISTS {} ({})".format(name, ','.join(unpacked_args)))
    console.success("Таблица успешно создана!")


def check_column(table, name, args):
    columns = query("SHOW COLUMNS FROM {}".format(table))
    if columns is None:
        columns = ()
    for item in columns:
        if item['Field'] == name:
            return True
    create_column(table, name, args)


def drop_column(table, name):
    console.process("Удаление поля \"{}\" из таблицы \"{}\"...".format(name, table))
    query("ALTER TABLE {}\
               DROP COLUMN {}".format(table, name))
    console.success("Поле успешно удалено!")


def create_column(table, name, args):
    console.process("Добавление поля \"{}\" в таблицу \"{}\"...".format(name, table))
    query("ALTER TABLE {}\
               ADD COLUMN {} {}".format(table, name, args))
    console.success("Поле успешно добавлено!")


class Connection:
    def __init__(self, **args):
        self.db = MySQLdb.connect(**args)
        self.cursor = self.db.cursor()
        self.cursor.execute('SET NAMES utf8mb4')
