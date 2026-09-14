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


from math import sqrt


def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


report("3PH PER-UNIT BASES")
try:
    oldm = number("Old base MVA: ")
    oldv = number("Old base kV LL: ")
    newm = number("New base MVA: ")
    newv = number("New base kV LL: ")
    r = number("Old R pu: ")
    x = number("Old X pu: ")
    if min(oldm, oldv, newm, newv) <= 0 or r < 0:
        raise ValueError
    factor = (newm / oldm) * (oldv / newv) ** 2
    oldz = oldv ** 2 / oldm
    newz = newv ** 2 / newm
    report("Base scale =", round(factor, 6))
    report("New R pu =", round(r * factor, 6))
    report("New X pu =", round(x * factor, 6))
    report("New Z % =", round(100 * sqrt(r*r + x*x) * factor, 4))
    report("R ohm =", round(r * oldz, 6))
    report("X ohm =", round(x * oldz, 6))
    report("Old Zbase ohm =", round(oldz, 6))
    report("New Zbase ohm =", round(newz, 6))
    report("New Ibase A =", round(newm * 1000 / (sqrt(3)*newv), 3))
    report("SAME physical side")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
