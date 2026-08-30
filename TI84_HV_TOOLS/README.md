# TI-84 Evo High-Voltage Engineering Check Suite

Ten standalone Python programs for daily substation design review and field support. The modules calculate load flow quantities, sequence fault current, CT voltage demand, battery duty, conceptual transformer-bank capacity, capacitor-bank behavior, neutral-grounding duty, arrester coordination margins, bus electrical duty, and two-dimensional rolling-sphere geometry.

## Files

| Program | Primary calculation |
|---|---|
| `ARREST.py` | MCOV, TOV, lightning-impulse, and switching-impulse margins |
| `BUSCHK.py` | MVA-to-current, continuous loading, short-time I-squared-t, and peak duty |
| `CAPBANK.py` | PF correction, discrete steps, actual PF, capacitance, voltage-rise and resonance screens |
| `CTBURD.py` | CT secondary current, lead/device burden, symmetrical voltage, and offset voltage demand |
| `DCLOAD.py` | Two-event DC duty, factor-adjusted Ah screen, charger output, and selected-battery use |
| `FAULT3.py` | Three-phase, line-to-ground, and line-to-line sequence fault currents |
| `NGR.py` | Resistor, system charging current, total ground-fault current, MW, and energy |
| `SPHERE.py` | Single-mast and equal-mast rolling-sphere cross sections |
| `VDROP.py` | Temperature-corrected exact phasor voltage drop and conductor loss |
| `XFMR.py` | 10%-design transformer-bank MVA, HV/MV FLA, and isolated-MV-bus fault screen |

See [INSTRUCTION_MANUAL.md](./INSTRUCTION_MANUAL.md) for prompt-by-prompt use and [CALCULATION_BASIS.md](./CALCULATION_BASIS.md) for formulas, sources, edition status, and limitations.

## Transfer and run

1. Connect the calculator and open TI Connect Evo.
2. Choose **SEND FILES**.
3. Select only the ten `.py` files in this folder.
4. On the calculator, open the Python application, select a program, and run it.
5. Record the program revision, every input, the output, project/asset, operating case, and governing source.

The files use only core Python and the `math` module. TI describes TI-Python as a CircuitPython adaptation and lists built-ins plus `math` among its included capabilities. TI also directs users to validate transferred programs on the physical calculator. See the [TI Python programming guide](https://education.ti.com/html/webhelp/EG_TI84PlusCEPY/EN/content/eg_pythonappprog/m_pygetstart/m_84ce_pyobapp.HTML).

## Control boundary

These are transparent independent checks, not sealed calculations, equipment selections, protection settings, construction instructions, switching orders, or energization authority. No conductor table, OEM curve, adopted design margin, sphere radius, CT class, battery factor, or acceptance criterion is embedded. Those values must come from the exact project study, Owner/EOR requirement, utility criterion, approved vendor data, and adopted code/standard.
