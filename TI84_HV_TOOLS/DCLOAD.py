print("DC DUTY/CHARGER CHECK")
try:
    cont = float(input("Continuous load A: "))
    hours = float(input("Autonomy hours: "))
    e1 = float(input("Event 1 total A: "))
    m1 = float(input("Event 1 minutes: "))
    e2 = float(input("Event 2 total A: "))
    m2 = float(input("Event 2 minutes: "))
    rate = float(input("OEM rate factor: "))
    temp = float(input("Temperature factor: "))
    age = float(input("Aging factor: "))
    design = float(input("Design factor: "))
    rech = float(input("Recharge factor: "))
    rehr = float(input("Recharge hours: "))
    chcorr = float(input("Charger corr factor: "))
    selected = float(input("Selected battery Ah: "))
    if min(cont, hours, rate, temp, age, design, rech, rehr, chcorr) <= 0:
        raise ValueError
    if min(e1, m1, e2, m2, selected) < 0:
        raise ValueError
    extra1 = max(0, e1 - cont) * m1 / 60
    extra2 = max(0, e2 - cont) * m2 / 60
    removed = cont * hours + extra1 + extra2
    rated = removed * rate * temp * age * design
    charger = (removed * rech / rehr + cont) * design * chcorr
    print("Continuous Ah =", round(cont * hours, 3))
    print("Event extra Ah =", round(extra1 + extra2, 3))
    print("Duty removed =", round(removed, 3), "Ah")
    print("Factored screen =", round(rated, 3), "Ah")
    print("Charger output =", round(charger, 3), "A")
    if selected > 0:
        print("Selected use =", round(100 * rated / selected, 1), "%")
        if selected >= rated:
            print("AH SCREEN MEETS")
        else:
            print("AH SCREEN EXCEEDS")
    else:
        print("Selection check = HOLD")
except:
    print("INPUT ERROR")
