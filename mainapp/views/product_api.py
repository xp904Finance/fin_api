from flask import Blueprint, request, jsonify
from db import session
from mainapp.Serializor import dumps
from mainapp.models import ProductClas

product_info = Blueprint('Product_info',__name__)


@product_info.route('/all_products/', methods=('GET', ))
def show_all_products(): # 显示所有的产品信息
    new_product = session.query(ProductClas).filter(is_novice=True).first()
    new_obj = dumps(new_product)
    '''
    将提取出来的new_product对象进行序列化，去除无用的属性，成为一个对象字典
    '''
    all_products = session.query(ProductClas).filter(is_novice=False).all()
    all_obj = dumps(all_products)
    data = {
        'new_product': new_obj,
        'all_product': all_obj,
    }
    return jsonify(data)