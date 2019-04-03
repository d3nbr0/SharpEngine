def on_command(data, user, msg):
    msg.enable_nickname()
    msg.add_line("ваш баланс: {}".format(user.get_money()))


cmd = {
    'name': 'баланс',
    'processing': on_command
}
