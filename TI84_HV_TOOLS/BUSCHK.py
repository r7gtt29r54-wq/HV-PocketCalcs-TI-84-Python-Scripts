from math import sqrt

print("BUS DUTY CHECK")
try:
    kv = float(input("Bus kV LL: "))
    norm = float(input("Normal MVA: "))
    cont = float(input("Contingency MVA: "))
    rating = float(input("Continuous rating A: "))
    fault = float(input("Sym fault kA: "))
    clear = float(input("Fault duration sec: "))
    stk = float(input("Bus ST rating kA: "))
    sts = float(input("ST rating sec: "))
    pkf = float(input("Peak multiplier: "))
    pkr = float(input("Peak rating kA: "))
    if min(kv, norm, cont, rating, fault, clear, stk, sts, pkf, pkr) <= 0:
        raise ValueError
    ina = norm * 1000 / (sqrt(3) * kv)
    ica = cont * 1000 / (sqrt(3) * kv)
    capmva = sqrt(3) * kv * rating / 1000
    duty = fault * fault * clear
    capacity = stk * stk * sts
    peak = fault * pkf
    print("Normal I =", round(ina, 1), "A")
    print("Cont I =", round(ica, 1), "A")
    print("Bus cap =", round(capmva, 2), "MVA")
    print("Normal load =", round(100 * ina / rating, 1), "%")
    print("Cont load =", round(100 * ica / rating, 1), "%")
    print("I2t duty =", round(duty, 2), "kA2s")
    print("I2t use =", round(100 * duty / capacity, 1), "%")
    print("Peak duty =", round(peak, 2), "kA")
    print("Peak use =", round(100 * peak / pkr, 1), "%")
    if ica <= rating and duty <= capacity and peak <= pkr:
        print("ENTERED DUTIES MEET")
    else:
        print("ONE OR MORE EXCEED")
except:
    print("INPUT ERROR")
