import requests

API_VERSION = "5.92"
API_BASE_URL = "https://api.vk.com/method"


class API:
    """API for requests to server"""

    def __init__(self, params):
        self.options = params
        self.session = requests.Session()
        assert 'access_token' in self.options, 'Access token has been not passed'
        assert 'group_id' in self.options, 'Group id has been not passed'

    def call(self, method, params={}):
        """The usual request. Returns JSON dict"""
        return self.call_with_object(method, params).json()

    def call_stringify(self, method, params={}):
        """Returns string response"""
        return self.call_with_object(method, params).text

    def call_with_object(self, method, params={}):
        """Returns request object response"""
        params.update({'access_token': self.options['access_token'], 'group_id': self.options['group_id'], 'v': API_VERSION})
        return self.session.post("{}/{}".format(API_BASE_URL, method), params)
