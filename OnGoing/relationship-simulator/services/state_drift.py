import random

def drift_state(state):

    state["mood"] = random.choice([
        "happy",
        "neutral",
        "thoughtful",
        "slightly tired",
        "anxious",
        "stressed",
    ])

    return state