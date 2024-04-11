import streamlit as st

def main():
    # Create a dropdown menu with three options
    option = st.selectbox('Select an option', ['Option 1', 'Option 2', 'Option 3'])

    # Display the selected option
    st.write('You selected:', option)

if __name__ == '__main__':
    main()