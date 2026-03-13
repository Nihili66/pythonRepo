window.addEventListener("DOMContentLoaded", async () => {
    let input = document.getElementById("message-input");

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    await loadMessages();
    await loadState();
    clearAnalysis();
});

function setLoading(isLoading) {
    let input = document.getElementById("message-input");
    let sendButton = document.getElementById("send-button");
    let clearButton = document.getElementById("clear-button");
    let saveStateButton = document.getElementById("save-state-button");
    let status = document.getElementById("status");

    input.disabled = isLoading;
    sendButton.disabled = isLoading;
    clearButton.disabled = isLoading;
    saveStateButton.disabled = isLoading;

    status.innerText = isLoading ? "Thinking..." : "";
}

function scrollToBottom() {
    let chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

function formatStateNumber(value) {
    return Number(value).toFixed(3);
}

function formatAnalysisNumber(value) {
    return Number(value ?? 0).toFixed(3);
}

function renderState(state) {
    let stateView = document.getElementById("state-view");

    stateView.innerHTML = `
        <div class="state-item"><strong>Mood:</strong> ${state.mood}</div>
        <div class="state-item"><strong>Overthinking:</strong> ${formatStateNumber(state.overthinking)}</div>
        <div class="state-item"><strong>Attention:</strong> ${formatStateNumber(state.attention)}</div>
        <div class="state-item"><strong>Energy:</strong> ${formatStateNumber(state.energy)}</div>
        <div class="state-item"><strong>Insecurity:</strong> ${formatStateNumber(state.insecurity)}</div>
        <div class="state-item"><strong>Attachment:</strong> ${formatStateNumber(state.attachment)}</div>
        <div class="state-item"><strong>Trust:</strong> ${formatStateNumber(state.trust)}</div>
        <div class="state-item"><strong>Frustration:</strong> ${formatStateNumber(state.frustration)}</div>
        <div class="state-item"><strong>Intimacy:</strong> ${formatStateNumber(state.intimacy)}</div>
        <div class="state-item"><strong>Jealousy:</strong> ${formatStateNumber(state.jealousy)}</div>
        <div class="state-item"><strong>Desire:</strong> ${formatStateNumber(state.desire)}</div>
        <div class="state-item"><strong>Situation:</strong> ${state.situation}</div>
    `;
}

function renderAnalysis(analysis) {
    let analysisView = document.getElementById("analysis-view");

    if (!analysis) {
        clearAnalysis();
        return;
    }

    analysisView.className = "";
    analysisView.innerHTML = `
        <div class="analysis-grid">
            <div class="analysis-item"><strong>Affection:</strong> ${formatAnalysisNumber(analysis.affection)}</div>
            <div class="analysis-item"><strong>Conflict:</strong> ${formatAnalysisNumber(analysis.conflict)}</div>
            <div class="analysis-item"><strong>Reassurance:</strong> ${formatAnalysisNumber(analysis.reassurance)}</div>
            <div class="analysis-item"><strong>Distance:</strong> ${formatAnalysisNumber(analysis.distance)}</div>
            <div class="analysis-item"><strong>Vulnerability:</strong> ${formatAnalysisNumber(analysis.vulnerability)}</div>
            <div class="analysis-item"><strong>Jealousy Trigger:</strong> ${formatAnalysisNumber(analysis.jealousy_trigger)}</div>
            <div class="analysis-item"><strong>Sexual Tension:</strong> ${formatAnalysisNumber(analysis.sexual_tension)}</div>
            <div class="analysis-item"><strong>Attention:</strong> ${formatAnalysisNumber(analysis.attention)}</div>
        </div>
    `;
}

function clearAnalysis() {
    let analysisView = document.getElementById("analysis-view");
    analysisView.className = "analysis-empty";
    analysisView.innerText = "No analysis yet.";
}

function fillStateForm(state) {
    document.getElementById("mood-input").value = state.mood ?? "";
    document.getElementById("overthinking-input").value = state.overthinking ?? 0;
    document.getElementById("attention-input").value = state.attention ?? 0;
    document.getElementById("energy-input").value = state.energy ?? 0;
    document.getElementById("insecurity-input").value = state.insecurity ?? 0;
    document.getElementById("attachment-input").value = state.attachment ?? 0;
    document.getElementById("trust-input").value = state.trust ?? 0;
    document.getElementById("frustration-input").value = state.frustration ?? 0;
    document.getElementById("intimacy-input").value = state.intimacy ?? 0;
    document.getElementById("jealousy-input").value = state.jealousy ?? 0;
    document.getElementById("desire-input").value = state.desire ?? 0;
    document.getElementById("situation-input").value = state.situation ?? "";
}

async function loadState() {
    let response = await fetch("/state");
    let data = await response.json();

    renderState(data.state);
    fillStateForm(data.state);
}

function collectStateFormData() {
    return {
        mood: document.getElementById("mood-input").value,
        overthinking: document.getElementById("overthinking-input").value,
        attention: document.getElementById("attention-input").value,
        energy: document.getElementById("energy-input").value,
        insecurity: document.getElementById("insecurity-input").value,
        attachment: document.getElementById("attachment-input").value,
        trust: document.getElementById("trust-input").value,
        frustration: document.getElementById("frustration-input").value,
        intimacy: document.getElementById("intimacy-input").value,
        jealousy: document.getElementById("jealousy-input").value,
        desire: document.getElementById("desire-input").value,
        situation: document.getElementById("situation-input").value
    };
}

async function saveState() {
    let response = await fetch("/state", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(collectStateFormData())
    });

    let data = await response.json();

    if (data.success) {
        renderState(data.state);
        fillStateForm(data.state);
    }
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

        if (data.state) {
            renderState(data.state);
            fillStateForm(data.state);
        } else {
            await loadState();
        }

        renderAnalysis(data.analysis);
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
        clearAnalysis();

        if (data.state) {
            renderState(data.state);
            fillStateForm(data.state);
        }
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