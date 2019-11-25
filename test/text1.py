import requests

def get_bank_info(bank_id):
    bank_info_url = "https://api.jisuapi.com/bankca" \
                    "rd/query?appkey=06d97dfdd1fd0bb5&bankcard=?"+bank_id
    resp = requests.get(bank_info_url)
    print(resp.text)



if __name__ == '__main__':
    get_bank_info("6231000330000719521")