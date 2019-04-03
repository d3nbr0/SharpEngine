from engine.vk.api.index import API
from engine.vk.updates.longpoll import LongPoll
from threading import Thread


class VK:
    def __init__(self, access_token, group_id):
        self.API = API({'access_token': access_token, 'group_id': group_id})
        self.update_check, self.listener, self.longpoll, self.longpoll_thread = None, None, None, None

    def listen_longpoll(self, execute):
        self.longpoll = LongPoll(self.API, execute)
        self.longpoll_thread = Thread(target=self.longpoll.update)
        self.longpoll_thread.start()
