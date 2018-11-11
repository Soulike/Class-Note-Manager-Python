from flask import g
import psycopg2


# 服务器启动时调用，连接数据库
def connectDatabase(address, port, dbname, username, password):
    if not hasattr(g, 'conn'):
        conn = psycopg2.connect(hostaddr = address, port = port, dbname = dbname, user = username,
                                password = password)
        g.conn = conn


def closeDatabase():
    if hasattr(g, 'conn'):
        g.conn.close()
