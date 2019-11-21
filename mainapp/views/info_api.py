import json

from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query

from db import session
from mainapp.models import Information, User, ReadLog

info_blue = Blueprint("info_blue", __name__)


@info_blue.route('/info/', methods=("GET",))
def get_info():
    """
    向前端发送实时资讯
    :return:
    """
    info: Information = session.query(Information).all()[0]
    title = info.information_name
    read_count = info.read_count
    img = info.image_url if info.image_url else ""
    release_date = info.release_time
    info_id = info.id
    if info:
        return jsonify({
            "status": 0,
            "msg": {
                "title": title,
                "num": read_count,
                "pic": img,
                "date": release_date,
                "info_id": info_id
            }
        })
    else:
        return jsonify({
            "status": 1,
            'msg': info if info else "没有数据"
        })


@info_blue.route("/user_read/", methods=("POST",))
def read_info():
    read_json_data = request.get_json()
    print(read_json_data)
    user_phone = read_json_data["user_phone"]
    info_id = read_json_data["info_id"]

    # 根据资讯id查资讯表
    info: Information = session.query(Information).filter_by(id=info_id).all()[0]
    title = info.information_name
    info_detail = info.detail_url
    abstract = info.abstract
    release_date = info.release_time

    read_log = ReadLog()

    # 根据用户id查用户表
    user = session.query(User).filter_by(phone_num=int(user_phone)).all()

    if user:  # 如果用户登录了，增加用户浏览记录
        read_log.user_id = user.user_id

        read_log.info_id = info.id
    else:  # 如果没登陆，增加游客浏览记录
        read_log.user_id = 0
        read_log.info_id = info.id
    session.add(read_log)

    info.read_count += 1  # 浏览量加1

    session.add(info)
    session.commit()
    # 向前端返回要查看的资讯内容

    return jsonify({
        "status": 0,
        "msg": {
            "title": title,  # 资讯标题
            "detail": info_detail,  # 资讯详情
            "abstract": abstract,  # 资讯摘要
            "date": release_date
        }
    })

