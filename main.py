from engine.vk.vk import VK
from engine.other.config import Config
from engine.other import console
from engine.other import hooks
from bot import bot
import engine.cmds.cmd as cmd

if __name__ == '__main__':

    PLATFORM_VERSION = "1.0.0 BETA"

    config = None
    vk = None
    workers_list = []


    def start():
        global config, vk
        console.log("Платформа для разработки чат-ботов ВКонтакте (v.: {}) © 2019".format(PLATFORM_VERSION))
        console.log("Чтение конфигурационного файла...")
        config = Config("config")
        console.log("Инициализация и подключение к ВКонтакте...")
        vk = VK(config.get_bot()['access_token'], config.get_bot()['group_id'])
        console.log("Подключение к боту...")
        assert hasattr(bot, 'init')
        bot.init(vk, config)
        vk.handle_longpoll(handle_update)
        console.log("Платформа успешно загружена!")
        cmd.listen()


    def handle_update(update):
        hooks.do(update['type'], update['object'])


    start()
