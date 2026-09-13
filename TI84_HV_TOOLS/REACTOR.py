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


from math import sqrt, pi


def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


report("SERIES REACTOR CHECK")
report("One radial source path")
try:
    kv = number("Bus base kV LL: ")
    sc = number("Source fault kA at 1pu: ")
    xr = number("Source X/R: ")
    limit = number("Target fault kA: ")
    voltage = number("Max voltage pu: ")
    hz = number("Frequency Hz: ")
    amps = number("Load current A: ")
    if min(kv,sc,limit,voltage,hz) <= 0 or min(xr,amps) < 0:
        raise ValueError
    z = kv/(sqrt(3)*sc)
    r = z/sqrt(1+xr*xr)
    x = r*xr
    req = voltage*kv/(sqrt(3)*limit)
    added = max(0, sqrt(max(0,req*req-r*r))-x)
    actual = voltage*kv/(sqrt(3)*sqrt(r*r+(x+added)**2))
    report("Source R ohm =", round(r, 5))
    report("Source X ohm =", round(x, 5))
    report("Min added X ohm =", round(added, 5))
    report("Inductance mH/ph =", round(1000*added/(2*pi*hz), 5))
    report("Calculated fault kA =", round(actual, 4))
    report("Load reactive Mvar =", round(3*amps*amps*added/1e6, 5))
    report("Load IX volts/ph =", round(amps*added, 3))
    report("No tolerance applied")
    report("OEM/voltage study HOLD")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR: discard run")
