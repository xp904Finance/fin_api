from db import session
from mainapp.models import UserTradeDetail


# 插入交易明细表
def insert_detail(user_id, behavior, trade_money):
    utd = UserTradeDetail()
    utd.user_id = user_id
    utd.behavior = behavior
    utd.trade_money = trade_money

    session.add(utd)
    session.commit()
