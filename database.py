import os
from tinydb import TinyDB
from tinydb.table import Table
from tinydb.storages import JSONStorage
from datetime import datetime, date, time
from tinydb_serialization import Serializer, SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

class DatabaseConnector:
    """
    Stellt die Datenbankverbindung als Singleton bereit.
    Abstrahiert den Dateipfad und die Serializer-Konfiguration.
    """
    # Die einzige Instanz der Klasse (Singleton Pattern)
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            # Pfad zur database.json im selben Ordner
            cls.__instance.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
        return cls.__instance
    
    def get_table(self, table_name: str) -> Table:
        """
        Gibt die gewünschte Tabelle zurück und nutzt dabei die konfigurierte Middleware.
        """
        return TinyDB(self.__instance.path, storage=serializer).table(table_name)

# --- Serializer Konfiguration ---

class DateSerializer(Serializer):
    OBJ_CLASS = date  # Serializer für date Objekte

    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return date.fromisoformat(s)

class TimeSerializer(Serializer):
    OBJ_CLASS = time  # Serializer für time Objekte
    
    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return time.fromisoformat(s)

# Middleware registrieren
serializer = SerializationMiddleware(JSONStorage)
serializer.register_serializer(DateTimeSerializer(), 'TinyDateTime')
serializer.register_serializer(DateSerializer(), 'TinyDate')
serializer.register_serializer(TimeSerializer(), 'TinyTime')