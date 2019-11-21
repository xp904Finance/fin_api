from flask import Blueprint, request, jsonify

myblue = Blueprint("myblue",__name__)

@myblue.route("/is/",methods=('POST','GET'))
def show_regist():
    try:
        re_data = request.get_json()
        num, status, yzpwd = re_data["phone_num"],re_data["status"],re_data["yzpwd"]
        if status == "注册":

        else:
            return jsonify