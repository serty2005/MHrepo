import sqlite3
import pyodbc
import os
from remotes_update import generate_guid


def main():
    # Подключение к базе данных SQLite
    sqlite_conn = sqlite3.connect('./files/EntitiesSD.db')
    sqlite_cursor = sqlite_conn.cursor()

    # Подключение к базе данных MSSQL
    mssql_conn = pyodbc.connect(os.getenv('MSSQLSTRING'))
    mssql_cursor = mssql_conn.cursor()
            
    # Получение текущего номера ревизии из таблицы DBVersion
    mssql_cursor.execute("SELECT revision FROM dbo.DBVersion")
    current_revision = mssql_cursor.fetchone()[0]

    try:
        # Выборка всех записей из таблицы workstations в базе SQLite
        sqlite_cursor.execute("SELECT id, Teamviewer, Anydesk, DeviceName, folder FROM workstations")
        workstations_data = sqlite_cursor.fetchall()

        for row in workstations_data:
            id, teamviewer, anydesk, device_name, folder = row
            
            # Проверка длины строк Anydesk и Teamviewer
            if anydesk and len(anydesk) > 50:
                print("Skipping record with too long Anydesk:", id, device_name)
                continue
            if teamviewer and len(teamviewer) > 50:
                print("Skipping record with too long Teamviewer:", id, device_name)
                continue
            if device_name is None:
                print("Skipping record without DeviceName:", id)
                continue

            # Вставка данных в таблицу MSSQL
            if anydesk and teamviewer:
                # Создание двух записей для Anydesk и Teamviewer
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, current_revision + 1, device_name, "Anydesk", folder, '', '', anydesk, '', 'False', ''))  
                mssql_conn.commit()
                
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (generate_guid(), current_revision + 1, device_name, "Teamviewer", folder, '', '', teamviewer, '', 'False', ''))  
                mssql_conn.commit()
            elif anydesk:
                # Создание записи для Anydesk
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, current_revision + 1, device_name, "Anydesk", folder, '', '', anydesk, '', 'False', ''))  
                mssql_conn.commit()
            elif teamviewer:
                # Создание записи для Teamviewer
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, current_revision + 1, device_name, "Teamviewer", folder, '', '', teamviewer, '', 'False', ''))  
                mssql_conn.commit()
            else:
                print("Neither Anydesk nor Teamviewer present for record with id:", id)

    except Exception as e:
        print("Error:", e)
        mssql_conn.rollback()

    finally:
        # Закрытие соединений
        sqlite_conn.close()
        mssql_conn.close()

if __name__ == "__main__":
    main()