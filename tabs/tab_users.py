import streamlit as st
from users import User

def run():
    st.header("Nutzer-Verwaltung")

    # Laden aus der Datenbank
    users_data = User.load_all()
    
    # Anzeige der Nutzer
    st.subheader("Vorhandene Nutzer")
    st.dataframe(users_data)

    # Formular
    st.subheader("Neuen Nutzer anlegen")
    with st.form("create_user_form"):
        email = st.text_input("E-Mail-Adresse (ID)")
        name = st.text_input("Name des Nutzers")
        
        submitted = st.form_submit_button("Nutzer speichern")
        
        if submitted:
            if email and name:
                # neues Objekt User erstellen und speichern
                new_user = User(email = email, name = name)
                new_user.store_data()
                
                st.success(f"Nutzer {name} erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Bitte alle Felder ausfüllen!")