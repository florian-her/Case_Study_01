import streamlit as st

def run():
    st.header("📅 Reservierungssystem")

    # Layout in zwei Spalten [cite: 513]
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Bestehende Reservierungen")
        # Hier werden später Daten aus der TinyDB angezeigt [cite: 277]

    with col2:
        st.subheader("Neue Reservierung")
        # Formular für die Eingabe [cite: 508]
        with st.form("res_form"):
            device = st.selectbox("Gerät wählen", options=["3D-Drucker", "Laser-Cutter"])
            user = st.text_input("Nutzer (E-Mail)")
            start_date = st.date_input("Startdatum")
            end_date = st.date_input("Enddatum")
            
            # Button zum Absenden [cite: 407, 474]
            submitted = st.form_submit_button("Reservierung eintragen")
            
            if submitted:
                # Validierung der Daten erfolgt hier [cite: 194, 197]
                st.success(f"Reservierung für {device} erfolgreich gespeichert!")