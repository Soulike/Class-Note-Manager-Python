import json


class Response:
    def __init__(self, isSuccess, msg, data):
        self.__isSuccess = isSuccess
        self.__msg = msg
        self.__data = data

    def getJson(self):
        ret = {
            'isSuccess': self.__isSuccess,
            'msg': self.__msg,
            'data': self.__data
        }
        return json.dumps(ret)
