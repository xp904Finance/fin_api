#!/usr/bin/python3
# coding: utf-8
from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query

from common import sms_
from mainapp.models import User
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
        phone_num, pwd = req_data['name'], req_data['pwd']
        if len(pwd.strip()) == 0:
            raise Exception('')
    except:
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

            # 将token存在redis缓存中

            return jsonify({
                'status': 0,
                'msg': '登录成功',
                'token': token,
                'data': {
                    'phone_num': login_user.phone_num,
                },
            })

        else:
            jsonify({
                'status': 3,
                'msg': '登录失败， 用户名或口令错误!',
            })
@user_blue.route('/send_code/', methods=('POST',))
def send_code():
    try:
        # 获取手机号
        # phone = request.args.get('phone')
        data = request.get_json()
        phone = data["phone"]
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


@user_blue.route('/regist/', methods=('POST', ))
def regist():
    # {"phone": "", "code": ""}
    data = request.get_json()
    status = data.get("status")
    if status == "注册":
        try:
            phone = data.get('phone')
            code = data.get('code')
            if sms_.validate_code(phone, code):
                user = User()
                user.phone_num = phone
                # user.password = encode4md5(phone[-6:])
                db.session.add(user)
                db.session.commit() # 提交事务
        except Exception as e:
            print(e)
            return jsonify({
                'status': 1,
                'msg': '注册失败'
            })
        return jsonify({
            'status': 0,
            'msg': '注册成功'
        })
    else:
        try:
            data = request.get_json()
            phone = data.get('phone')
            code = data.get('code')
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
        phone,pwd,qrpwd = data["phone"],data["pwd"],data["qrpwd"]
        if len(pwd) >= 6 and (pwd == qrpwd):
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

