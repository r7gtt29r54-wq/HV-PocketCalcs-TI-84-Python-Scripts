from math import sqrt

print("XFMR 10% CAPACITY CHECK")
try:
    mw = float(input("Plant MWac: "))
    pf = float(input("Plant PF: "))
    margin = float(input("Planning margin %: "))
    hv = float(input("HV kV LL: "))
    mv = float(input("MV kV LL: "))
    zpct = float(input("Transformer Z %: "))
    units = int(input("Installed units: "))
    if min(mw, pf, hv, mv, zpct, units) <= 0:
        raise ValueError
    if margin < 0 or pf > 1:
        raise ValueError
    total = mw / pf * (1 + margin / 100)
    unitmva = total / units
    ihv = total * 1000 / (sqrt(3) * hv)
    imv_total = total * 1000 / (sqrt(3) * mv)
    imv_unit = imv_total / units
    isc_unit = imv_unit / (zpct / 100) / 1000
    print("Required total =", round(total, 3), "MVA")
    print("Planning/unit =", round(unitmva, 3), "MVA")
    print("HV bank FLA =", round(ihv, 1), "A")
    print("MV total FLA =", round(imv_total, 1), "A")
    print("MV FLA/unit =", round(imv_unit, 1), "A")
    print("MV fault/unit =", round(isc_unit, 3), "kA")
except:
    print("INPUT ERROR")
