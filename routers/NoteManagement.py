from flask import Blueprint, request, session, g

from modules import MDConverter
from objects import Response


NoteManagement = Blueprint('NoteManagement', __name__)


@NoteManagement.route('/submitNote', method = ['POST'])
def submitNote():
    userId = session['id']
    if userId is None:
        res = Response(False, '登录状态失效', {}).getJson()
    else:
        cur = g.conn.cursor()
        cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('username', 'accounts', 'id'), (userId,))
        result = cur.fetchone()

        if result is None or len(result) == 0:
            res = Response(False, '用户不存在', {})
        else:
            req = request.get_json()

            noteContent = req['noteContent']
            noteId = req['noteId']

            if noteId == -1:  # 是一个新的笔记
                pass
            else:  # 是修改以前的笔记
                pass


@NoteManagement.route('/deleteNote', methods = ['POST'])
def deleteNote():
    pass


@NoteManagement.route('/getNoteList', methods = ['GET'])
def getNoteList():
    pass


@NoteManagement.route('/getNote', methods = ['GET'])
def getNote():
    pass


@NoteManagement.route('/noteConvert', methods = ['POST'])
def noteConvert():
    if session['id'] is None:
        res = Response(False, '登录状态失效', {}).getJson()
    else:
        req = request.get_json()
        markdown = req['markdown']
        if markdown is None:
            res = Response(True, '转换成功', '').getJson()
        else:
            converter = MDConverter.MDConverter()
            result = converter.makeHtml(markdown)
            res = Response(True, '转换成功', result).getJson()

    return res
