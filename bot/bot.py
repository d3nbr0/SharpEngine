from engine.other import console
from engine.other import hooks
from bot import command
import bot.module
import random


def init(this_vk, this_config):
    bot.module.VK = this_vk
    bot.module.config = this_config
    console.log("Подключение модулей...")
    bot.module.load_modules()
    console.log("Загрузка команд...")
    command.load_commands()
    console.log("Загружено {} команд".format(len(command.commands)))


def message_new(msg):
    rmsg = bot.module.message.New()
    if command.exec_command(msg, rmsg):
        params = rmsg.vk_object()
        params.update({'peer_id': msg['peer_id'], 'random_id': random.randint(1000000, 9999999)})
        bot.module.VK.API.call('messages.send', params)
        console.log('Сообщение: {} | От: {}{}'.format(
            msg['text'],
            msg['from_id'],
            ' | Чат: {}'.format(msg['peer_id'] - 2000000000) if msg['peer_id'] > 2000000000 else ''
        ))


hooks.add('message_new', message_new)
