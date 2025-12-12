import streamlit as st

# 1. Konfiguration der Seite
st.set_page_config(page_title="Geräte-Verwaltung", layout="wide")

st.title("Geräte-Verwaltung der Hochschule")

# 2. Mock-Daten initialisieren
# Simuliert die Datenbank, solange noch keine realen Daten bestehen 
if 'devices' not in st.session_state:
    st.session_state.devices = [
        {"id": "1", "name": "3D-Drucker Prusa MK3", "user": "m.panny@fh.at"},
        {"id": "2", "name": "Laser-Cutter", "user": "j.huber@fh.at"}
    ]

# 3. Aufbau der Navigation (Tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "Geräte-Verwaltung", 
    "Nutzer-Verwaltung", 
    "Reservierungen", 
    "Wartung"
])

# --- TAB 1: Geräte-Verwaltung ---
with tab1:
    st.header("Geräte Übersicht")
    
    # Anzeige der "Datenbank" (Mock-Daten)
    st.dataframe(st.session_state.devices)
    
    st.subheader("Neues Gerät anlegen")
    # Formular für Eingaben [cite: 461]
    with st.form("new_device"):
        name = st.text_input("Gerätename")
        verantwortlicher = st.text_input("Verantwortlicher (Email)")
        
        submitted = st.form_submit_button("Gerät speichern")
        if submitted:
            # nur visuelles Feedback
            st.success(f"Gerät '{name}' wurde (simuliert) angelegt!")
            # Daten in den Session State hängen, damit man sofort was sieht
            st.session_state.devices.append({"id": "99", "name": name, "user": verantwortlicher})

# --- TAB 2: Nutzer-Verwaltung ---
with tab2:
    st.header("Nutzer Übersicht")
    st.write("Hier kommt die Nutzer-Verwaltung hin.")
    # FLO !!!!!!!!!!!: Baue hier ein Formular ähnlich wie oben!

# --- TAB 3: Reservierungen ---
with tab3:
    st.header("Reservierungssystem")
    st.info("Dieses Feature wird später implementiert.")

# --- TAB 4: Wartung ---
with tab4:
    st.header("Wartungs-Management")
    st.info("Dieses Feature wird später implementiert.")