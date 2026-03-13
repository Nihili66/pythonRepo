from datetime import datetime

def get_current_situation():

    hour = datetime.now().hour

    if 0 <= hour < 8:
        return "sleeping"

    if 8 <= hour < 9:
        return "getting ready for work"

    if 9 <= hour < 12:
        return "working at the design studio"

    if 12 <= hour < 13:
        return "having lunch with coworkers"

    if 13 <= hour < 17:
        return "working"

    if 17 <= hour < 19:
        return "commuting or relaxing"

    if 19 <= hour < 22:
        return "at home relaxing"

    return "in bed scrolling on her phone"