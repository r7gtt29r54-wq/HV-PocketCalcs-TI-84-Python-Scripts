# ZSIZE 2026-09-12: equal two-winding units, infinite HV source.
# Every Z% is on the entered PER-UNIT transformer MVA/kV base.
from math import sqrt, ceil


def number(prompt, low, high):
    value = float(input(prompt))
    if value != value or value < low or value > high:
        raise ValueError
    return value


print("XFMR IMPEDANCE SIZING")
print("Infinite HV source")
print("Equal 2-winding units")
try:
    s = number("Z base MVA/unit: ", 0.000001, 1000000)
    hv = number("HV base kV LL: ", 0.000001, 10000)
    lv = number("LV base kV LL: ", 0.000001, 10000)
    limit = number("Breaker sym kA: ", 0.000001, 1000000)
    c = number("Max voltage pu: ", 1, 2)
    margin = number("Duty headroom %: ", 0, 99.999)
    other = number("Other fault kA: ", 0, 1000000)
    n = number("Units on SAME LV: ", 1, 1000)
    if n != int(n) or hv <= lv:
        raise ValueError
    tol = number("Minus Z tol %: ", 0, 99.999)
    step = number("Z step pct points: ", 0.000001, 100)
    proposed = number("OEM Z% (0=auto): ", 0, 10000)
    target = limit * (1 - margin / 100)
    budget = target - other
    if budget <= 0:
        print("NO XFMR DUTY BUDGET")
        print("Change sources/rating")
    else:
        ib = s / (sqrt(3) * lv)
        ih = s * 1000 / (sqrt(3) * hv)
        baseohm = lv * lv / s
        actual = 100 * c * n * ib / budget
        nominal = actual / (1 - tol / 100)
        candidate = ceil(nominal / step) * step
        selected = proposed if proposed > 0 else candidate
        if selected <= 2.5 and tol < 10:
            print("CHECK LOW-Z TOLERANCE")
        lowz = selected * (1 - tol / 100)
        fault = c * n * ib * 100 / lowz + other
        print("Base MVA/unit =", s)
        print("HV FLA/unit A =", round(ih, 2))
        print("LV FLA/unit A =", round(ib * 1000, 2))
        print("LV Zbase ohm =", round(baseohm, 5))
        print("Target duty kA =", round(target, 4))
        print("XFMR budget kA =", round(budget, 4))
        print("Min actual Z% =", round(actual, 4))
        print("Min nominal Z% =", round(nominal, 4))
        print("Rounded candidate % =", round(candidate, 6))
        print("Checked nominal % =", round(selected, 6))
        print("Lowest actual Z% =", round(lowz, 4))
        print("Worst screen kA =", round(fault, 4))
        print("Target spare kA =", round(target - fault, 4))
        if fault <= target and not (selected <= 2.5 and tol < 10):
            print("ENTERED SCREEN MEETS")
        else:
            print("REVISE CANDIDATE/BASIS")
        print("PROCUREMENT HOLD")
        print("Study + OEM review")
except (ValueError, OverflowError, EOFError):
    print("INPUT ERROR")
