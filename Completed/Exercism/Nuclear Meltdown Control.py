def is_criticality_balanced(temperature, neutrons_emitted):
    if temperature < 800 and neutrons_emitted > 500 and temperature * neutrons_emitted < 500000:
        return True
    else:
        return False


def reactor_efficiency(voltage, current, theoretical_max_power):
    generated_power = voltage * current
    efficiency = (generated_power/theoretical_max_power)
    if efficiency > 0.8:
        return 'green'
    elif 0.8 > efficiency > 0.6:
        return 'orange'
    elif 0.6 > efficiency > 0.3:
        return 'red'
    else:
        return 'black'


def fail_safe(temperature, neutrons_produced_per_second, threshold):
    x = temperature * neutrons_produced_per_second
    if x < 0.9 * threshold:
        return 'LOW'
    elif (1.1 * threshold) < x > (0.9 * threshold):
        return 'NORMAL'
    else:
        return 'DANGER'
