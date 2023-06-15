import mysql.connector
import datetime

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


def add_keys(server_id, telegram_id, username, start_date, stop_date):
    mydb = create_connection()

    if mydb is None:
        logger.error('Не удалось создать соединение с БД')
        return "Произошла ошибка, обратитесь к админстратору"

    try:
        with mydb.cursor(buffered=True) as mycursor:
            # узнаем user_id юзера
            mycursor.execute("SELECT user_id FROM users WHERE telegram_id = %s", ([telegram_id]))
            result_id = mycursor.fetchone()
            _userId = result_id[0]

            try:
                # обращаемся к бд, что бы взять несипользуемый ключ
                mycursor.execute("SELECT * FROM outline_keys WHERE used = %s AND server_id = %s", (0, server_id))
                result_id = mycursor.fetchone()
                _key_id, _outline_id, _sever_id, _key_value, _used = result_id
            except Exception as e:
                logger.error('Ошибка при получении ключа из БД id пользователя: ' + str(_userId) + ', %s', e)
                _key_value = "Произошла ошибка, обратитесь к админстратору"
                pass

            # меняем used c 0 на 1 у текущего ключа
            mycursor.execute("""UPDATE outline_keys SET used = 1 WHERE outline_key_id = %s AND used = 0;""",
                             [_outline_id])

            # добавляем в таблицу user_keys приобретенный юзером ключ, + дата начала и конца действия ключа
            mycursor.execute(
                "INSERT INTO user_keys (user_id, key_id, name, start_date, stop_date) VALUES (%s, %s, %s, %s, %s)",
                (_userId, _key_id, username, start_date, stop_date)
            )

        return _key_value
    except mysql.connector.errors as err:
        logger.error('Произошла ошибка при добавлении ключа: ' + str(_userId) + ', %s', datetime.datetime.now(), err)
        _key_value = "Произошла ошибка, обратитесь к админстратору"
    finally:
        mydb.close()
        return _key_value
