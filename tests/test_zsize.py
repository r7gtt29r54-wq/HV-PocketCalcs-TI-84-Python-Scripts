"""Independent fault-limit reconstruction and adverse-case checks."""
import math
import subprocess
import sys
from pathlib import Path

PROGRAM = Path(__file__).resolve().parents[1] / "TI84_HV_TOOLS/ZSIZE.py"


def run(values):
    return subprocess.run([sys.executable, str(PROGRAM)],
                          input="\n".join(map(str, values)) + "\n",
                          text=True, capture_output=True, check=True).stdout


def result(output, label):
    return float(output.split(label + " = ")[1].splitlines()[0])


base = [100, 138, 34.5, 12.8, 1, 0, 0, 1, 7.5, 1, 0]
out = run(base)
assert abs(result(out, "Min actual Z%") - 13.0741) < 0.0001
assert abs(result(out, "Min nominal Z%") - 14.1341) < 0.0001
assert result(out, "Rounded candidate %") == 15
assert "ENTERED SCREEN MEETS" in out

for c, margin, other, count in [(1, 0, 0, 1), (1.05, 10, 1, 1),
                                (1, 0, 0, 2), (1.1, 15, 2, 3)]:
    data = base[:]
    data[4:8] = [c, margin, other, count]
    out = run(data)
    z = result(out, "Rounded candidate %")
    # Calculate from physical LV ohms and phase voltage, independently
    # of the program's per-unit current formula.
    ohms = (34500 ** 2 / 100000000) * z / 100 * 0.925
    fault = c * 34500 / math.sqrt(3) / ohms * count / 1000 + other
    target = 12.8 * (1 - margin / 100)
    assert fault <= target
    prev_ohms = (34500 ** 2 / 100000000) * (z - 1) / 100 * 0.925
    assert c * 34500 / math.sqrt(3) / prev_ohms * count / 1000 + other > target
    assert "PROCUREMENT HOLD" in out

data = base[:]
data[-1] = 14
assert "REVISE CANDIDATE/BASIS" in run(data)
data = base[:]
data[6] = 12.8
assert "NO XFMR DUTY BUDGET" in run(data)
for index, value in [(0, 0), (1, float('nan')), (2, float('inf')),
                     (3, -1), (4, 0.9), (5, 100), (6, -1),
                     (7, 1.5), (8, 100), (9, 0), (10, -1)]:
    data = base[:]
    data[index] = value
    assert "INPUT ERROR" in run(data), (index, value)
data = base[:]
data[3] = 200
assert "Low-Z: using 10% tol" in run(data)
assert "Checked minus tol % = 10" in run(data)
PROGRAM.read_text(encoding="ascii")
assert len(PROGRAM.stem) <= 8
print("PASS: ZSIZE baseline, physical-ohm checks, topology, tolerance and invalid inputs")
