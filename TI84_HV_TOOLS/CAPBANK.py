from math import acos, tan, pi, sqrt, ceil

print("CAP BANK DESIGN CHECK")
try:
    mw = float(input("Load MW: "))
    pf1 = float(input("Initial PF: "))
    pf2 = float(input("Target PF: "))
    kv = float(input("Bank kV LL: "))
    hz = float(input("Frequency Hz: "))
    con = int(input("1=DELTA 2=WYE: "))
    step = float(input("Selected step Mvar: "))
    n = int(input("Number of steps: "))
    ssc = float(input("Source SC MVA: "))
    if mw <= 0 or kv <= 0 or hz <= 0 or step <= 0 or n <= 0 or ssc < 0:
        raise ValueError
    if pf1 <= 0 or pf1 >= 1 or pf2 <= pf1 or pf2 > 1:
        raise ValueError
    if con != 1 and con != 2:
        raise ValueError
    q1 = mw * tan(acos(pf1))
    q2 = mw * tan(acos(pf2))
    qreq = q1 - q2
    nreq = int(ceil(qreq / step))
    qbank = step * n
    qnet = q1 - qbank
    pfact = mw / sqrt(mw * mw + qnet * qnet)
    omega = 2 * pi * hz
    v = kv * 1000
    if con == 1:
        cstep = step * 1e12 / (3 * omega * v * v)
    else:
        cstep = step * 1e12 / (omega * v * v)
    print("Initial Q =", round(q1, 3), "Mvar")
    print("Ideal bank =", round(qreq, 3), "Mvar")
    print("Steps required =", nreq)
    print("Selected bank =", round(qbank, 3), "Mvar")
    print("C per phase/step =", round(cstep, 3), "uF")
    print("Actual PF =", round(pfact, 5))
    if qnet >= 0:
        print("Actual PF is LAG")
    else:
        print("Actual PF is LEAD")
    if ssc > 0:
        print("Approx dV =", round(100 * qbank / ssc, 3), "%")
        print("Resonance order =", round(sqrt(ssc / qbank), 3))
    else:
        print("dV/resonance = HOLD")
except:
    print("INPUT ERROR")
