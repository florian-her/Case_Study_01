import streamlit as st
from users import User

def run():
    st.header("Nutzer-Verwaltung")

    # 1. Laden aus der Datenbank
    users_data = User.load_all()
    
    # 2. Anzeige der Nutzer
    st.subheader("Vorhandene Nutzer")
    if users_data:
        st.dataframe(users_data, use_container_width=True)
    else:
        st.info("Noch keine Nutzer angelegt.")

    # 3. Bereich zum Löschen von Nutzern
    st.divider()
    st.subheader("Nutzer löschen")
    
    if users_data:
        # Erstellt eine Liste aller E-Mails für das Dropdown
        user_emails = [u['email'] for u in users_data]
        selected_email = st.selectbox("Wähle einen Nutzer zum Löschen aus:", user_emails)
        
        if st.button("Nutzer löschen", type="primary"):
            User.delete(selected_email)
            st.warning(f"Nutzer {selected_email} wurde gelöscht.")
            st.rerun()
    else:
        st.write("Keine Nutzer zum Löschen vorhanden.")

    # 4. Formular zum Anlegen eines neuen Nutzers
    st.divider()
    st.subheader("Neuen Nutzer anlegen")
    with st.form("create_user_form"):
        email = st.text_input("E-Mail-Adresse (ID)")
        name = st.text_input("Name des Nutzers")
        
        submitted = st.form_submit_button("Nutzer speichern")
        
        if submitted:
            if email and name:
                new_user = User(email=email, name=name)
                new_user.store_data()
                st.success(f"Nutzer {name} erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Bitte alle Felder ausfüllen!")