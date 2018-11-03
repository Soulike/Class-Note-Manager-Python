import psycopg2

dbCur = None


def connectDatabase(address, port, dbname, username, password):
    global dbCur
    conn = psycopg2.connect(hostaddr = address, port = port, dbname = dbname, user = username,
                            password = password)
    dbCur = conn.cursor()


def getDbCur():
    return dbCur
