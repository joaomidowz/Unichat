import streamlit as st
import requests
import time

API_URL = "http://localhost:3001"

# Function to initialize Streamlit session state
def initialize_state():
    if "selected_chat_id" not in st.session_state:
        st.session_state.selected_chat_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "latest_message_id" not in st.session_state:
        st.session_state.latest_message_id = None  # Track the latest message

initialize_state()

st.title("WhatsApp Chats")

# Function to fetch chats from Node.js backend
def fetch_chats():
    try:
        response = requests.get(f"{API_URL}/get-chats")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching chats: {e}")
        return []

# Function to fetch the last 10 messages of a specific chat
def fetch_messages(chat_id):
    try:
        response = requests.get(f"{API_URL}/get-messages", params={"chatId": chat_id})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching messages: {e}")
        return []

# Function to send a message to a specific chat
def send_message(chat_id, content):
    try:
        payload = {"chatId": chat_id, "content": content}
        response = requests.post(f"{API_URL}/send-message", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending message: {e}")
        return None

# Fetch and display chats in Streamlit
chats = fetch_chats()

# Display list of chats with a dropdown to select a chat
chat_names = {chat['name']: chat['id'] for chat in chats}
st.subheader("Select a Chat:")
selected_chat_name = st.selectbox("", options=chat_names.keys(), index=0)
st.divider()

# Update selected chat state
st.session_state.selected_chat_id = chat_names[selected_chat_name]

# Display the last 10 messages of the selected chat and allow sending a message
if st.session_state.selected_chat_id:
    selected_chat_id = st.session_state.selected_chat_id
    st.subheader(f"Chat with {selected_chat_name}")

    # Use `st.empty()` for dynamic message updates
    message_display = st.empty()

    # Place `st.chat_input` outside the loop
    user_message = st.chat_input("Type a message...", key=f"chat_input_{selected_chat_id}")

    if user_message:
        send_result = send_message(selected_chat_id, user_message)
        if send_result and send_result.get("success"):
            # Set flag to fetch new messages after sending
            st.session_state.latest_message_id = None  # Reset latest message ID to force refresh

    # Main loop to refresh messages every 5 seconds
    while True:
        messages = fetch_messages(selected_chat_id)
        if messages:
            # Only update if new messages are detected
            if messages[0]["timestamp"] != st.session_state.latest_message_id:
                st.session_state.messages = messages
                st.session_state.latest_message_id = messages[0]["timestamp"]

                # Clear and display the updated messages
                with message_display.container():
                    for message in st.session_state.messages:
                        if message["from"] == "You":
                            with st.chat_message("assistant"):
                                st.write(message["body"])
                                st.markdown(f"<small>{message['timestamp']}</small>", unsafe_allow_html=True)
                        else:
                            with st.chat_message("user"):
                                st.write(message["body"])
                                st.markdown(f"<small>{message['timestamp']}</small>", unsafe_allow_html=True)

        # Refresh interval
        time.sleep(0.5)  # Wait 1 second before the next refresh
