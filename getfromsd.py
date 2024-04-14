import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


# Функция для создания таблицы в базе данных SQLite
def create_table():
    path = os.getenv("BDPATH") + 'fiscal_registers_fromSD.db'
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fiscal_registers
                 (RNKKT TEXT, FNNumber TEXT, KKTRegDate TEXT, UUID TEXT PRIMARY KEY,
                  FRSerialNumber TEXT, FNExpireDate TEXT)''')
    conn.commit()
    conn.close()


# Функция для вставки данных из JSON объекта в базу данных SQLite
def insert_data_from_json(sd_data):
    path = os.getenv("BDPATH") + 'fiscal_registers_fromSD.db'
    conn = sqlite3.connect(path)
    c = conn.cursor()
    for entry in sd_data:
            RNKKT = entry['RNKKT']
            FNNumber = entry['FNNumber']
            KKTRegDate = entry['KKTRegDate']
            UUID = entry['UUID']
            FRSerialNumber = entry['FRSerialNumber']
            FNExpireDate = entry['FNExpireDate']
            c.execute('''INSERT OR REPLACE INTO fiscal_registers 
                         (RNKKT, FNNumber, KKTRegDate, UUID, FRSerialNumber, FNExpireDate)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                         (RNKKT, FNNumber, KKTRegDate, UUID, FRSerialNumber, FNExpireDate))
    conn.commit()
    conn.close()


# Функция для получения данных по указанной ручке и обновления базы данных
def update_database():
    url = 'https://myhoreca.itsm365.com/sd/services/rest/find/objectBase$FR'
    params = {'accessKey': os.getenv('SDKEY'), 'attrs': 'UUID,FRSerialNumber,RNKKT,KKTRegDate,FNExpireDate,FNNumber'}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        sd_data = response.json()
        create_table()
        insert_data_from_json(sd_data)
        print("База данных обновлена успешно.")
    else:
        print("Ошибка при получении данных:", response.status_code)


update_database()
