import streamlit as st
import os
import speech_recognition as sr
import pyttsx3
import socket

# Set up the speech recognition engine
r = sr.Recognizer()
engine = sr.TextToSpeech()

# Set up the Pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(1)

# Define the function to handle client connections
def handle_client():
    client_socket, address = server_socket.accept()
    print("Connected by", address)

    # Receive the file from the client
    file_data = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file_data += data

    # Save the file to the local file system
    file_path = "/home/pi/files/" + address[1] + ".txt"
    with open(file_path, "wb") as f:
        f.write(file_data)

    # Speak the file name
    engine.say(address[1] + ".txt")
    engine.runAndWait()

    # Send a message back to the client
    message = "File received and saved."
    client_socket.sendall(message.encode())

    # Close the client connection
    client_socket.close()

# Start the server
print("Server started. Listening for connections...")
while True:
    handle_client()

    # Set up the Streamlit app
    st.title("File Manager")
    st.write("Welcome to the file manager!")

    # Add a text input for the user to enter a file name
    file_name_input = st.text_input("Enter a file name:", "")

    # Add a button to upload the file
    upload_button = st.button("Upload File")

    # Define the function to handle the file upload
    def handle_file_upload():
        file_path = "/home/pi/files/" + file_name_input.value + ".txt"
        with open(file_path, "wb") as f:
            f.write(b"This is a test file.")

        # Speak the file name
        engine.say(file_name_input.value + ".txt")
        engine.runAndWait()

        # Update the file list
        file_list = [f for f in os.listdir("/home/pi/files/") if f.endswith(".txt")]
        st.write("File list:")
        for f in file_list:
            st.write(f)

    # Add a button to play the audio file
    play_button = st.button("Play Audio")

    # Define the function to handle the audio playback
    def handle_play_audio():
        file_path = "/home/pi/files/" + file_name_input.value + ".txt"
        with open(file_path, "rb") as f:
            audio_data = f.read()

        # Play the audio file
        engine.say(audio_data)
        engine.runAndWait()

    # Add a button to delete the file
    delete_button = st.button("Delete File")

    # Define the function to handle the file deletion
    def handle_delete_file():
        file_path = "/home/pi/files/" + file_name_input.value + ".txt"
        os.unlink(file_path)

        # Speak the file name
        engine.say(file_name_input.value + ".txt has been deleted.")
        engine.runAndWait()

        # Update the file list
        file_list = [f for f in os.listdir("/home/pi/files/") if f.endswith(".txt")]
        st.write("File list:")
        for f in file_list:
            st.write(f)

    # Add the buttons to the UI
    st.grid([upload_button, play_button, delete_button])

    # Add a button to exit the app
    exit_button = st.button("Exit")

    # Define the function to handle the exit
    def handle_exit():
        st.write("Goodbye!")
        engine.runAndWait()
        sys.exit()

    # Add the exit button to the UI
    st.grid([exit_button])

    # Run the app
    if __name__ == "__main__":
        st.launch(function_name="app")
