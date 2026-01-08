import os 
from tinydb import TinyDB, Query
from serializer import serializer

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')

class User:
    db_connector = TinyDB(DB_PATH, storage=serializer).table('users')

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def store_data(self):
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.email == self.email)
        data = {"email": self.email, "name": self.name}

        if result:
            self.db_connector.update(data, doc_ids=[result[0].doc_id])
        else:
            self.db_connector.insert(data)
        
    @classmethod
    def load_all(cls):
        return cls.db_connector.all()

    @classmethod
    def delete(cls, email):
        """Löscht einen Nutzer anhand der E-Mail-Adresse [Neu hinzugefügt]"""
        UserQuery = Query()
        cls.db_connector.remove(UserQuery.email == email)