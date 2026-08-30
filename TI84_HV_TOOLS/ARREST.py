print("ARRESTER COORDINATION")
try:
    vll = float(input("Max system kV LL: "))
    kg = float(input("Cont LG multiplier: "))
    mcov = float(input("Selected MCOV kV: "))
    tov = float(input("System TOV kV LG: "))
    tovcap = float(input("OEM TOV cap kV: "))
    tovsec = float(input("TOV duration sec: "))
    bil = float(input("Equipment BIL kV: "))
    lipl = float(input("Arrester LIPL kV: "))
    siwl = float(input("Switch withstand kV: "))
    sspl = float(input("Arrester SSPL kV: "))
    if min(vll, kg, mcov, tov, tovcap, tovsec) <= 0:
        raise ValueError
    if min(bil, lipl) <= 0 or min(siwl, sspl) < 0:
        raise ValueError
    req = vll * kg
    mcm = 100 * (mcov / req - 1)
    tvm = 100 * (tovcap / tov - 1)
    lim = 100 * (bil / lipl - 1)
    print("Req MCOV =", round(req, 3), "kV")
    print("MCOV margin =", round(mcm, 2), "%")
    print("TOV =", round(tov / mcov, 3), "pu MCOV")
    print("TOV margin =", round(tvm, 2), "%")
    print("At", round(tovsec, 3), "sec")
    print("LI margin =", round(lim, 2), "%")
    if siwl > 0 and sspl > 0:
        sim = 100 * (siwl / sspl - 1)
        print("SI margin =", round(sim, 2), "%")
    else:
        print("SI margin = HOLD")
    if mcm >= 0 and tvm >= 0:
        print("VOLTAGE CHECKS MEET")
    else:
        print("VOLTAGE CHECK FAIL")
except:
    print("INPUT ERROR")
