from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query

from common import rd1
from db import session
from mainapp.models import Information, User, ReadLog

info_blue = Blueprint("info_blue", __name__)


@info_blue.route('/info/', methods=("GET",))
def get_info():
    """
    向前端发送实时资讯
    :return:
    """
    data = {
        "head": {"title": "热门活动", "more": "查看更多"},
        "doc": ["债券", "银行", "期货"],
        "con": [
            [
                # 最新资讯
            ],
            [
                # 银行资讯
            ],
            [
                # 期货资讯
            ]
        ],
    }
    info_list = session.query(Information).all()
    if len(info_list) != 0:
        for info in info_list:
            title = info.information_name  # 标题
            read_count = info.read_count  # 阅读量
            img = info.image_url if info.image_url else ""  # 图片路径
            date = info.release_time  # 发布日期
            info_id = info.id  # 资讯id
            info_class = info.info_class

            info_data = {
                "title": title,
                "date": date,
                "num": read_count,
                "pic": img,
                "info_id": info_id
            }

            if info_class == "zhaiquan":  # 期货资讯
                data["con"][0].append(info_data)
            elif info_class == "banks":  # 最新资讯
                data["con"][1].append(info_data)
            elif info_class == "futures":  # 银行资讯
                data["con"][2].append(info_data)
        return jsonify(data)
    else:
        return jsonify({
            "status": 1,
            'msg': "当前数据库没有数据……"
        })


@info_blue.route("/user_read/", methods=("POST",))
def read_info():
    json_data = request.get_json()
    user_phone = json_data.get("user_phone")
    user_token = json_data.get("token")
    info_id = json_data.get("info_id")

    # 根据资讯id查资讯表
    info: Information = session.query(Information).filter_by(id=info_id).all()[0]
    title = info.information_name
    info_detail = info.detail
    abstract = info.abstract
    release_date = info.release_time

    # 实例化一个访问记录的对象
    read_log = ReadLog()

    # 根据用户id查用户表
    user = session.query(User).filter_by(phone_num=int(user_phone)).all()

    if rd1.get(user_phone) == user_token:  # 如果用户登录了，增加用户浏览记录:查看redis有无token
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
        "title": title,  # 资讯标题
        "date": release_date,  # 资讯发布时间
        "abstract": abstract,  # 摘要
        "detail": info_detail  # 详情
    })
