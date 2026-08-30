from math import sqrt, acos, sin

print("EXACT 3PH VOLT DROP")
try:
    mw = float(input("Receiving load MW: "))
    kv = float(input("Receiving kV LL: "))
    pf = float(input("PF 0-1: "))
    mode = int(input("1=LAG 2=LEAD: "))
    length = float(input("One-way length ft: "))
    rbase = float(input("R ohm/kft at base C: "))
    xbase = float(input("X ohm/kft: "))
    tbase = float(input("Base temp C: "))
    top = float(input("Operating temp C: "))
    alpha = float(input("R alpha per C: "))
    n = int(input("Parallel runs/phase: "))
    if min(mw, kv, pf, length, rbase, n) <= 0:
        raise ValueError
    if pf > 1 or xbase < 0 or alpha < 0:
        raise ValueError
    if mode != 1 and mode != 2:
        raise ValueError
    rtemp = rbase * (1 + alpha * (top - tbase))
    if rtemp <= 0:
        raise ValueError
    r = rtemp * length / (1000 * n)
    x = xbase * length / (1000 * n)
    ia = mw * 1000 / (sqrt(3) * kv * pf)
    iq = ia * sin(acos(pf))
    if mode == 1:
        iq = -iq
    ic = complex(ia * pf, iq)
    z = complex(r, x)
    vr = kv * 1000 / sqrt(3)
    vs = complex(vr, 0) + z * ic
    vsll = sqrt(3) * abs(vs)
    drop = vsll - kv * 1000
    loss = 3 * ia * ia * r / 1000
    print("Line current =", round(ia, 2), "A")
    print("R at temp =", round(rtemp, 5), "ohm/kft")
    print("Circuit R =", round(r, 5), "ohm")
    print("Circuit X =", round(x, 5), "ohm")
    print("Sending kV =", round(vsll / 1000, 5))
    print("Exact dV =", round(drop, 2), "V")
    print("Exact dV =", round(100 * drop / (kv * 1000), 4), "%")
    print("Conductor loss =", round(loss, 3), "kW")
except:
    print("INPUT ERROR")
