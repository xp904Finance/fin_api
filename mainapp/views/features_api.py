from common.bank_ import get_bank_info
from flask import Blueprint, request, jsonify
import db
from mainapp.models import BandCard
import requests

features_tools = Blueprint('features_tool', __name__)


@features_tools.route('/info/', methods=('POST',))
def bank_info():
    bank = BandCard()
    bank_data = request.get_json()
    print(bank_data)
    try:
        bank_id = bank_data["bank_id"]
        print(bank_id)
        if bank_id:
            bank_dicts = get_bank_info(bank_id)
            print(bank_dicts)
            bank_name = bank_dicts['bank_name']
            bank_logo = bank_dicts["logo_href"]
            bank_type = bank_dicts["card_type"]
            bank.id_card = bank_id

            print(bank_name, bank_logo, bank_type)
            bank.user_id = 14
            bank.bank_name = bank_name
            bank.card_type = bank_type
            bank.logo_href = bank_logo.replace("\\", "")
            print(bank,type(bank))
            try:
                print("----------------")
                db.session.add(bank)
                db.session.commit()
                print("++++++++++++++++++++++++++++++++++++++++")
                return jsonify({
                    'status': 1,
                    'msg': '绑定银行卡成功！',

                })
            except Exception as e:
                return jsonify({
                    "error": e
                })
        else:
            return jsonify({
                'status': 2,
                'msg': "输入的银行卡号不能为空！"
            })
    except:
        return jsonify({
            'status': 3,
            'msg': '绑定银行卡失败！'
        })


@features_tools.route('/show/', methods=('GET',))
def my_bank_info():
    bank = BandCard()
    user_id = request.args.get("user_id")
    if user_id:
        bank_details = db.session.query(BandCard).filter_by(user_id=user_id).all()
        user_bank = []
        if bank_details:
            for bank_detail in bank_details:
                data = {
                    'bank_name': bank_detail.bank_name,
                    'bank_id': bank_detail.id_card,
                    'bank_type': bank_detail.card_type,
                    'bank_logo': bank_detail.logo_href
                }
                user_bank.append(data)
            return jsonify({
                'status': 1,
                'data': user_bank
            })
        else:
            return jsonify({
                'status': 0,
                'msg': '该用户还没有绑定银行卡，请先去绑定银行卡！'
            })

    return jsonify({
        'status': 2,
        'msg': '请先去登陆后在进行查询！'
    })
