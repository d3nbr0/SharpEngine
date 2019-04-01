import engine.other.console as console
import sys


def listen():
    while True:
        text = input()
        if text in commands.keys():
            commands[text]()
        else:
            console.error("Команда \"{}\" не найдена.".format(text))


def close():
    console.success("Завершение работы...")
    sys.exit()


commands = {'close': close, 'exit': close, 'quit': close}
