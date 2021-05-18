from flask import  g, current_app, Blueprint

import cx_Oracle

bp = Blueprint('db', __name__)

poolName = 'connectionPool' # Update references to g

def __getDatabaseConnection__():
    if poolName not in g:
        __createDatabaseConnectionPool__()
    return g.connectionPool.acquire()

def __createDatabaseConnectionPool__():
    if poolName not in g:
        username = current_app.config['DATABASE_USER']
        password = current_app.config['DATABASE_PASS']
        location = current_app.config['DATABASE_HOST']
        g.connectionPool = cx_Oracle.SessionPool(username, password,
        location, min=2, max=8, increment=1, encoding='UTF-8')

def __fetchQuery__(query, args, fetchstyle):
    dbConnection = __getDatabaseConnection__()
    cursor = dbConnection.cursor()
    result = cursor.execute(query, args)
    if fetchstyle == 'one':
        return result.fetchone()
    else:
        return result.fetchall()
    dbConnection.close()


def fetchOne(query, args):
    return __fetchQuery__(query, args, 'one')

def fetchAll(query, args):
    return __fetchQuery__(query, args, 'all')

def commit(query, args):
    dbConnection = __getDatabaseConnection__()
    cursor = dbConnection.cursor()
    result = cursor.execute(query, args)
    dbConnection.commit()
    dbConnection.close()
    return result


def runPlSqlFunction(functionName, returnType, args):
    dbConnection = __getDatabaseConnection__()
    cursor = dbConnection.cursor()
    result = cursor.callfunc(functionName, returnType, args)
    return result
