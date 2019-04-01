class Plugin:
    def input(self, arg, currency='balance'):
        if arg == 'всё' or arg == 'все':
            arg = getattr(self, currency)
        else:
            arg = arg.replace('к', '000')
        return int(arg) if arg.isdigit() else None
