#!/usr/bin/python3
# coding: utf-8

from unittest import TestCase
import requests

base_url = 'http://localhost:6000/user/'

class TestAppUser(TestCase):
    # def test_login(self):
    #     url = base_url+"login/"
    #     data = {
    #         'name': '13259775913',
    #         'pwd': '123456.'
    #     }
    #
    #     resp = requests.post(url, json=data)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(resp.json().get('status'), 0)
    #
    #     print(resp.json())
    #
    #
    # def test_send_code(self):
    #     url = base_url+"send_code/"
    #     # resp = requests.get(url)
    #     data = {
    #         "phone":"13259775913",
    #         'flag': '注册',
    #     }
    #     resp = requests.post(url,json=data)
    #     print(resp)
    #
    # def test_regist(self):
    #     url = base_url+"regist/"
    #     data = {
    #         'flag':'注册',
    #         'phone': '13259775913',
    #         'code': '94874'
    #     }
    #
    #     resp = requests.post(url, json=data)
    #     print(resp.json())
    # def test_setpwd(self):
    #     url = base_url+"setpwd/"
    #     data = {
    #         'phone':'13259775913',
    #         'pwd':'xc1234567',
    #         'qrpwd':'xc1234567'
    #     }
    #     resp = requests.post(url,json=data)
    #     print(resp.json())

    def test(self):
        url = base_url+'jizhangben/'
        data = {
            'phone':'17802926563',
            'year':2019,
            'month':11
        }
        resp = requests.post(url,json=data)
        print(resp.json())