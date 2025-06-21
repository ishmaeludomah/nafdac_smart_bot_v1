document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const inputField = document.getElementById("user-input");

    inputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});

function toggleChat() {
    const widget = document.getElementById("chat-widget");
    const toggle = document.getElementById("chat-toggle");
    if (widget.style.display === "flex") {
        widget.style.display = "none";
        toggle.style.display = "block";
    } else {
        widget.style.display = "flex";
        toggle.style.display = "none";
    }
}

function sendMessage() {
    const inputField = document.getElementById("user-input");
    const userMessage = inputField.value.trim();
    if (!userMessage) return;

    appendMessage("You", userMessage, "user-message");
    inputField.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const botReply = data.reply;
        appendMessage("NAFDAC SmartBot", botReply, "bot-message");
    })
    .catch(err => {
        appendMessage("Error", "Sorry, something went wrong.", "bot-message");
        console.error(err);
    });
}

function appendMessage(sender, message, className) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.className = className;
    messageDiv.innerHTML = `<strong>${sender}:</strong><br>${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
