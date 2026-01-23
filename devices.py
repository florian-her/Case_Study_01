from datetime import datetime, date, timedelta
from serializable import Serializable
from database import DatabaseConnector

class Device(Serializable):
    # 1. Verbindung zur Tabelle 'devices' über das Singleton herstellen
    db_connector = DatabaseConnector().get_table("devices")

    def __init__(self, device_id, name, responsible_person, creation_date, end_of_life, 
                 maintenance_cost, maintenance_interval, next_maintenance=None, last_update=None):
        
        # 2. Den Konstruktor der Mutterklasse aufrufen
        super().__init__(id=device_id, creation_date=creation_date, last_update=last_update)
        
        # Eigene Attribute setzen
        self.device_id = device_id
        self.name = name
        self.responsible_person = responsible_person
        self.end_of_life = end_of_life
        self.maintenance_cost = maintenance_cost
        self.maintenance_interval = maintenance_interval

        # Logik für das Wartungsdatum
        if next_maintenance is None:
            # Sicherheitscheck, falls creation_date ein String ist
            if isinstance(self.creation_date, str):
                c_date = date.fromisoformat(self.creation_date)
            else:
                c_date = self.creation_date
            
            if isinstance(c_date, datetime):
                c_date = c_date.date()

            self.next_maintenance = c_date + timedelta(days=int(self.maintenance_interval))
        else:
            self.next_maintenance = next_maintenance

    def __str__(self):
        return f"Device: {self.name} ({self.device_id})"

    @classmethod
    def instantiate_from_dict(cls, data: dict):
        return cls(
            device_id=data.get("device_id"),
            name=data.get("name"),
            responsible_person=data.get("responsible_person"),
            creation_date=data.get("creation_date"),
            end_of_life=data.get("end_of_life"),
            maintenance_cost=data.get("maintenance_cost"),
            maintenance_interval=data.get("maintenance_interval"),
            next_maintenance=data.get("next_maintenance"),
            last_update=data.get("last_update")
        )