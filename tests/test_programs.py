import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "TI84_HV_TOOLS"

CASES = {
    "ARREST.py": (
        "36.5\n0.57735\n24.4\n30\n32\n10\n200\n80\n150\n100\n",
        ["Req MCOV = 21.073 kV", "TOV margin = 6.67 %", "VOLTAGE CHECKS MEET"],
    ),
    "BUSCHK.py": (
        "230\n500\n600\n2000\n40\n0.25\n63\n1\n2.6\n104\n",
        ["Cont I = 1506.1 A", "I2t use = 10.1 %", "ENTERED DUTIES MEET"],
    ),
    "CAPBANK.py": (
        "50\n0.9\n0.98\n34.5\n60\n1\n5\n3\n1000\n",
        ["Ideal bank = 14.063 Mvar", "Actual PF = 0.98343", "Resonance order = 8.165"],
    ),
    "CTBURD.py": (
        "40\n2000\n5\n500\n0.2\n2\n1\n0.5\n400\n20\n",
        ["Rated burden = 8.0 VA", "Offset req V = 1722.0 V", "EXCITATION CURVE CHECK"],
    ),
    "DCLOAD.py": (
        "10\n8\n50\n1\n30\n1\n1.1\n1.15\n1.25\n1.1\n1.1\n8\n1\n200\n",
        ["Duty removed = 81.0 Ah", "Charger output = 23.251 A", "AH SCREEN MEETS"],
    ),
    "FAULT3.py": (
        "100\n34.5\n1\n0.01\n0.1\n0.01\n0.1\n0.03\n0.3\n0\n0\n",
        ["3PH = 16.6517 kA", "SLG = 9.991 kA", "L-L = 14.4208 kA"],
    ),
    "NGR.py": (
        "34.5\n400\n10\n60\n2\n",
        ["NGR R = 49.7965 ohm", "Charging I = 45.055 A", "Energy = 79.6743 MJ"],
    ),
    "SPHERE.py": (
        "2\n150\n60\n20\n150\n",
        ["Max spacing = 203.9608", "Vertical margin = 19.9038", "BELOW MIDPOINT ARC"],
    ),
    "VDROP.py": (
        "50\n34.5\n0.95\n1\n10000\n0.1\n0.08\n75\n90\n0.00393\n2\n",
        ["Sending kV = 35.45941", "Exact dV = 2.7809 %", "Conductor loss = 1232.254 kW"],
    ),
    "XFMR.py": (
        "300\n0.95\n10\n230\n34.5\n10\n2\n",
        ["Required total = 347.368 MVA", "HV bank FLA = 872.0 A", "MV fault/unit = 29.066 kA"],
    ),
}


def run(name, data):
    result = subprocess.run(
        [sys.executable, str(ROOT / name)],
        input=data,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


for name, (data, expected) in CASES.items():
    output = run(name, data)
    for token in expected:
        if token not in output:
            raise AssertionError(name + " missing: " + token + "\n" + output)

for path in ROOT.glob("*.py"):
    path.read_text(encoding="ascii")

bad = run("BUSCHK.py", "0\n")
if "INPUT ERROR" not in bad:
    raise AssertionError("BUSCHK invalid-input guard failed")

print("PASS: 10 numeric cases, ASCII checks, and invalid-input guard")
