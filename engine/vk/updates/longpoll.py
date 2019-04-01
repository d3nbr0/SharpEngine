import requests


WAIT_RECONNECT = 25


class LongPoll:
    def __init__(self, API):
        self.API = API
        self.key, self.server, self.ts = None, None, None
        self.updates = []
        self.is_work = True

    def get_server(self):
        server_info = self.API.call("groups.getLongPollServer")
        self.key = server_info['response']['key']
        self.server = server_info['response']['server']
        self.ts = server_info['response']['ts']

    def update(self):
        while self.is_work:
            if self.ts is None:
                self.get_server()
            server_respond = requests.get('{}?act=a_check&key={}&ts={}&wait={}'.format(self.server, self.key, self.ts,
                                                                                       WAIT_RECONNECT)).json()
            if 'failed' in server_respond:
                self.handle_error(server_respond)
                continue
            self.ts = server_respond['ts']
            for item in server_respond['updates']:
                self.updates.append(item)

    def handle_error(self, error):
        if error['failed'] == 1:
            self.ts = error['ts']
        if error['failed'] == 2 or error['failed'] == 3:
            self.ts = None
