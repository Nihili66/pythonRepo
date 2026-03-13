from flask import Flask, render_template, request, jsonify
from services.llm_service import generate_ai_response
from database.db import get_db
from services.life_simulation import get_current_situation
from services.emotion_engine import update_emotional_state
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

@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"messages": get_conversation()})


@app.route("/send_message", methods=["POST"])
def send_message():
    state["situation"] = get_current_situation()

    user_message = request.json.get("message")

    interpreted_message = apply_behavior(user_message, state)

    state.update(update_emotional_state(user_message, state))

    save_message("user", user_message)

    conversation = get_conversation()

    simulate_delay(state)

    ai_response = generate_ai_response(conversation, state)

    save_message("assistant", ai_response)

    return jsonify({"response": ai_response})


@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    clear_conversation()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)