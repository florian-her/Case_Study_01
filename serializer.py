from datetime import date, datetime
from tinydb_serialization import Serializer, SerializationMiddleware

class DataSerializer(Serializer):
    OBJ_CLASS = date        # Die Klasse, die gespeichert wird

    def encode(self, obj):
        return obj.isoformat() #Datum zu Text
    
    def decode(self, s):
        return date.fromisoformat(s) #Text zu Datum
    
serializer = SerializationMiddleware()
serializer.register_serializer(DataSerializer(), 'TinyDate')