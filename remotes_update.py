import requests
import sqlite3
import uuid
import os
import json
import load_data as load

# Генерация уникального GUID
def generate_guid():
    return str(uuid.uuid4())

# Создание подключения к базе данных SQLite
pathbd = os.getenv("BDPATH") + 'EntitiesSD.db'

# Использование контекстного менеджера для работы с базой данных
with sqlite3.connect(pathbd) as conn:
    cursor = conn.cursor()

    # Создание таблицы для рабочих станций
    cursor.execute('''CREATE TABLE IF NOT EXISTS workstations (
                    id TEXT PRIMARY KEY,
                    UUID TEXT,
                    GK INTEGER,
                    Teamviewer TEXT,
                    AnyDesk TEXT,
                    DeviceName TEXT,
                    lastModifiedDate TEXT,
                    owner TEXT,
                    folder TEXT)''')
 
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
                    UUID TEXT,
                    title TEXT,
                    metaClass TEXT)''')

    # Загрузка данных
    url = f"https://myhoreca.itsm365.com/sd/services/rest/find/objectBase$Workstation?accessKey={os.getenv('SDKEY')}&attrs=UUID,GK,Teamviewer,AnyDesk,DeviceName,lastModifiedDate,owner"
    data = load(url)

    if data:
        owners_guids = {}  # Словарь для хранения GUID'ов владельцев
        for item in data:
            workstation_id = generate_guid()
            workstation_uuid = item.get("UUID")
            workstation_gk = item.get("GK")
            workstation_teamviewer = item.get("Teamviewer")
            workstation_anydesk = item.get("AnyDesk")
            workstation_device_name = item.get("DeviceName")
            workstation_last_modified_date = item.get("lastModifiedDate")
            workstation_owner = item.get("owner")
            workstation_owner_uuid = None
            owner_title = None
            owner_meta_class = None
            if workstation_owner:
                workstation_owner_uuid = workstation_owner.get("UUID")
                owner_title = workstation_owner.get("title")
                owner_meta_class = workstation_owner.get("metaClass")

                # Генерация GUID для владельцев и сохранение в словаре
                if workstation_owner_uuid not in owners_guids:
                    owners_guids[workstation_owner_uuid] = generate_guid()

            workstation_folder = owners_guids.get(workstation_owner_uuid)

            # Добавление записи в таблицу рабочих станций
            cursor.execute('''INSERT INTO workstations (id, UUID, GK, Teamviewer, AnyDesk, DeviceName, lastModifiedDate, owner, folder) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (workstation_id, workstation_uuid, workstation_gk, workstation_teamviewer, workstation_anydesk, workstation_device_name, workstation_last_modified_date, workstation_owner_uuid, workstation_folder))

            # Добавление записи в таблицу владельцев
            cursor.execute('''INSERT OR IGNORE INTO owners (id, UUID, title, metaClass) VALUES (?, ?, ?, ?)''', (owners_guids.get(workstation_owner_uuid), workstation_owner_uuid, owner_title, owner_meta_class))

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
        print("Данные успешно добавлены в базу данных.")
    else:
        print("Ошибка загрузки данных.")
