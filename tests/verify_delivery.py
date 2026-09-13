"""Check program coverage, worked examples and documentation links."""
import ast
import re
from pathlib import Path
from review_examples import CASES, execute

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT/'TI84_HV_TOOLS'
manual = (TOOLS/'INSTRUCTION_MANUAL.md').read_text()
readme = (TOOLS/'README.md').read_text()
basis = (TOOLS/'CALCULATION_BASIS.md').read_text()
assert set(CASES) == {p.stem for p in TOOLS.glob('*.py')}
for name, values in CASES.items():
    assert ('./'+name+'.py') in readme
    assert '\n## '+name+' ' in manual
    assert execute(name,values) in manual, name+' worked transcript stale'
    source=(TOOLS/(name+'.py')).read_text(encoding='ascii')
    compile(source, name, 'exec')
    assert len(name)<=8 and len(source.encode()) < 16000
    assert 'def report(' in source and 'CANCELLED' in source
    assert 'except:' not in source
    assert not any(s in source for s in ['urllib','requests','subprocess','open('])
for name in CASES:
    assert '\n## '+name+' ' in basis
for doc in TOOLS.glob('*.md'):
    text=doc.read_text()
    for rel in re.findall(r'\]\((\.{1,2}/[^)#]+)(?:#[^)]*)?\)', text):
        assert (doc.parent/rel).exists(), (doc,rel)
print('PASS: 18 manual transcripts, equation/link coverage, ASCII/syntax and standalone files')
