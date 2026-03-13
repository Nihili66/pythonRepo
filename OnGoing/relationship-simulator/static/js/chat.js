window.addEventListener("DOMContentLoaded", () => {
    loadMessages();

    let input = document.getElementById("message-input");

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});

function setLoading(isLoading) {
    let input = document.getElementById("message-input");
    let sendButton = document.getElementById("send-button");
    let clearButton = document.getElementById("clear-button");
    let status = document.getElementById("status");

    input.disabled = isLoading;
    sendButton.disabled = isLoading;
    clearButton.disabled = isLoading;

    status.innerText = isLoading ? "Typing..." : "";
}

function scrollToBottom() {
    let chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function loadMessages() {

    let response = await fetch("/messages");
    let data = await response.json();

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";

    for (let message of data.messages) {
        let role = message.role === "assistant" ? "ai" : message.role;
        addMessage(role, message.content);
    }

    scrollToBottom();
}

async function sendMessage() {

    let input = document.getElementById("message-input");
    let message = input.value.trim();

    if (!message) return;

    addMessage("user", message);
    input.value = "";
    setLoading(true);

    try {
        let response = await fetch("/send_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({message: message})
        });

        let data = await response.json();

        addMessage("ai", data.response);
    } catch (error) {
        addMessage("ai", "Something went wrong. Please try again.");
    } finally {
        setLoading(false);
        input.focus();
    }
}

async function clearChat() {

    let confirmed = window.confirm("Are you sure you want to clear the chat?");
    if (!confirmed) return;

    let response = await fetch("/clear_chat", {
        method: "POST"
    });

    let data = await response.json();

    if (data.success) {
        document.getElementById("chat-box").innerHTML = "";
        scrollToBottom();
    }
}

function addMessage(role, text) {

    let chatBox = document.getElementById("chat-box");

    let messageDiv = document.createElement("div");
    messageDiv.className = role;
    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);
    scrollToBottom();
}