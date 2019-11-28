from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from common.trade_log import insert_detail
from db import session
from mainapp.Serializor import *
from mainapp.models import ProductClas
from common.get_target_ import get_user_obj, get_pro_obj, create_userpro, get_deadline, update_info

product_info = Blueprint('Product_info', __name__)


@product_info.route('/all/', methods=('GET', ))  # 产品页面所有产品路由
def show_all_products():  # 显示所有的产品信息
    all_list = []
    new_product = session.query(ProductClas).filter_by(is_novice=1).first()
    new_obj = dumps_all(new_product)
    all_list.append(new_obj)
    '''
    将提取出来的new_product对象进行序列化，去除无用的属性，成为一个对象字典
    '''
    all_products = session.query(ProductClas).filter(and_(ProductClas.is_novice == 0, ProductClas.product_name.like('钱多多%'))).all()
    all_obj = dumps_all(all_products)
    all_list.extend(all_obj)
    data = {
        'all_product': all_list
    }
    return jsonify(data)


@product_info.route('/series1/', methods=('GET', ))
def show_series1_products():  # 显示1~6个月的产品
    series1_obj = session.query(ProductClas).filter(and_(ProductClas.trade <= 31, ProductClas.is_novice == 0, ProductClas.product_name.like('钱多多%'))).all()
    series1_list = dumps_all(series1_obj)
    data = {
        'series1_product': series1_list,
    }
    return jsonify(data)


@product_info.route('/series2/', methods=('GET', ))
def show_series2_products():  # 显示1~6个月的产品
    series2_obj = session.query(ProductClas).filter(and_(ProductClas.trade > 30, ProductClas.trade <= 180, ProductClas.product_name.like('钱多多%'))).all()
    series2_list = dumps_all(series2_obj)
    data = {
        'series2_product': series2_list,
    }
    return jsonify(data)


@product_info.route('/series3/', methods=('GET', ))
def show_series3_products():  # 显示6个月以上的产品
    series3_obj = session.query(ProductClas).filter(ProductClas.trade > 180, ProductClas.product_name.like('钱多多%')).all()
    series3_list = dumps_all(series3_obj)
    data = {
        'series3_product': series3_list,
    }
    return jsonify(data)


@product_info.route('/detail/', methods=('GET',))
def show_products_detail():  # 显示产品的详细信息
    # phone_num = request.args.get('phone_num')
    # if not phone_num:
    #     return jsonify({
    #         'status': 1,
    #         'msg': '您还未登录，请登录后再进行操作!'
    #     })
    pro_name = request.args.get('product_name')
    product_obj = get_pro_obj(pro_name)
    pro_detail = dumps_detail(product_obj)
    data = {
        'product_detail': pro_detail,
    }
    return jsonify(data)


@product_info.route('/novice_list/', methods=('GET',))
def get_novice_list():
    # phone_num = request.args.get('phone_num')
    # if not phone_num:
    #     return jsonify({
    #         'status': 1,
    #         'msg': '您还未登录，请登录后再进行操作!'
    #     })
    novice_list = session.query(ProductClas).filter(ProductClas.is_novice == 1).all()
    novice_obj_list = dumps_all(novice_list)
    data = {
        'status': 0,
        'product_list': novice_obj_list,
    }
    return jsonify(data)


@product_info.route('/pay/', methods=('POST',))
def deal_pay():  # 处理购买请求
    json_data = request.get_json()
    print(json_data)
    try:
        phone_num = json_data['phone_num']
    except Exception as e:
        print(e)
        return jsonify({
            'status': 1,
            'msg': '您还未登录，请登录后再进行操作!'
        })
    pro_name = json_data['product_name']
    pay_num = int(json_data['pay_num'])
    if pay_num < 100:
        return jsonify({
                'status': 5,
                'msg': '抱歉，此产品起购金额为100，请重新输入购买金额！'
            })
    user_account_obj = get_user_obj(phone_num)
    pro_obj = get_pro_obj(pro_name)
    print(user_account_obj.user_balance, type(user_account_obj.user_balance))
    if pro_obj.is_novice:  # 判断是否是新手产品
        if user_account_obj.pay_count > 0:
            return jsonify({
                'status': 4,
                'msg': '抱歉，此产品仅限新手用户购买！'
            })
        elif user_account_obj.user_balance < pay_num:
            return jsonify({
                'status': 2,
                'msg': '购买失败,账户余额不足，请充值!'
            })
        elif pro_obj.pro_balance < pay_num:
            return jsonify({
                'status': 3,
                'msg': '购买失败,产品剩余量不足，请重新输入购买数量!'
            })
        update_info(user_account_obj, pro_obj, pay_num)
        user_id = user_account_obj.user_id
        behavior = '购买产品'
        deadline = get_deadline(trade=pro_obj.trade)
        create_userpro(user_id, pro_name, pay_num, deadline)
        insert_detail(user_id, behavior, -pay_num)
        session.commit()
        return jsonify({
            'status': 0,
            'msg': '购买成功!'
        })
    else:
        if user_account_obj.user_balance < pay_num:
            return jsonify({
                'status': 2,
                'msg': '购买失败,账户余额不足，请充值!'
            })
        elif pro_obj.pro_balance < pay_num:
            return jsonify({
                'status': 3,
                'msg': '购买失败,产品剩余量不足，请重新输入购买数量!'
            })
        update_info(user_account_obj, pro_obj, pay_num)
        user_id = user_account_obj.user_id
        behavior = '购买产品'
        deadline = get_deadline(trade=pro_obj.trade)
        create_userpro(user_id, pro_name, pay_num, deadline)
        insert_detail(user_id, behavior, -pay_num)
        return jsonify({
            'status': 0,
            'msg': '购买成功!'
        })


@product_info.route('/time_list/', methods=('GET', ))  # 产品页面所有产品路由
def show_time_products():  # 显示所有的产品信息
    # phone_num = request.args.get('phone_num')
    # if not phone_num:
    #     return jsonify({
    #         'status': 1,
    #         'msg': '您还未登录，请登录后再进行操作!'
    #     })
    all_products = session.query(ProductClas).filter(ProductClas.product_name.like('理个财%')).all()
    all_obj = dumps_all(all_products)
    return jsonify({
        'status': 0,
        'all_product': all_obj,
    })
