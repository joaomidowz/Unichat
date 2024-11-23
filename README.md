# UNICHAT Omnichannel

---

## Overview
This project combines a WhatsApp bot with a Streamlit dashboard. The WhatsApp bot uses predefined auto-responses stored in an SQLite database, while the Streamlit dashboard provides a user interface for managing and visualizing these auto-responses.

## Features
- **WhatsApp Integration**: A bot that uses *whatsapp-web.js* to connect to WhatsApp and automatically respond to messages based on triggers.
- **SQLite Database**: Auto-responses are stored and managed using an SQLite database.
- **Streamlit Dashboard**: A web interface for managing auto-responses and visualizing data.

---

## Installation

### Prerequisites
Ensure you have [Node.js](https://nodejs.org/) and [Python](https://www.python.org/) installed.

### Python Dependencies
Install required Python packages:
```bash
pip install streamlit
pip install imaplib2
pip install email
```

### Optional Python Packages
These are additional packages that could be useful:
```bash
pip install streamlit-modal  # Not implemented
pip install streamlit-extras  # Not yet used but has useful widgets
```

### Node.js Dependencies
Install required Node.js packages:
```bash
npm install express whatsapp-web.js qrcode-terminal
npm install qrcode
npm install sqlite3
```

---

### GMAIL App Password
You have to enable IMAP on your gmail configuration and generate an APP Password to use


### WhatsApp App Password
Configure your Whatsapp and Scan the QRCODE

---

## Running the Project

### Start the Streamlit Application
Run the Streamlit dashboard:
```bash
streamlit run Home.py
```

### Start the WhatsApp Bot
Run the Express server for the WhatsApp bot:
```bash
node server.js
```

## Viewing Auto-Responses
To see configured auto-responses, you can directly query the SQLite database or use the provided API.

### Using SQLite Command Line
```bash
sqlite3 auto_responses.db
SELECT * FROM auto_responses;
.exit
```

### Using Curl Command
Retrieve auto-responses via the API:
```bash
curl http://localhost:3001/get-auto-responses
```

## API Endpoints
- `/get-qr` - Get the QR code for WhatsApp connection.
- `/check-connection` - Check WhatsApp connection status.
- `/auto-message` - Configure a new auto-response.
- `/get-auto-responses` - Retrieve all configured auto-responses.


---

## Authors
- **Gustavo Lopes Nomelini**
- **João Gabriel Custódio**
- **Eduardo Lucas Santos Ferreira**

## Contributing
Feel free to open issues or submit pull requests if you have suggestions or enhancements.

## License
This project is licensed under the [MIT License](LICENSE).

---

With this README, you should be able to understand the purpose of the project, how to install dependencies, run the application, and interact with the auto-responses. If you have any issues, please consult the documentation for the libraries used or open an issue in the project repository.
