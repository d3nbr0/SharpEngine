import json


class New:
    def __init__(self):
        self.reset()

    def add_line(self, text):
        self.__msg.append(text)

    def add_this_line(self, text):
        self.__msg[-1] += text

    def add_start_line(self, text):
        self.__msg[0] = text + self.__msg[0]

    def add_lines(self, lines):
        self.__msg += lines

    def add_attachment(self, attachment):
        self.__attachments.append(attachment)

    def vk_object(self):
        return {
            'message': '<br>'.join(self.__msg),
            'attachments': ','.join(self.__attachments),
            'keyboard': json.dumps(self.__buttons, ensure_ascii=False).encode('utf8')
        }

    def add_button(self, button):
        if len(self.__buttons['buttons']) == 0 or len(self.__buttons['buttons'][-1]) + 1 > 4:
            self.add_button_line()
        self.__buttons['buttons'][-1].append(self.__button_object(button))

    def add_buttons(self, buttons):
        for item in buttons:
            self.add_button(item)

    def add_button_line(self):
        self.__buttons['buttons'].append([])

    def enable_nickname(self):
        self.__nickname = True

    def nickname(self):
        return self.__nickname

    def reset(self):
        self.__msg = []
        self.__attachments = []
        self.__nickname = False
        self.__buttons = {
            'one_time': False,
            'buttons': []
        }

    @staticmethod
    def __button_object(button):
        return {
            'action': {
                'type': 'text',
                'label': button if isinstance(button, str) else button['text']
            },
            'color': 'default' if isinstance(button, str) or 'color' not in button else button['color']
        }
