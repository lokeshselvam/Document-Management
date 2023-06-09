import json
import streamlit as st
from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

# Define the Streamlit app
def main():
    st.set_page_config(
        page_title="NAS Manager",
        page_icon="📂",
    )
    st.sidebar.success("Select the above page")
    if 'username' not in st.session_state:
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
                    st.session_state['username'] = username
                    nav_page("FileManager")
                else:
                    st.error("Invalid username or password")
            elif mode == "Register":
                # Add the new user to the JSON data and save it to the file
                users[username] = {"password": password}
                with open("users.json", "w") as f:
                    json.dump(users, f)
                st.success("Registered!")
    else:
        html = '<meta http-equiv="refresh" content="0; url=/FileManager" />'
        st.write(html, unsafe_allow_html=True)
if __name__=="__main__":
    main()
