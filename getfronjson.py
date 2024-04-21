import json
import sqlite3
import os

# Функция для создания таблицы в базе данных SQLite
def create_table():

    path = os.getenv("BDPATH") + 'fiscal_registers_fromPOS.db'
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fiscal_registers
                 (modelName TEXT, serialNumber TEXT PRIMARY KEY, RNM TEXT, organizationName TEXT,
                  fn_serial TEXT, datetime_reg TEXT, dateTime_end TEXT, ofdName TEXT,
                  bootVersion TEXT, ffdVersion TEXT, fnExecution TEXT, INN TEXT)''')
    conn.commit()
    conn.close()


# Функция для вставки данных из файла .json в базу данных SQLite
def insert_data_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        path = os.getenv("BDPATH") + 'fiscal_registers_fromPOS.db'
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO fiscal_registers 
                     (modelName, serialNumber, RNM, organizationName, fn_serial, datetime_reg, 
                     dateTime_end, ofdName, bootVersion, ffdVersion, fnExecution, INN)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (data['modelName'], data['serialNumber'], data['RNM'], data['organizationName'],
                      data['fn_serial'], data['datetime_reg'], data['dateTime_end'], data['ofdName'],
                      data['bootVersion'], data['ffdVersion'], data['fnExecution'], data['INN']))
        conn.commit()
        conn.close()


# Функция для обхода всех файлов .json в заданной директории и чтения данных из них
def process_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            insert_data_from_json(file_path)


if __name__ == '__main__':
    create_table()
    process_json_files(os.getenv('JSONPATH'))
