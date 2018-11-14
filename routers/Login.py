from flask import Blueprint
from flask import request

import database
from functions import log, session
from objects import Response

Login = Blueprint('Login', __name__)


@Login.route('/login', methods = ['POST'])
def login():
    try:
        req = request.get_json()
        username = req['username']
        password = req['password']

        conn = database.conn
        with conn.cursor() as cur:
            try:
                cur.execute('SELECT {0},{1} FROM {2} WHERE {3}=%s'.format('id', 'password', 'accounts', 'username'),
                            (username,))
            except Exception as e:
                log('在处理登录请求时，数据库查询出现错误，错误信息：')
                log(e)
                res = Response(False, '服务器错误', {})
            else:
                result = cur.fetchone()
                if result is None or len(result) == 0:
                    res = Response(False, '用户不存在', {})
                elif password == result[1]:
                    res = Response(True, '登录成功', {})
                    session.setSession(result[0])
                else:
                    res = Response(False, '密码错误', {})
    except Exception as e:
        log('在处理登录请求时未能捕获的错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})

    return res.getJson()


@Login.route('/validSession', methods = ['GET'])
def validSession():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '会话已失效', {})
        else:
            res = Response(True, '会话有效', {})
    except Exception as e:
        log('在处理会话验证请求时未能捕获的错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()
