import os

from main import NOTE_FILE_POSITION
from .log import log


# 读取笔记文件并返回内容
def readNoteFile(noteId):
    ret = None
    try:
        with open('{0}/{1}.md'.format(NOTE_FILE_POSITION, noteId), 'r') as file:
            ret = file.read()
    except IOError as e:
        log(e)
        ret = None
    finally:
        return ret


# 删除笔记文件
def deleteNoteFile(noteId):
    ret = False
    filePath = '{0}/{1}.md'.format(NOTE_FILE_POSITION, noteId)
    try:
        if os.path.exists(filePath):
            os.remove(filePath)
            ret = True
    except OSError as e:
        log(e)
        ret = False
    return ret


# 创建及写入笔记文件
def writeNoteFile(noteId, content):
    tempFilePath = '{0}/{1}_temp.md'.format(NOTE_FILE_POSITION, noteId)
    filePath = '{0}/{1}.md'.format(NOTE_FILE_POSITION, noteId)
    try:
        with open(tempFilePath, 'w') as tempFile:
            tempFile.write(content)
    except IOError as e:
        os.remove(tempFilePath)
        log(e)
        ret = False
    else:
        try:
            os.rename(tempFilePath, filePath)
        except IOError as e:
            os.remove(tempFilePath)
            log(e)
            ret = False
        else:
            ret = True
    return ret
