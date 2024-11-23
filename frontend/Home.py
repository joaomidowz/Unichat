import streamlit as st
import requests
import qrcode
from PIL import Image
import io
import time




st.title('UNICHAT Omnichannel')
st.subheader('First Scan this QRCode with your WhatsApp:')
st.divider()

# Function to fetch the QR code from the Node.js API
def fetch_qr_code():
    try:
        response = requests.get("http://localhost:3001/get-qr")
        response.raise_for_status()
        data = response.json()
        if "qrCode" in data:
            return data["qrCode"]
    except (requests.exceptions.RequestException, ValueError):
        st.error("Error fetching QR code.")
    return None


# Function to check WhatsApp connection status
def is_whatsapp_connected():
    try:
        response = requests.get("http://localhost:3001/check-connection")
        response.raise_for_status()
        data = response.json()
        return data.get("connected", False)
    except requests.exceptions.RequestException:
        st.error("Error checking connection status.")
    return False


# Function to convert a PIL image to bytes
def pil_image_to_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


# Main app logic
qr_placeholder = st.empty()  # Placeholder for displaying QR code
connected = False

while not connected:
    # Check connection status
    connected = is_whatsapp_connected()

    if not connected:
        # Fetch new QR code if not connected
        qr_code_data = fetch_qr_code()
        if qr_code_data:
            img = qrcode.make(qr_code_data)
            img_bytes = pil_image_to_bytes(img)  # Convert PIL image to bytes
            qr_placeholder.image(img_bytes, caption="Scan this QR Code with WhatsApp")
        else:
            qr_placeholder.write("Waiting for QR code...")

        # Wait before fetching a new QR code
        time.sleep(5)
    else:
        qr_placeholder.header("WhatsApp connected successfully!")