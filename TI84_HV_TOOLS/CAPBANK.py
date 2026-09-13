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


from math import acos, tan, pi, sqrt, ceil

report("CAP BANK DESIGN CHECK")
try:
    mw = number("Load MW: ")
    pf1 = number("Initial PF: ")
    pf2 = number("Target PF: ")
    kv = number("Operating kV LL: ")
    ratedkv = number("Bank rated kV LL: ")
    hz = number("Frequency Hz: ")
    con = whole("1=DELTA 2=WYE: ")
    step = number("Selected step Mvar: ")
    n = whole("Number of steps: ")
    ssc = number("Source SC MVA: ")
    if mw <= 0 or min(kv, ratedkv, hz, step) <= 0 or n <= 0 or ssc < 0:
        raise ValueError
    if pf1 <= 0 or pf1 >= 1 or pf2 <= pf1 or pf2 > 1:
        raise ValueError
    if con != 1 and con != 2:
        raise ValueError
    q1 = mw * tan(acos(pf1))
    q2 = mw * tan(acos(pf2))
    qreq = q1 - q2
    qstep = step * (kv / ratedkv) ** 2
    nreq = int(ceil(qreq / qstep))
    qbank = qstep * n
    qnet = q1 - qbank
    pfact = mw / sqrt(mw * mw + qnet * qnet)
    omega = 2 * pi * hz
    v = ratedkv * 1000
    if con == 1:
        cstep = step * 1e12 / (3 * omega * v * v)
    else:
        cstep = step * 1e12 / (omega * v * v)
    report("Initial Q =", round(q1, 3), "Mvar")
    report("Ideal bank =", round(qreq, 3), "Mvar")
    report("Steps required =", nreq)
    report("Selected bank =", round(qbank, 3), "Mvar")
    report("At operating voltage")
    report("Bank line current A =", round(qbank*1000/(sqrt(3)*kv), 2))
    report("C per phase/step =", round(cstep, 3), "uF")
    report("Actual PF =", round(pfact, 5))
    if qnet >= 0:
        report("Actual PF is LAG")
    else:
        report("Actual PF is LEAD")
    if ssc > 0:
        report("Approx dV =", round(100 * qbank / ssc, 3), "%")
        report("Resonance order =", round(sqrt(ssc / qbank), 3))
    else:
        report("dV/resonance = HOLD")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
