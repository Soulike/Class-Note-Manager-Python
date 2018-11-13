from flask import Blueprint
from flask import request

from objects import Response
from functions import log, session
import database

Login = Blueprint('Login', __name__)


@Login.route('/login', methods = ['POST'])
def login():
    req = request.get_json()

    username = req['username']
    password = req['password']

    try:
        conn = database.conn
        cur = conn.cursor()

        cur.execute('SELECT {0},{1} FROM {2} WHERE {3}=%s'.format('id', 'password', 'accounts', 'username'),
                    (username,))
        result = cur.fetchone()
        cur.close()

        if result is None or len(result) == 0:
            res = Response(False, '用户不存在', {})
        elif password == result[1]:
            res = Response(True, '登录成功', {})
            session.setSession(result[0])
        else:
            res = Response(False, '密码错误', {})
    except Exception as e:
        res = Response(False, '服务器错误', {})
        log(e)

    return res.getJson()


@Login.route('/validSession', methods = ['GET'])
def validSession():
    userId = session.getSessionUserId()
    if userId is None:
        res = Response(False, '会话已失效', {})
    else:
        res = Response(True, '会话有效', {})
    return res.getJson()
