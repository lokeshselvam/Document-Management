import json
import streamlit as st

# Define the Streamlit app
def main():
    st.title("Login / Register")
    mode = st.radio("Select mode:", ("Login", "Register"))
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button(mode):
        # Load the JSON data from the file
        with open("users.json", "r") as f:
            users = json.load(f)
        if mode == "Login":
            # Check if the entered username and password match a record in the JSON data
            if username in users and users[username]["password"] == password:
                st.success("Logged in!")
            else:
                st.error("Invalid username or password")
        elif mode == "Register":
            # Add the new user to the JSON data and save it to the file
            users[username] = {"password": password}
            with open("users.json", "w") as f:
                json.dump(users, f)
            st.success("Registered!")
