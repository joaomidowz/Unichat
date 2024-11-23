const express = require("express");
const { Client } = require("whatsapp-web.js");
const sqlite3 = require("sqlite3").verbose();
const app = express();
const port = 3001;

app.use(express.json()); // Middleware to parse JSON request bodies

// Initialize SQLite database
const db = new sqlite3.Database('./auto_responses.db', (err) => {
    if (err) {
        console.error("Error connecting to SQLite database:", err.message);
        return;
    }
    console.log("Connected to SQLite database.");

    // Create auto_responses table if it does not exist
    db.run(`CREATE TABLE IF NOT EXISTS auto_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trigger_message TEXT UNIQUE NOT NULL,
        response_message TEXT NOT NULL
    )`);
});

// Initialize WhatsApp client
const client = new Client();
let qrCode = null;
let isConnected = false;

// Handle QR code generation
client.on("qr", (qr) => {
    qrCode = qr;
    isConnected = false;
    console.log("QR code generated. Scan the QR code to connect.");
});

// Handle successful connection
client.on("ready", () => {
    isConnected = true;
    qrCode = null; // Clear QR code after connection
    console.log("WhatsApp client is connected and ready.");
});

// Listen for incoming messages and handle auto-responses
client.on("message", async (msg) => {
    const incomingMessage = msg.body.toLowerCase();
    console.log("Received message:", incomingMessage);

    // Query the database for a matching trigger message
    db.get("SELECT response_message FROM auto_responses WHERE trigger_message = ?", [incomingMessage], (err, row) => {
        if (err) {
            console.error("Error querying SQLite database:", err.message);
            return;
        }
        if (row) {
            console.log(`Trigger matched: "${incomingMessage}". Sending response: "${row.response_message}"`);
            msg.reply(row.response_message);
        }
    });
});

// Endpoint to get the QR code
app.get("/get-qr", (req, res) => {
    if (!isConnected && qrCode) {
        res.json({ qrCode });
    } else {
        res.json({ qrCode: null });
    }
});

// Endpoint to check WhatsApp connection status
app.get("/check-connection", (req, res) => {
    res.json({ connected: isConnected });
});

// Endpoint to configure an auto-response (stored in SQLite)
app.post("/auto-message", (req, res) => {
    const { triggerMessage, responseMessage } = req.body;

    console.log("Received auto-message request:", { triggerMessage, responseMessage });

    if (!triggerMessage || !responseMessage) {
        console.error("Missing trigger or response message");
        return res.status(400).json({ error: "Trigger and response messages are required" });
    }

    // Insert or replace the auto-response in the database
    db.run("INSERT OR REPLACE INTO auto_responses (trigger_message, response_message) VALUES (?, ?)", [triggerMessage.toLowerCase(), responseMessage], function(err) {
        if (err) {
            console.error("Error inserting auto-response into SQLite:", err.message);
            return res.status(500).json({ error: "Error saving auto-response" });
        }
        console.log("Auto-response configured:", { triggerMessage, responseMessage });
        res.json({ success: true, message: "Auto-reply configured successfully!" });
    });
});

// Endpoint to retrieve all auto-responses
app.get("/get-auto-responses", (req, res) => {
    db.all("SELECT trigger_message, response_message FROM auto_responses", [], (err, rows) => {
        if (err) {
            console.error("Error retrieving auto-responses:", err.message);
            return res.status(500).json({ error: "Error retrieving auto-responses" });
        }
        const autoResponses = {};
        rows.forEach(row => {
            autoResponses[row.trigger_message] = row.response_message;
        });
        console.log("Fetched auto-responses:", autoResponses);
        res.json(autoResponses);
    });
});

// Endpoint to delete an auto-response
app.delete("/delete-auto-response", (req, res) => {
    const { triggerMessage } = req.body;

    if (!triggerMessage) {
        return res.status(400).json({ error: "Trigger message is required to delete an auto-response." });
    }

    db.run("DELETE FROM auto_responses WHERE trigger_message = ?", [triggerMessage.toLowerCase()], function (err) {
        if (err) {
            console.error("Error deleting auto-response from SQLite:", err.message);
            return res.status(500).json({ error: "Error deleting auto-response" });
        }

        if (this.changes > 0) {
            console.log(`Auto-response for trigger "${triggerMessage}" deleted.`);
            res.json({ success: true, message: "Auto-response deleted successfully!" });
        } else {
            res.status(404).json({ error: "Auto-response not found." });
        }
    });
});

// Endpoint to retrieve the latest chats
app.get("/get-chats", async (req, res) => {
    try {
        const chats = await client.getChats();
        const chatData = chats.slice(0, 10).map((chat) => ({
            id: chat.id._serialized,
            name: chat.name || chat.id.user,
            isGroup: chat.isGroup,
            lastMessage: chat.lastMessage ? chat.lastMessage.body : "No messages",
            timestamp: chat.timestamp
                ? new Date(chat.timestamp * 1000).toLocaleString("pt-BR")
                : "N/A",
        }));

        res.json(chatData);
    } catch (error) {
        console.error("Error fetching chats:", error);
        res.status(500).json({ error: "Error fetching chats" });
    }
});

// Endpoint to send a message
app.post("/send-message", async (req, res) => {
    const { chatId, content } = req.body;

    if (!chatId || !content) {
        return res.status(400).json({ error: "ChatId and content are required" });
    }

    try {
        const chat = await client.getChatById(chatId);
        await chat.sendMessage(content);
        res.json({ success: true, message: "Message sent successfully!" });
    } catch (error) {
        console.error("Error sending message:", error);
        res.status(500).json({ error: "Error sending message" });
    }
});

// Endpoint to retrieve the last 10 messages of a specific chat
app.get("/get-messages", async (req, res) => {
    const chatId = req.query.chatId;
    if (!chatId) {
        return res.status(400).json({ error: "chatId is required" });
    }

    try {
        const chat = await client.getChatById(chatId);
        const messages = await chat.fetchMessages({ limit: 10 });
        const formattedMessages = messages.map((message) => ({
            from: message.fromMe ? "You" : message.author || message.from,
            body: message.body,
            timestamp: new Date(message.timestamp * 1000).toLocaleString("pt-BR"),
        }));

        res.json(formattedMessages);
    } catch (error) {
        console.error("Error fetching messages:", error);
        res.status(500).json({ error: "Error fetching messages" });
    }
});

// Start the WhatsApp client and server
client.initialize();

app.listen(port, () => {
    console.log(`WhatsApp API running at http://localhost:${port}`);
});