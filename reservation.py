from datetime import datetime
from serializable import Serializable
from database import DatabaseConnector

class Reservation(Serializable):
    # 1. Verbindung zur Tabelle 'reservations'
    db_connector = DatabaseConnector().get_table("reservations")

    def __init__(self, device_id, user_id, start_date, end_date, reservation_id=None, creation_date=None, last_update=None):
        # ID-Handling: Falls keine ID übergeben wird, generieren wir eine
        if not reservation_id:
            reservation_id = f"{device_id}_{start_date}"
            
        # 2. Konstruktor der Mutterklasse aufrufen
        super().__init__(id=reservation_id, creation_date=creation_date, last_update=last_update)
        
        self.device_id = device_id
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"Reservation: {self.device_id} reserved by {self.user_id} ({self.start_date} -> {self.end_date})"

    @classmethod
    def instantiate_from_dict(cls, data: dict):
        # 3. Umwandlung von Datenbank-Dict zurück in Objekt
        return cls(
            reservation_id=data.get("id"), # Serializable speichert die ID unter "id"
            device_id=data.get("device_id"),
            user_id=data.get("user_id"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            creation_date=data.get("creation_date"),
            last_update=data.get("last_update")
        )