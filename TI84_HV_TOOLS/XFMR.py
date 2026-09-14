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

report("XFMR 10% CAPACITY CHECK")
try:
    mw = number("Plant MWac: ")
    pf = number("Plant PF: ")
    margin = number("Planning margin %: ")
    hv = number("HV kV LL: ")
    mv = number("MV kV LL: ")
    zpct = number("Z% (0=unknown): ")
    units = whole("Installed units: ")
    if min(mw, pf, hv, mv, units) <= 0 or zpct < 0:
        raise ValueError
    if margin < 0 or pf > 1:
        raise ValueError
    total = mw / pf * (1 + margin / 100)
    unitmva = total / units
    ihv = total * 1000 / (sqrt(3) * hv)
    imv_total = total * 1000 / (sqrt(3) * mv)
    imv_unit = imv_total / units
    report("Required total =", round(total, 3), "MVA")
    report("Planning/unit =", round(unitmva, 3), "MVA")
    report("HV bank FLA =", round(ihv, 1), "A")
    report("MV total FLA =", round(imv_total, 1), "A")
    report("MV FLA/unit =", round(imv_unit, 1), "A")
    report("Planning FLA incl margin")
    report("MV total is sum only")
    if zpct > 0:
        report("Z% noted =", zpct)
        report("Fault needs OEM MVA base")
    report("Use ZSIZE for impedance")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
