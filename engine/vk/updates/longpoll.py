import requests


WAIT_RECONNECT = 25


class LongPoll:
    def __init__(self, API, update_method):
        self.API = API
        self.data = {'ts': None, 'server': None, 'key': None}
        self.handle = update_method
        self.is_work = True

    def get_server(self):
        server_info = self.API.call("groups.getLongPollServer")
        self.data['key'] = server_info['response']['key']
        self.data['server'] = server_info['response']['server']
        self.data['ts'] = server_info['response']['ts']

    def update(self):
        while self.is_work:
            if self.data['ts'] is None:
                self.get_server()
            server_respond = requests.get('{}?act=a_check&key={}&ts={}&wait={}'.format(self.data['server'],
                                                                                       self.data['key'],
                                                                                       self.data['ts'],
                                                                                       WAIT_RECONNECT)).json()
            if 'failed' in server_respond:
                self.handle_error(server_respond)
                continue
            self.data['ts'] = server_respond['ts']
            for item in server_respond['updates']:
                self.handle(item)

    def handle_error(self, error):
        if error['failed'] == 1:
            self.data['ts'] = error['ts']
        if error['failed'] == 2 or error['failed'] == 3:
            self.data['ts'] = None
