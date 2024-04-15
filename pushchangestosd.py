import sqlite3
import requests
import os
from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# Функция для сравнения данных и отправки запроса на редактирование объекта в SD
def compare_and_update():

    pathbd = os.getenv("BDPATH") + 'fiscal_registers_fromSD.db'
    conn_sd = sqlite3.connect(pathbd)
    path = os.getenv("BDPATH") + 'fiscal_registers_fromPOS.db'
    conn_json = sqlite3.connect(path)
    c_json = conn_json.cursor()
    c_sd = conn_sd.cursor()

    # Выбираем данные для сравнения из базы данных SD
    c_sd.execute('''SELECT FRSerialNumber, FNNumber, FNExpireDate, UUID
                    FROM fiscal_registers''')
    sd_data = c_sd.fetchall()

    # Выбираем данные для сравнения из базы данных JSON
    c_json.execute('''SELECT serialNumber, fn_serial, dateTime_end
                      FROM fiscal_registers''')
    json_data = c_json.fetchall()

    # Сравниваем данные и отправляем запросы на обновление при несоответствии
    for sd_entry in sd_data:
        for json_entry in json_data:
            # Проверяем совпадение по FRSerialNumber и serialNumber
            if sd_entry[0] == json_entry[0]:
                # Преобразуем даты из строкового формата в объекты datetime для корректного сравнения
                sd_date = parser.parse(sd_entry[2])
                json_date = parser.parse(json_entry[2])

                if sd_date != json_date:  # Сравниваем даты
                    
                    print(f"Объект с UUID {sd_entry[3]} будет изменен.") # Выводим UUID объекта для тестирования
                    formatted_date = json_date.strftime('%Y.%m.%d %H:%M:%S')

                    # Отправляем запрос на редактирование объекта в SD
                    edit_url = f'https://myhoreca.itsm365.com/sd/services/rest/edit/{sd_entry[3]}/'
                    params = {'accessKey': os.getenv('SDKEY'), 'FNNumber': json_entry[1], 'FNExpireDate': formatted_date}
                    response = requests.post(edit_url, params=params)
                    if response.status_code == 200 or 201:
                        print(f"Объект с UUID {sd_entry[3]} успешно обновлен.")
                    else:
                        print(f"Ошибка при обновлении объекта с UUID {sd_entry[3]}:", response.status_code)

    conn_json.close()
    conn_sd.close()


# Вызываем функцию для сравнения данных и обновления объектов при несоответствии
compare_and_update()
