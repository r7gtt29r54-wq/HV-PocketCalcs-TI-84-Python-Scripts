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


# Constant-current load; individual conductor R at operating temperature.
def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


report("DC CONTROL LOOP DROP")
try:
    vs = number("Min source volts: ")
    amps = number("Duty current A: ")
    length = number("One-way length ft: ")
    r = number("Wire ohm/kft: ")
    extra = number("Other loop ohm: ")
    vmin = number("Device min volts: ")
    if min(vs, vmin) <= 0 or min(amps, length, r, extra) < 0:
        raise ValueError
    loop = 2 * length * r / 1000 + extra
    drop = amps * loop
    loadv = vs - drop
    report("Loop R ohm =", round(loop, 5))
    report("Drop V =", round(drop, 4))
    report("Drop % =", round(100 * drop / vs, 3))
    report("Device V =", round(loadv, 4))
    report("Margin V =", round(loadv-vmin, 4))
    report("Loop loss W =", round(amps*amps*loop, 3))
    if amps > 0 and r > 0:
        budget = (vs-vmin)/amps - extra
        if budget >= 0:
            report("Max one-way ft =", round(500*budget/r, 2))
        else:
            report("NO WIRE DROP BUDGET")
    if loadv >= vmin:
        report("ENTERED DUTY MEETS")
    else:
        report("DEVICE VOLTAGE LOW")
    report("Check OEM coil duty")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
