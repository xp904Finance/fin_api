from common import rd1 as rd


def add_token(phone,token):
    # 登录成功后绑定token和user_id
    rd.set(phone,token)
    print(rd.get(phone))


def remove_token(phone):
    # 退出时删除token
    rd.delete(phone)


def valid_token(phone):
    if rd.get(phone):
        return True
    else:
        False
def get_user_id_for_token(token):
    # 获取token绑定的id
    pass