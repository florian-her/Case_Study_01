import streamlit as st
# Importiere die neuen Module aus dem Ordner "tabs"
from tabs import tab_devices, tab_users, tab_reservation, tab_maintenance

# 1. Konfiguration
st.set_page_config(page_title="Geräte-Verwaltung", layout="wide")
st.title("Geräte-Verwaltung der Hochschule")

# 2. Mock-Daten entfernt

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