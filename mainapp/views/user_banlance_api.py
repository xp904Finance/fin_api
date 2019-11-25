import math
import time

from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query

from common import rd1
from db import session
from mainapp.models import Information, User, ReadLog, UserBalanceFinance, BalanceFinancing

balance_blue = Blueprint("balance_blue", __name__)


def _get_user_balance_paid_days(start_time):
    """
    :param start_time: 起始时间戳
    :return: 返回距离当前的天数，小于1天按0计算
    """
    now_time = time.time()
    days = math.floor((now_time - start_time) / (60 * 60 * 24))
    return days


@balance_blue.route("/balance/", methods=("GET",))
def user_balance_api():
    user_phone = request.args.get("user_phone")
    user = session.query(User).filter_by(phone_num=user_phone).all()  # 获取用户实例
    balance_rate = session.query(BalanceFinancing).filter(id=0).balance_rate  # 获取余额宝当前利率

    if user:  # 如果查到了
        user = user[0]  # 获取该用户
        # 先更改用户余额信息
        user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
        user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
        user_paid_date = user_balance_data[0].paid_date  # 获取用户买入余额宝的日期
        days = _get_user_balance_paid_days(user_paid_date)  # 返回得到用户已购买的天数
        user_balance = balance_rate * days  # 计算已赚到的钱

        all_money = user_balance_money + user_balance

        # 更新表中数据
        user.user_balance_finances[0].paid_money = all_money
        user.user_balance_finances[0].income += user_balance
        session.commit()  # 提交数据

        income = user.user_balance_finances[0].income  # 累积收入

        return jsonify({
            "balance_money": all_money,  # 余额宝里的金额
            "user_balance": income,  # 已经赚到的钱
            "balance_rate": balance_rate  # 利率
        })


# 转入转出api
@balance_blue.route("out_or_in/", methods=("GET",))
def balance_out_api():
    flag = request.args.get("flag")
    user_phone = request.args.get("user_phone")
    user = session.query(User).filter_by(phone_num=user_phone).all()[0]  # 获取用户
    user_bank_cards = user.user_ditails[0].bank_cards  # 获取用户对应银行信息表
    user_card_list = []
    if user_bank_cards:
        for user_bank_card in user_bank_cards:
            user_bank_dict = {
                "bank_name": user_bank_card.bank_name,  # 银行名
                "logo": user_bank_card.logo_href  # 银行logo
            }
            user_card_list.append(user_bank_dict)  # 用户下已绑定的银行卡信息列表

        if flag == "转入":  # 返回转入逻辑需要的数据
            return jsonify({
                """
                用户已绑定的银行卡，
                """
                "user_bank_cards": user_card_list
            })
        elif flag == "转出":  # 返回转出逻辑需要的数据

            return jsonify({
                """
                用户已绑定的银行卡，
                """
                "user_bank_cards": user_card_list
            })
        else:
            return jsonify({
                "status": 1,
                'msg': "没有此功能"
            })


# 确认api
@balance_blue.route("sure_out_or_in/", methods=("POST",))
def sure_out_api():
    """
    传入账户名和转入转出信息
    :return:
    """
    post_data = request.get_json()
    flag = post_data['flag']
    user_phone = post_data["user_phone"]
    user = session.query(User).filter_by(phone_num=user_phone).all()[0]  # 获取用户
    user_bank_cards = user.user_ditails[0].bank_cards  # 获取用户对应银行信息表
    if flag == "转入":
        return jsonify({
            """
            用户已绑定的银行卡，
            """
        })
    elif flag == "转出":
        return jsonify({
            """
            用户已绑定的银行卡，
            """
        })
    else:
        return jsonify({
            "status": 1,
            'msg': "没有此功能"
        })
