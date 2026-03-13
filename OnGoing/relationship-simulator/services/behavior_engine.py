import random

def apply_behavior(user_message, state):

    msg = user_message

    interpretation = msg

    # Overthinking
    if random.random() < state["overthinking"]:

        if "ok" in msg.lower():
            interpretation = "User might be upset or distant"

    # Insecurity
    if random.random() < state["insecurity"]:

        if "friend" in msg.lower():
            state["jealousy"] += 0.1

    # Low energy
    if state["energy"] < 0.3:
        state["mood"] = "tired"

    # Clamp values
    state["jealousy"] = min(1, state["jealousy"])

    return interpretation