import datetime
import random
import time
from unittest import TestCase
import requests
import math

from db import session
from mainapp.Serializor import dumps
from mainapp.models import *

base_url = 'http://localhost:8080/phone_pay/'


class TestAppUser(TestCase):
    def test_ba(self):
        try:
            ubfs = session.query(UserBalanceFinance).all()
            for ubf in ubfs:
                print(ubf.paid_date)
        except Exception as e:
            print(e)