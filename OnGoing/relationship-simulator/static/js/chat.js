async function sendMessage() {

    let input = document.getElementById("message-input");
    let message = input.value;

    if (!message) return;

    addMessage("user", message);

    input.value = "";

    let response = await fetch("/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({message: message})
    });

    let data = await response.json();

    addMessage("ai", data.response);
}

function addMessage(role, text) {

    let chatBox = document.getElementById("chat-box");

    let messageDiv = document.createElement("div");
    messageDiv.className = role;
    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);
}