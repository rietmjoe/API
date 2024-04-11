import streamlit as st

# Token für API-Abragen
# dPhbYjYBIcaVh4KzZFNn99qMlGQrQmc96AhS4E9Y


# To install streamlit, type the following command in the terminal
# pip install streamlit

# to start the frontpage
# streamlit hello

# To run the app, type the following command in the terminal
# streamlit run app.py

# Page hübsch darstellen
st.set_page_config(page_title="Entdecke lokale Aktivitäten", layout="wide")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("st_logo.png", width=200)  
with col2:
    st.write("")

# Add a welcome title and subtitle with a more engaging message
st.title("Entdecke, was du in deiner Nähe unternehmen kannst!")
st.subheader("Gib deinen Standort und das Wetter ein, und wir schlagen dir vor, was du unternehmen kannst.")

# Create a form for user input to make the page cleaner
with st.form("user_input"):
    # Create a text input for location
    location = st.number_input("Gib deinen Postleitzahl ein")

    # Create a dropdown menu with weather options
    weather = st.selectbox("Wähle das Wetter aus", ["Regnerisch", "Sonnig", "Bewölkt"])
    
    # Submit button for the form
    submitted = st.form_submit_button("Vorschläge anzeigen")
    if submitted:
        st.write(f"Für {location} bei {weather} Wetter, empfehlen wir folgendes:")

        # Hier an API anknüpfen
        if weather == "Sonnig":
            st.write("Genieße einen Tag am See!")
        elif weather == "Regnerisch":
            st.write("Hier Antworten basierend auf API")
        else:
            st.write("Ein Spaziergang im bewölkten Wetter kann erfrischend sein!")


