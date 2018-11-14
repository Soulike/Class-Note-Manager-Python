from datetime import datetime


# 打日志，多用于输出错误信息
def log(msg):
    print('{0} {1}'.format(datetime.now(), msg))
