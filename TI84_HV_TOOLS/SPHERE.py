from math import sqrt

print("ROLLING SPHERE 2D")
print("1=SINGLE MAST")
print("2=EQUAL MASTS")
try:
    mode = int(input("Mode: "))
    s = float(input("Sphere radius: "))
    hm = float(input("Mast height: "))
    he = float(input("Equipment height: "))
    if s <= 0 or hm <= 0 or he < 0:
        raise ValueError
    if mode == 1:
        h = min(hm, s)
        if he >= h:
            raise ValueError
        if hm > s:
            print("Single-mast height capped at R")
        x = float(input("Target offset: "))
        if x < 0:
            raise ValueError
        a = sqrt(2 * s * h - h * h)
        b = sqrt(2 * s * he - he * he)
        cover = a - b
        print("Max offset =", round(cover, 4))
        print("Offset margin =", round(cover - x, 4))
        if x < cover:
            print("BELOW 2D ARC")
        else:
            print("TOUCH/OUTSIDE ARC")
    elif mode == 2:
        h = hm
        if he >= h:
            raise ValueError
        d = float(input("Mast spacing: "))
        if d <= 0 or d >= 2 * s:
            raise ValueError
        dh = h - he
        if dh >= 2 * s:
            dmax = 2 * s
        else:
            dmax = 2 * sqrt(2 * s * dh - dh * dh)
        ymid = h + sqrt(s * s - (d / 2) ** 2) - s
        print("Max spacing =", round(dmax, 4))
        print("Arc at midpoint =", round(ymid, 4))
        print("Vertical margin =", round(ymid - he, 4))
        if d < dmax and he < ymid:
            print("BELOW MIDPOINT ARC")
        else:
            print("TOUCH/OUTSIDE ARC")
    else:
        raise ValueError
except:
    print("INPUT ERROR")
