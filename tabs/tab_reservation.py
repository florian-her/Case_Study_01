import streamlit as st
from datetime import date
from devices import Device
from users import User
from reservation import Reservation

def run():
    st.header("Reservierungssystem")

    # Daten laden für Geräte und Nutzer
    devices = Device.find_all()
    users = User.find_all()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Bestehende Reservierungen")
        reservations = Reservation.find_all()
        
        if reservations:
            # Liste für die Anzeige
            res_data = []
            for r in reservations:
                res_data.append({
                    "Gerät-ID": r.device_id,
                    "Nutzer": r.user_id,
                    "Von": r.start_date,
                    "Bis": r.end_date
                })
            st.dataframe(res_data, use_container_width=True)
        else:
            st.info("Keine Reservierungen gefunden.")

    with col2:
        st.subheader("Neue Reservierung")
        
        # Mapping erstellen: Name -> Objekt 
        device_map = {d.name: d.device_id for d in devices}
        user_map = {u.name: u.email for u in users}

        with st.form("res_form"):
            # Dropdowns mit echten Daten
            if not device_map or not user_map:
                st.warning("Bitte erst Geräte und Nutzer anlegen!")
                selected_device_name = None
                selected_user_name = None
            else:
                selected_device_name = st.selectbox("Gerät wählen", options=list(device_map.keys()))
                selected_user_name = st.selectbox("Nutzer wählen", options=list(user_map.keys()))
            
            start_date = st.date_input("Startdatum", value=date.today())
            end_date = st.date_input("Enddatum", value=date.today())
            
            submitted = st.form_submit_button("Reservierung eintragen")
            
            if submitted and selected_device_name and selected_user_name:
                dev_id = device_map[selected_device_name]
                usr_id = user_map[selected_user_name]

                # Neues Reservierungsobjekt erstellen
                new_res = Reservation(
                    device_id=dev_id,
                    user_id=usr_id,
                    start_date=start_date,
                    end_date=end_date
                )
                
                # Speichern
                new_res.store_data()
                st.success(f"Reservierung für '{selected_device_name}' erfolgreich gespeichert!")
                st.rerun()