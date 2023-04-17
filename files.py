import os
import streamlit as st

# Define the Streamlit app
def main():
   
    file_type = st.selectbox("Select file type:", ("All", "Image", "Text", "PDF"))
    files = get_files(file_type)
    file = st.selectbox("Select a file:", files)
    if file:
        download_button(file)

    # File upload section
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a file to upload" )
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)

def get_files(file_type):
    """Get a list of files of the specified type."""
    files = []
    for filename in os.listdir("."):
        if file_type == "All":
            files.append(filename)
        elif file_type == "Image" and filename.endswith((".png", ".jpg", ".jpeg")):
            files.append(filename)
        elif file_type == "Text" and filename.endswith(".txt"):
            files.append(filename)
        elif file_type == "PDF" and filename.endswith(".pdf"):
            files.append(filename)
    return files

def download_button(file):
    """Display a download button for the specified file."""
    with open(file, "rb") as f:
        contents = f.read()
    st.download_button(
        label=f"Download {file}",
        data=contents,
        file_name=file
    )

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the current directory."""
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Saved {uploaded_file.name}")
