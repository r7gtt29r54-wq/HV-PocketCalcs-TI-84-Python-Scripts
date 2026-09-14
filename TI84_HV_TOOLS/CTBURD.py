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


report("CT LOOP / EXCITATION")
try:
    ipf = number("Primary fault kA: ")
    ipr = number("CT tap primary A: ")
    isr = number("CT rated sec A: ")
    length = number("One-way lead ft: ")
    rohm = number("Lead ohm/kft: ")
    va = number("Total device VA: ")
    pf = number("Device burden PF: ")
    rct = number("CT winding ohm: ")
    cvolt = number("C class V (0=unknown): ")
    xr = number("Primary X/R: ")
    exc = number("Exc V limit (0=none): ")
    if min(ipf, ipr, isr, pf) <= 0 or pf > 1:
        raise ValueError
    if min(length, rohm, va, rct, cvolt, xr, exc) < 0:
        raise ValueError
    ifsec = ipf * 1000 * isr / ipr
    rlead = 2 * length * rohm / 1000
    zdev = va / (isr * isr)
    rext = rlead + zdev * pf
    xext = zdev * sqrt(1-pf*pf)
    zext = sqrt(rext*rext + xext*xext)
    zint = sqrt((rext+rct)**2 + xext*xext)
    vterm = ifsec * zext
    vint = ifsec * zint
    voff = vint * (1+xr)
    report("Fault secondary A =", round(ifsec, 3))
    report("Lead loop R ohm =", round(rlead, 4))
    report("External R ohm =", round(rext, 4))
    report("External X ohm =", round(xext, 4))
    report("Rated burden VA =", round(isr*isr*zext, 3))
    report("Sym terminal V =", round(vterm, 2))
    report("Sym internal V =", round(vint, 2))
    report("Offset req V =", round(voff, 2))
    if cvolt > 0:
        report("Terminal/C ratio =", round(vterm/cvolt, 4))
        report("C class is not knee V")
    if exc > 0:
        report("Exc limit/req =", round(exc/voff, 4) if voff > 0 else 0)
        if voff <= exc:
            report("ENTERED EXC LIMIT MEETS")
        else:
            report("EXCITATION LIMIT EXCEEDS")
    else:
        report("EXCITATION CURVE HOLD")
    report("No remanence/time model")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR: discard run")
