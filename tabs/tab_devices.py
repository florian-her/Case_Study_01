import streamlit as st
from datetime import date

def run():
    st.header("Geräte-Verwaltung")
    
    # --- ANZEIGE ---
    if 'devices' in st.session_state:
        st.dataframe(st.session_state.devices)
    
    st.markdown("---")
    
    # --- NEUES GERÄT ANLEGEN ---
    st.subheader("Neues Gerät anlegen")
    
    with st.form("new_device_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            device_id = st.text_input("Geräte-ID (Inventarnummer)")
            name = st.text_input("Gerätename")
            verantwortlicher = st.text_input("Verantwortliche Person (E-Mail)")
        
        with col2:
            creation_date = st.date_input("Anschaffungsdatum", value=date.today())
            end_of_life = st.date_input("End of Life (Datum)")
        
        st.markdown("### Wartungs-Einstellungen")
        col3, col4 = st.columns(2)
        with col3:
            maintenance_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, step=1)
            maintenance_cost = st.number_input("Wartungskosten (€)", min_value=0.0, step=0.10)
        with col4:
            next_maintenance = st.date_input("Nächster Wartungstermin")

        submitted = st.form_submit_button("Gerät speichern")
        
        if submitted:
            st.success(f"Gerät '{name}' wurde erfolgreich (simuliert) angelegt!")
            new_device_entry = {
                "id": device_id, 
                "name": name, 
                "user": verantwortlicher,
                "next_maintenance": next_maintenance
            }
            st.session_state.devices.append(new_device_entry)
            st.rerun()