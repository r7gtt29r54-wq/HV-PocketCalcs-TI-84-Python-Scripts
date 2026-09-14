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


report("BUS HEAT BALANCE")
report("All heat in W/m")
try:
    rdc = number("Hot DC R ohm/m: ")
    skin = number("Rac/Rdc factor: ")
    qc = number("Convection loss W/m: ")
    qr = number("Radiation loss W/m: ")
    qcond = number("Conduction loss W/m: ")
    qs = number("Solar gain W/m: ")
    duty = number("Duty current A: ")
    kv = number("Bus kV LL: ")
    if min(rdc, kv) <= 0 or skin < 1 or min(qc,qr,qcond,qs,duty) < 0:
        raise ValueError
    rac = rdc*skin
    net = qc+qr+qcond-qs
    report("Hot AC R ohm/m =", rac)
    report("Net cooling W/m =", round(net, 4))
    report("Duty Joule W/m =", round(duty*duty*rac, 4))
    if net < 0:
        report("SOLAR EXCEEDS COOLING")
    else:
        amps = sqrt(net/rac)
        report("Thermal current A =", round(amps, 3))
        report("Thermal MVA =", round(sqrt(3)*kv*amps/1000, 3))
        report("Current margin A =", round(amps-duty, 3))
        if duty <= amps:
            report("HEAT BALANCE MEETS")
        else:
            report("HEAT BALANCE EXCEEDS")
    report("Use common temp/weather")
    report("Check joints/apparatus")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR: discard run")
