from flask import Blueprint, request, jsonify

import db
from mainapp.models import User, RiskLevel,UserDetail

risk_level = Blueprint('risk_assess',__name__)

@risk_level.route('/naire/',methods=('POST',))
def risk_level_assess():
    data = request.get_json()
    print(type(data))
    user_phone = data['user_phone']
    print(user_phone)

    print(type(user_phone))
    print("*"*10)
    user_id = db.session.query(User).filter_by(phone_num=user_phone).first().id

    print(user_id)
    print("*" * 10)
    user_options = data['options']
    print(user_options)
    score = 0
    for user_option in user_options:
        if user_option == 'A':
            score += 5
        elif user_option == 'B':
            score += 10
        elif user_option == 'C':
            score += 15
        else:
            score += 20
    print(score)
    if score >= 90:
        risk_grande = '谨慎型'
    elif score >= 80:
        risk_grande = '稳健型'
    elif score >= 70:
        risk_grande = '平衡型'
    elif score >= 60:
        risk_grande = '进取型'
    else:
        risk_grande = '激进型'
    print(risk_grande)
    user = db.session.query(UserDetail).filter_by(user_id=user_id).first()
    user.risk_rank = risk_grande
    risk_count = db.session.query(RiskLevel).filter_by(f_level=risk_grande).first()
    risk_count.user_count += 1
    try:
        db.session.commit()
        return jsonify({
            'status':1,
            'msg':'等级评估完成！',
            'score':score,
            'risk_grande':risk_grande
        })
    except Exception as e:
        return jsonify({
            'status':0,
            'error':e,
            'msg':'评估结果保存失败，请再次尝试～～～'
        })
