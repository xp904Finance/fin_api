from unittest import TestCase
import requests


base_url = 'http://localhost:8080/portrait/'


class TestAppUser(TestCase):

    def test_read(self):
        print("*" * 50)
        url = base_url + 'get_portrait/'
        data = {
            "phone_num": '13259775913',
            'new_portrait': '111111111'
        }
        resp = requests.post(url, json=data)
        return resp