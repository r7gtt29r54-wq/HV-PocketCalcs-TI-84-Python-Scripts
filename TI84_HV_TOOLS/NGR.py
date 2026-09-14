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


# Reviewed input handling: reject NaN, infinity and impractical magnitudes.
def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


from math import sqrt, pi

report("NGR + CHARGING CHECK")
try:
    kv = number("System kV LL: ")
    ir = number("Resistive GF A: ")
    sec = number("Duty time sec: ")
    hz = number("Frequency Hz: ")
    cph = number("Total C/phase uF: ")
    if min(kv, ir, sec, hz) <= 0 or cph < 0:
        raise ValueError
    vlg = kv * 1000 / sqrt(3)
    r = vlg / ir
    ic = 3 * 2 * pi * hz * cph * 1e-6 * vlg
    it = sqrt(ir * ir + ic * ic)
    mw = vlg * ir / 1e6
    report("VLG =", round(vlg, 2), "V")
    report("NGR R =", round(r, 4), "ohm")
    report("Charging I =", round(ic, 3), "A")
    report("Total GF I =", round(it, 3), "A")
    if ic > 0:
        report("IR/IC ratio =", round(ir / ic, 3))
    else:
        report("IR/IC ratio = INF")
    report("Resistor duty =", round(mw, 4), "MW")
    report("Energy =", round(mw * sec, 4), "MJ")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
