from users import User
from devices import Device
from datetime import date

# 1. Teste User
print("--- TESTE USER ---")
u1 = User("test@fh.at", "Max Mustermann")
u1.store_data()
print("User gespeichert.")

alle_user = User.load_all()
print(f"Gefundene User in DB: {len(alle_user)}")
print(alle_user)

# 2. Teste Device
print("\n--- TESTE DEVICE ---")
d1 = Device(
    device_id="123", 
    name="Test-Gerät", 
    responsible_person="test@fh.at",
    creation_date=date.today(),
    end_of_life=date(2030, 1, 1),
    maintenance_interval=180,
    maintenance_cost=50.0,
    next_maintenance=date(2025, 12, 1)
)
d1.store_data()
print("Gerät gespeichert.")

alle_geraete = Device.load_all()
print(f"Gefundene Geräte in DB: {len(alle_geraete)}")
print(alle_geraete)