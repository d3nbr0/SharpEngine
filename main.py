from engine.vk.vk import VK
from engine.other.config import Config
from engine.other import console
from time import sleep
import bot.bot as bot
import engine.other.worker as worker
import engine.cmds.cmd as cmd

if __name__ == '__main__':

    PLATFORM_VERSION = "1.1.0 BETA"

    config = None
    vk = None
    workers = []


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
        init_workers(int(config.get_bot()['workers_count']))
        vk.listen_longpoll(handle_update)
        console.log("Платформа успешно загружена!")
        cmd.listen(vk, config)


    def init_workers(count):
        for item in range(count):
            workers.append(worker.Worker())
        console.debug("Workers loaded: {}".format(count))


    def handle_update(update):
        find_worker = True
        while find_worker:
            for i, item in enumerate(workers):
                console.debug("Worker: {}".format(i))
                if not item.is_busy:
                    item.update = update
                    find_worker = False
                    break
            sleep(0.001)


    start()
