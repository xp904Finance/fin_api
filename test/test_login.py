#!/usr/bin/python3
# coding: utf-8

from unittest import TestCase
import requests

base_url = 'http://localhost:8080/info/'


class TestAppUser(TestCase):
    # def test_info(self):
    #     url = base_url + "info/"
    #     resp = requests.get(url)
    #     print(resp)

    def test_read(self):
        print("*" * 50)
        url = base_url + 'user_read/'
        data = {
            "user_phone": 11111111111,
            'info_id': 530
        }
        resp = requests.post(url, json=data)
        print(resp)
        print("-" * 50)
