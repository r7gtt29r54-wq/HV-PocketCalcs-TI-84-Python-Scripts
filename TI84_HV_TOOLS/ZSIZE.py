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


# Every Z% is on the entered PER-UNIT transformer MVA/kV base.
from math import sqrt, ceil


def number(prompt, low, high):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or value < low or value > high:
        raise ValueError
    return value


report("XFMR IMPEDANCE SIZING")
report("Infinite HV source")
report("Equal 2-winding units")
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
        report("NO XFMR DUTY BUDGET")
        report("Change sources/rating")
    else:
        ib = s / (sqrt(3) * lv)
        ih = s * 1000 / (sqrt(3) * hv)
        baseohm = lv * lv / s
        actual = 100 * c * n * ib / budget
        nominal = actual / (1 - tol / 100)
        candidate = ceil(nominal / step) * step
        # For the standard two-winding tolerance, low-Z uses 10%.
        if candidate <= 2.5 and tol < 10:
            report("Low-Z: using 10% tol")
            tol = 10
            nominal = actual / (1-tol/100)
            candidate = ceil(nominal / step) * step
        selected = proposed if proposed > 0 else candidate
        checktol = tol
        if selected <= 2.5 and checktol < 10:
            report("Low-Z OEM: using 10%")
            checktol = 10
        lowz = selected * (1 - checktol / 100)
        fault = c * n * ib * 100 / lowz + other
        report("Base MVA/unit =", s)
        report("HV FLA/unit A =", round(ih, 2))
        report("LV FLA/unit A =", round(ib * 1000, 2))
        report("LV Zbase ohm =", round(baseohm, 5))
        report("Target duty kA =", round(target, 4))
        report("XFMR budget kA =", round(budget, 4))
        report("Min actual Z% =", round(actual, 4))
        report("Min nominal Z% =", round(nominal, 4))
        report("Rounded candidate % =", round(candidate, 6))
        report("Checked nominal % =", round(selected, 6))
        report("Checked minus tol % =", checktol)
        report("Lowest actual Z% =", round(lowz, 4))
        report("Worst screen kA =", round(fault, 4))
        report("Target spare kA =", round(target - fault, 4))
        if fault <= target:
            report("ENTERED SCREEN MEETS")
        else:
            report("REVISE CANDIDATE/BASIS")
        report("PROCUREMENT HOLD")
        report("Study + OEM review")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, OverflowError, EOFError):
    report("INPUT ERROR")
