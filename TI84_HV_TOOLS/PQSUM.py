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


from math import sqrt


def number(prompt):
    text = input(prompt)
    if text.strip().upper() == "Q":
        raise KeyboardInterrupt
    value = float(text)
    if value != value or abs(value) > 1e12:
        raise ValueError
    return value


report("3PH P-Q SUM")
report("Load P+, generation P-")
report("Inductive Q+, cap Q-")
try:
    kv = number("Bus kV LL: ")
    count = whole("Number of items: ")
    if kv <= 0 or count < 1 or count > 30:
        raise ValueError
    p = 0
    q = 0
    for i in range(count):
        report("Item", i+1)
        p += number("Signed MW: ")
        q += number("Signed Mvar: ")
    s = sqrt(p*p + q*q)
    report("Net MW =", round(p, 4))
    report("Net Mvar =", round(q, 4))
    report("Net MVA =", round(s, 4))
    report("Bus current A =", round(1000*s/(sqrt(3)*kv), 3))
    if s > 0:
        report("PF magnitude =", round(abs(p)/s, 5))
    else:
        report("PF undefined: zero S")
    report("Net exchange only")
    report("Check each branch duty")
except KeyboardInterrupt:
    report("CANCELLED")
except (ValueError, ZeroDivisionError, OverflowError, EOFError):
    report("INPUT ERROR")
