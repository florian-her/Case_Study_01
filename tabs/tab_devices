import streamlit as st

def run():
    st.header("Geräte Übersicht")
    
    # Zugriff auf die Mock-Daten im Session State (wird in main.py initialisiert)
    if 'devices' in st.session_state:
        st.dataframe(st.session_state.devices)
    
    st.subheader("Neues Gerät anlegen")
    with st.form("new_device"):
        name = st.text_input("Gerätename")
        verantwortlicher = st.text_input("Verantwortlicher (Email)")
        
        submitted = st.form_submit_button("Gerät speichern")
        if submitted:
            st.success(f"Gerät '{name}' wurde (simuliert) angelegt!")
            st.session_state.devices.append({"id": "99", "name": name, "user": verantwortlicher})