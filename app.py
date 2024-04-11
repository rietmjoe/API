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


# Pagegestaltung Header
st.image("berg2.jpg", use_column_width=True)

# Stelle das Logo dar
col1, col2 = st.columns([1, 3])
with col1:
    st.image("st_logo.png", width=50)  
with col2:
    st.write("")

st.title("Entdecke, was du in deiner Nähe unternehmen kannst!")
st.subheader("Gib deinen Standort und das Wetter ein, und wir schlagen dir vor, was du unternehmen kannst.")




# Benutzereingaben
with st.form("user_input"):

    # Sie hend no irgend e Kategorie wölle. Luegemer mol was machbar isch.
    category = st.selectbox("Was suchst du?", ["Kultur", "Sport", "Touristenattraktion"])

    # PLZ Eingabe mit St. Gallen als Default 
    location = st.number_input("Gib deine Postleitzahl ein", value=9000, min_value=1000, max_value=9999, step=1)

    # Dropdown für Wetter
    weather = st.selectbox("Wähle das Wetter aus", ["Sonnig", "Regnerisch", "Bewölkt"])
    
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