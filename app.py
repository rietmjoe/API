import streamlit as st
import requests


# Streamlit starten

# Token für API-Abragen
# dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y

# Streamlit installieren mit folgendem Code im Eingabefenster (Rechtsklick auf app.py --> Open in Integrated Terminal)
# pip install streamlit

# Hello Page starten (nicht nötig)
# streamlit hello

# Um die Anwendung zu starten, den folgenden Command in das Eingabefenster eingeben. Danach Link anwählen, wenn nicht automatisch geöffnet. 
# streamlit run app.py


# Setze die Seitenkonfiguration
st.set_page_config(page_title="Entdecke lokale Aktivitäten", layout="wide")

# Header-Bild
st.image("berg2.jpg", use_column_width=True)

# Logo und Titel
col1, col2 = st.columns([1, 8])
with col1:
    st.image("st_logo.png", width=50)  
with col2:
    st.title("Entdecke, was du in deiner Nähe unternehmen kannst!")
    st.subheader("Gib deinen Standort und das Wetter ein, und wir schlagen dir vor, was du unternehmen kannst.")

# Benutzereingaben
with st.form("user_input"):
    category = st.selectbox("Was suchst du?", ["Museum", "Sport", "Touristenattraktion"])
    season = st.selectbox("Zu welcher Jahreszeit?", ["Sommer", "Herbst", "Winter", "Frühling"])
    weather = st.selectbox("Wähle das Wetter aus", ["Sonnig", "Regnerisch"])
    location = st.number_input("Gib deine Postleitzahl ein", value=9000, min_value=1000, max_value=9999, step=1)

    submitted = st.form_submit_button("Vorschläge anzeigen")





# API-Integration
    if submitted:
        api_url = "https://opendata.myswitzerland.io/v1/attractions"
        headers = {
            "x-api-key": "dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y"
        }
        response = requests.get(api_url, headers=headers)


        

        if response.status_code == 200:
            attractions = response.json()["data"]
            # Du könntest hier weitere Logik hinzufügen, um auf die Kategorie oder das Wetter zu filtern
            for attraction in attractions:
                # Überprüfe hier, ob die Attraktion den Benutzereingaben entspricht
                st.write(attraction["name"])
                st.write(attraction["abstract"])
                st.image(attraction["photo"])
        else:
            st.error("Fehler beim Laden der Attraktionen.")








#     "category" kann man vermutlich filtern mit "title": "Museum" im Antwort-JSON

# Seasons wird geprüft, ob die Antwort hier vorhanden ist. Hier sind bspw. alle 4 Seasons drin
#  "name": "seasons",
#                     "values": [
#                         {
#                             "name": "winter",
#                             "title": "Winter"
#                         },
#                         {
#                             "name": "spring",
#                             "title": "Spring"
#                         },
#                         {
#                             "name": "summer",
#                             "title": "Summer"
#                         },
#                         {
#                             "name": "autumn",
#                             "title": "Autumn"
#                         }
#                     ]

# Wetter am besten mit Regnerisch = indoor und Sonnig = outdoor
# "name": "indooroutdoorclassifications",
#                     "values": [
#                         {
#                             "name": "outdoor",
#                             "title": "Outdoor"
#                         }
#                     ]

# PLZ keine Ahnung bis jetzt, da nur Koordinaten in API vorhanden sind.