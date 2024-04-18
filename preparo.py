import sqlite3
import pyodbc
import os


def main():
    # Подключение к базе данных SQLite
    sqlite_conn = sqlite3.connect('./files/EntitiesSD.db')
    sqlite_cursor = sqlite_conn.cursor()

    # Подключение к базе данных MSSQL
    mssql_conn = pyodbc.connect(os.getenv('MSSQLSTRING'))
    mssql_cursor = mssql_conn.cursor()

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
            
            # Вставка данных в таблицу MSSQL
            if anydesk and teamviewer:
                # Создание двух записей для Anydesk и Teamviewer
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, 1, device_name, "Anydesk", folder, '', '', anydesk, '', 'False', ''))  # Добавляем 1 для revision
                mssql_conn.commit()
                
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, 1, device_name, "Teamviewer", folder, '', '', teamviewer, '', 'False', ''))  # Добавляем 1 для revision
                mssql_conn.commit()
            elif anydesk:
                # Создание записи для Anydesk
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, 1, device_name, "Anydesk", folder, '', '', anydesk, '', 'False', ''))  # Добавляем 1 для revision
                mssql_conn.commit()
            elif teamviewer:
                # Создание записи для Teamviewer
                mssql_cursor.execute("INSERT INTO dbo.Entities (id, revision, name, type, folder, ip, port, login, password, deleted, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (id, 1, device_name, "Teamviewer", folder, '', '', teamviewer, '', 'False', ''))  # Добавляем 1 для revision
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