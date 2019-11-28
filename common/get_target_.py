import datetime
from db import session
from mainapp.Serializor import dumps
from mainapp.models import User, UserAccount, ProductClas, UserProduct


def get_user_obj(phone_num):
    """
    :param phone_num: 用户手机号
    :return: 通过手机号查询到相对应的用户账户表
    """
    user_obj = session.query(User).filter(User.phone_num == phone_num).first()
    user_dict = dumps(user_obj)
    user_id = user_dict['id']
    user_acount_obj = session.query(UserAccount).filter(UserAccount.user_id == user_id).first()
    print(user_acount_obj)
    return user_acount_obj


def get_pro_obj(pro_name):
    """

    :param pro_name: 产品名称
    :return: 返回一个产品模型对象
    """
    pro_obj = session.query(ProductClas).filter(ProductClas.product_name == pro_name).first()
    return pro_obj


def get_deadline(trade):
    """

    :param trade: 交易天数，即产品的天数
    :return: 返回值为datetime类型的时间对象，值为当前时间加上交易天数之后的时间
    """
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=trade)
    deadline_dt = now + delta
    deadline = deadline_dt.strptime(deadline_dt.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    # n_days.strftime('%Y-%m-%d %H:%M:%S') 转化为字符串格式
    return deadline


def create_userpro(user_id, product_name, purchased, dead_line):
    """
    :param user_id:用户id
    :param product_name: 产品名
    :param purchased: 支付金额
    :param dead_line: 到期时间
    :return: 提交user_product模型对象
    """
    user = UserProduct()
    user.user_id = user_id
    user.product_name = product_name
    user.Purchased = purchased
    user.dead_line = dead_line
    session.add(user)
    session.commit()


def update_info(user_account_obj, pro_obj, pay_num):
    user_account_obj.user_balance -= pay_num
    user_account_obj.pay_count += 1
    pro_obj.pro_balance -= pay_num
    pro_obj.paid_count += 1
    if pro_obj.pro_balance == 0:
        pro_obj.id_saling = 0
    session.commit()


