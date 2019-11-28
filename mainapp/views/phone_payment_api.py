import math
import time

from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query

from common import rd1
from common.trade_log import insert_detail
from db import session
from mainapp.models import Information, User, ReadLog, UserBalanceFinance, BalanceFinancing

phone_payment_blue = Blueprint("payment_blue", __name__)


@phone_payment_blue.route("/phone/", methods=("GET",))
def phone_payment():
    user_phone = request.args.get("phone")
    print(user_phone)
    user = session.query(User).filter_by(phone_num=user_phone).first()

    user_recharge = user.recharge_logs
    if user_recharge:  # 如果充过返回上次充值的手机号
        return jsonify({
            "phone": user_recharge[0].recharge_phone_num
        })

    # 如果没充过返回自己的手机号
    print(11111)
    return jsonify({
        "phone": user_phone
    })


@phone_payment_blue.route("/phone_pay/", methods=("POST",))
def phone_payment_api():
    post_data = request.get_json()
    user_phone = post_data["phone"]
    pay_phone = post_data["pay_phone"]  # 要充值的手机号
    pay_money = post_data["pay_money"]  # 要充值的钱数
    way = post_data["way"]  # 通过什么充值
    try:
        user = session.query(User).filter_by(phone_num=user_phone).first()
        if "余额"in way:
            user_balance = user.user_accounts[0].user_balance
            if user_balance >= pay_money:
                # 用户余额大于等于要充值的钱数，执行充值功能
                user.user_accounts[0].user_balance -= pay_money  # 修改用户余额
                insert_detail(user.id, "手机充值", -pay_money)  # 添加充值记录
                session.commit()  # 提交数据库
                return jsonify({
                    "status": 0,
                    "msg": f"{pay_phone}充值成功^-^"
                })
            else:
                return jsonify({
                    "status": 1,
                    "msg": "充值失败！用户余额不足！"
                })
        elif "银行" in way:
            return jsonify({
                "status": 0,
                "msg": "充值失败！用户余额不足！"
            })
        else:
            return jsonify({
                "status": 3,
                "msg": "没有此功能！"
            })
    except:
        return jsonify({
            "status": 3,
            "msg": "查无此用户！"
        })


