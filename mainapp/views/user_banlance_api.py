import math
import time

from flask import Blueprint, request
from flask import jsonify

from common.trade_log import insert_detail
from db import session
from mainapp.models import User, UserBalanceFinance, BalanceFinancing

balance_blue = Blueprint("balance_blue", __name__)


def get_user_balance_paid_days(start_time):
    """
    :param start_time: 起始时间戳
    :return: 返回距离当前的天数，小于1天按0计算
    """
    now_time = time.time()
    days = math.floor((now_time - time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) / (60 * 60 * 24))
    return days


@balance_blue.route("/balance/", methods=("GET",))
def user_balance_api():
    """
    进入余额宝界面，获取用户手机号
    :return: 如果查到了，返回用户信息，没查到返回错误信息
    """
    user_phone = request.args.get("user")
    print(user_phone)
    user = session.query(User).filter_by(phone_num=user_phone).all()  # 获取用户实例
    balance_rate = session.query(BalanceFinancing).first().balance_rate  # 获取余额宝当前利率

    if user:  # 如果查到了
        user = user[0]  # 获取该用户
        # 先更改用户余额信息
        if user.user_balance_finances:
            user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
            user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
            user_paid_date = user_balance_data[0].paid_date  # 获取用户买入余额宝的日期
            days = get_user_balance_paid_days(str(user_paid_date))  # 返回得到用户已购买的天数
            user_balance = balance_rate * days  # 计算已赚到的钱

            all_money = user_balance_money + user_balance  # 余额宝所有金额

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
        else:
            return jsonify({
                "balance_money": 0,  # 余额宝里的金额
                "user_balance": 0,  # 已经赚到的钱
                "balance_rate": balance_rate  # 利率
            })
    else:
        return jsonify({
            "status": 1,
            "msg": "查无此用户"
        })


# 转入转出api
@balance_blue.route("/out_or_in/", methods=("GET",))
def balance_out_api():
    """
    接收手机号，查询当前手机号下的银行卡信息
    :return: 银行卡信息列表，没有返回0， 转出需要余额宝钱；转入 账户余额，银行卡信息列表，没有返回空数组
    """
    flag = request.args.get("flag")
    user_phone = request.args.get("user")
    user = session.query(User).filter_by(phone_num=user_phone).first()  # 获取用户
    user_bank_cards = user.band_cards  # 获取用户对应银行信息表
    balance_rate = session.query(BalanceFinancing).first().balance_rate  # 获取余额宝当前利率
    user_card_list = []
    if user_bank_cards:  # 获取银行卡信息列表
        for user_bank_card in user_bank_cards:
            user_bank_dict = {
                "bank_name": user_bank_card.bank_name + "(" + user_bank_card.id_card[-4:] + ")",  # 银行名
                "logo": user_bank_card.logo_href  # 银行logo
            }
            user_card_list.append(user_bank_dict)  # 用户下已绑定的银行卡信息列表
    else:
        user_card_list = False

    if flag == "转入":  # 返回转入逻辑需要的数据
        user_account_balance = user.user_accounts[0].user_balance if user.user_accounts[0].user_balance else 0
        user_card_list = user_card_list if user_card_list else []
        return jsonify({
            "user_account_balance": user_account_balance,  # 用户账户余额
            "user_bank_cards": user_card_list  # 用户银行卡列表
        })
    elif flag == "转出":  # 返回转出逻辑需要的数据
        user_card_list = user_card_list if user_card_list else 0
        try:
            user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
            user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
            user_paid_date = user_balance_data[0].paid_date.strftime('%Y-%m-%d %H:%M:%S')  # 获取用户买入余额宝的日期
            days = get_user_balance_paid_days(user_paid_date)  # 返回得到用户已购买的天数
            user_balance = balance_rate * days  # 计算已赚到的钱

            all_money = user_balance_money + user_balance  # 余额宝所有金额
            return jsonify({
                "balance_money": all_money,
                "user_bank_cards": user_card_list
            })
        except Exception as e:
            return jsonify({
                "balance_money": 0,
                "user_bank_cards": user_card_list
            })
    else:
        return jsonify({
            "status": 1,
            'msg': "没有此功能"
        })


# 确认api
@balance_blue.route("/sure_out_or_in/", methods=("POST",))
def sure_out_api():
    """
    user,flag,card_id,money,
    :return:
    """
    post_data = request.get_json()
    flag = post_data['flag']
    user_phone = post_data["user"]
    money = int(post_data["money"])
    print(money)
    user = session.query(User).filter_by(phone_num=user_phone).all()[0]  # 获取用户
    user_bank_cards = user.band_cards  # 获取用户对应银行信息表
    if flag == "转入":
        card_id = post_data["card_id"]
        if "余额" in card_id:
            card_id = post_data["card_id"]
            user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
            user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
            user.user_accounts[0].user_balance -= money
            user_balance_data[0].paid_money += money
            session.commit()
            insert_detail(user.id, "余额宝充值", money)
            return jsonify({
                "status": 0,
                "mdg": "转入成功！"
            })
        elif "银行" in card_id:
            user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
            user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
            if user.user_accounts[0].user_balance >= money:
                if user_balance_money:
                    user_balance_data[0].paid_money += money
                else:
                    ubf = UserBalanceFinance()
                    ubf.user_id = user.id
                    ubf.paid_money = money
                    session.add(ubf)
                user.user_accounts[0].user_balance -= money
                session.commit()
                insert_detail(user.id, "余额宝充值", money)
                return jsonify({
                    "status": 0,
                    "mdg": "转入成功！"
                })
            else:
                return jsonify({
                    "status": 1,
                    "mdg": "账户余额不足，转入失败！"

                })
        else:
            return jsonify({
                "status": 3,
                "msg": "别胡来"
            })
    elif flag == "转出":
        try:
            card_id = post_data["card_id"]
            print(card_id)
            user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
            user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
            user_balance_data[0].paid_money -= money
            session.commit()
            insert_detail(user.id, "余额宝提现", -money)
            return jsonify({
                "status": 333,
                "mdg": "转出成功！"
            })
        except:
            user_balance_data = user.user_balance_finances  # 根据表关系查询该用户下的用户余额宝表
            user_balance_money = user_balance_data[0].paid_money if user_balance_data else 0  # 获取用户余额宝总额
            user_balance_data[0].paid_money -= money
            user.user_accounts[0].user_balance += money
            session.commit()
            insert_detail(user.id, "余额宝提现", money)
            return jsonify({

                "status": 0,
                "mdg": "转出成功！"
            })

    else:
        return jsonify({
            "status": 1,
            'msg': "没有此功能"
        })
