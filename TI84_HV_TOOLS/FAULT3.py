from math import sqrt

print("SEQUENCE FAULT CHECK")
try:
    base = float(input("System base MVA: "))
    kv = float(input("Fault bus kV LL: "))
    vpu = float(input("Prefault voltage pu: "))
    r1 = float(input("R1 pu: "))
    x1 = float(input("X1 pu: "))
    r2 = float(input("R2 pu: "))
    x2 = float(input("X2 pu: "))
    r0 = float(input("R0 pu: "))
    x0 = float(input("X0 pu: "))
    rf = float(input("Fault R pu: "))
    xf = float(input("Fault X pu: "))
    if min(base, kv, vpu) <= 0:
        raise ValueError
    if min(r1, x1, r2, x2, r0, x0, rf, xf) < 0:
        raise ValueError
    z3 = sqrt((r1 + rf) ** 2 + (x1 + xf) ** 2)
    zlg = sqrt((r1 + r2 + r0 + 3 * rf) ** 2 +
               (x1 + x2 + x0 + 3 * xf) ** 2)
    zll = sqrt((r1 + r2 + rf) ** 2 +
               (x1 + x2 + xf) ** 2)
    if min(z3, zlg, zll) <= 0:
        raise ValueError
    ibase = base / (sqrt(3) * kv)
    i3pu = vpu / z3
    ilgpu = 3 * vpu / zlg
    illpu = sqrt(3) * vpu / zll
    print("I base =", round(ibase, 4), "kA")
    print("3PH =", round(i3pu, 4), "pu")
    print("3PH =", round(i3pu * ibase, 4), "kA")
    print("3PH fault =", round(sqrt(3) * kv * i3pu * ibase, 2), "MVA")
    print("SLG =", round(ilgpu, 4), "pu")
    print("SLG =", round(ilgpu * ibase, 4), "kA")
    print("L-L =", round(illpu, 4), "pu")
    print("L-L =", round(illpu * ibase, 4), "kA")
    if r1 > 0:
        print("Positive X/R =", round(x1 / r1, 3))
    else:
        print("Positive X/R = INF")
except:
    print("INPUT ERROR")
