"""Regression cases motivated by independent audit findings."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'TI84_HV_TOOLS'


def run(name, values):
    return subprocess.run([sys.executable, str(ROOT / (name+'.py'))],
                          input='\n'.join(map(str,values))+'\n',
                          text=True, capture_output=True, check=True).stdout


# Normal current can exceed contingency current; both must pass.
out = run('BUSCHK', [230, 1000, 100, 2000, 40, .25, 63, 1, 2.6, 104])
assert 'ONE OR MORE EXCEED' in out
assert 'ENTERED DUTIES MEET' not in out

# Sphere lower midpoint never more than R below equal supports for d<2R.
out = run('SPHERE', [2, 100, 160, 10, 190])
assert 'Max spacing = 200.0' in out
assert 'BELOW MIDPOINT ARC' in out

# Sequential replacement rejects a period shorter than its one-minute model.
out = run('DCLOAD', [1,10,0.5])
assert 'INPUT ERROR' in out

# Reject NaN, including a late input not protected by a leading min().
out = run('BUSCHK', [230, 500, 600, 2000, 'nan', .25, 63, 1, 2.6, 104])
assert 'INPUT ERROR' in out

# 0.1 pu at 100 MVA/100 kV = 10 ohm, or 0.8 pu at 200 MVA/50 kV.
out = run('PUBASE', [100,100,200,50,0,.1])
assert 'New X pu = 0.8' in out and 'X ohm = 10.0' in out
out = run('PUBASE', [200,50,100,100,0,.8])
assert 'New X pu = 0.1' in out

# 1000 ft outgoing+return at 1 ohm/kft plus 0.5 ohm terminals = 2.5 ohm.
out = run('DCDROP', [125,5,1000,1,.5,100])
assert 'Device V = 112.5' in out and 'Max one-way ft = 2250.0' in out
out = run('DCDROP', [125,20,1000,1,.5,100])
assert 'DEVICE VOLTAGE LOW' in out

out = run('WENNER', [5,.1,10])
assert 'App rho ohm-m = 314.159' in out
out = run('WENNER', [1,.2,10])
assert 'DEPTH MODEL REQUIRED' in out and 'App rho' not in out
out = run('PQSUM', [34.5,2,30,20,20,-5])
assert 'Net MVA = 52.2015' in out and 'Bus current A = 873.582' in out
out = run('PQSUM', [34.5,2,30,20,-30,-20])
assert 'PF undefined' in out and 'Bus current A = 0.0' in out
out = run('UNBAL', [100,100,103,2])
assert 'Unbalance % = 1.9802' in out and 'ENTERED LIMIT MEETS' in out
out = run('UNBAL', [100,100,103,1])
assert 'ENTERED LIMIT EXCEEDS' in out

for name in ['PUBASE', 'DCDROP', 'WENNER', 'PQSUM', 'UNBAL']:
    assert 'INPUT ERROR' in run(name,['nan'])
    (ROOT/(name+'.py')).read_text(encoding='ascii')
print('PASS: audit bug cases, per-unit round trip, DC loop voltage and invalid values')
