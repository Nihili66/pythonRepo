import sqlite3

DB_NAME = "db.sqlite3"

def insert_state(state):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO relationship_state (
        mood, situation,
        overthinking, attention, energy, insecurity,
        attachment, trust, frustration, intimacy,
        jealousy, desire
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state.get("mood", "Neutral"),
        state.get("situation", "unknown"),
        state.get("overthinking", 0.6),
        state.get("attention", 0.6),
        state.get("energy", 0.6),
        state.get("insecurity", 0.6),
        state.get("attachment", 0.6),
        state.get("trust", 0.6),
        state.get("frustration", 0.6),
        state.get("intimacy", 0.6),
        state.get("jealousy", 0.6),
        state.get("desire", 0.6)
    ))

    conn.commit()
    conn.close()
    print("State inserted successfully.")


if __name__ == "__main__":
    state = {
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
        "desire": 0.6
    }

    insert_state(state)