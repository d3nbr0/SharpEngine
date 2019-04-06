import os
import importlib
import bot.user_plugins as plugins

VK = None
config = None
__modules = None
blocked_modules = []
blocked_dirs = []
last_load = ["user"]


def load_modules():
    global config, VK, __modules
    __modules = None
    plugins.plugins = []
    this_modules = []
    for root, dirs, files in os.walk('bot\\modules'):
        if root not in blocked_dirs:
            check_modules = filter(lambda x: x.endswith('.py'), files)
            for item in check_modules:
                module = item[:-3]
                if module not in blocked_modules and module not in last_load:
                    add_module(root.replace('\\', '.'), module, this_modules)
    __modules = Module(this_modules + [{'name': 'config', 'module': config}, {'name': 'VK', 'module': VK}])
    for item in this_modules:
        init_module(item['module'])
    for module in last_load:
        add_module("bot.modules", module)
        init_module(getattr(__modules, module))


def add_module(path, module, this_modules=None):
    global __modules
    globals()[module] = importlib.import_module("{}.{}".format(path,
                                                               module))
    if this_modules is not None:
        this_modules.append({'name': module, 'module': globals()[module]})
    else:
        __modules.add(module, globals()[module])


def init_module(module):
    module.module = __modules
    module.error = catch
    if hasattr(module, 'init'):
        module.init()
    if hasattr(module, 'Plugin'):
        plugins.add_plugin(module.Plugin)


class Module:
    def __init__(self, modules):
        for item in modules:
            self.add(item['name'], item['module'])

    def add(self, name, module):
        setattr(self, name, module)


def catch(condition, message):
    if not condition:
        raise CommandException(message)


class CommandException(Exception):
    def __init__(self, message):
        self.message = message
