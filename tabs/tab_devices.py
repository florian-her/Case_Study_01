import streamlit as st
from datetime import date
from devices import Device
from users import User

def run():
    st.header("Geräte-Verwaltung")
    
    # 1. ANZEIGE 
    # Lade alle Geräte als OBJEKTE
    devices = Device.find_all()
    
    if devices:
        st.subheader("Alle registrierten Geräte")
        
        display_data = []
        for d in devices:
            display_data.append({
                "ID": d.device_id,
                "Name": d.name,
                "Verantwortlich": d.responsible_person,
                "Wartungstermin": d.next_maintenance
            })
            
        st.dataframe(display_data, use_container_width=True)
    else:
        st.info("Noch keine Geräte in der Datenbank vorhanden.")

    st.markdown("---")

    # 2. GERÄT LÖSCHEN
    if devices:
        st.subheader("Gerät löschen")
        # Liste der IDs für das Dropdown erstellen
        device_ids = [d.device_id for d in devices]
        selected_id = st.selectbox("Wähle ein Gerät anhand der ID zum Löschen aus:", device_ids)
        
        if st.button("Gerät löschen", type="primary"):
            device_to_delete = next((d for d in devices if d.device_id == selected_id), None)
            
            if device_to_delete:
                device_to_delete.delete()
                st.success(f"Gerät mit ID {selected_id} wurde erfolgreich gelöscht.")
                st.rerun()
            else:
                st.error("Gerät nicht gefunden.")
        st.markdown("---")

    # 3. NEUES GERÄT ANLEGEN
    st.subheader("Neues Gerät anlegen")
    
    # Laden der Nutzer für Dropdown
    users = User.find_all()
    user_emails = [u.email for u in users]

    if not user_emails:
        st.warning("Bitte lege zuerst einen Nutzer in der Nutzer-Verwaltung an.")
    
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
                # Neues Gerät-Objekt erstellen
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
                # Speichern (ruft upsert via Serializable auf)
                new_device.store_data()
                st.success(f"Gerät '{name}' erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Bitte ID, Name und Verantwortlichen ausfüllen.")