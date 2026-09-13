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

report("ROLLING SPHERE 2D")
report("1=SINGLE MAST")
report("2=EQUAL MASTS")
try:
    mode = whole("Mode: ")
    s = number("Sphere radius: ")
    hm = number("Mast height: ")
    he = number("Equipment height: ")
    if s <= 0 or hm <= 0 or he < 0:
        raise ValueError
    if mode == 1:
        h = min(hm, s)
        if he >= h:
            raise ValueError
        if hm > s:
            report("Single-mast height capped at R")
        x = number("Target offset: ")
        if x < 0:
            raise ValueError
        a = sqrt(2 * s * h - h * h)
        b = sqrt(2 * s * he - he * he)
        cover = a - b
        report("Max offset =", round(cover, 4))
        report("Offset margin =", round(cover - x, 4))
        if x < cover:
            report("BELOW 2D ARC")
        else:
            report("TOUCH/OUTSIDE ARC")
    elif mode == 2:
        h = hm
        if he >= h:
            raise ValueError
        d = number("Mast spacing: ")
        if d <= 0 or d >= 2 * s:
            raise ValueError
        dh = h - he
        if dh >= s:
            dmax = 2 * s
        else:
            dmax = 2 * sqrt(2 * s * dh - dh * dh)
        ymid = h + sqrt(s * s - (d / 2) ** 2) - s
        report("Max spacing =", round(dmax, 4))
        report("Arc at midpoint =", round(ymid, 4))
        report("Vertical margin =", round(ymid - he, 4))
        if d < dmax and he < ymid:
            report("BELOW MIDPOINT ARC")
        else:
            report("TOUCH/OUTSIDE ARC")
    else:
        raise ValueError
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
