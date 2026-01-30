import streamlit as st
import pandas as pd
from datetime import date, timedelta
from devices import Device

def run():
    st.header("Wartungs-Management")
    
    # Daten laden
    devices = Device.find_all()
    
    if not devices:
        st.warning("Keine Geräte im System gefunden.")
        return

    st.subheader("Aktueller Wartungsstatus")
    
    # Sortieren nach Datum (Zugriff via Attribut .next_maintenance)
    sorted_devices = sorted(devices, key=lambda x: x.next_maintenance if x.next_maintenance else date.max)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Alle Geräte (nach Dringlichkeit sortiert):**")
        
        display_data = []
        for d in sorted_devices:
            status = "OK"
            # Datumsvergleich
            if d.next_maintenance < date.today():
                status = "ÜBERFÄLLIG"
            elif d.next_maintenance <= date.today() + timedelta(days=7):
                status = "Bald fällig"
            
            display_data.append({
                "Gerät": d.name,
                "Status": status,
                "Fällig am": d.next_maintenance,
                "Kosten (€)": f"{d.maintenance_cost:.2f}"
            })
        
        df = pd.DataFrame(display_data)

        # Styling Funktion
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

        st.dataframe(
            df.style.map(highlight_status, subset=['Status']),
            use_container_width=True
        )

    with col2:
        # Metriken berechnen
        num_overdue = sum(1 for d in sorted_devices if d.next_maintenance < date.today())
        # Kosten berechnen
        total_cost = sum(d.maintenance_cost for d in sorted_devices if d.next_maintenance.year == date.today().year)
        
        st.metric("Überfällige Geräte", num_overdue, delta_color="inverse")
        st.metric("Geschätzte Kosten (dieses Jahr)", f"{total_cost} €")

    st.markdown("---")

    st.subheader("Wartung protokollieren")
    
    with st.form("maintenance_form"):
        # Mapping Name -> Objekt
        device_map = {d.name: d for d in devices}
        selected_device_name = st.selectbox("Welches Gerät wurde gewartet?", list(device_map.keys()))
        
        c1, c2 = st.columns(2)
        with c1:
            maintenance_date = st.date_input("Datum der Durchführung", value=date.today())
            technician = st.text_input("Durchgeführt von", "Techniker A")
        
        with c2:
            real_cost = st.number_input("Tatsächliche Kosten (€)", min_value=0.0, step=10.0)
            notes = st.text_area("Bemerkungen / Bericht", "Filter getauscht, Software Update...")

        submit_maintenance = st.form_submit_button("Wartung abschließen & Speichern")
        
        if submit_maintenance:
            # Wir holen das Objekt direkt aus der Map
            selected_device = device_map[selected_device_name]
            
            if selected_device:
                # Neues Datum berechnen (Intervall nutzen!)
                # Falls maintenance_interval ein String ist, sicherheitshalber casten
                interval = int(selected_device.maintenance_interval)
                new_date = maintenance_date + timedelta(days=interval)
                
                # Attribute aktualisieren
                selected_device.next_maintenance = new_date
                
                selected_device.store_data()
                
                st.success(f"Wartung für '{selected_device_name}' gespeichert! Nächster Termin: {new_date}")
                st.rerun()