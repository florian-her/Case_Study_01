from serializable import Serializable
from database import DatabaseConnector

class User(Serializable):
    db_connector = DatabaseConnector().get_table("users")

    def __init__(self, email, name, creation_date=None, last_update=None):
        super().__init__(id=email, creation_date=creation_date, last_update=last_update)
        
        self.email = email
        self.name = name

    def __str__(self):
        return f"User: {self.name} ({self.email})"

    @classmethod
    def instantiate_from_dict(cls, data: dict):
        return cls(
            email=data.get("email"),
            name=data.get("name"),
            creation_date=data.get("creation_date"),
            last_update=data.get("last_update")
        )