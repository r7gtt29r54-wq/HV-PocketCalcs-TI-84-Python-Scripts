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


from math import pi


def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


report("WENNER APPARENT RHO")
try:
    a = number("Equal spacing m: ")
    depth = number("Probe depth m: ")
    r = number("Measured R ohm: ")
    if a <= 0 or min(depth, r) < 0:
        raise ValueError
    report("Depth/spacing =", round(depth / a, 4))
    if depth > .1 * a:
        report("DEPTH MODEL REQUIRED")
        report("Shallow formula withheld")
    else:
        report("App rho ohm-m =", round(2 * pi * a * r, 3))
        report("Shallow-probe estimate")
        report("Repeat spacings/axes")
        report("Not grid resistance")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
