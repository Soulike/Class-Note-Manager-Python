from flask import session


def getSessionUserId():
    if session.get('userId'):
        return session.get('userId')
    else:
        return None


def setSession(userId):
    session['userId'] = userId
