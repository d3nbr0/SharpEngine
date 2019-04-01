from engine.other import console

actions = {}


def add(name, execute):
    actions[name] = execute


def do(name, *args):
    if name not in actions:
        console.error("Обработчик для события \"{}\" не найден. Добавьте\
 обработчик, либо отключите эту настройку в группе".format(name))
    else:
        actions[name](*args)
