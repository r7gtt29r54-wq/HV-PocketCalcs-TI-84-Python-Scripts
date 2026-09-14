# HV PocketCalcs — TI-84 Evo Python

18 standalone pocket programs for HV design and calculation checks. Verify the worked examples on your calculator before routine use.

[Complete instruction manual](../README.md) · [Calculation models](./CALCULATION_BASIS.md)

| Program | Daily use |
|---|---|
| [ARREST.py](./ARREST.py) | Arrester voltage coordination |
| [BUSCHK.py](./BUSCHK.py) | Bus continuous, short-time and peak duty |
| [CAPBANK.py](./CAPBANK.py) | Capacitor bank selection at operating voltage |
| [CTBURD.py](./CTBURD.py) | CT burden and internal excitation demand |
| [DCLOAD.py](./DCLOAD.py) | Sequential battery duty and charger calculation |
| [FAULT3.py](./FAULT3.py) | Three-phase and sequence fault currents |
| [NGR.py](./NGR.py) | Neutral resistor and capacitive charging duty |
| [SPHERE.py](./SPHERE.py) | Single-mast or equal-support rolling-sphere section |
| [VDROP.py](./VDROP.py) | Receiving-end three-phase voltage-drop phasor |
| [XFMR.py](./XFMR.py) | Concept transformer capacity and winding currents |
| [ZSIZE.py](./ZSIZE.py) | Transformer impedance from a downstream duty limit |
| [PUBASE.py](./PUBASE.py) | Per-unit R/X base conversion |
| [DCDROP.py](./DCDROP.py) | DC control-loop voltage and maximum length |
| [PQSUM.py](./PQSUM.py) | Signed real/reactive power aggregation |
| [WENNER.py](./WENNER.py) | Wenner apparent resistivity |
| [UNBAL.py](./UNBAL.py) | Line-voltage magnitude unbalance |
| [BUSAMP.py](./BUSAMP.py) | Bus conductor heat-balance check |
| [REACTOR.py](./REACTOR.py) | Radial series-reactor impedance sizing |

## Use

1. Review the program's input definitions and worked case in the manual.
2. Transfer the desired `.py` files with TI Connect Evo; documentation and tests remain on the computer.
3. Run in the Python app. Enter `Q` to cancel; restart after an input error. Review wrapped output using shell scrolling.
4. Verify the worked example on the physical calculator before routine use.

Each script is independent. No vendor tables, operating limits, sphere radius, protective margin, OEM battery curve or equipment rating is silently supplied. Numerical matches support review under the stated model; procurement/operating decisions require the applicable study and accountable approval.

## Desktop verification

Run from the repository root:

```sh
python3 -B tests/test_programs.py
python3 -B tests/test_zsize.py
python3 -B tests/test_regressions.py
python3 -B tests/test_suite.py
python3 -B tests/verify_delivery.py
```
