from flask import Blueprint, request, jsonify
import db
from mainapp.models import *
portrait_blue = Blueprint('/portrait_blue/', __name__)


@portrait_blue.route('/get_portrait/', methods=('POST', ))
def get_portrait():
    # 前端返回phone和new_portrait
    data = request.get_json()
    phone_num = data["phone_num"]
    new_portrait = data["new_portrait"]
    username = data['username'],
    address = data['address'],
    zip_code = data['zip_code'],
    # 手机号存在
    try:
        user = db.session.query(User).filter_by(phone_num=phone_num).first()
        ud = user.user_details[0]
        # 用户头像存在
        if ud:
            ud.portrait = new_portrait
            ud.username = username
            ud.address = address
            ud.zip_code = zip_code
        db.session.commit()
        return jsonify({
            'status': 1,
            'msg': '头像修改成功'
        })
    # 手机号不存在
    except Exception as e:
        return jsonify({
            'error': e,
            'msg': '该用户不存在'
        })













