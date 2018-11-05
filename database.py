import psycopg2

dbCur = None


# 服务器启动时调用，连接数据库
def connectDatabase(address, port, dbname, username, password):
    global dbCur
    conn = psycopg2.connect(hostaddr = address, port = port, dbname = dbname, user = username,
                            password = password)
    dbCur = conn.cursor()


# 返回数据库连接指针
def getDbCur():
    return dbCur
