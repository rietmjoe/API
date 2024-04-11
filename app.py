import streamlit as st

# Token für API-Abragen
# dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y


# To install streamlit, type the following command in the terminal
# pip install streamlit

# to start the frontpage
# streamlit hello

# To run the app, type the following command in the terminal
# streamlit run app.py

# Setze die Seitenkonfiguration
st.set_page_config(page_title="Entdecke lokale Aktivitäten", layout="wide")

# Stelle das Logo dar
col1, col2 = st.columns([1, 3])
with col1:
    st.image("st_logo.png", width=50)  
with col2:
    st.write("")


# Initialisiere den Bildindex im Session State, falls noch nicht vorhanden
if 'bild_index' not in st.session_state:
    st.session_state.bild_index = 0
    
# Bildliste
bilder = ["luzern.jpg", "berg.jpg", "berg2.jpg"]

# Container für das Bild und die Navigation
col1, col2, col3 = st.columns([1, 3, 1])

# Knopf für das vorherige Bild
with col1:
    if st.button('◀️'):
        # Gehe zum vorherigen Bild, bleibe bei 0, wenn bereits am Anfang
        st.session_state.bild_index = max(st.session_state.bild_index - 1, 0)

# Zeige das aktuelle Bild
with col2:
    st.image(bilder[st.session_state.bild_index], use_column_width=True)

# Knopf für das nächste Bild
with col3:
    if st.button('▶️'):
        # Gehe zum nächsten Bild, bleibe am Ende, wenn bereits am letzten Bild
        st.session_state.bild_index = min(st.session_state.bild_index + 1, len(bilder) - 1)



# Willkommenstitel und -untertitel
st.title("Entdecke, was du in deiner Nähe unternehmen kannst!")
st.subheader("Gib deinen Standort und das Wetter ein, und wir schlagen dir vor, was du unternehmen kannst.")

# Formular für Benutzereingaben
with st.form("user_input"):
    # Texteingabe für die Postleitzahl mit vornotiertem Wert
    location = st.number_input("Gib deine Postleitzahl ein", value=9000, min_value=1000, max_value=9999, step=1)

    # Dropdown-Menü für Wetteroptionen
    weather = st.selectbox("Wähle das Wetter aus", ["Regnerisch", "Sonnig", "Bewölkt"])
    
    # Submit-Button für das Formular
    submitted = st.form_submit_button("Vorschläge anzeigen")
    if submitted:
        st.write(f"Für die Postleitzahl {location} bei {weather} Wetter, empfehlen wir folgendes:")

        # API-Integration hier
        if weather == "Sonnig":
            st.write("Geniesse einen Tag am See!")
        elif weather == "Regnerisch":
            st.write("Geh besser nicht an den See")
        else:
            st.write("Ein Spaziergang im bewölkten Wetter kann erfrischend sein!")


