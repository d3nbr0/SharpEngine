import engine.other.console as console
import bot.bot as bot
import sys
from time import sleep

VK = None
config = None


def listen(this_vk, this_config):
    global VK, config
    VK = this_vk
    config = this_config
    while True:
        text = input()
        if text in commands.keys():
            commands[text]()
        else:
            console.error("Команда \"{}\" не найдена.".format(text))


def reload_bot():
    console.process("Перезагрузка бота...")
    bot.handle = False
    sleep(1)
    bot.init(VK, config)
    bot.handle = True
    console.success("Бот успешно перезагружен!")


def close():
    console.success("Завершение работы...")
    sys.exit(0)


commands = {
    'close': close, 'exit': close, 'quit': close,
    'reload': reload_bot
}
