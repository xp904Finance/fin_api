from unittest import TestCase
import requests

from common import rd1, rd2


class TestAppUser(TestCase):
    def test_redis(self):

        print(rd2.keys())
