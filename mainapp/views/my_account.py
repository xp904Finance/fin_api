from db import session
from mainapp.models import *

from flask import Blueprint, request, jsonify

from mainapp.views.user_banlance_api import get_user_balance_paid_days

acc_blue = Blueprint("acc_blue", __name__)


@acc_blue.route("/myaccount/", methods=("GET",))
def my_account():
    balance_rate = session.query(BalanceFinancing).first().balance_rate  # 获取余额宝当前利率
    phone = request.args.get("user_phone")
    print(phone)
    try:
        user = session.query(User).filter_by(phone_num=phone).first()
        print("---->", user)
        user_id = user.id
        ua = session.query(UserAccount).filter_by(user_id=user_id).first()
        ud = session.query(UserDetail).filter_by(user_id=user_id).first()
        ub = session.query(UserBalanceFinance).filter_by(user_id=user_id).first()
        if ub:
            user_balance_money = ub.paid_money  # 获取用户余额宝总额
            user_paid_date = str(ub.paid_date)  # 获取用户买入余额宝的日期
            days = get_user_balance_paid_days(user_paid_date)  # 返回得到用户已购买的天数
            income = ub.income
        else:
            user_balance_money = 0  # 获取用户余额宝,没有为0
            days = 0
            income = 0
        user_balance = balance_rate * days  # 计算已赚到的钱
        balance_money = user_balance_money + user_balance  # 余额宝所有金额

        user_name = ud.username if ud.username else phone  # 获取用户姓名
        u_account_money = ua.user_balance + balance_money  # 总资产
        return jsonify({
            "user_name": user_name,
            "u_account_money": u_account_money,
            "user_money": ua.user_balance,
            "income": income,
            "user_portrait": ud.portrait
        })

    except Exception as e:
        print(e)
        return jsonify({
            "status": 1,
            "msg": "查询出错"
        })
