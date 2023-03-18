import streamlit as st

def signup():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            # Your signup logic here
            st.success("You have successfully signed up!")
        else:
            st.error("Passwords do not match. Please try again.")

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Your login logic here
        st.success("You have successfully logged in!")

option = st.sidebar.selectbox("Select an option", ["Login", "Sign Up"])

if option == "Login":
    login()
else:
    signup()
