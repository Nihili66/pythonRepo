from flask import Flask, render_template, request, jsonify
from services.llm_service import generate_ai_response
from database.db import get_db
from services.life_simulation import get_current_situation
from services.emotion_engine import update_emotional_state
from services.emotion_engine_llm import update_emotional_state_llm
from services.delay_engine import simulate_delay
from services.behavior_engine import apply_behavior

app = Flask(__name__)

state = {
    "mood": "affectionate",
    "overthinking": 0.01,
    "attention": 0.999,
    "energy": 0.001,
    "insecurity": 0.999,
    "attachment": 0.999,
    "trust": 0.5,
    "frustration": 0.8,
    "intimacy": 0.999,
    "jealousy": 0.888,
    "desire": 0.999,
    "situation": "unknown"
}


def get_conversation():

    db = get_db()

    rows = db.execute(
        "SELECT role, content FROM messages ORDER BY id ASC"
    ).fetchall()

    conversation = []

    for r in rows:
        conversation.append({
            "role": r["role"],
            "content": r["content"]
        })

    return conversation


def save_message(role, content):

    db = get_db()

    db.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
    )

    db.commit()


def clear_conversation():

    db = get_db()

    db.execute("DELETE FROM messages")
    db.commit()


def get_serializable_state():
    return dict(state)


def clamp_stat_value(value):
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None

    return max(0.0, min(1.0, numeric_value))


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"messages": get_conversation()})


@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({"state": get_serializable_state()})


@app.route("/state", methods=["POST"])
def update_state():
    data = request.json or {}

    numeric_fields = [
        "overthinking",
        "attention",
        "energy",
        "insecurity",
        "attachment",
        "trust",
        "frustration",
        "intimacy",
        "jealousy",
        "desire"
    ]

    if "mood" in data:
        state["mood"] = str(data["mood"]).strip() or state["mood"]

    if "situation" in data:
        state["situation"] = str(data["situation"]).strip() or state["situation"]

    for field in numeric_fields:
        if field in data:
            clamped_value = clamp_stat_value(data[field])
            if clamped_value is not None:
                state[field] = clamped_value

    return jsonify({"success": True, "state": get_serializable_state()})


@app.route("/send_message", methods=["POST"])
def send_message():
    state["situation"] = get_current_situation()

    user_message = request.json.get("message")

    interpreted_message = apply_behavior(user_message, state)

    state.update(update_emotional_state_llm(user_message, state))

    save_message("user", user_message)

    conversation = get_conversation()

    simulate_delay(state)

    ai_response = generate_ai_response(conversation, state)

    save_message("assistant", ai_response)

    return jsonify({
        "response": ai_response,
        "state": get_serializable_state()
    })


@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    clear_conversation()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)