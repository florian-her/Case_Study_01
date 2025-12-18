import streamlit as st
# Importiere die neuen Module aus dem Ordner "tabs"
import tabs.tab_devices as tab_devices
import tabs.tab_users as tab_users
import tabs.tab_reservation as tab_reservation
import tabs.tab_maintenance as tab_maintenance

# 1. Konfiguration
st.set_page_config(page_title="Geräte-Verwaltung", layout="wide")
st.title("Geräte-Verwaltung der Hochschule")

# 2. Mock-Daten Initialisierung (Global für alle Tabs)
if 'devices' not in st.session_state:
    st.session_state.devices = [
        {"id": "1", "name": "3D-Drucker Prusa MK3", "user": "m.panny@fh.at"},
        {"id": "2", "name": "Laser-Cutter", "user": "j.huber@fh.at"}
    ]

# 3. Tabs erstellen
tab1, tab2, tab3, tab4 = st.tabs([
    "Geräte-Verwaltung", 
    "Nutzer-Verwaltung", 
    "Reservierungen", 
    "Wartung"
])

# 4. Inhalte laden (Modular)
with tab1:
    tab_devices.run()

with tab2:
    tab_users.run()

with tab3:
    tab_reservation.run()

with tab4:
    tab_maintenance.run()