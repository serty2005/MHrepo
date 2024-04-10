import requests
import sqlite3


# Функция для создания таблицы в базе данных SQLite
def create_table():
    conn = sqlite3.connect('fiscal_registers_fromSD.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fiscal_registers
                 (RNKKT TEXT, FNNumber TEXT, KKTRegDate TEXT, UUID TEXT PRIMARY KEY,
                  FRSerialNumber TEXT, FNExpireDate TEXT)''')
    conn.commit()
    conn.close()


# Функция для вставки данных из JSON объекта в базу данных SQLite
def insert_data_from_json(json_data):
    conn = sqlite3.connect('fiscal_registers_fromSD.db')
    c = conn.cursor()
    for entry in json_data:
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
    params = {'accessKey': 'be65d663-b9de-4f09-b476-b2b8fb2d6423', 'attrs': 'UUID,FRSerialNumber,RNKKT,KKTRegDate,FNExpireDate,FNNumber'}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        json_data = response.json()
        create_table()
        insert_data_from_json(json_data)
        print("База данных обновлена успешно.")
    else:
        print("Ошибка при получении данных:", response.status_code)