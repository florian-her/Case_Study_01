import streamlit as st

def run():
    st.header("Reservierungssystem")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Bestehende Reservierungen")

    with col2:
        st.subheader("Neue Reservierung")
        with st.form("res_form"):
            device = st.selectbox("Gerät wählen", options=["3D-Drucker", "Laser-Cutter"])
            user = st.text_input("Nutzer (E-Mail)")
            start_date = st.date_input("Startdatum")
            end_date = st.date_input("Enddatum")
            
            submitted = st.form_submit_button("Reservierung eintragen")
            
            if submitted:
                st.success(f"Reservierung für {device} erfolgreich gespeichert!")