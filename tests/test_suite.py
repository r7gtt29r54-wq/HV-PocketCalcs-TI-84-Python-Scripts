"""Independent equations, adverse cases and compatibility checks for all modules."""
import ast
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'TI84_HV_TOOLS'


def run(name, data):
    r = subprocess.run([sys.executable, str(TOOLS/(name+'.py'))],
                       input='\n'.join(map(str, data))+'\n', text=True,
                       capture_output=True, timeout=5, check=True)
    assert not r.stderr, r.stderr
    return r.stdout


def val(out, key):
    return float(out.split(key+' = ')[1].split()[0])


# Sequential sections: 10,16,21 Ah from the given synthetic Kt values.
dc = [3,50,1,10,58,30,1,1,.2,1.2,1.1,1.3,3,1.1,1.25,1.1,40,1,10,1.1,8,1.1,1]
out = run('DCLOAD', dc)
assert 'Section 2 Ah = 16.0' in out and 'Section 3 Ah = 21.0' in out
assert val(out, 'Required rated Ah') == 36.3
assert val(out, 'Duty removed Ah') == 12
assert val(out, 'Charger output A') == 12.815
bad = dc[:]; bad[11] = .1  # duration 58 Kt less than duration 1 Kt
assert 'INPUT ERROR' in run('DCLOAD', bad)
assert 'INPUT ERROR' in run('DCLOAD', [1,10,.5])

# Device VA with PF=0.6 at 5 A gives 0.12+j0.16 ohm.
# With .2 ohm leads and .5 winding: |Zext|=.35777, |Zint|=.83546.
out = run('CTBURD', [40,2000,5,500,.2,5,.6,.5,400,20,1000])
assert abs(val(out, 'Sym terminal V') - 100*math.hypot(.32,.16)) < .011
assert abs(val(out, 'Offset req V') - 2100*math.hypot(.82,.16)) < .011
assert 'EXCITATION LIMIT EXCEEDS' in out

# Heat balance: (60+30-10)/.0001 => sqrt(800000) A.
out = run('BUSAMP', [.0001,1,60,30,0,10,800,34.5])
assert abs(val(out, 'Thermal current A') - math.sqrt(800000)) < .001
assert 'SOLAR EXCEEDS COOLING' in run('BUSAMP',[.0001,1,0,0,0,10,0,34.5])

# Reactor checked from resulting physical series impedance.
out = run('REACTOR', [34.5,25,10,12.8,1.05,60,1000])
rr=val(out,'Source R ohm'); xx=val(out,'Source X ohm'); add=val(out,'Min added X ohm')
assert abs(1.05*34.5/(math.sqrt(3)*math.hypot(rr,xx+add))-12.8) < .001
assert val(run('REACTOR',[34.5,10,10,12.8,1,60,1000]),'Min added X ohm') == 0

# Capacitor Q varies with V squared, not linearly.
out=run('CAPBANK',[50,.9,.98,34.5,69,60,1,5,3,1000])
assert val(out,'Selected bank') == 3.75
# Leading PF can give a receiving-to-sending voltage rise (negative drop).
out=run('VDROP',[10,34.5,.8,2,1000,.001,1,20,20,0,1])
assert val(out,'Sending kV') < 34.5

# A transformer planning margin changes planning current, not an unknown Z base.
out=run('XFMR',[300,.95,10,230,34.5,0,2])
assert 'fault/unit' not in out.lower()
assert val(out,'MV FLA/unit') == 2906.6

# Equal Z1=Z2=Z0 and solid fault: SLG equals three-phase; LL is sqrt(3)/2.
out=run('FAULT3',[100,34.5,1,0,.1,0,.1,0,.1,0,0])
lines=out.splitlines()
extract=lambda key: float(next(x.split('=')[1].split()[0] for x in lines if x.startswith(key) and x.endswith('kA')))
assert extract('3PH =') == extract('SLG =')
assert abs(extract('L-L =')/extract('3PH =') - math.sqrt(3)/2) < .00002

# Protection margin can fail even when MCOV/TOV pass.
out=run('ARREST',[36.5,.57735,24.4,30,32,10,200,190,150,100,20,15])
assert 'VOLTAGE CHECK FAIL' in out
assert 'ST scaling needs OEM' in run('BUSCHK',[230,100,100,2000,80,.01,63,1,2,200])

names = {p.stem for p in TOOLS.glob('*.py')}
expected={'ARREST','BUSCHK','CAPBANK','CTBURD','DCLOAD','FAULT3','NGR','SPHERE','VDROP','XFMR','ZSIZE','PUBASE','DCDROP','PQSUM','WENNER','UNBAL','BUSAMP','REACTOR'}
assert names == expected
for name in names:
    p=TOOLS/(name+'.py')
    source=p.read_text(encoding='ascii')
    assert len(name)<=8
    tree=ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node,ast.ImportFrom): assert node.module=='math'
        assert not isinstance(node,(ast.Import,ast.JoinedStr,ast.AsyncFunctionDef))
    for bad in ['nan','inf','-inf','1e200','garbage','']:
        assert 'INPUT ERROR' in run(name,[bad]), (name,bad)
    assert 'CANCELLED' in run(name,['Q']), name
    assert 'CANCELLED' in run(name,['q']), name
print('PASS: 18 modules; independent DC, CT, thermal, reactor and topology tests; 144 input/cancel checks')
