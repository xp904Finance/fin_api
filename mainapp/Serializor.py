

def _clear_state(instance: dict):
    # 对模型类对象进行属性‘_sa_instance_state’属性的清除
    instance.pop('_sa_instance_state')
    return instance


def dumps(obj):
    if isinstance(obj, list):
        # 多个数据模型类对象的实例
        return [
            _clear_state(item.__dict__)
            for item in obj
        ]

    # 普通的模型类的实例对象
    return _clear_state(obj.__dict__)


def all_clear_state(instance:dict):
    """
    :param instance: 各个模型类查询出来的模型对象
    :return: 将下列的属性pop掉之后的对象返回
    """
    instance.pop('_sa_instance_state')
    instance.pop('bank_id')
    instance.pop('risk_level')
    instance.pop('paid_count')
    instance.pop('produce')
    return instance


def dumps_all(obj):
    if isinstance(obj, list):
        # 多个数据模型类对象的实例
        return [
            all_clear_state(item.__dict__)
            for item in obj
        ]

    # 普通的模型类的实例对象
    return all_clear_state(obj.__dict__)


def detail_clear_state(instance:dict):
    """
    :param instance: 各个模型类查询出来的模型对象
    :return: 将下列的属性pop掉之后的对象返回
    """
    instance.pop('_sa_instance_state')
    instance.pop('id_saling')
    instance.pop('bank_id')
    return instance


def dumps_detail(obj):
    if isinstance(obj, list):
        # 多个数据模型类对象的实例
        return [
            detail_clear_state(item.__dict__)
            for item in obj
        ]

    # 普通的模型类的实例对象
    return detail_clear_state(obj.__dict__)

# 序列化模型
# models ="模型类"
# obj ：模型或者模型的列表


'''
from  datetime import  datetime,date

from models.models import Base


def dumps(obj):
    if isinstance(obj, list):
        # 多个数据模型类对象的实例
        data = []
        for item in obj:
            data.append(covert_instance(item))
        # print(data)
        return data

    return covert_instance(obj)


def covert_instance(item):
    item_dict = item.__dict__
    if '_sa_instance_state' in item_dict.keys():
        item_dict.pop('_sa_instance_state')
    instance = {}
    for key, value in item_dict.items():
        if isinstance(value, Base):
            instance[key] = dumps(value)
        elif isinstance(value, datetime):
            instance[key] = '%s-%s-%s' % (value.year, value.month, value.day)
        else:
            instance[key] = value
    return instance
    
    # lazy='immediate'
'''


