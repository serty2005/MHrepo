import sqlite3
import uuid
import os
import load_data as load

# Загрузка данных из ServiceDesk

# Генерация уникального GUID
def generate_guid():
    return str(uuid.uuid4())

# Создание подключения к базе данных SQLite
pathbd = os.getenv("BDPATH") + 'EntitiesSD.db'

# Использование контекстного менеджера для работы с базой данных
with sqlite3.connect(pathbd) as conn:
    cursor = conn.cursor()

    # Создание таблицы для серверов
    cursor.execute('''CREATE TABLE IF NOT EXISTS servers (
                    id TEXT PRIMARY KEY,
                    UUID TEXT,
                    UniqueID TEXT,
                    DeviceName TEXT,
                    Teamviewer TEXT,
                    RDP TEXT,
                    IP TEXT,
                    CabinetLink TEXT,
                    owner TEXT,
                    AnyDesk TEXT,
                    folder TEXT)''')

    # Создание таблицы для владельцев
    cursor.execute('''CREATE TABLE IF NOT EXISTS owners (
                    id TEXT PRIMARY KEY,
                    UUID TEXT)''')

    # Загрузка данных о серверах
    url_servers = f"https://myhoreca.itsm365.com/sd/services/rest/find/objectBase$Server?accessKey={os.getenv('SDKEY')}&attrs=UUID,UniqueID,DeviceName,Teamviewer,RDP,IP,CabinetLink,owner,AnyDesk"
    data_servers = load(url_servers)

    if data_servers:
        owners_guids = {}  # Словарь для хранения GUID'ов владельцев
        for item in data_servers:
            server_id = generate_guid()
            server_uuid = item.get("UUID")
            server_unique_id = item.get("UniqueID")
            server_device_name = item.get("DeviceName")
            server_teamviewer = item.get("Teamviewer")
            server_rdp = item.get("RDP")
            server_ip = item.get("IP")
            server_cabinet_link = item.get("CabinetLink")
            server_owner = item.get("owner")
            server_owner_uuid = None
            if server_owner:
                server_owner_uuid = server_owner.get("UUID")

                # Генерация GUID для владельцев и сохранение в словаре
                if server_owner_uuid not in owners_guids:
                    owners_guids[server_owner_uuid] = generate_guid()

            server_anydesk = item.get("AnyDesk")
            server_folder = owners_guids.get(server_owner_uuid)

            # Добавление записи в таблицу серверов
            cursor.execute('''INSERT INTO servers (id, UUID, UniqueID, DeviceName, Teamviewer, RDP, IP, CabinetLink, owner, AnyDesk, folder) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (server_id, server_uuid, server_unique_id, server_device_name, server_teamviewer, server_rdp, server_ip, server_cabinet_link, server_owner_uuid, server_anydesk, server_folder))

            # Добавление записи в таблицу владельцев
            cursor.execute('''INSERT OR IGNORE INTO owners (id, UUID) VALUES (?, ?)''', (owners_guids.get(server_owner_uuid), server_owner_uuid))

        # Сохранение изменений
        conn.commit()
        print("Данные о серверах успешно добавлены в базу данных.")
    else:
        print("Ошибка загрузки данных о серверах.")
