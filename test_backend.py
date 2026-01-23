from datetime import date
from users import User
from devices import Device
from reservation import Reservation

def run_test():
    print("=== STARTE BACKEND TEST ===")

    # 1. TEST: Nutzer anlegen
    print("\n--- 1. Nutzer erstellen & speichern ---")
    u1 = User(email="max@mustermann.at", name="Max Mustermann")
    u2 = User(email="anna@beispiel.com", name="Anna Beispiel")
    
    # store_data() kommt jetzt aus serializable.py!
    u1.store_data() 
    u2.store_data() 
    print("-> Nutzer gespeichert.")

    # Überprüfen, ob sie geladen werden können
    loaded_users = User.find_all()
    print(f"-> Anzahl Nutzer in DB: {len(loaded_users)}")
    for u in loaded_users:
        print(f"   - {u}")

    # 2. TEST: Gerät anlegen
    print("\n--- 2. Gerät erstellen & speichern ---")
    d1 = Device(
        device_id="DEV-001",
        name="High-End 3D Drucker",
        responsible_person="max@mustermann.at",
        creation_date=date.today(),
        end_of_life=date(2030, 12, 31),
        maintenance_cost=150.0,
        maintenance_interval=180
    )
    
    d1.store_data()
    print("-> Gerät gespeichert.")
    
    # Testen ob next_maintenance automatisch berechnet wurde (Logik im Device __init__)
    print(f"-> Automatisch berechnete nächste Wartung: {d1.next_maintenance}")

    # 3. TEST: Reservierung anlegen (Die neue Klasse)
    print("\n--- 3. Reservierung erstellen ---")
    r1 = Reservation(
        device_id=d1.device_id,
        user_id=u1.email,
        start_date=date(2024, 5, 1),
        end_date=date(2024, 5, 5)
    )
    
    r1.store_data()
    print("-> Reservierung gespeichert.")

    # Überprüfen der Reservierungen
    loaded_reservations = Reservation.find_all()
    print(f"-> Anzahl Reservierungen in DB: {len(loaded_reservations)}")
    for r in loaded_reservations:
        print(f"   - {r}")

    print("\n=== TEST ERFOLGREICH ABGESCHLOSSEN ===")

if __name__ == "__main__":
    run_test()