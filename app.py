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
st.set_page_config(page_title="Discover local activities", layout="wide")

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
        st.title("Discover what you can do in your area!")
        st.subheader("Please enter the relevant information below and we will suggest what you can do.")
        st.write("\* means all (no filter)")

    # Benutzereingaben
    with st.form("user_input"):
        experienceType = st.selectbox("What experience type are you looking for?", ["*", "Nature", "Education", "Adventure", "Culture", "Active", "Urban", "Relax", "Culinary"])
        season = st.selectbox("At what time of year?", ["*", "Summer", "Autumn", "Winter", "Spring"])
        suitableFor = st.selectbox("Suitable for:", ["*", "Children", "Group", "Individual", "Family", "Couples"])

        weatherOptions = {
            "*": "*",
            "Sunny": "outdoor",
            "Rainy": "indoor",
        }
        weather = st.selectbox("Weather:", weatherOptions.keys())
        
        geoLocationOptions = {
            "*": "*",
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

        postalCode = st.number_input("Enter your postal code.", value=9000, min_value=1000, max_value=9658, step=1)
        searchRadius = st.number_input("Search radius (in m):", value=1000, min_value=100, max_value=20000, step=1)
        hitAmount = st.number_input("Adjust how many hits will be shown:", value=5, min_value=1, max_value=50, step=1)

        submitted = st.form_submit_button("Show suggestions")


    # API-Integration (backend)

    # Funktion zur Abfrage der Koordinaten anhand der Postleitzahl
    def get_coordinates_from_postcode(postcode):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'postalcode': postcode,
            'country': 'Switzerland',
            'format': 'json'
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                return latitude, longitude
            else:
                return "No data found for this postcode."
        else:
            return "Error retrieving coordinates."
        
    if submitted:
        api_url = "https://opendata.myswitzerland.io/v1/attractions"
        headers = {
            "x-api-key": "dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y"
        }

        # facet filters (AND-linked), python f-string for variable filtering (Filterzeichenkette für die API-Abfrage)
        facet_filters = (
            f"experiencetype:{experienceType},"
            f"seasons:{season},"
            f"suitablefortype:{suitableFor},"
            f"geographicallocations:{geoLocationOptions[geoLocation]},"
            f"indooroutdoorclassifications:{weatherOptions[weather]}"
        )

        lat, lon = get_coordinates_from_postcode(postalCode) # Koordinaten für ausgewählte plz abrufen
        coordsAndRadius = f"{lat},{lon},{searchRadius}"

        params = {
            'facet.filter': facet_filters, 
            'geo.dist': coordsAndRadius,
            'expand': 'true',                  # Hole vollständige Daten für jede Attraktion
            'striphtml': 'true',               # Entferne HTML-Tags aus den Texten
            'hitsPerPage': hitAmount,               # Maximale Anzahl von Ergebnissen pro Seite
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
                    st.write("No summary available.")

                if "description" in attraction:
                    st.write(attraction["description"])
                else:
                    st.write("No description available.")
                
                if "address" in attraction and attraction['address']: # Check if address is available
                    address = attraction['address'][0]
                    st.subheader("Address")
                    st.write(address.get('name', 'No name available'))
                    st.write(f"**Street:** {address.get('streetAddress', 'No street available')}")
                    st.write(f"**Postcode/location:** {address.get('postalCode', 'No postal code available')} {address.get('addressLocality', 'No location available')}")
                    st.write(f"**Country:** {address.get('addressCountry', 'No country available')}")
                    st.write(f"**Telephone:** {address.get('telephone', 'No phone number available')}")
                    st.write(f"**Email:** {address.get('email', 'No email available')}")
                    st.write(f"**Website:** [Link to the website]({address.get('url', '#')})")
                else:
                    st.write("No address available.")

                if "geo" in attraction:
                    data = {
                        "latitude": [attraction["geo"]["latitude"]],
                        "longitude": [attraction["geo"]["longitude"]],
                    }
                    df = pd.DataFrame(data)
                    st.map(df)
                else:
                    st.write("No coordinates available.")

                if "url" in attraction:
                    st.link_button("More informations", attraction["url"])
                else:
                    st.write("No link available")

                st.divider()

        else:
            st.error("Error loading the attractions.")