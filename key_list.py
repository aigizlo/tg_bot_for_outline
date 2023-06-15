import mysql.connector
from logger import logger
from create_connection import create_connection
import datetime


mydb = create_connection()

def get_user_keys(telegram_id):
    try:
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT user_id FROM users WHERE telegram_id = %s", (telegram_id,))
        result_id = mycursor.fetchone()
        user_id = result_id[0]

        mycursor.execute(
            f"SELECT ok.key_value, uk.stop_date  FROM outline_keys ok  JOIN user_keys uk ON ok.key_id = uk.key_id WHERE uk.user_id = {user_id} AND ok.server_id = 1"
        )
        key_date_amster = mycursor.fetchall()

        mycursor.execute(
            f"SELECT ok.key_value, uk.stop_date  FROM outline_keys ok  JOIN user_keys uk ON ok.key_id = uk.key_id WHERE uk.user_id = {user_id} AND ok.server_id = 2")
        key_date_german = mycursor.fetchall()

        amsterdam_keys_text = ""
        germany_keys_text = ""

        if key_date_amster:
            amsterdam_keys_text = "Ключи Амстердама :\n\n"
            for key, date in key_date_amster:
                amsterdam_keys_text += f"- {key}, действителен до {date.strftime('%d %B %Y ')}\n"

        if key_date_german:
            germany_keys_text = "Ключи Германии :\n\n"
            for key, date in key_date_german:
                germany_keys_text += f"- {key}, действителен до {date.strftime('%d %B %Y ')}\n"

        if not key_date_amster and not key_date_german:
            answer = "У вас нет ключей"
        else:
            answer = amsterdam_keys_text + "\n" + germany_keys_text

        return answer

    except mysql.connector.errors.ProgrammingError as err:
        answer = "Произошла ошибка, обратитесь к админстратору"
        logger.error('Произошла ошибка при попытке найти его ключи в БД: ' + str(user_id) + ' %s', datetime.datetime.now(), err)
        return answer