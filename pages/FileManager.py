import os
import streamlit as st
import mimetypes
import files as fm
from PIL import Image

st.write(st.session_state['username'])
# if 'username' not in st.session_state:
#     html = '<meta http-equiv="refresh" content="0; url=/" />'
#     st.write(html, unsafe_allow_html=True)

st.set_page_config(page_title="File Manager", page_icon=":file_folder:")

st.title("File Manager")

# Get the current working directory
cwd = os.getcwd()

# List all files in the current directory
files = os.listdir(cwd)

# Create a sidebar with buttons for navigating directories
with st.sidebar:
    st.header("Navigation")
    if st.button("Home", key="home"):
        os.chdir(cwd)
        files = os.listdir(cwd)
    if st.button("Parent Directory", key="parent"):
        os.chdir("..")
        files = os.listdir(os.getcwd())

# Add a search bar
search_term = st.sidebar.text_input("Search", key="search")

# Add sorting and filtering options
sort_by = st.sidebar.selectbox("Sort by", ["Name", "Date Modified", "Size"], key="sort_by")
if sort_by == "Name":
    files.sort()
elif sort_by == "Date Modified":
    files.sort(key=lambda x: os.path.getmtime(os.path.join(cwd, x)), reverse=True)
elif sort_by == "Size":
    files.sort(key=lambda x: os.path.getsize(os.path.join(cwd, x)), reverse=True)

file_types = st.sidebar.multiselect("Filter by file type", list(set([mimetypes.guess_type(f)[0] for f in files])), key="file_types")

# Filter files by search term and file type
filtered_files = [f for f in files if search_term.lower() in f.lower() and (not file_types or mimetypes.guess_type(f)[0] in file_types)]

# Display the current directory and its contents
col1, col2 = st.columns(2)
with col1:
    st.write(f"Current directory: {cwd}")
with col2:
    st.write(f"{len(filtered_files)} file(s)")

for i, file in enumerate(filtered_files):
    file_path = os.path.join(cwd, file)
    file_type = mimetypes.guess_type(file_path)[0]
    file_size = os.path.getsize(file_path)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if file_type and file_type.startswith("image"):
            img = Image.open(file_path)
            st.image(img, width=50)
        else:
            st.write(":page_facing_up:")

    with col2:
        st.write(file)
        st.write(f"Type: {file_type or 'Unknown'}")
        st.write(f"Size: {file_size / 1024:.2f} KB")

    with col3:
        if st.button("Delete", key=f"delete_{i}"):
            os.remove(file_path)
            st.experimental_rerun()

fm.main()
