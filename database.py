import psycopg2

conn = None


# 服务器启动时调用，连接数据库
def connectDatabase(address, port, dbname, username, password):
    global conn
    conn = psycopg2.connect(hostaddr = address, port = port, dbname = dbname, user = username,
                            password = password)


# 断开数据库连接，在程序退出时调用
def disconnectDatabase():
    global conn
    conn.close()
