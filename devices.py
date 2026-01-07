import os
from tinydb import TinyDB, Query
from serializer import serializer

# Gleich wie users.py
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')

class Device:
    db_connector = TinyDB(DB_PATH, storage=serializer).table('devices')

    def __init__(self, device_id, name, responsible_person, creation_date, end_of_life, maintenance_cost, next_maintenance, maintenance_interval):

        self.device_id = device_id
        self.name = name
        self.responsible_person = responsible_person
        self.creation_date = creation_date
        self.end_of_life = end_of_life
        self.maintenance_cost = maintenance_cost
        self.next_maintenance = next_maintenance
        self.maintenance_interval = maintenance_interval

    def store_data(self):
        print(f"Speichere Gerät {self.name} ...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_id == self.device_id)

        # Alle Daten in ein Dictionary
        data = {
            "device_id": self.device_id,
            "name": self.name,
            "responsible_person": self.responsible_person,
            "creation_date": self.creation_date,
            "end_of_life": self.end_of_life,
            "maintenance_cost": self.maintenance_cost,
            "next_maintenance": self.next_maintenance,
            "maintenance_interval": self.maintenance_interval
        }

        if result:
            self.db_connector.update(data, doc_ids=[result[0].doc_id])
        else:
            self.db_connector.insert(data)

    
    @classmethod
    def load_all(cls):
        return cls.db_connector.all()