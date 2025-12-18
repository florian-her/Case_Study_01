import streamlit as st

def run():
    st.header("Nutzer-Verwaltung")
    
    # Anzeige der Nutzer
    st.subheader("Vorhandene Nutzer")
    if 'users' in st.session_state:
        st.dataframe(st.session_state.users)

    # Formular
    st.subheader("Neuen Nutzer anlegen")
    with st.form("create_user_form"):
        email = st.text_input("E-Mail-Adresse (ID)")
        name = st.text_input("Name des Nutzers")
        
        submitted = st.form_submit_button("Nutzer speichern")
        
        if submitted:
            if email and name:
                new_user = {"email": email, "name": name}
                st.session_state.users.append(new_user)
                st.success(f"Nutzer {name} erfolgreich angelegt!")
                st.rerun()
            else:
                st.error("Bitte alle Felder ausfüllen!")