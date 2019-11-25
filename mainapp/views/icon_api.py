
from flask import Blueprint, jsonify

ico = Blueprint('ico',__name__)


@ico.route('/img/',methods=('GET',))
def get_ico():
    index1 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav1.jpg",
        "name": "我的账户",
        "url": "",
        "nid":0
    }
    index2 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav2.jpg",
        "name": "邀请朋友",
        "url": "",
        "nid": 1
    }
    index3 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav3.jpg",
        "name": "一键绑卡",
        "url": "",
        "nid": 2
    }
    index4 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav4.jpg",
        "name": "新手礼包",
        "url": "",
        "nid": 3
    }
    index5 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav5.jpg",
        "name": "期限理财",
        "url": "",
        "nid": 4
    }
    index6 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav6.jpg",
        "name": "银行精选",
        "url": "",
        "nid": 5
    }
    index7 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav7.jpg",
        "name": "余额理财",
        "url": "",
        "nid": 6
    }
    index8 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav8.jpg",
        "name": "记账本",
        "url": "",
        "nid": 7
    }
    index9 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav9.jpg",
        "name": "计算器",
        "url": "",
        "nid": 8
    }
    index10 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav10.jpg",
        "name": "手机缴费",
        "url": "",
        "nid": 9
    }
    index11 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav11.jpg",
        "name": "专项活动",
        "url": "",
        "nid": 10
    }
    index12 = {
        "pic": "http://money.woftsun.com/res/img/inde-nav12.jpg",
        "name": "小夕客服",
        "url": "",
        "nid": 11
    }
    data = [index1,index2,index3,index4,index5,index6,index7,index8,index9,index10,index11,index12]

    return jsonify(data)