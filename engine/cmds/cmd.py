import engine.other.console as console
import engine.other.hooks as hooks
import bot.bot as bot
import sys
from time import sleep

VK = None
config = None
commands = {}


def listen(this_vk, this_config):
    global VK, config, commands
    VK = this_vk
    config = this_config
    init()
    while True:
        text = input()
        if text in commands.keys():
            commands[text]()
        else:
            console.error("Команда \"{}\" не найдена.".format(text))


def init():
    def cmd_reload_bot():
        console.process("Перезагрузка бота...")
        hooks.handle = False
        while hooks.is_busy:
            sleep(0.1)
        bot.init(VK, config)
        hooks.handle = True
        console.success("Бот успешно перезагружен!")

    def cmd_close():
        console.success("Завершение работы...")
        sys.exit(0)

    register_command('reload', cmd_reload_bot)
    register_command(['close', 'exit', 'quit'], cmd_close)


def register_command(cmd_name, execute):
    global commands
    if isinstance(cmd_name, list):
        for item in cmd_name:
            commands[item] = execute
    else:
        commands[cmd_name] = execute

