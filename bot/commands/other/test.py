import bot.module as module
import time

# data =>
#     message - объект полученного сообщения (подробнее в документации ВКонтакте)
#     args - аргументы сообщения, разделённые по пробелам
#     other =>
#         retime - время получения сообщения
#
# user - объект пользователя, загруженного из базы данных в класс
#
# msg =>
#     add_line(text) - добавляет 1 строку
#     add_lines(lines) - добавляет список строк
#     add_this_line(text) - добавляет текст к последней строке (не создаёт новую)
#     add_start_line(text) - добавляет текст в начало самой первой строки
#     add_attachment(attachment) - добавляет вложение к сообщению (подробнее в документации ВКонтакте)
#     enable_nickname() - включает использование никнейма в данной команде
#     reset() - сбрасывает всё сообщение (удаляет все строки, вложения и выключает исп. никнейма)


def on_command(data, user, msg):
    msg.add_line('Пинг: {} сек.'.format(time.time() - data['other']['retime']))


cmd = {
    'name': 'тест',
    'processing': on_command
}
