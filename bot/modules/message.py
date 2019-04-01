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
        return {'message': '<br>'.join(self.__msg), 'attachments': ','.join(self.__attachments)}

    def enable_nickname(self):
        self.__nickname = True

    def nickname(self):
        return self.__nickname

    def reset(self):
        self.__msg = []
        self.__attachments = []
        self.__nickname = False
