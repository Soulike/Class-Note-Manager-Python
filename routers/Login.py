from flask import Blueprint
from flask import request
from objects import Response
from database import getDbCur

Login = Blueprint('Login', __name__)


@Login.route('/login', methods = ['POST'])
def login():
    req = request.get_json()

    username = req['username']
    password = req['password']

    cur = getDbCur()
    print(cur)

    res = Response(False, '登录失败', {})

    return res.getJson()
