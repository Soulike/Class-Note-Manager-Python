from datetime import datetime


def log(msg):
    print('{0} {1}'.format(datetime.now(), msg))
