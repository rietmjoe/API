import streamlit as st
import requests  # Für die API-Abfrage
import pandas as pd  # Für die Darstellung der Koordinaten auf der Karte


# Streamlit starten

# Token für API-Abragen
# dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y

# Streamlit installieren mit folgendem Code im Eingabefenster (Rechtsklick auf app.py --> Open in Integrated Terminal)
# pip install streamlit

# Hello Page starten (nicht benötigt)
# streamlit hello

# Um die Anwendung zu starten, den folgenden Command in das Eingabefenster eingeben. Danach Link anwählen, wenn nicht automatisch geöffnet.
# streamlit run app.py

# Streamlit Documentation https://docs.streamlit.io/develop/api-reference


# Setze die Seitenkonfiguration (Titel, Icon, Layout der Page)
st.set_page_config(
    page_title="Discover local activities", page_icon="st_logo.png", layout="wide"
)


# Frontend

# Header-Bild
st.image("berg2.jpg", use_column_width=True)

# Erstelle seitenübergreifend drei Spalten: Die mittlere Spalte für den Hauptinhalt
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Verwende nur die mittlere Spalte für die Anzeige der Inhalte

    # Logo und Titel
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("st_logo.png", width=50)
    with col2:
        st.title("Discover what you can do in your area!")
        st.subheader(
            "Please enter the relevant information below and we will suggest what you can do."
        )
        st.write("\* means all (no filter)")

    # Benutzereingaben
    # Selectboxen für die Auswahl der Filterkriterien
    with st.form("user_input"):
        experienceType = st.selectbox(
            "What experience type are you looking for?",
            [
                "*",
                "Nature",
                "Education",
                "Adventure",
                "Culture",
                "Active",
                "Urban",
                "Relax",
                "Culinary",
            ],
        )
        season = st.selectbox(
            "At what time of year?", ["*", "Summer", "Autumn", "Winter", "Spring"]
        )
        suitableFor = st.selectbox(
            "Suitable for:",
            ["*", "Children", "Group", "Individual", "Family", "Couples"],
        )

        weatherOptions = {
            "*": "*",
            "Sunny": "outdoor",
            "Rainy": "indoor",
        }
        # Sunny oder Rainy anwählen, outdoor oder indoor wird an die API übergeben
        weather = st.selectbox("Weather:", weatherOptions.keys())

        # Werte in Frontend = "Along the grand tour", Werte in API = "alongthegrandtour"
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
            "Central location": "centrallocation",
        }
        geoLocation = st.selectbox("Geographical location:", geoLocationOptions.keys())

        postalCode = st.number_input(
            "Enter your postal code.",
            value=9000,
            min_value=1000,
            max_value=9658,
            step=1,
        )
        searchRadius = st.number_input(
            "Search radius (in m):", value=1000, min_value=100, max_value=20000, step=1
        )
        hitAmount = st.number_input(
            "Adjust how many hits will be shown:",
            value=5,
            min_value=1,
            max_value=50,
            step=1,
        )

        submitted = st.form_submit_button("Show suggestions")

    # API-Integration (backend)

    # Funktion zur Abfrage der Koordinaten anhand der Postleitzahl
    def get_coordinates_from_postcode(postcode):
        url = "https://nominatim.openstreetmap.org/search"
        params = {"postalcode": postcode, "country": "Switzerland", "format": "json"}

        # Get Anfrage an die API mit definierten Parametern
        response = requests.get(url, params=params)
        # Wenn Abfrage erfolgreich, dann Daten auslesen
        if response.status_code == 200:
            # Extrahiere JSON-Daten aus der Antwort und speichere sie in der Variable data
            data = response.json()
            if data:
                # Extrahiere Breiten- und Längengrad aus den erhaltenen Daten
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
                return latitude, longitude
            else:
                return "No data found for this postcode."
        # Sonst Fehlermeldung
        else:
            return "Error retrieving coordinates."

    # Wenn der Button "Show suggestions" gedrückt wurde, dann führe die API-Abfrage durch
    if submitted:
        api_url = "https://opendata.myswitzerland.io/v1/attractions"
        # Persönlicher API-Key für die Abfrage
        headers = {"x-api-key": "dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y"}

        # facet filters (AND-linked), python f-string for variable filtering (Filterzeichenkette für die API-Abfrage)
        facet_filters = (
            f"experiencetype:{experienceType},"
            f"seasons:{season},"
            f"suitablefortype:{suitableFor},"
            f"geographicallocations:{geoLocationOptions[geoLocation]},"
            f"indooroutdoorclassifications:{weatherOptions[weather]}"
        )

        # GET-Abfrage für die Koordinaten basierend auf PLZ (Siehe Funktion oben)
        lat, lon = get_coordinates_from_postcode(
            postalCode
        )  # Koordinaten für ausgewählte PLZ abrufen, speichern in lat und lon
        coordsAndRadius = f"{lat},{lon},{searchRadius}"

        params = {
            "facet.filter": facet_filters,
            "geo.dist": coordsAndRadius,
            "expand": "true",  # Hole vollständige Daten für jede Attraktion
            "striphtml": "true",  # Entferne HTML-Tags aus den Texten
            "hitsPerPage": hitAmount,  # Maximale Anzahl von Ergebnissen pro Seite basierend auf Input vorhin
        }

        # GET-Abfrage an die API mit den definierten Parametern, URL sowie API-Key
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            # JSON Daten extrahieren und in Variable attractions speichern
            attractions = response.json()["data"]

            # For-Schleife für die Anzeige der Attraktionen
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

                if (
                    "address" in attraction and attraction["address"]
                ):  # Check if address is available
                    address = attraction["address"][0]
                    st.subheader("Address")
                    st.write(address.get("name", "No name available"))
                    st.write(
                        f"**Street:** {address.get('streetAddress', 'No street available')}"
                    )
                    st.write(
                        f"**Postcode/location:** {address.get('postalCode', 'No postal code available')} {address.get('addressLocality', 'No location available')}"
                    )
                    st.write(
                        f"**Country:** {address.get('addressCountry', 'No country available')}"
                    )
                    st.write(
                        f"**Telephone:** {address.get('telephone', 'No phone number available')}"
                    )
                    st.write(f"**Email:** {address.get('email', 'No email available')}")
                    st.write(
                        f"**Website:** [Link to the website]({address.get('url', '#')})"
                    )
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

                # Trennlinie zwischen den Attraktionen
                st.divider()

        else:
            st.error("Error loading the attractions.")
