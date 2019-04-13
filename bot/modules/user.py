import types
import re
import bot.user_plugins as plugins


def init():
    module.db.check_table("accounts", id="INTEGER AUTO_INCREMENT PRIMARY KEY", vkid="INTEGER NOT NULL", nickname="TEXT NOT NULL")


class User(*plugins.get_plugins()):
    def __init__(self, vkid):
        user = self.load_user(vkid)
        if user is None:
            columns = [[], []]
            for key in module.registration.columns.keys():
                formatted_column = module.registration.columns[key](vkid) if isinstance(module.registration.columns[key], types.FunctionType) \
                                   else module.registration.columns[key]
                columns[0].append(key)
                columns[1].append("'{}'".format(formatted_column))
            module.db.query("INSERT INTO accounts ({}) VALUES ({})".format(','.join(columns[0]), ','.join(columns[1])))
            user = self.load_user(vkid)
        for key in user.keys():
            setattr(self, key, user[key])
        self.modify = {}

    def add(self, column, value):
        if column not in self.modify:
            self.modify[column] = {'action': 'add', 'value': value}
        else:
            self.modify[column]['value'] += value
        setattr(self, column, getattr(self, column) + value)

    def set(self, column, value):
        self.modify[column] = {'action': 'set', 'value': value}
        setattr(self, column, value)

    def save(self):
        modified_columns = []
        for key in self.modify.keys():
            if self.modify[key]['action'] == 'set':
                modified_columns.append("{} = '{}'".format(key, self.modify[key]['value']))
            else:
                modified_columns.append("{} = {} + '{}'".format(key, key, self.modify[key]['value']))
        if len(modified_columns) == 0:
            return
        module.db.query("UPDATE accounts SET {} WHERE vkid = {}".format(','.join(modified_columns), self.vkid))


    @staticmethod
    def load_user(vkid):
        return module.db.query_one("SELECT * FROM accounts WHERE vkid = {}".format(vkid))

    @staticmethod
    def load_from_link(link):
        match = re.findall(r'\[id(\w+)\|.+\]', link)
        if len(match) != 0 and User.load_user(match[0]) is not None:
            return User(match[0])
        else:
            return None
