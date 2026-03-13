def update_emotional_state(user_message, state):

    msg = user_message.lower()

    if "miss you" in msg or "love you" in msg:
        state["attachment"] += 0.05
        state["intimacy"] += 0.05
        state["mood"] = "happy"

    elif "ok" == msg or "k" == msg:
        state["frustration"] += 0.05
        state["mood"] = "slightly annoyed"

    elif "busy" in msg:
        state["frustration"] += 0.02
        state["mood"] = "slightly annoyed"

    elif "who are you with" in msg:
        state["jealousy"] += 0.05
        state["mood"] = "slightly annoyed"

    # Clamp values
    "for key in state:"
    " if key != ""mood"":"
    "    state[key] = max(0, min(1, state[key]))"

    return state