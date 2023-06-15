import mysql.connector

from logger import logger

def create_connection():
    logger.info('Подключение к БД')
    try:
        return mysql.connector.connect(
            host="localhost",
            user="aigiz",
            password="Imaroot1",
            database="outline",
            autocommit=True
        )
    except mysql.connector.errors.InterfaceError as err:
        logger.error('Ошибка подключения к БД: %s', err)
        return None

# datetime
# CODE
# user_id
# telegram_id
# amout
#
#
# CMD_ADD_MONEY
# ERROR_GGHJJJ
# CMD_BUY_KEY server df,gdfkgdfkj
#
# 2023-06-15 12:12:12 CMD_BUY_KEY server df,gdfkgdfkj
# ERR_DATABASE_CONNECTION dfkjghfjkhgkjdfhgkjdfhgkdfjghkdfjhgkfdj fjgdfkghdkfgkf
