from db import session
from mainapp.models import *

from flask import Blueprint, request, jsonify


account_blue = Blueprint("account_blue", __name__)


@account_blue.route("/acc_money/", methods=("GET",))
def acc_money():
    phone = request.args.get("phone")
    try:
        user = session.query(User).filter_by(phone_num=phone).first()
        uc = session.query(UserAccount).filter_by(user_id=user.id).first()
        account_money = uc.user_balance
        return jsonify({
            "status": 0,
            "money": account_money
        })
    except:
        return jsonify({
            "status": 1,
            "msg": "查无此用户！"
        })


@account_blue.route("/handle_money/", methods=("POST",))
def handle_money():
    json_data = request.get_json()
    phone = json_data["phone"]
    money = int(json_data["money"])
    flag = json_data["flag"]
    try:
        user = session.query(User).filter_by(phone_num=phone).first()
        ua = session.query(UserAccount).filter_by(user_id=user.id).first()
        if flag == "充值":
            ua.user_balance += money
            session.commit()
            return jsonify({
                'status': 0,
                "msg": "充值成功！"
            })
        elif flag == "提现":
            if ua.user_balance >= money:
                ua.user_balance -= money
                session.commit()
                return jsonify({
                    'status': 0,
                    "msg": "提现成功！"
                })
            else:
                return jsonify({
                    "status": 2,
                    "msg": "账户余额不足，提现失败！"
                })
        else:
            return jsonify({
                "status": 1,
                "msg": "没有此功能！"
            })
    except:
        return jsonify({
            "status": 1,
            "msg": "查无此用户！"
        })
