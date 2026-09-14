# Enter Q to cancel any prompt.
def report(*items):
    for item in items:
        if isinstance(item, float) and (item != item or abs(item) == float("inf")):
            raise ValueError
    print(*items)


def whole(prompt):
    value = number(prompt)
    if value != int(value):
        raise ValueError
    return int(value)


# Magnitude deviation metric; not negative/positive sequence ratio.
def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12 or value < 0:
        raise ValueError
    return value


report("LL VOLTAGE UNBALANCE")
try:
    ab = number("Vab RMS: ")
    bc = number("Vbc RMS: ")
    ca = number("Vca RMS: ")
    allowed = number("Allowed deviation %: ")
    avg = (ab+bc+ca)/3
    if avg <= 0:
        raise ValueError
    dev = max(abs(ab-avg), abs(bc-avg), abs(ca-avg))
    pct = 100*dev/avg
    report("Average V =", round(avg, 4))
    report("Max deviation V =", round(dev, 4))
    report("Unbalance % =", round(pct, 4))
    if pct <= allowed:
        report("ENTERED LIMIT MEETS")
    else:
        report("ENTERED LIMIT EXCEEDS")
    report("Not V2/V1 sequence")
    report("Same units for all V")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
