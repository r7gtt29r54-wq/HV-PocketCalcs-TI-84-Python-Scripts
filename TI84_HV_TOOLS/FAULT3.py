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


from math import sqrt

report("SEQUENCE FAULT CHECK")
try:
    base = number("System base MVA: ")
    kv = number("Fault bus kV LL: ")
    vpu = number("Prefault voltage pu: ")
    r1 = number("R1 pu: ")
    x1 = number("X1 pu: ")
    r2 = number("R2 pu: ")
    x2 = number("X2 pu: ")
    r0 = number("R0 pu: ")
    x0 = number("X0 pu: ")
    rf = number("Fault R pu: ")
    xf = number("Fault X pu: ")
    if min(base, kv, vpu) <= 0:
        raise ValueError
    if min(r1, x1, r2, x2, r0, x0, rf, xf) < 0:
        raise ValueError
    z3 = sqrt((r1 + rf) ** 2 + (x1 + xf) ** 2)
    zlg = sqrt((r1 + r2 + r0 + 3 * rf) ** 2 +
               (x1 + x2 + x0 + 3 * xf) ** 2)
    zll = sqrt((r1 + r2 + rf) ** 2 +
               (x1 + x2 + xf) ** 2)
    if min(z3, zlg, zll) <= 0:
        raise ValueError
    ibase = base / (sqrt(3) * kv)
    i3pu = vpu / z3
    ilgpu = 3 * vpu / zlg
    illpu = sqrt(3) * vpu / zll
    report("I base =", round(ibase, 4), "kA")
    report("3PH =", round(i3pu, 4), "pu")
    report("3PH =", round(i3pu * ibase, 4), "kA")
    report("3PH fault =", round(sqrt(3) * kv * i3pu * ibase, 2), "MVA")
    report("SLG =", round(ilgpu, 4), "pu")
    report("SLG =", round(ilgpu * ibase, 4), "kA")
    report("L-L =", round(illpu, 4), "pu")
    report("L-L =", round(illpu * ibase, 4), "kA")
    if r1 > 0:
        report("Positive X/R =", round(x1 / r1, 3))
    else:
        report("Positive X/R = INF")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
