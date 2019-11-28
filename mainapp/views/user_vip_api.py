import datetime

import db
from mainapp.models import *

from flask import Blueprint, request, jsonify


user_vip_blue = Blueprint("user_vip_blue", __name__)


@user_vip_blue.route("/user_vip/", methods=("POST",))
def user_vip():
    post_data = request.get_json()
    phone = post_data["phone"]
    vip_name = post_data["vip_name"]
    print(phone,vip_name)

    try:
        user = db.session.query(User).filter_by(phone_num=phone).first()
        print(user.id)
        vip_pro = db.session.query(VipActivity).filter_by(vip_name=vip_name).first()
        print(vip_pro.vip_name)
        valid_time = int(vip_pro.valid_time.split("天")[0])
        print(valid_time)
        if vip_pro.vip_count <= 0:
            return jsonify({
                "status": 1,
                "msg": "当前优惠券剩余量不足，领取失败!"
            })

        now_time = datetime.datetime.now() + datetime.timedelta(days=valid_time)
        uvp = UserVipPackage()
        uvp.user_id = user.id
        uvp.vip_name = vip_name
        uvp.expires_time = str(now_time)
        uvp.is_expires = 1
        db.session.add(uvp)
        vip_pro.vip_count -= 1
        db.session.commit()
        return jsonify({
            "status": 0,
            "msg": "领取成功！"
        })

    except:
        return jsonify({
            "status": 1,
            "msg": "领取用户或优惠券不存在！"
        })
