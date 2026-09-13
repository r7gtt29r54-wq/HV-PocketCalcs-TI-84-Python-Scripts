"""Review examples: synthetic values, not project/OEM design data."""
import ast
import builtins
import contextlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'ARREST': [36.5,.57735,24.4,30,32,10,200,80,150,100,20,15],
    'BUSCHK': [230,500,600,2000,40,.25,63,1,2.6,104],
    'CAPBANK': [50,.9,.98,34.5,34.5,60,1,5,3,1000],
    'CTBURD': [40,2000,5,500,.2,3,1,.5,400,20,1000],
    'DCLOAD': [3,50,1,10,58,30,1,1,.2,1.2,1.1,1.3,3,1.1,1.25,1.1,40,1,10,1.1,8,1.1,1],
    'FAULT3': [100,34.5,1,.01,.1,.01,.1,.03,.3,0,0],
    'NGR': [34.5,400,10,60,2],
    'SPHERE': [2,150,60,20,150],
    'VDROP': [50,34.5,.95,1,10000,.1,.08,75,90,.00393,2],
    'XFMR': [300,.95,10,230,34.5,0,2],
    'ZSIZE': [100,138,34.5,12.8,1,0,0,1,7.5,1,0],
    'PUBASE': [100,100,200,50,0,.1],
    'DCDROP': [125,5,1000,1,.5,100],
    'PQSUM': [34.5,2,30,20,20,-5],
    'WENNER': [5,.1,10],
    'UNBAL': [100,100,103,2],
    'BUSAMP': [.0001,1,60,30,0,10,800,34.5],
    'REACTOR': [34.5,25,10,12.8,1.05,60,1000],
}


def execute(name, values):
    supplied = iter(values)
    stream = io.StringIO()
    def ask(prompt):
        value = next(supplied)
        print(prompt + str(value))
        return str(value)
    env = {'__builtins__': dict(vars(builtins), input=ask)}
    path = ROOT / 'TI84_HV_TOOLS' / (name+'.py')
    with contextlib.redirect_stdout(stream):
        exec(compile(path.read_text(encoding='ascii'), str(path), 'exec'), env)
    assert next(supplied, None) is None, name
    assert 'INPUT ERROR' not in stream.getvalue(), stream.getvalue()
    return stream.getvalue()


if __name__ == '__main__':
    print(json.dumps({k:execute(k,v) for k,v in CASES.items()}))
