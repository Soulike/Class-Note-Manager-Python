from flask import Blueprint, request

from modules import MDConverter
from objects import Response

NoteManagement = Blueprint('NoteManagement', __name__)


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
    # username = session['username']
    # if username is None:
    #    return Response(False, '登录状态失效', {}).getJson()

    req = request.get_json()
    markdown = req['markdown']
    if markdown is None:
        return Response(True, '转换成功', '').getJson()

    converter = MDConverter.MDConverter()

    result = converter.makeHtml(markdown)

    return Response(True, '转换成功', result).getJson()
