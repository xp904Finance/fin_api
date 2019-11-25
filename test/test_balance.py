import datetime
import time
from unittest import TestCase
import requests
import math

from db import session
from mainapp.Serializor import dumps
from mainapp.models import User

base_url = 'http://localhost:8080/bank/'


class TestAppUser(TestCase):
    def test_ba(self):
        url = base_url + "info/"
        data = {
            "bank_id": "6212261202011584349"
        }
        res = requests.post(url, json=data)
        print(res.json())