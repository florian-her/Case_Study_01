import streamlit as st
import pandas as pd  # Pandas importieren für das Styling, Voschlag von AI
from datetime import date, timedelta

def run():
    st.header("Wartungs-Management")
    
    # Sicherheits-Check
    if 'devices' not in st.session_state or not st.session_state.devices:
        st.warning("Keine Geräte im System gefunden.")
        return

    devices = st.session_state.devices

    # --- TEIL 1: DASHBOARD / ÜBERSICHT ---
    st.subheader("Aktueller Wartungsstatus")
    
    # Mock-Daten Anreicherung
    for d in devices:
        if "next_maintenance" not in d:
            d["next_maintenance"] = date.today() + timedelta(days=30)
        if "maintenance_cost" not in d:
            d["maintenance_cost"] = 50.0

    # Sortieren nach Datum
    sorted_devices = sorted(devices, key=lambda x: x["next_maintenance"])

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Alle Geräte (nach Dringlichkeit sortiert):**")
        
        display_data = []
        for d in sorted_devices:
            status = "OK"
            if d["next_maintenance"] < date.today():
                status = "ÜBERFÄLLIG"
            elif d["next_maintenance"] <= date.today() + timedelta(days=7):
                status = "Bald fällig"
            
            display_data.append({
                "Gerät": d["name"],
                "Status": status,
                "Fällig am": d["next_maintenance"],
                "Kosten (€)": f"{d['maintenance_cost']:.2f}"
            })
        
        df = pd.DataFrame(display_data)  # DataFrame für Styling

        # Funktion, die Farben bestimmt
        def highlight_status(val):
            color = ''
            weight = 'normal'
            if val == 'ÜBERFÄLLIG':
                color = 'red'
                weight = 'bold'
            elif val == 'Bald fällig':
                color = 'orange'
                weight = 'bold'
            elif val == 'OK':
                color = 'green'
            
            return f'color: {color}; font-weight: {weight}'

        # Style nur für die Spalte "Status" 
        st.dataframe(
            df.style.map(highlight_status, subset=['Status']),
            use_container_width=True
        )

    with col2:
        # Kleine Metriken
        num_overdue = sum(1 for d in sorted_devices if d["next_maintenance"] < date.today())
        total_cost = sum(d["maintenance_cost"] for d in sorted_devices if d["next_maintenance"].year == date.today().year)
        
        st.metric("Überfällige Geräte", num_overdue, delta_color="inverse")
        st.metric("Geschätzte Kosten (dieses Jahr)", f"{total_cost} €")

    st.markdown("---")

    # --- TEIL 2: WARTUNG DURCHFÜHREN ---
    st.subheader("Wartung protokollieren")
    
    with st.form("maintenance_form"):
        device_names = [d["name"] for d in devices]
        selected_device_name = st.selectbox("Welches Gerät wurde gewartet?", device_names)
        
        c1, c2 = st.columns(2)
        with c1:
            maintenance_date = st.date_input("Datum der Durchführung", value=date.today())
            technician = st.text_input("Durchgeführt von", "Techniker A")
        
        with c2:
            real_cost = st.number_input("Tatsächliche Kosten (€)", min_value=0.0, step=10.0)
            notes = st.text_area("Bemerkungen / Bericht", "Filter getauscht, Software Update...")

        submit_maintenance = st.form_submit_button("Wartung abschließen & Speichern")
        
        if submit_maintenance:
            selected_device = next((d for d in devices if d["name"] == selected_device_name), None)
            
            if selected_device:
                old_date = selected_device["next_maintenance"]
                new_date = maintenance_date + timedelta(days=365)
                selected_device["next_maintenance"] = new_date
                
                st.success(f"Wartung für '{selected_device_name}' gespeichert!")
                st.rerun()