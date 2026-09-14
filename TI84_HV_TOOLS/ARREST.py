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


report("ARRESTER COORDINATION")
try:
    vll = number("Max system kV LL: ")
    kg = number("Cont LG multiplier: ")
    mcov = number("Selected MCOV kV: ")
    tov = number("System TOV kV LG: ")
    tovcap = number("OEM TOV cap kV: ")
    tovsec = number("TOV duration sec: ")
    bil = number("Equipment BIL kV: ")
    lipl = number("Arrester LIPL kV: ")
    siwl = number("Switch withstand kV: ")
    sspl = number("Arrester SSPL kV: ")
    req_li = number("Required LI margin %: ")
    req_si = number("Required SI margin %: ")
    if min(vll, kg, mcov, tov, tovcap, tovsec) <= 0:
        raise ValueError
    if min(bil, lipl) <= 0 or min(siwl, sspl, req_li, req_si) < 0:
        raise ValueError
    if (siwl == 0) != (sspl == 0):
        raise ValueError
    req = vll * kg
    mcm = 100 * (mcov / req - 1)
    tvm = 100 * (tovcap / tov - 1)
    lim = 100 * (bil / lipl - 1)
    report("Req MCOV =", round(req, 3), "kV")
    report("MCOV margin =", round(mcm, 2), "%")
    report("TOV =", round(tov / mcov, 3), "pu MCOV")
    report("TOV margin =", round(tvm, 2), "%")
    report("At", round(tovsec, 3), "sec")
    report("LI margin =", round(lim, 2), "%")
    if siwl > 0 and sspl > 0:
        sim = 100 * (siwl / sspl - 1)
        report("SI margin =", round(sim, 2), "%")
    else:
        report("SI margin = HOLD")
    if mcm >= 0 and tvm >= 0 and lim >= req_li and (siwl == 0 or sim >= req_si):
        if siwl > 0:
            report("VOLTAGE CHECKS MEET")
        else:
            report("MCOV/TOV/LI MEET")
    else:
        report("VOLTAGE CHECK FAIL")
    if siwl == 0:
        report("SI duty not evaluated")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
