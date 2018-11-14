from flask import session


# 从 Session 中获取 userId，如果不存在就返回 None
def getSessionUserId():
    if session.get('userId'):
        return session.get('userId')
    else:
        return None


# 给当前 Session 设置 userId
def setSession(userId):
    session['userId'] = userId
