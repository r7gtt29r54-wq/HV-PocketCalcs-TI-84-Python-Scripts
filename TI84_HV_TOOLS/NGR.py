from math import sqrt, pi

print("NGR + CHARGING CHECK")
try:
    kv = float(input("System kV LL: "))
    ir = float(input("Resistive GF A: "))
    sec = float(input("Duty time sec: "))
    hz = float(input("Frequency Hz: "))
    cph = float(input("Total C/phase uF: "))
    if min(kv, ir, sec, hz) <= 0 or cph < 0:
        raise ValueError
    vlg = kv * 1000 / sqrt(3)
    r = vlg / ir
    ic = 3 * 2 * pi * hz * cph * 1e-6 * vlg
    it = sqrt(ir * ir + ic * ic)
    mw = vlg * ir / 1e6
    print("VLG =", round(vlg, 2), "V")
    print("NGR R =", round(r, 4), "ohm")
    print("Charging I =", round(ic, 3), "A")
    print("Total GF I =", round(it, 3), "A")
    if ic > 0:
        print("IR/IC ratio =", round(ir / ic, 3))
    else:
        print("IR/IC ratio = INF")
    print("Resistor duty =", round(mw, 4), "MW")
    print("Energy =", round(mw * sec, 4), "MJ")
except:
    print("INPUT ERROR")
