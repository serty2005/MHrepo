import schedule
import time
import os
from getfromsd import update_database_from_SD
from pushchangestosd import compare_and_update
from pushnew import process_json_folder



def run_tasks():
    # Задание для работы с папкой с JSON файлами каждый час
    schedule.every().hour.do(process_json_folder, os.getenv('JSONPATH'))

    # Задание для выгрузки данных из SD каждые 2 часа
    schedule.every(2).hours.do(update_database_from_SD)

    # Задание для сравнения и обновления данных каждые 2 часа
    schedule.every(2).hours.do(compare_and_update)

    # Запускаем бесконечный цикл для выполнения задач с периодичностью
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_tasks()