import random
import time

DELAY_ENABLED = False

def simulate_delay(state):

    if not DELAY_ENABLED:
        return

    base_delay = random.randint(2, 6)

    # If Emma is working
    if "working" in state["situation"]:
        base_delay += random.randint(5, 15)

    # If she is sleeping
    if "sleeping" in state["situation"]:
        base_delay += random.randint(30, 60)

    # If attachment is high she replies faster
    base_delay -= int(state["attachment"] * 3)

    base_delay = max(1, base_delay)

    time.sleep(base_delay)