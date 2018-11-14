from datetime import datetime

from flask import Blueprint, request

import database
from functions import session, note, log
from modules import MDConverter
from objects import Response

NoteManagement = Blueprint('NoteManagement', __name__)


@NoteManagement.route('/submitNote', methods = ['POST'])
def submitNote():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '登录状态失效', {})
        else:
            conn = database.conn
            with conn.cursor() as cur:
                try:
                    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('username', 'accounts', 'id'), (userId,))
                except Exception as e:
                    log('在处理笔记提交请求时，数据库查询发生错误，错误信息：')
                    log(e)
                    res = Response(False, '服务器错误', {})
                else:
                    result = cur.fetchone()

                    if result is None or len(result) == 0:
                        res = Response(False, '用户不存在', {})
                    else:
                        req = request.get_json()

                        fileName = req['fileName']
                        noteContent = req['noteContent']
                        noteId = req['noteId']
                        nowTime = datetime.now()

                        if fileName is None or noteContent is None or noteId is None:
                            res = Response(False, '提交格式非法', {})
                        elif noteId == -1:  # 是一个新的笔记
                            try:
                                # 向数据库插入笔记信息
                                cur.execute(
                                    'INSERT INTO {0} ({1},{2},{3},{4}) VALUES (%s, %s, %s, %s)'.format(
                                        'notes', 'name', 'submit_time', 'last_update_time', 'account_id'),
                                    (fileName, nowTime, nowTime, userId))
                                conn.commit()
                            except Exception as e:
                                conn.rollback()
                                log('在处理笔记提交请求时，数据库提交发生错误，错误信息：')
                                log(e)
                                res = Response(False, '提交失败，请检查是否与之前的笔记名重复', {})
                            else:
                                try:
                                    # 写入笔记文件
                                    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('id', 'notes', 'submit_time'),
                                                (nowTime,))
                                except Exception as e:
                                    log('在处理笔记提交请求时，数据库查询发生错误，错误信息：')
                                    log(e)
                                    res = Response(False, '服务器错误', {})
                                else:
                                    result = cur.fetchone()
                                    noteId = result[0]
                                    # 如果笔记文件写入失败了，就把数据库记录也删掉
                                    if not note.writeNoteFile(noteId, noteContent):
                                        res = Response(False, '服务器错误', {})
                                        try:
                                            cur.execute('DELETE FROM {0} WHERE {1}=%s'.format('notes', 'submit_time'),
                                                        (nowTime,))
                                            conn.commit()
                                        except Exception as e:
                                            log('在处理笔记提交请求时，数据库提交发生错误，错误信息：')
                                            log(e)
                                    else:
                                        res = Response(True, '提交成功', {})
                        else:  # 是修改以前的笔记
                            if not note.writeNoteFile(noteId, noteContent):
                                res = Response(False, '修改失败，请重试', {})
                            else:
                                try:
                                    cur.execute(
                                        'UPDATE {0} SET {1}=%s WHERE {2}=%s'.format('notes', 'last_update_time', 'id'),
                                        (nowTime, noteId))
                                    conn.commit()
                                except Exception as e:
                                    # 这一个数据库操作修改最后修改时间，不是特别要紧，没有必要把之前的所有操作回滚
                                    conn.rollback()
                                    log('在处理笔记提交请求时，数据库提交发生错误，错误信息：')
                                    log(e)
                                finally:
                                    res = Response(True, '修改成功', {})
    except Exception as e:
        log('在处理笔记提交请求时出现未捕获的错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()


@NoteManagement.route('/deleteNote', methods = ['POST'])
def deleteNote():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '登录状态失效', {})
        else:
            conn = database.conn
            with conn.cursor() as cur:
                try:
                    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('username', 'accounts', 'id'), (userId,))
                except Exception as e:
                    log('在处理删除笔记请求时出现数据库查询错误，错误信息：')
                    log(e)
                    res = Response(False, '服务器错误', {})
                else:
                    result = cur.fetchone()

                    if result is None or len(result) == 0:
                        res = Response(False, '用户不存在', {})
                    else:
                        req = request.get_json()

                        noteId = req.get('id')

                        if noteId is None or int(noteId) <= 0:
                            res = Response(False, '提交格式非法', {})
                        else:
                            try:
                                cur.execute('DELETE FROM {0} WHERE {1}=%s'.format('notes', 'id'), (noteId,))
                                conn.commit()
                            except Exception as e:
                                log('在处理删除笔记请求时出现数据库提交错误，错误信息：')
                                log(e)
                                res = Response(False, '服务器错误', {})
                            else:
                                if note.deleteNoteFile(noteId) is True:
                                    res = Response(True, '删除成功', {})
                                else:
                                    res = Response(True, '删除失败', {})
    except Exception as e:
        log('在处理删除笔记请求时出现未捕获错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()


@NoteManagement.route('/getNoteList', methods = ['GET'])
def getNoteList():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '登录状态失效', {})
        else:
            conn = database.conn
            with conn.cursor() as cur:
                try:
                    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('username', 'accounts', 'id'), (userId,))
                except Exception as e:
                    log('在处理获取笔记列表请求时出现数据库查询错误，错误信息：')
                    log(e)
                    res = Response(False, '服务器错误', {})
                else:
                    result = cur.fetchone()
                    if result is None or len(result) == 0:
                        res = Response(False, '用户不存在', {})
                    else:
                        try:
                            cur.execute('SELECT {0},{1},{2} FROM {3} WHERE {4}=%s'.format('id', 'name', 'last_update_time', 'notes','account_id'), （userId,))
                        except Exception as e:
                            log('在处理获取笔记列表请求时出现数据库查询错误，错误信息：')
                            log(e)
                            res = Response(False, '服务器错误', {})
                        else:
                            results = cur.fetchall()
                            data = []
                            for result in results:
                                data.append({
                                    'id': result[0],
                                    'name': result[1],
                                    'lastModified': str(result[2])
                                })
                            res = Response(True, '获取成功', data)
    except Exception as e:
        log('在处理获取笔记列表请求时出现未捕获错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()


@NoteManagement.route('/getNote', methods = ['GET'])
def getNote():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '登录状态失效', {})
        else:
            conn = database.conn
            with conn.cursor() as cur:
                try:
                    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('username', 'accounts', 'id'), (userId,))
                except Exception as e:
                    log('在处理获取笔记请求时出现数据库查询错误，错误信息：')
                    log(e)
                    res = Response(False, '服务器错误', {})
                else:
                    result = cur.fetchone()

                    if result is None or len(result) == 0:
                        res = Response(False, '用户不存在', {})
                    else:
                        req = request.args

                        noteId = req.get('id')

                        if noteId is None or int(noteId) <= 0:
                            res = Response(False, '提交格式非法', {})
                        else:
                            noteContent = note.readNoteFile(noteId)
                            if (noteContent is not None):
                                try:
                                    cur.execute(
                                        'SELECT {0},{1} FROM {2} WHERE {3}=%s'.format('name', 'last_update_time',
                                                                                      'notes',
                                                                                      'id'),
                                        noteId)
                                except Exception as e:
                                    log('在处理获取笔记请求时出现数据库查询错误，错误信息：')
                                    log(e)
                                    res = Response(False, '服务器错误', {})
                                else:
                                    result = cur.fetchone()
                                    title = result[0]
                                    last_modify_time = result[1]
                                    converter = MDConverter()
                                    res = Response(True, '获取成功',
                                                   {'title': title, 'lastModifiedDate': str(last_modify_time),
                                                    'content': converter.makeHtml(noteContent)})
                            else:
                                res = Response(False, '服务器错误', {})
    except Exception as e:
        log('在处理获取笔记请求时出现未捕获错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()


@NoteManagement.route('/getNoteRaw', methods = ['GET'])
def getNoteRaw():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '登录状态失效', {})
        else:
            conn = database.conn
            with conn.cursor() as cur:
                try:
                    cur.execute('SELECT {0} FROM {1} WHERE {2}=%s'.format('username', 'accounts', 'id'), (userId,))
                except Exception as e:
                    log('在处理获取笔记原文请求时出现数据库查询错误，错误信息：')
                    log(e)
                    res = Response(False, '服务器错误', {})
                else:
                    result = cur.fetchone()

                    if result is None or len(result) == 0:
                        res = Response(False, '用户不存在', {})
                    else:
                        req = request.args
                        noteId = req.get('id')
                        if noteId is None or int(noteId) <= 0:
                            res = Response(False, '提交格式非法', {})
                        else:
                            noteContent = note.readNoteFile(noteId)
                            if noteContent is not None:
                                try:
                                    cur.execute(
                                        'SELECT {0},{1} FROM {2} WHERE {3}=%s'.format('name', 'last_update_time',
                                                                                      'notes',
                                                                                      'id'),
                                        noteId)
                                except Exception as e:
                                    log('在处理获取笔记原文请求时出现数据库查询错误，错误信息：')
                                    log(e)
                                    res = Response(False, '服务器错误', {})
                                else:
                                    result = cur.fetchone()
                                    title = result[0]
                                    res = Response(True, '获取成功', {'title': title,
                                                                  'content': noteContent})
                            else:
                                res = Response(False, '服务器错误', {})
    except Exception as e:
        log('在处理获取笔记原文请求时出现未捕获错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()


@NoteManagement.route('/noteConvert', methods = ['POST'])
def noteConvert():
    try:
        userId = session.getSessionUserId()
        if userId is None:
            res = Response(False, '登录状态失效', {})
        else:
            req = request.get_json()
            markdown = req['markdown']
            if markdown is None:
                res = Response(True, '转换成功', '')
            else:
                converter = MDConverter()
                result = converter.makeHtml(markdown)
                res = Response(True, '转换成功', result)
    except Exception as e:
        log('在处理转换笔记请求时出现未捕获错误，错误信息：')
        log(e)
        res = Response(False, '服务器错误', {})
    return res.getJson()
