# UNICHAT Omnichannel



## Collaborators

Thanks to the amazing contributors who helped build this project:

| ![Gustavo Nomelini](https://github.com/gustavo-nomelini.png?size=50) | ![João Gabriel Custódio](https://github.com/joaomidowz.png?size=50) | ![Lucas Eduardo Santos Ferreira](https://github.com/EduLucas23.png?size=50) |
|:--------------------------------------------------------------------:|:--------------------------------------------------------------:|:--------------------------------------------------------------:|
| [Gustavo Lopes Nomelini](https://github.com/gustavo-nomelini)             | [João Gabriel Custódio](https://github.com/joaomidowz)             | [Lucas Eduardo Santos Ferreira](https://github.com/EduLucas23)             |


## Overview
This project combines a WhatsApp bot with a Streamlit dashboard. The WhatsApp bot uses predefined auto-responses stored in an SQLite database, while the Streamlit dashboard provides a user interface for managing and visualizing these auto-responses.

## Features
- **WhatsApp Integration**: A bot that uses *whatsapp-web.js* to connect to WhatsApp and automatically respond to messages based on triggers.
- **SQLite Database**: Auto-responses are stored and managed using an SQLite database.
- **Streamlit Dashboard**: A web interface for managing auto-responses and visualizing data.
  - The Dashboard can be improved to have a better interface that displays more data and statistics with an enhanced user experience.
  
---

# Installation
## Prerequisites
Ensure you have [Node.js](https://nodejs.org/) and [Python](https://www.python.org/) installed.

### Python Dependencies
Install required Python packages:
```bash
pip install streamlit
pip install imaplib2
pip install email
```

### Optional Python Packages
These are additional packages that could be useful **(they are not implemented yet)** :
```bash
pip install streamlit-modal  # Not implemented
pip install streamlit-extras  # Not yet used but has useful widgets
```

### Node.js Dependencies
Install required Node.js packages:
```bash
npm install express
npm install whatsapp-web.js
npm install qrcode-terminal
npm install qrcode
npm install sqlite3
```

---

## GMAIL App Password
You have to enable IMAP on your gmail configuration and generate an APP Password to use


## WhatsApp Login
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

# Acknowledgments
This project uses the [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) library for integrating WhatsApp functionalities. 

A huge thanks to the developers and contributors of this library for providing an easy-to-use API and making it available for open use. Your work is greatly appreciated!


# Contributing
Feel free to open issues or submit pull requests if you have suggestions or enhancements !

# LICENSE
This project is licensed under the [MIT License](LICENSE).

---

With this README, you should be able to understand the purpose of the project, how to install dependencies, run the application, and interact with the auto-responses. If you have any issues, please consult the documentation for the libraries used or open an issue in the project repository.
