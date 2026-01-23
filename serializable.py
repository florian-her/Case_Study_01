from abc import ABC, abstractmethod
from datetime import datetime
from tinydb import Query
from typing import Self

class Serializable(ABC):
    # Diese Variable muss in den Vererbungen (Device, User) überschrieben werden!

    db_connector = None

    def __init__(self, id, creation_date: datetime = None, last_update: datetime = None) -> None:
        self.id = id
        self.creation_date = creation_date if creation_date else datetime.now()
        self.last_update = last_update if last_update else datetime.now()

    @classmethod
    @abstractmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        """Muss von den Vererbungen implementiert werden, um Objekte aus Dicts zu erzeugen."""
        pass

    def store_data(self):
        """Speichert oder aktualisiert das Objekt in der Datenbank (Upsert)."""
        print(f"Storing data for ID {self.id}...")
        self.last_update = datetime.now()

        query = Query()
        # upsert prüft anhand der ID, ob ein Update oder Insert nötig ist
        result = self.db_connector.upsert(self.__to_dict(), query.id == self.id)
        
        if result:
            print("Data updated.")
        else:
            print("Data inserted.")
    
    def delete(self):
        """Löscht das Objekt anhand der ID aus der Datenbank."""
        print(f"Deleting data for ID {self.id}...")
        query = Query()
        if self.db_connector.remove(query.id == self.id):
            print("Data deleted.")
        else:
            print("Data not found.")
    
    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1) -> Self | list[Self]:
        """Sucht nach Einträgen anhand eines beliebigen Attributs."""
        ObjectQuery = Query()
        result = cls.db_connector.search(ObjectQuery[by_attribute] == attribute_value)

        if result:
            if num_to_return == -1:
                num_to_return = len(result)

            data = result[:num_to_return]
            # Erstellt Objekte aus den gefundenen Dictionaries
            object_results = [cls.instantiate_from_dict(d) for d in data]
            return object_results if num_to_return > 1 else object_results[0]
        else:
            return None
           
    @classmethod
    def find_all(cls) -> list[Self]:
        """Lädt alle Einträge der Tabelle und gibt eine Liste von Objekten zurück."""
        objects = []
        for obj_data in cls.db_connector.all():
            objects.append(cls.instantiate_from_dict(obj_data))
        return objects

    def __repr__(self):
        return self.__str__()
    
    @abstractmethod
    def __str__(self):
        pass
    
    # Do not modify this function unless you really know what you are doing!
    def __to_dict(self, *args):
        """
        Rekursive Konvertierung des Objekts in ein Dictionary für TinyDB.
        """
        # If no object is passed to the function convert the object itself
        if len(args) > 0:
            obj = args[0] # ignore all other objects but the first one
        else:
            obj = self

        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.__to_dict(v)
            return data
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            data = [self.__to_dict(v) for v in obj]
            return data
        elif hasattr(obj, "__dict__"):
            data = []
            for k, v in obj.__dict__.items():
                # Filtert private Attribute (starten mit __, z.B. __instance) aus, falls nötig
                data.append((k, self.__to_dict(v)))
            return dict(data)
        else:
            return obj