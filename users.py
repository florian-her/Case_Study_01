import os 
from tinydb import TinyDB, Query
from serializer import serializer

#Pfad
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')

class User:
    #Verbindung herstellen
    db_connector = TinyDB(DB_PATH, storage=serializer).table('users')

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def store_data(self):
        print(f"Speichere User {self.email} ...")
        UserQuery = Query()
        #Prüfen ob User schon existiert
        result = self.db_connector.search(UserQuery.email == self.email)

        #Dicnotary zum Speichern
        data ={"email": self.email, "name": self.name}

        if result:
            self.db_connector.update(data, doc_ids=[result[0].doc_id])
        else:
            self.db_connector.insert(data)
        
    @classmethod
    def load_all(cls):
        """Lädt alle user aus der Liste von Dictionaries für Streamlit"""
        return cls.db_connector.all()