import random

from flask import Blueprint, jsonify
from mainapp.models import Information
import db

ico = Blueprint('ico', __name__)


@ico.route('/img/', methods=('GET',))
def get_ico():
    info = db.session.query(Information).all()
    print(info[random.randint(0,len(info))])
    indexNews = []
    for i in range(3):
        info_dict = {
            "img": "",
            "new1": info[random.randint(0,len(info))].information_name,
            "new2": info[random.randint(0,len(info))].information_name,
        }
        indexNews.append(info_dict)
    index1 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav1.jpg",
        "name": "我的账户",
        "nid": 0
    }
    index2 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav2.jpg",
        "name": "邀请朋友",
        "nid": 1
    }
    index3 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav3.jpg",
        "name": "一键绑卡",
        "nid": 2
    }
    index4 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav4.jpg",
        "name": "新手礼包",
        "nid": 3
    }
    index5 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav5.jpg",
        "name": "期限理财",
        "nid": 4
    }
    index6 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav6.jpg",
        "name": "银行精选",
        "nid": 5
    }
    index7 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav7.jpg",
        "name": "余额理财",
        "nid": 6
    }
    index8 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav8.jpg",
        "name": "记账本",
        "nid": 7
    }
    index9 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav9.jpg",
        "name": "计算器",
        "nid": 8
    }
    index10 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav10.jpg",
        "name": "手机缴费",
        "nid": 9
    }
    index11 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav11.jpg",
        "name": "专项活动",
        "nid": 10
    }
    index12 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav12.jpg",
        "name": "小夕客服",
        "nid": 11
    }
    data = [index1, index2, index3, index4, index5, index6, index7, index8, index9, index10, index11, index12]

    return jsonify(
        {
            "data": data,
            "indexNews": indexNews
        })
"""
{
    "data": data,
    "indexNews": indexNews
}
"""