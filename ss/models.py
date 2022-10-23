import requests as requests


class Logins:

    def __init__(self, url):
        self.url = url

    # async def post(self, user_name, email, password):
    #     paras = {'user_name': user_name, 'email': email, 'password': password}
    #     requests.post(self.url, data=paras)

    def get(self):
        return requests.get(self.url + "/logins/arian")
