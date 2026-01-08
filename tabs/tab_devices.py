import streamlit as st
from datetime import date
from devices import Device
from users import User

def run():
    st.header("Geräte-Verwaltung")
    
    # 1. ANZEIGE 
    # Lade alle Geräte aus der Datenbank
    devices_data = Device.load_all()
    if devices_data:
        st.subheader("Alle registrierten Geräte")
        # Anzeigen der Dictionaries als Tabelle
        st.dataframe(devices_data, use_container_width=True)
    else:
        st.info("Noch keine Geräte in der Datenbank vorhanden.")

    st.markdown("---")

    # 2. GERÄT LÖSCHEN
    if devices_data:
        st.subheader("Gerät löschen")
        # Liste der IDs für das Dropdown erstellen
        device_ids = [d['device_id'] for d in devices_data]
        selected_id = st.selectbox("Wähle ein Gerät anhand der ID zum Löschen aus:", device_ids)
        
        if st.button("Gerät löschen", type="primary"):
            # Aufruf der Lösch-Methode aus backend
            Device.delete(selected_id)
            st.warning(f"Gerät mit ID {selected_id} wurde erfolgreich gelöscht.")
            # Wichtig, neu laden
            st.rerun()
        st.markdown("---")

    # 3. NEUES GERÄT ANLEGEN
    st.subheader("Neues Gerät anlegen")
    
    # Laden der Nutzer für dropdown
    users_db = User.load_all()
    user_emails = [u['email'] for u in users_db]

    # Falls noch keine Nutzer existieren, Warnung anzeigen
    if not user_emails:
        st.warning("Bitte lege zuerst einen Nutzer in der Nutzer-Verwaltung an, um einen Verantwortlichen zuweisen zu können.")
    
    with st.form("new_device_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            device_id = st.text_input("Geräte-ID (Inventarnummer)")
            name = st.text_input("Gerätename")
            # dropdown für Verantwortlichen
            verantwortlicher = st.selectbox("Verantwortliche Person", options=user_emails)
        
        with col2:
            creation_date = st.date_input("Anschaffungsdatum", value=date.today())
            end_of_life = st.date_input("End of Life (Datum)", value=date.today())
        
        st.markdown("### Wartungs-Einstellungen")
        col3, col4 = st.columns(2)
        with col3:
            maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1)
            maintenance_cost = st.number_input("Wartungskosten (€)", min_value=0.0, step=0.10)
        with col4:
            next_maintenance = st.date_input("Nächster Wartungstermin", value=date.today())
            
        submitted = st.form_submit_button("Gerät speichern")
        
        if submitted:
            if device_id and name and verantwortlicher:
                # Neues Gerät-Objekt erstellen und speichern
                # Daten an Device-Klasse übergeben
                new_device = Device(
                    device_id=device_id,
                    name=name,
                    responsible_person=verantwortlicher,
                    creation_date=creation_date,
                    end_of_life=end_of_life,
                    maintenance_cost=maintenance_cost,
                    next_maintenance=next_maintenance,
                    maintenance_interval=maintenance_interval
                )
                new_device.store_data()
                st.success(f"Gerät '{name}' erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Bitte ID, Name und Verantwortlichen ausfüllen.")