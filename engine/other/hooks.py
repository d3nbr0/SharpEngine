from engine.other import console

actions = {}
handle = True
is_busy = False


def add(name, execute):
    actions[name] = execute


def do(name, *args):
    global is_busy
    if handle:
        if name not in actions:
            console.error("Обработчик для события \"{}\" не найден. Добавьте\
     обработчик, либо отключите эту настройку в группе".format(name))
        else:
            is_busy = True
            actions[name](*args)
            is_busy = False
