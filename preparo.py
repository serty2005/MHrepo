import sqlite3
import pyodbc

# Строка подключения к базе данных MSSQL
CLBASESTRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.25.1.220,1433;DATABASE=CLEARbatServer;UID=sa;PWD=Resto#Test01"

def main():
    # Подключение к базе данных SQLite
    sqlite_conn = sqlite3.connect('./files/EntitiesSD.db')
    sqlite_cursor = sqlite_conn.cursor()

    # Подключение к базе данных MSSQL
    mssql_conn = pyodbc.connect(CLBASESTRING)
    mssql_cursor = mssql_conn.cursor()

    try:
        # Выборка всех записей из таблицы workstations в базе SQLite
        sqlite_cursor.execute("SELECT id, Teamviewer, Anydesk, DeviceName, folder FROM workstations")
        workstations_data = sqlite_cursor.fetchall()

        for row in workstations_data:
            id, teamviewer, anydesk, device_name, folder = row
            
            # Проверка на наличие только цифр в полях Teamviewer и Anydesk
            if (teamviewer and not teamviewer.isdigit()) or anydesk:
                print("Skipping record with non-numeric Teamviewer or Anydesk:", id, device_name)
                continue
            
            # Проверка на наличие хотя бы одного из полей Teamviewer и Anydesk
            if not (teamviewer or anydesk):
                print("Skipping record with no Teamviewer or Anydesk:", id, device_name)
                continue
            
            # Вставка данных в таблицу MSSQL
            mssql_cursor.execute("INSERT INTO dbo.Entities (id, name, type, folder, login, revision) VALUES (?, ?, ?, ?, ?, ?)",
                                 (id, device_name, "Teamviewer" if teamviewer else "Anydesk", folder, teamviewer or anydesk, 1))  # Добавляем 1 для revision
            mssql_conn.commit()

    except Exception as e:
        print("Error:", e)
        mssql_conn.rollback()

    finally:
        # Закрытие соединений
        sqlite_conn.close()
        mssql_conn.close()

if __name__ == "__main__":
    main()