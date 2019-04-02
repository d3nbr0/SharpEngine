from engine.vk.api.index import API
from engine.vk.updates.longpoll import LongPoll
from threading import Thread
from time import sleep


class VK:
    def __init__(self, access_token, group_id):
        self.API = API({'access_token': access_token, 'group_id': group_id})
        self.update_check, self.listener, self.longpoll, self.longpoll_thread = None, None, None, None

    def handle_longpoll(self, execute):
        self.update_check = execute
        self.longpoll = LongPoll(self.API)
        self.longpoll_thread = Thread(target=self.longpoll.update)
        self.longpoll_thread.start()
        self.listener = Thread(target=self.__listen)
        self.listener.start()

    def __listen(self):
        while True:
            for item in self.longpoll.updates:
                self.update_check(item)
                self.longpoll.updates.remove(item)
            sleep(0.0005)
