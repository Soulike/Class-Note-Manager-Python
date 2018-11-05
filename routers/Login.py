from flask import Blueprint
from flask import request
from flask import session

from database import getDbCur
from objects import Response

Login = Blueprint('Login', __name__)


@Login.route('/login', methods = ['POST'])
def login():
    req = request.get_json()

    username = req['username']
    password = req['password']

    cur = getDbCur()

    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('password', 'accounts', 'username'), (username,))
    result = cur.fetchone()

    if len(result) == 0:
        res = Response(False, '用户不存在', {})
    elif password == result[0]:
        res = Response(True, '登录成功', {})
        session['username'] = username
    else:
        res = Response(False, '密码错误', {})

    return res.getJson()
