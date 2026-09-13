# Local review revision 2026-09-12. Enter Q to cancel any prompt.
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


from math import sqrt, acos, sin

report("EXACT 3PH VOLT DROP")
try:
    mw = number("Receiving load MW: ")
    kv = number("Receiving kV LL: ")
    pf = number("PF 0-1: ")
    mode = whole("1=LAG 2=LEAD: ")
    length = number("One-way length ft: ")
    rbase = number("R ohm/kft at base C: ")
    xbase = number("X ohm/kft: ")
    tbase = number("Base temp C: ")
    top = number("Operating temp C: ")
    alpha = number("Alpha at BASE C: ")
    n = whole("Parallel runs/phase: ")
    if min(mw, kv, pf, length, rbase, n) <= 0:
        raise ValueError
    if pf > 1 or xbase < 0 or alpha < 0:
        raise ValueError
    if mode != 1 and mode != 2:
        raise ValueError
    rtemp = rbase * (1 + alpha * (top - tbase))
    if rtemp <= 0:
        raise ValueError
    r = rtemp * length / (1000 * n)
    x = xbase * length / (1000 * n)
    ia = mw * 1000 / (sqrt(3) * kv * pf)
    iq = ia * sin(acos(pf))
    if mode == 1:
        iq = -iq
    vr = kv * 1000 / sqrt(3)
    vsreal = vr + r * ia * pf - x * iq
    vsimag = x * ia * pf + r * iq
    vsll = sqrt(3) * sqrt(vsreal * vsreal + vsimag * vsimag)
    drop = vsll - kv * 1000
    loss = 3 * ia * ia * r / 1000
    report("Line current =", round(ia, 2), "A")
    report("R at temp =", round(rtemp, 5), "ohm/kft")
    report("Circuit R =", round(r, 5), "ohm")
    report("Circuit X =", round(x, 5), "ohm")
    report("Sending kV =", round(vsll / 1000, 5))
    report("Exact dV =", round(drop, 2), "V")
    report("Exact dV =", round(100 * drop / (kv * 1000), 4), "%")
    report("Conductor loss =", round(loss, 3), "kW")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
