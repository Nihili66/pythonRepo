from together import Together
import json
import os

os.environ["TOGETHER_API_KEY"] = "tgp_v1_1KVPaagyT5MOd-q3QD2C6x9NDCIHusHHlv_4sijULbE"

client = Together()


def analyze_message_llm(user_message):

    prompt = f"""
Analyze the emotional tone of the following message in the context of a romantic relationship.

Message:
"{user_message}"

Return ONLY valid JSON with values between 0 and 1.

Fields:
affection
conflict
reassurance
distance
vulnerability
jealousy_trigger
sexual_tension
attention

Example output:
{{
"affection": 0.6,
"conflict": 0.1,
"reassurance": 0.3,
"distance": 0.0,
"vulnerability": 0.2,
"jealousy_trigger": 0.0,
"sexual_tension": 0.1,
"attention": 0.7
}}
"""

    response = client.chat.completions.create(
        model="ServiceNow-AI/Apriel-1.6-15b-Thinker",
        messages=[
            {"role": "system", "content": "You are an emotional signal analyzer."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "affection":0,
            "conflict":0,
            "reassurance":0,
            "distance":0,
            "vulnerability":0,
            "jealousy_trigger":0,
            "sexual_tension":0,
            "attention":0
        }

def clamp(value):
    return max(0, min(1, value))

def update_emotional_state_llm(user_message, state):

    signals = analyze_message_llm(user_message)

    affection = signals["affection"]
    conflict = signals["conflict"]
    reassurance = signals["reassurance"]
    distance = signals["distance"]
    vulnerability = signals["vulnerability"]
    jealousy_trigger = signals["jealousy_trigger"]
    sexual_tension = signals["sexual_tension"]
    attention_signal = signals["attention"]

    # Attachment
    state["attachment"] += affection * 0.3
    state["attachment"] -= distance * 0.2

    # Trust
    state["trust"] += reassurance * 0.4
    state["trust"] -= conflict * 0.2

    # Intimacy
    state["intimacy"] += vulnerability * 0.5
    state["intimacy"] += affection * 0.2

    # Frustration
    state["frustration"] += conflict * 0.5
    state["frustration"] -= reassurance * 0.3

    # Jealousy
    state["jealousy"] += jealousy_trigger * 0.6

    # Desire
    state["desire"] += sexual_tension * 0.5

    # Attention
    state["attention"] += attention_signal * 0.4
    state["attention"] -= distance * 0.3

    # Insecurity
    state["insecurity"] += jealousy_trigger * 0.4
    state["insecurity"] -= reassurance * 0.3

    # Overthinking
    state["overthinking"] += conflict * 0.3
    state["overthinking"] += distance * 0.2

    # Energy
    state["energy"] += affection * 0.2
    state["energy"] -= conflict * 0.2

    # Clamp all numeric states
    for key in state:
        if isinstance(state[key], float):
            state[key] = clamp(state[key])

    # Mood update
    if state["frustration"] > 0.7:
        state["mood"] = "irritated"

    elif state["attachment"] > 0.8 and state["trust"] > 0.6:
        state["mood"] = "affectionate"

    elif state["jealousy"] > 0.7:
        state["mood"] = "jealous"

    elif state["insecurity"] > 0.7:
        state["mood"] = "insecure"

    else:
        state["mood"] = "neutral"

    return state
