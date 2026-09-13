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


def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


report("DC DUTY / OEM Kt")
report("Sequential total loads")
try:
    count = whole("Periods (1-8): ")
    if count < 1 or count > 8:
        raise ValueError
    amps = []
    mins = []
    removed = 0
    duration = 0
    for i in range(count):
        report("Period", i + 1)
        a = number("Total current A: ")
        t = number("Duration minutes: ")
        if a < 0 or t < 1:
            raise ValueError
        amps.append(a)
        mins.append(t)
        removed += a * t / 60
        duration += t
    mode = whole("OEM Kt? 1=YES 0=NO: ")
    if mode != 0 and mode != 1:
        raise ValueError
    if mode == 1:
        # Enter exact manufacturer Kt at every required elapsed time.
        # Cache equal durations; never invent a discharge curve.
        times = []
        factors = []
        maxcap = 0
        governing = 0
        for end in range(count):
            elapsed = sum(mins[:end + 1])
            section = 0
            prev = 0
            for start in range(end + 1):
                delta = amps[start] - prev
                prev = amps[start]
                if delta != 0:
                    if elapsed in times:
                        k = factors[times.index(elapsed)]
                    else:
                        report("Kt for", elapsed, "min")
                        k = number("OEM Kt (Ah/A): ")
                        if k <= 0:
                            raise ValueError
                        times.append(elapsed)
                        factors.append(k)
                    section += delta * k
                elapsed -= mins[start]
            report("Section", end+1, "Ah =", round(section, 3))
            if section > maxcap:
                maxcap = section
                governing = end + 1
        # A larger-duration Kt cannot be smaller within one cell model.
        for i in range(len(times)):
            for j in range(len(times)):
                if times[i] > times[j] and factors[i] < factors[j]:
                    raise ValueError
        randomcap = number("Random duty size Ah: ")
        temp = number("Temp size multiplier: ")
        age = number("Aging multiplier: ")
        design = number("Battery design mult: ")
        selected = number("Selected Ah (0=none): ")
        if min(randomcap, selected) < 0 or min(temp, age, design) < 1:
            raise ValueError
        rated = (maxcap + randomcap) * temp * age * design
        report("Governing section =", governing)
        report("Raw cell size Ah =", round(maxcap + randomcap, 3))
        report("Required rated Ah =", round(rated, 3))
        if selected > 0:
            report("Selected use % =", round(100*rated/selected, 2))
            if selected >= rated:
                report("ENTERED Kt SIZE MEETS")
            else:
                report("BATTERY SIZE EXCEEDS")
    else:
        report("Battery size HOLD")
    randomah = number("Random removed Ah: ")
    cont = number("Recharge load A: ")
    rech = number("Recharge multiplier: ")
    hours = number("Recharge hours: ")
    designc = number("Charger design mult: ")
    corr = number("Charger altitude mult: ")
    if min(randomah, cont) < 0 or min(rech, designc, corr) < 1 or hours <= 0:
        raise ValueError
    totalah = removed + randomah
    charger = (totalah * rech / hours + cont) * designc * corr
    report("Duty minutes =", round(duration, 3))
    report("Peak duty A =", max(amps))
    report("Duty removed Ah =", round(totalah, 3))
    report("Charger output A =", round(charger, 3))
    report("Verify OEM cell/endpoint")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR: discard run")
