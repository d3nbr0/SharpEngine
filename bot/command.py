from engine.other import console
import importlib.util
import os
import time
import sys
import traceback
import bot.module


commands = []


def load_commands():
    global commands
    commands = []
    for root, dirs, files in os.walk('bot\\commands'):
        check_cmds = filter(lambda x: x.endswith('.py'), files)
        for item in check_cmds:
            spec = importlib.util.spec_from_file_location("", "{}\\{}".format(root, item))
            cmd = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cmd)
            if hasattr(cmd, 'cmd'):
                if 'disabled' not in cmd.cmd or not cmd.cmd['disabled']:
                    cmd.error = bot.module.catch
                    commands.append(cmd)
            else:
                console.error("Команда \"{}\\{}\" не была загружена".format(root, item))


def exec_command(message, rmsg):
    args = message['text'].lower().split(' ')
    for item in commands:
        if item.cmd['name'] == args[0]:
            user = bot.module.user.User(message['from_id'])
            try:
                item.cmd['processing']({'msg': message, 'args': args, 'other': {'retime': time.time()}}, user, rmsg)
            except bot.module.CommandException as cmd:
                rmsg.add_line(cmd.message)
            except Exception:
                ex_type, ex, tb = sys.exc_info()
                rmsg.reset()
                rmsg.add_line('❌ Возникла системная ошибка при обработке команды')
                console.error("Ошибка при выполнении команды \"{}\": ({}) {}\n{}".format(message['text'], ex_type, ex, traceback.format_tb(tb)))
            if rmsg.nickname():
                rmsg.add_start_line("{}, ".format(user.nickname))
            user.save()
            return True
    return False
