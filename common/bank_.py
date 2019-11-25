import requests


def get_bank_info(bank_id):
    bank_info_url = "https://api.jisuapi.com/bankcard/query?appkey=dc8e79cf1880bb1d&bankcard=" + bank_id
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Host':'api.jisuapi.com',
        'Referer':'https://www.jisuapi.com/my/api',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
    }
    param_dict = {
        'appkey':'dc8e79cf1880bb1d',
        'bankcard': bank_id,
    }
    response = requests.get(bank_info_url,headers=headers,params=param_dict)
    info_obj = eval(response.text)['result']
    info_dict = {
        'id_card': info_obj['bankcard'],
        'bank_name': info_obj['bank'],
        'card_type': info_obj['type'],
        'logo_href': info_obj['logo'],
        # 'location': info_obj['province'] + '省' + info_obj['city'] + '市' #归属地 格式:山西省吕梁市
    }
    return info_dict


def bank_serializor(response):
    pass