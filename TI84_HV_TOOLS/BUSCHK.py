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


from math import sqrt

report("BUS DUTY CHECK")
try:
    kv = number("Bus kV LL: ")
    norm = number("Normal MVA: ")
    cont = number("Contingency MVA: ")
    rating = number("Continuous rating A: ")
    fault = number("Sym fault kA: ")
    clear = number("Fault duration sec: ")
    stk = number("Bus ST rating kA: ")
    sts = number("ST rating sec: ")
    pkf = number("Peak multiplier: ")
    pkr = number("Peak rating kA: ")
    if min(kv, norm, cont, rating, fault, clear, stk, sts, pkf, pkr) <= 0:
        raise ValueError
    ina = norm * 1000 / (sqrt(3) * kv)
    ica = cont * 1000 / (sqrt(3) * kv)
    capmva = sqrt(3) * kv * rating / 1000
    duty = fault * fault * clear
    capacity = stk * stk * sts
    peak = fault * pkf
    report("Normal I =", round(ina, 1), "A")
    report("Cont I =", round(ica, 1), "A")
    report("Bus cap =", round(capmva, 2), "MVA")
    report("Normal load =", round(100 * ina / rating, 1), "%")
    report("Cont load =", round(100 * ica / rating, 1), "%")
    report("I2t duty =", round(duty, 2), "kA2s")
    report("I2t use =", round(100 * duty / capacity, 1), "%")
    report("Peak duty =", round(peak, 2), "kA")
    report("Peak use =", round(100 * peak / pkr, 1), "%")
    thermal_range = fault <= stk and clear <= sts
    if not thermal_range:
        report("ST scaling needs OEM")
    if max(ina, ica) <= rating and duty <= capacity and peak <= pkr and thermal_range:
        report("ENTERED DUTIES MEET")
    else:
        report("ONE OR MORE EXCEED/HOLD")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
