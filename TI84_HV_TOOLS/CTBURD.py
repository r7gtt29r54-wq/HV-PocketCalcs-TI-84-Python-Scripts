print("CT BURDEN/SATURATION")
try:
    ipf = float(input("Primary fault kA: "))
    ipr = float(input("CT tap primary A: "))
    isr = float(input("CT rated sec A: "))
    length = float(input("One-way lead ft: "))
    rohm = float(input("Lead ohm/kft: "))
    rva = float(input("Relay burden VA: "))
    ova = float(input("Other burden VA: "))
    rct = float(input("CT winding ohm: "))
    cvolt = float(input("Effective C class V: "))
    xr = float(input("Primary X/R: "))
    if min(ipf, ipr, isr, cvolt) <= 0:
        raise ValueError
    if min(length, rohm, rva, ova, rct, xr) < 0:
        raise ValueError
    ifsec = ipf * 1000 * isr / ipr
    rlead = 2 * length * rohm / 1000
    zdev = (rva + ova) / (isr * isr)
    zext = rlead + zdev
    vrated = isr * isr * zext
    vterm = ifsec * zext
    vint = ifsec * (zext + rct)
    voff = vint * (1 + xr)
    print("Fault secondary =", round(ifsec, 3), "A")
    print("Lead loop R =", round(rlead, 4), "ohm")
    print("External Z =", round(zext, 4), "ohm")
    print("Rated burden =", round(vrated, 3), "VA")
    print("Sym terminal V =", round(vterm, 2), "V")
    print("Sym internal V =", round(vint, 2), "V")
    print("Class use sym =", round(100 * vterm / cvolt, 1), "%")
    print("Offset req V =", round(voff, 2), "V")
    print("Class use offset =", round(100 * voff / cvolt, 1), "%")
    if voff <= cvolt:
        print("OFFSET SCREEN MEETS")
    else:
        print("EXCITATION CURVE CHECK")
except:
    print("INPUT ERROR")
