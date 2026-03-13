from flask import Flask, render_template, request, jsonify
from services.llm_service import generate_ai_response
from database.db import get_db
from services.life_simulation import get_current_situation
from services.emotion_engine import update_emotional_state
from services.emotion_engine_llm import update_emotional_state_llm
from services.delay_engine import simulate_delay
from services.behavior_engine import apply_behavior

app = Flask(__name__)

DEFAULT_STATE = {
    "mood": "Neutral",
    "overthinking": 0.6,
    "attention": 0.6,
    "energy": 0.6,
    "insecurity": 0.6,
    "attachment": 0.6,
    "trust": 0.6,
    "frustration": 0.6,
    "intimacy": 0.6,
    "jealousy": 0.6,
    "desire": 0.6,
    "situation": "unknown"
}

state = dict(DEFAULT_STATE)


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
    load_state_from_db()
    return dict(state)


def clamp_stat_value(value):
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None

    return max(0.0, min(1.0, numeric_value))


def load_state_from_db():
    db = get_db()

    row = db.execute(
        """
        SELECT
            mood,
            situation,
            overthinking,
            attention,
            energy,
            insecurity,
            attachment,
            trust,
            frustration,
            intimacy,
            jealousy,
            desire
        FROM relationship_state
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        save_state_to_db(state)
        return dict(state)

    loaded_state = {
        "mood": row["mood"] or DEFAULT_STATE["mood"],
        "situation": row["situation"] or DEFAULT_STATE["situation"],
        "overthinking": float(row["overthinking"] if row["overthinking"] is not None else DEFAULT_STATE["overthinking"]),
        "attention": float(row["attention"] if row["attention"] is not None else DEFAULT_STATE["attention"]),
        "energy": float(row["energy"] if row["energy"] is not None else DEFAULT_STATE["energy"]),
        "insecurity": float(row["insecurity"] if row["insecurity"] is not None else DEFAULT_STATE["insecurity"]),
        "attachment": float(row["attachment"] if row["attachment"] is not None else DEFAULT_STATE["attachment"]),
        "trust": float(row["trust"] if row["trust"] is not None else DEFAULT_STATE["trust"]),
        "frustration": float(row["frustration"] if row["frustration"] is not None else DEFAULT_STATE["frustration"]),
        "intimacy": float(row["intimacy"] if row["intimacy"] is not None else DEFAULT_STATE["intimacy"]),
        "jealousy": float(row["jealousy"] if row["jealousy"] is not None else DEFAULT_STATE["jealousy"]),
        "desire": float(row["desire"] if row["desire"] is not None else DEFAULT_STATE["desire"])
    }

    state.clear()
    state.update(loaded_state)

    return dict(state)


def save_state_to_db(current_state):
    db = get_db()

    db.execute(
        """
        UPDATE relationship_state
        SET mood         = ?,
            situation    = ?,
            overthinking = ?,
            attention    = ?,
            energy       = ?,
            insecurity   = ?,
            attachment   = ?,
            trust        = ?,
            frustration  = ?,
            intimacy     = ?,
            jealousy     = ?,
            desire       = ?,
            last_updated = CURRENT_TIMESTAMP
        WHERE id = 1
        """,
        (
            current_state["mood"],
            current_state.get("situation", "unknown"),
            current_state["overthinking"],
            current_state["attention"],
            current_state["energy"],
            current_state["insecurity"],
            current_state["attachment"],
            current_state["trust"],
            current_state["frustration"],
            current_state["intimacy"],
            current_state["jealousy"],
            current_state["desire"]
        )
    )

    db.commit()


def reset_state():
    state.clear()
    state.update(dict(DEFAULT_STATE))
    save_state_to_db(state)
    return dict(state)


load_state_from_db()


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify({"messages": get_conversation()})


@app.route("/state", methods=["GET"])
def get_state():
    latest_state = load_state_from_db()
    return jsonify({"state": latest_state})


@app.route("/state", methods=["POST"])
def update_state():
    load_state_from_db()

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

    save_state_to_db(state)

    return jsonify({"success": True, "state": get_serializable_state()})


@app.route("/send_message", methods=["POST"])
def send_message():
    load_state_from_db()

    state["situation"] = get_current_situation()

    user_message = request.json.get("message")

    interpreted_message = apply_behavior(user_message, state)

    state.update(update_emotional_state_llm(user_message, state))

    save_state_to_db(state)

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
    reset_state()
    return jsonify({
        "success": True,
        "state": get_serializable_state()
    })


if __name__ == "__main__":
    app.run(debug=True)