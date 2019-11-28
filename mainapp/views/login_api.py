#!/usr/bin/python3
# coding: utf-8
import time

from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query

from common import sms_
from common.cache import add_token, remove_token
from mainapp.models import User, VipActivity, UserDetail, UserAccount
import db

from common.crypo import encode4md5
from common.token import new_token

user_blue = Blueprint('user_blue', __name__)


@user_blue.route('/login/', methods=('POST',))
def login():
    # 获取请求上传的json数据
    # {'phone_num': '', 'pwd': ''}
    try:
        req_data = request.get_json()  # dict
        print(req_data)
        phone_num, pwd = req_data['name'], req_data['pwd']
        if len(pwd.strip()) == 0:
            raise Exception('')
    except Exception as e:
        print(e)
        return jsonify({
            'status': 1,
            'msg': '请求参数不完整，请提供name和pwd的json格式的参数'
        })

    query: Query = db.session.query(User).filter(User.phone_num == phone_num)
    if query.count() == 0:
        return jsonify({
            'status': 2,
            'msg': '查无此用户'
        })
    else:
        login_user: User = query.first()
        if encode4md5(pwd) == login_user.password:
            token = new_token()
            add_token(phone_num, token)
            # 将token存在redis缓存中
            details = login_user.user_accounts
            for detail in details:
                money_dict = {
                    "money":detail.user_balance,
                }
            return jsonify({
                'status': 0,
                'msg': '登录成功',
                'token': token,
                'money': money_dict,
                'data': {
                    'phone_num': login_user.phone_num,
                },
            })

        else:
            return jsonify({
                'status': 3,
                'msg': '登录失败， 用户名或口令错误!',
            })


@user_blue.route('/send_code/', methods=('POST',))
def send_code():
    try:
        # 获取手机号
        # phone = request.args.get('phone')
        data = request.get_json()
        # print(data['phone'])
        phone = data["phone"]
        flag = data["flag"]
        query: Query = db.session.query(User).filter(User.phone_num == phone)
        if flag == "注册":
            if query.count() != 0:
                return jsonify({
                    "status": 1,
                    "msg": "该用户已存在"
                })
            else:
                sms_.send_code(phone)
        if flag == "忘记密码":
            if query.count() == 0:
                return jsonify({
                    "status" : 1,
                    "msg" : "该用户不存在"
                })
            else:
                sms_.send_code(phone)
    except:
        return jsonify({
            'status': 1,
            'msg': '发送失败，请重试'
        })

    return jsonify({
        'status': 0,
        'msg': '发送成功'
    })


@user_blue.route('/regist/', methods=('POST',))
def regist():
    # {"phone": "", "code": ""}
    data = request.get_json()
    status = data["flag"]
    if status == "注册":
        try:
            phone = data['phone']
            query: Query = db.session.query(User).filter(User.phone_num == phone)
            if query.count() != 0:
                return jsonify({
                    "status":"1",
                    "msg":"该手机号已注册"
                })
            code = data['code']
            if sms_.validate_code(phone, code):
                user = User()
                user.phone_num = phone
                user.password = encode4md5(phone[-6:])
                print(user.password)
                try:
                    query = data['query']
                    user.invited_user_id = query
                except Exception as e:
                    print(e)
                db.session.add(user)
                db.session.commit() # 提交事务

        except Exception as e:
            print(e)
            return jsonify({
                'status': 1,
                'msg': '注册失败'
            })
        try:
            u = db.session.query(User).filter(User.phone_num == phone).first()
            u_id = u.id
            print(u_id)
            ud = UserDetail()
            ud.user_id = u_id
            ud.username = ''
            ud.portrait = ''
            ud.address = ''
            ud.risk_rank = ''
            ud.zip_code = ''
            ua = UserAccount()
            ua.user_id = u_id
            print(ua.user_id)
            ua.user_balance = 0
            ua.pay_password = ''
            ua.pay_count = 0
            db.session.add(ua)
            db.session.add(ud)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                'status': 4,
                'msg': '用户基本信息创建失败'
            })
        return jsonify({
            'status': 0,
            'msg': '注册成功'
        })
    if status == "忘记密码":
        try:
            data = request.get_json()
            phone = data['phone']
            query: Query = db.session.query(User).filter(User.phone_num == phone)
            if query.count() == 0:
                return jsonify({
                    'status': 1,
                    'msg': '该手机号未被注册'
                })
            code = data['code']
            if sms_.validate_code(phone, code):
                return jsonify({
                    'status': 0,
                    'msg': '重置密码请求成功'
                })
        except Exception as e:
            print(e)
            return jsonify({
                'status': 1,
                'msg': '重置密码请求失败'
            })

@user_blue.route('/setpwd/',methods=('POST',))
def set():
    try:
        data = request.get_json()
        phone,pwd = data["name"],data["pwd"]
        if len(pwd) >= 6:
            query: Query = db.session.query(User).filter(User.phone_num == phone)
            user: User = query.first()
            # user = User.query.get(phone)
            user.password = encode4md5(pwd)
            db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            'status': 2,
            'msg': '密码更改失败'
        })
    return jsonify({
        'status': 0,
        'msg': '密码修改成功'
    })
@user_blue.route('/exit/',methods=('POST',))
def exit():
    try:
        data = request.get_json()
        token = data["token"]
        remove_token(token)
    except Exception as e:
        print(e)
        return jsonify({
            'status': 1,
            'msg': '退出异常'
        })
    return jsonify({
        'status': 0,
        'msg': '退出成功'
    })
@user_blue.route('/resetpwd/',methods=('POST',))
def resetpwd():
    data = request.get_json()
    phone,oldpwd,newpwd = data['phone'],data['oldpwd'],data['newpwd']
    query: Query = db.session.query(User).filter(User.phone_num == phone)
    if query.count() == 0:
        return jsonify({
            'status': 1,
            'msg': '该手机号未被注册'
        })
    user: User = query.first()
    if encode4md5(oldpwd) == user.password:
        try:
            user.password = encode4md5(newpwd)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                'status': 2,
                'msg': '密码更改失败'
            })
        return jsonify({
            'status': 0,
            'msg': '密码修改成功'
        })
    else:
        return jsonify({
            'status': 2,
            'msg': '密码更改失败'
        })


@user_blue.route('cashbookinfo/',methods=('POST',))
def book():
    data = request.get_json()
    phone,year,month  = data["phone"],data["year"],data["month"]
    query: Query = db.session.query(User).filter(User.phone_num == phone)
    now_user: User = query.first()
    user_id = now_user.id
    details = db.session.execute("select * from user_trade_detail where user_id={} and trade_time like '{}-{}%'".format(user_id,year,month))
    details = details.fetchall()
    date_dict = {}
    for d in details:
        date_dict[d.trade_time.day] = []
    mon_money_jia = 0
    mon_money_pay = 0

    for d in details:
        if d.trade_money > 0:
            mon_money_jia += d.trade_money
        else:
            mon_money_pay += d.trade_money
        d_dict = {}
        print(d)
        d_dict["behavior"] = d.behavior
        d_dict["week"] = d.trade_time.strftime('%w')
        d_dict["trade_money"] = d.trade_money
        date_dict[d.trade_time.day].append(d_dict)
    dict2 = {}

    for i in date_dict:
        list1 = date_dict[i]
        day_money_jia = 0
        day_money_pay = 0
        list2 = []
        for j in list1:
            if j["trade_money"] > 0:
                day_money_jia += j["trade_money"]
            else:
                day_money_pay += j["trade_money"]
        list2.append(day_money_pay)
        list2.append(day_money_jia)
        dict2[i] = list2
    list3 = [date_dict,dict2]
    return jsonify({
        # "date_dict":date_dict,
        "data":list3,
        "mon_money_jia":mon_money_jia,
        "mon_money_pay":mon_money_pay,
        # "day_money":dict2
    })


@user_blue.route('/vip/',methods=('GET',))
def vip():
    vips = db.session.query(VipActivity).all()
    vip_list = []
    for vip in vips:
        vip_dict = {
            'vip_name':vip.vip_name,
            # 'vip_count', vip.vip_count,
            'worth':vip.worth,
            'valid_time':vip.valid_time,
        }
        vip_list.append(vip_dict)
    return jsonify({
        'status': 0,
        'msg': '发送成功',
        'data':vip_list
    })
@user_blue.route('/youhuiquan/',methods=('POST',))
def youhuiquan():
    try:
        data = request.get_json()
        phone = data['phone']
        u = db.session.query(User).filter(User.phone_num == phone).first()
        details = u.user_vip_packages
        list1 = []
        for detail in details:
            d_dict = {
                'vip_name',detail.vip_name,
                'expires_time',detail.expires_time,
                'is_expires ', detail.is_expires,
            }
            list1.append(d_dict)
    except Exception as e:
        print(e)
        return jsonify({
            'status': 1,
            'msg': '无法获取优惠券',
        })
    return jsonify({
        'status': 0,
        'msg': '获取优惠券成功',
        'data':list1,
    })
# dd = db.session.execute(f"-- select * from user_trade_detail where user_id={user_id} and trade_time like '2019-11%'")
