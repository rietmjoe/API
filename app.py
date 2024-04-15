import streamlit as st
import requests
import pandas as pd # Für die Darstellung der Koordinaten auf der Karte


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

# Erstelle drei Spalten: Die mittlere Spalte für den Hauptinhalt
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Verwende nur die mittlere Spalte für die Anzeige der Inhalte
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
        season = st.selectbox("Zu welcher Jahreszeit?", ["Summer", "Autumn", "Winter", "Spring"])
        suitableFor = st.selectbox("Suitable for:", ["Children", "Group", "Individual", "Family", "Couples", "Womenonly"])

        weatherOptions = {
            "All": "*",
            "Sunny": "outdoor",
            "Rainy": "indoor",
        }
        weather = st.selectbox("Weather:", weatherOptions.keys())
        
        geoLocationOptions = {
            "All": "*",
            "Along the grand tour": "alongthegrandtour",
            "In the city": "inthecity",
            "In the mountains": "inthemountains",
            "In the country side": "inthecountryside",
            "In the alpine mountains": "inthealpinemountains",
            "At the lake": "atthelake",
            "By the river": "bytheriver",
            "At the forest": "attheforest",
            "Central location": "centrallocation"
        }
        geoLocation = st.selectbox("Geographical location:", geoLocationOptions.keys())



        location = st.number_input("Gib deine Postleitzahl ein", value=9000, min_value=1000, max_value=9999, step=1)

        submitted = st.form_submit_button("Vorschläge anzeigen")




    # API-Integration
    if submitted:
        api_url = "https://opendata.myswitzerland.io/v1/attractions"
        headers = {
            "x-api-key": "dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y"
        }

        # facet filters (AND-linked), python f-string for variable filtering (Filterzeichenkette für die API-Abfrage)
        facet_filters = (
            f"seasons:{season},"
            f"suitablefortype:{suitableFor},"
            f"geographicallocations:{geoLocationOptions[geoLocation]},"
            f"indooroutdoorclassifications:{weatherOptions[weather]}"
        )

        params = {
            'facet.filter': facet_filters, 
            'expand': 'true',                  # Hole vollständige Daten für jede Attraktion
            'striphtml': 'true',               # Entferne HTML-Tags aus den Texten
            'hitsPerPage': '5',               # Maximale Anzahl von Ergebnissen pro Seite
        }

        response = requests.get(api_url, headers=headers, params=params)


        if response.status_code == 200:
            attractions = response.json()["data"]
            for attraction in attractions:
                st.header(attraction["name"])

                if "photo" in attraction:
                    # Bild zentriert und responsive innerhalb der mittleren Spalte anzeigen
                    st.image(attraction["photo"], use_column_width=True)
                else:
                    st.write("Kein Foto verfügbar.")

                if "abstract" in attraction:
                    st.write(attraction["abstract"])
                else:
                    st.write("Keine Zusammenfassung verfügbar.")

                if "description" in attraction:
                    st.write(attraction["description"])
                else:
                    st.write("Keine Beschreibung verfügbar.")
                
                st.subheader("Address")
                if "address" in attraction and attraction['address']: # Check if address is available
                    address = attraction['address'][0]
                    st.write(address.get('name', 'Kein Name verfügbar'))
                    st.write(f"**Strasse:** {address.get('streetAddress', 'Keine Strasse verfügbar')}")
                    st.write(f"**PLZ/Ort:** {address.get('postalCode', 'Keine PLZ verfügbar')} {address.get('addressLocality', 'Kein Ort verfügbar')}")
                    st.write(f"**Land:** {address.get('addressCountry', 'Kein Land verfügbar')}")
                    st.write(f"**Telefon:** {address.get('telephone', 'Keine Telefonnummer verfügbar')}")
                    st.write(f"**Email:** {address.get('email', 'Keine E-Mail verfügbar')}")
                    st.write(f"**Website:** [Link zur Website]({address.get('url', '#')})")
                else:
                    st.write("No address available.")

                if "geo" in attraction:
                    # st.write("Koordinaten: ", attraction["geo"]["latitude"], attraction["geo"]["longitude"])
                    data = {
                        "latitude": [attraction["geo"]["latitude"]],
                        "longitude": [attraction["geo"]["longitude"]],
                        "name": attraction["name"]
                    }
                    df = pd.DataFrame(data)
                    st.map(df)
                else:
                    st.write("Keine Koordinaten verfügbar.")

                if "url" in attraction:
                    st.link_button("More informations", attraction["url"])
                else:
                    st.write("Kein Link verfügbar.")

                st.divider()

        else:
            st.error("Fehler beim Laden der Attraktionen.")


