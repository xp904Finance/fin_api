from flask import Blueprint, request
from flask import jsonify
from sqlalchemy.orm import Query


info_blue = Blueprint("info_blue", __name__)


@info_blue.route('', methods=("GET",))
def get_info():
    """
    向前端发送实时资讯
    :return:
    """

