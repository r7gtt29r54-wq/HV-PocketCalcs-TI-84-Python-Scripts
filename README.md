# HV PocketCalcs — complete instruction manual

18 standalone calculation programs. Calculator-specific operation should be checked using the worked examples.

## Running a program

Transfer the desired `.py` files only, then select and run the program in the calculator Python app. Each is standalone with core Python and `math` only. Enter numeric values with a decimal point, no commas or unit suffixes. Enter `Q` at any prompt to cancel; an invalid value ends the run. On an input/numerical error, discard the entire run including any earlier intermediate section results. Results may wrap; scroll the Python shell to review them. Rerun to change inputs.

Record asset, source revision, units, operating configuration and program revision. `MEETS` refers only to entered criteria under the documented model. Examples are synthetic arithmetic checks, never project/OEM input defaults. Desktop examples and regressions are verified; physical TI-84 Evo execution remains unverified.

## Program index

| Program | Purpose |
|---|---|
| [ARREST.py](./TI84_HV_TOOLS/ARREST.py) | Arrester voltage coordination |
| [BUSCHK.py](./TI84_HV_TOOLS/BUSCHK.py) | Bus continuous, short-time and peak duty |
| [CAPBANK.py](./TI84_HV_TOOLS/CAPBANK.py) | Capacitor bank selection at operating voltage |
| [CTBURD.py](./TI84_HV_TOOLS/CTBURD.py) | CT burden and internal excitation demand |
| [DCLOAD.py](./TI84_HV_TOOLS/DCLOAD.py) | Sequential battery duty and charger calculation |
| [FAULT3.py](./TI84_HV_TOOLS/FAULT3.py) | Three-phase and sequence fault currents |
| [NGR.py](./TI84_HV_TOOLS/NGR.py) | Neutral resistor and capacitive charging duty |
| [SPHERE.py](./TI84_HV_TOOLS/SPHERE.py) | Single-mast or equal-support rolling-sphere section |
| [VDROP.py](./TI84_HV_TOOLS/VDROP.py) | Receiving-end three-phase voltage-drop phasor |
| [XFMR.py](./TI84_HV_TOOLS/XFMR.py) | Concept transformer capacity and winding currents |
| [ZSIZE.py](./TI84_HV_TOOLS/ZSIZE.py) | Transformer impedance from a downstream duty limit |
| [PUBASE.py](./TI84_HV_TOOLS/PUBASE.py) | Per-unit R/X base conversion |
| [DCDROP.py](./TI84_HV_TOOLS/DCDROP.py) | DC control-loop voltage and maximum length |
| [PQSUM.py](./TI84_HV_TOOLS/PQSUM.py) | Signed real/reactive power aggregation |
| [WENNER.py](./TI84_HV_TOOLS/WENNER.py) | Wenner apparent resistivity |
| [UNBAL.py](./TI84_HV_TOOLS/UNBAL.py) | Line-voltage magnitude unbalance |
| [BUSAMP.py](./TI84_HV_TOOLS/BUSAMP.py) | Bus conductor heat-balance check |
| [REACTOR.py](./TI84_HV_TOOLS/REACTOR.py) | Radial series-reactor impedance sizing |

## ARREST — Arrester voltage coordination

**Inputs in order:** Maximum continuous kV LL; continuous LG/VLL ratio; selected MCOV kV RMS; system TOV kV LG RMS; OEM TOV capability kV at the same duration/prior duty; duration seconds; BIL and LIPL kV crest; SI withstand and SSPL kV crest; required LI and SI margins percent.

**Equations:** `Required MCOV = maximum VLL times entered LG multiplier; each margin is 100(capability/duty - 1).`

**Outputs and interpretation:** Uses entered LI/SI criteria in the decision. Enter SI withstand=SSPL=0 to omit SI, which remains unevaluated. One zero and one positive SI value is invalid. Protective levels must represent the relevant waveform and equipment location; no lead/separation, FOW, energy, or curve interpolation is modeled. MCOV and TOV have separate service cases. No universal margin is embedded.


### Worked run

```text
ARRESTER COORDINATION
Max system kV LL: 36.5
Cont LG multiplier: 0.57735
Selected MCOV kV: 24.4
System TOV kV LG: 30
OEM TOV cap kV: 32
TOV duration sec: 10
Equipment BIL kV: 200
Arrester LIPL kV: 80
Switch withstand kV: 150
Arrester SSPL kV: 100
Required LI margin %: 20
Required SI margin %: 15
Req MCOV = 21.073 kV
MCOV margin = 15.79 %
TOV = 1.23 pu MCOV
TOV margin = 6.67 %
At 10.0 sec
LI margin = 150.0 %
SI margin = 50.0 %
VOLTAGE CHECKS MEET
```

## BUSCHK — Bus continuous, short-time and peak duty

**Inputs in order:** Bus kV LL; normal MVA; contingency MVA; continuous A rating; symmetrical kA; clearing seconds; short-time kA rating and its seconds; peak multiplier; peak kA withstand.

**Equations:** `I = 1000 MVA/(sqrt(3) kV); thermal duty = Isym^2 t; peak = entered multiplier times Isym.`

**Outputs and interpretation:** Checks both normal and contingency current. I-squared-t equivalence outside the entered short-time current or time rating is explicitly held even if the product is below the rating. The result does not calculate ampacity, forces, sag or support strength. Use maximum credible clearing time and an applicable peak factor.


### Worked run

```text
BUS DUTY CHECK
Bus kV LL: 230
Normal MVA: 500
Contingency MVA: 600
Continuous rating A: 2000
Sym fault kA: 40
Fault duration sec: 0.25
Bus ST rating kA: 63
ST rating sec: 1
Peak multiplier: 2.6
Peak rating kA: 104
Normal I = 1255.1 A
Cont I = 1506.1 A
Bus cap = 796.74 MVA
Normal load = 62.8 %
Cont load = 75.3 %
I2t duty = 400.0 kA2s
I2t use = 10.1 %
Peak duty = 104.0 kA
Peak use = 100.0 %
ENTERED DUTIES MEET
```

## CAPBANK — Capacitor bank selection at operating voltage

**Inputs in order:** Load MW; initial lagging PF; improved target PF; operating kV LL; bank rated kV LL; frequency Hz; 1=delta or 2=wye; rated Mvar per step; selected steps; source fault MVA (0 omits screens).

**Equations:** `Qneed = P(tan(acos(PF1))-tan(acos(PF2))); Qstep,op = Qstep,rated (Vop/Vrated)^2; Cdelta = Q/(3 omega VLL^2); Cwye = Q/(omega VLL^2).`

**Outputs and interpretation:** Outputs required steps, selected operating Mvar, actual PF direction, line current, and capacitance per phase per step in microfarads. The integer-step ceiling can overshoot into leading PF. dV%=100 Q/Ssc and resonance order=sqrt(Ssc/Q) are first-order screens. Bank temperature, harmonics, reactors, switching/inrush, fuses and unbalance need separate design.


### Worked run

```text
CAP BANK DESIGN CHECK
Load MW: 50
Initial PF: 0.9
Target PF: 0.98
Operating kV LL: 34.5
Bank rated kV LL: 34.5
Frequency Hz: 60
1=DELTA 2=WYE: 1
Selected step Mvar: 5
Number of steps: 3
Source SC MVA: 1000
Initial Q = 24.216 Mvar
Ideal bank = 14.063 Mvar
Steps required = 3
Selected bank = 15.0 Mvar
At operating voltage
Bank line current A = 251.02
C per phase/step = 3.714 uF
Actual PF = 0.98343
Actual PF is LAG
Approx dV = 1.5 %
Resonance order = 8.165
```

## CTBURD — CT burden and internal excitation demand

**Inputs in order:** Primary fault kA; CT primary tap A; rated secondary A; one-way lead ft; hot lead ohm/kft; total connected device VA at rated secondary current; aggregate burden PF (inductive); winding ohm on the tap; effective terminal C-class V (0 unknown); primary X/R; permitted INTERNAL exciting V from curve/OEM criterion (0 unknown).

**Equations:** `Ifsec = Ifprimary Israted/Itap; Zdev = VA/Israted^2; Rext = 2 L r/1000 + Zdev PF; Xext = Zdev sqrt(1-PF^2); Vterminal=Ifsec |Zext|; Vinternal=Ifsec |Zext+RCT|; Voffset=(1+X/R) Vinternal.`

**Outputs and interpretation:** The VA and PF must represent the combined devices at the relevant frequency/current, not an arbitrary sum of incompatible burdens. The terminal/C ratio is informational, not a saturation certification. Enter excitation voltage at a defined allowable exciting-current/flux criterion, not a C-class label relabeled as knee voltage. No remanence or time-to-saturation, CT error, relay algorithm or waveform model. Use the applicable CT requirements and OEM data before application.


### Worked run

```text
CT LOOP / EXCITATION
Primary fault kA: 40
CT tap primary A: 2000
CT rated sec A: 5
One-way lead ft: 500
Lead ohm/kft: 0.2
Total device VA: 3
Device burden PF: 1
CT winding ohm: 0.5
C class V (0=unknown): 400
Primary X/R: 20
Exc V limit (0=none): 1000
Fault secondary A = 100.0
Lead loop R ohm = 0.2
External R ohm = 0.32
External X ohm = 0.0
Rated burden VA = 8.0
Sym terminal V = 32.0
Sym internal V = 82.0
Offset req V = 1722.0
Terminal/C ratio = 0.08
C class is not knee V
Exc limit/req = 0.5807
EXCITATION LIMIT EXCEEDS
No remanence/time model
```

## DCLOAD — Sequential battery duty and charger calculation

**Inputs in order:** Period count 1-8; for each period TOTAL current A and duration minutes (at least 1). OEM Kt available: 1 yes, 0 no. If yes: enter prompted Kt in Ah/A at each displayed cumulative duration, then separately calculated random-duty size Ah, temperature multiplier, aging multiplier, battery design multiplier and selected rated Ah (0 none). Finally enter random Ah actually removed, load supported during recharge A, recharge multiplier, hours, charger design multiplier and altitude multiplier.

**Equations:** `Aremoved = sum(Ai ti/60). For each endpoint s, Fs=sum((Ap-Ap-1) Kt), with A0=0 and t measured from start of period p to end of section s. Required rated Ah=(max Fs+random-duty size Ah) temperature aging design. Charger=[Aremoved recharge/recharge-hours+continuous recharge load] charger-design altitude.`

**Outputs and interpretation:** Use one exact cell family, temperature basis, endpoint V/cell and capacity rating definition. Kt is rated Ah divided by discharge A at the displayed duration; it is not ampere/plate Rt and is not elapsed hours. The program caches repeated durations and rejects Kt decreasing with increasing time. Negative load changes are retained. All section endpoints are evaluated. Synthetic factors in the example are test data, not OEM curves. Random size and random Ah removed are distinct quantities; enter 0 only if absent. No-Kt mode still calculates charge removed/charger but holds battery size. Fixed sequential total loads must already combine simultaneous loads; calculate the separate random-duty capacity for the applicable duty cycle. Subminute transients, random combinations, cell count/voltage window, initial capacity, coup de fouet and selected-size curve validity require review. Multipliers below 1 are excluded to avoid assumed capacity credit. Discard earlier section prints if later inputs produce an error.


### Worked run

```text
DC DUTY / OEM Kt
Sequential total loads
Periods (1-8): 3
Period 1
Total current A: 50
Duration minutes: 1
Period 2
Total current A: 10
Duration minutes: 58
Period 3
Total current A: 30
Duration minutes: 1
OEM Kt? 1=YES 0=NO: 1
Kt for 1.0 min
OEM Kt (Ah/A): 0.2
Section 1 Ah = 10.0
Kt for 59.0 min
OEM Kt (Ah/A): 1.2
Kt for 58.0 min
OEM Kt (Ah/A): 1.1
Section 2 Ah = 16.0
Kt for 60.0 min
OEM Kt (Ah/A): 1.3
Section 3 Ah = 21.0
Random duty size Ah: 3
Temp size multiplier: 1.1
Aging multiplier: 1.25
Battery design mult: 1.1
Selected Ah (0=none): 40
Governing section = 3
Raw cell size Ah = 24.0
Required rated Ah = 36.3
Selected use % = 90.75
ENTERED Kt SIZE MEETS
Random removed Ah: 1
Recharge load A: 10
Recharge multiplier: 1.1
Recharge hours: 8
Charger design mult: 1.1
Charger altitude mult: 1
Duty minutes = 60.0
Peak duty A = 50.0
Duty removed Ah = 12.0
Charger output A = 12.815
Verify OEM cell/endpoint
```

## FAULT3 — Three-phase and sequence fault currents

**Inputs in order:** System base MVA; fault-bus base kV LL; prefault voltage pu; R1/X1, R2/X2, R0/X0 in pu; fault R/X in pu.

**Equations:** `I3pu=c/|Z1+Zf|; ILGpu=3c/|Z1+Z2+Z0+3Zf|; ILLpu=sqrt(3)c/|Z1+Z2+Zf|; Ibase,kA=MVA/(sqrt(3) kV).`

**Outputs and interpretation:** All impedances must be on the same base and represent the actual winding/grounding topology. One entered Zf is interpreted per phase for 3PH, phase-to-ground for SLG, and between the two faulted phases for LL; use separate runs if physical fault impedances differ. Passive nonnegative R/X model only; zero denominators rejected. Outputs are RMS symmetrical magnitudes, not breaker asymmetrical/peak duty, decrement, or inverter behavior.


### Worked run

```text
SEQUENCE FAULT CHECK
System base MVA: 100
Fault bus kV LL: 34.5
Prefault voltage pu: 1
R1 pu: 0.01
X1 pu: 0.1
R2 pu: 0.01
X2 pu: 0.1
R0 pu: 0.03
X0 pu: 0.3
Fault R pu: 0
Fault X pu: 0
I base = 1.6735 kA
3PH = 9.9504 pu
3PH = 16.6517 kA
3PH fault = 995.04 MVA
SLG = 5.9702 pu
SLG = 9.991 kA
L-L = 8.6173 pu
L-L = 14.4208 kA
Positive X/R = 10.0
```

## NGR — Neutral resistor and capacitive charging duty

**Inputs in order:** System kV LL; desired resistive ground-fault A; duty seconds; frequency Hz; total capacitance to ground PER PHASE in microfarads for the connected island.

**Equations:** `VLG=1000 kVLL/sqrt(3); R=VLG/IR; IC=3 omega Cphase VLG; Itotal=sqrt(IR^2+IC^2); P=VLG IR; E=P seconds.`

**Outputs and interpretation:** R is the directly connected neutral resistor, not three times that value; 3R belongs in a sequence network. Assumes full neutral displacement, balanced phase capacitances, negligible source impedances and one resistive grounding source. Power/energy use constant resistance and voltage; no temperature-rise, endurance or grounding-transformer rating is established. Transformer-referred resistors need ratio conversion. IR/IC is reported without a universal acceptance threshold.


### Worked run

```text
NGR + CHARGING CHECK
System kV LL: 34.5
Resistive GF A: 400
Duty time sec: 10
Frequency Hz: 60
Total C/phase uF: 2
VLG = 19918.58 V
NGR R = 49.7965 ohm
Charging I = 45.055 A
Total GF I = 402.529 A
IR/IC ratio = 8.878
Resistor duty = 7.9674 MW
Energy = 79.6743 MJ
```

## SPHERE — Single-mast or equal-support rolling-sphere section

**Inputs in order:** Mode 1 single or 2 equal supports; sphere radius; mast/support height; equipment height; then target offset (mode 1) or support spacing (mode 2), all in the SAME length units.

**Equations:** `Single: offset=sqrt(2Rh-h^2)-sqrt(2Rhe-he^2), h=min(hmast,R). Equal supports: ymid=hmast+sqrt(R^2-(d/2)^2)-R; dmax=2sqrt(2Rdh-dh^2) for dh<R, otherwise 2R.`

**Outputs and interpretation:** Equality is touching/outside, never below. Mode 2 requires d<2R and he<hmast. Midpoint geometry does not establish 3-D protection between isolated mast pairs or side-stroke coverage. Geometry is derived; radius/attraction model must come from adopted study. Heights above R are capped only in mode 1. No protection-angle default, probabilistic risk rate or current-standard radius selection is embedded.


### Worked run

```text
ROLLING SPHERE 2D
1=SINGLE MAST
2=EQUAL MASTS
Mode: 2
Sphere radius: 150
Mast height: 60
Equipment height: 20
Mast spacing: 150
Max spacing = 203.9608
Arc at midpoint = 39.9038
Vertical margin = 19.9038
BELOW MIDPOINT ARC
```

## VDROP — Receiving-end three-phase voltage-drop phasor

**Inputs in order:** Receiving MW; receiving kV LL; PF magnitude; 1 lag or 2 lead; one-way ft; R ohm/kft at base temperature; X ohm/kft; base C; operating C; alpha per C referenced to that BASE temperature; equal parallel runs per phase.

**Equations:** `Rhot=Rbase[1+alpha_base(Top-Tbase)]; R,X = per-kft values times length/(1000 n); I = 1000 MW/(sqrt(3) kV PF); Vs=Vr+(R+jX)I; loss=3 I^2 R.`

**Outputs and interpretation:** Uses explicit real/imaginary arithmetic. Alpha20 cannot be used directly with a 75 C base resistance: convert alpha_base=alpha20/[1+alpha20(Tbase-20)] or use independently corrected R and alpha=0. The example explicitly treats 0.00393 as a supplied coefficient at its entered base, not as a material table. Equal parallel impedance/current division excludes mutual/sheath effects. R should represent relevant AC resistance. Negative signed voltage change can occur for leading loads. Excludes charging, taps, unbalance and distributed line effects.


### Worked run

```text
EXACT 3PH VOLT DROP
Receiving load MW: 50
Receiving kV LL: 34.5
PF 0-1: 0.95
1=LAG 2=LEAD: 1
One-way length ft: 10000
R ohm/kft at base C: 0.1
X ohm/kft: 0.08
Base temp C: 75
Operating temp C: 90
Alpha at BASE C: 0.00393
Parallel runs/phase: 2
Line current = 880.78 A
R at temp = 0.1059 ohm/kft
Circuit R = 0.52948 ohm
Circuit X = 0.4 ohm
Sending kV = 35.45941
Exact dV = 959.41 V
Exact dV = 2.7809 %
Conductor loss = 1232.254 kW
```

## XFMR — Concept transformer capacity and winding currents

**Inputs in order:** Plant MWac; PF; planning margin percent; HV kV LL; MV kV LL; optional Z% (0 unknown); installed units.

**Equations:** `Total planning MVA=MWac/PF (1+margin/100); per-unit allocation=total/N; planning FLA=1000 MVA/(sqrt(3) kV).`

**Outputs and interpretation:** Outputs total and per-unit planning MVA, HV bank FLA, aggregate MV FLA and per-unit MV FLA. Equal allocation and common voltage bases assumed. Normally split MV buses use per-unit current; the sum is not a common-bus duty. Z is recorded only: planning MVA is not the OEM impedance base. This module does not calculate fault duty, cooling-stage capability, N-1, losses or reactive export at the POI. It preserves the user's requested 10%-design scope.


### Worked run

```text
XFMR 10% CAPACITY CHECK
Plant MWac: 300
Plant PF: 0.95
Planning margin %: 10
HV kV LL: 230
MV kV LL: 34.5
Z% (0=unknown): 0
Installed units: 2
Required total = 347.368 MVA
Planning/unit = 173.684 MVA
HV bank FLA = 872.0 A
MV total FLA = 5813.1 A
MV FLA/unit = 2906.6 A
Planning FLA incl margin
MV total is sum only
Use ZSIZE for impedance
```

## ZSIZE — Transformer impedance from a downstream duty limit

**Inputs in order:** Per-transformer Z-base MVA; HV/LV base kV LL; permissible symmetrical breaker kA; maximum voltage pu (1-2); duty headroom percent; other contributing kA through the studied breaker; equal units on SAME LV bus; negative relative tolerance percent; rounding increment in percentage points; OEM nominal Z% (0 checks generated candidate).

**Equations:** `Ibase,kA=Sunit/(sqrt(3) kVLV); target=limit(1-headroom/100); budget=target-other; Zactual%=100 c N Ibase/budget; Znom%=Zactual/(1-tolerance/100); candidate=ceil(Znom/step) step.`

**Outputs and interpretation:** Infinite HV source; no finite-source credit. Split LV buses use N=1 despite a common HV bus. All Z values use the entered unit base and tap. Low-Z candidates at/below 2.5% use at least 10% tolerance; if this forces a higher candidate, the 10% treatment is retained conservatively. A low-Z OEM proposal receives its own minimum 10% check. Other contributions are a conservative magnitude sum. No budget means no candidate. Rounding is upward but reporting precision does not create an OEM guarantee. No upper-Z/voltage-performance limit, full breaker duty or procurement release is established.


### Worked run

```text
XFMR IMPEDANCE SIZING
Infinite HV source
Equal 2-winding units
Z base MVA/unit: 100
HV base kV LL: 138
LV base kV LL: 34.5
Breaker sym kA: 12.8
Max voltage pu: 1
Duty headroom %: 0
Other fault kA: 0
Units on SAME LV: 1
Minus Z tol %: 7.5
Z step pct points: 1
OEM Z% (0=auto): 0
Base MVA/unit = 100.0
HV FLA/unit A = 418.37
LV FLA/unit A = 1673.48
LV Zbase ohm = 11.9025
Target duty kA = 12.8
XFMR budget kA = 12.8
Min actual Z% = 13.0741
Min nominal Z% = 14.1341
Rounded candidate % = 15.0
Checked nominal % = 15.0
Checked minus tol % = 7.5
Lowest actual Z% = 13.875
Worst screen kA = 12.0611
Target spare kA = 0.7389
ENTERED SCREEN MEETS
PROCUREMENT HOLD
Study + OEM review
```

## PUBASE — Per-unit R/X base conversion

**Inputs in order:** Old MVA, old kV LL, new MVA, new kV LL, old R pu, old X pu.

**Equations:** `Znew=Zold(Snew/Sold)(Vold/Vnew)^2; Zbase=kV^2/MVA; Ibase=1000 MVA/(sqrt(3) kV).`

**Outputs and interpretation:** Voltage bases refer to the SAME physical side. Outputs new R/X pu, magnitude percent, physical R/X ohms and both base impedances/current. Negative X allowed. Physical transformer-side referral requires the turns-ratio-squared operation in addition to base conversion.


### Worked run

```text
3PH PER-UNIT BASES
Old base MVA: 100
Old base kV LL: 100
New base MVA: 200
New base kV LL: 50
Old R pu: 0
Old X pu: 0.1
Base scale = 8.0
New R pu = 0.0
New X pu = 0.8
New Z % = 80.0
R ohm = 0.0
X ohm = 10.0
Old Zbase ohm = 100.0
New Zbase ohm = 12.5
New Ibase A = 2309.401
SAME physical side
```

## DCDROP — DC control-loop voltage and maximum length

**Inputs in order:** Minimum source V; duty current A; one-way ft; single-wire ohm/kft at operating temperature; other total loop ohms; required minimum device V.

**Equations:** `Rloop=2 L r/1000+Rother; Vdevice=Vs-I Rloop; Lmax=500[(Vs-Vmin)/I-Rother]/r.`

**Outputs and interpretation:** Constant-current model. Outputs total loop R, drop, device volts, margin, loss watts and maximum length when I and r are nonzero. Negative length budget is flagged. OEM coil/current at the applicable voltage, contact drops, inrush, shared segments and battery end voltage matter. Constant-power loads need a different circuit solution.


### Worked run

```text
DC CONTROL LOOP DROP
Min source volts: 125
Duty current A: 5
One-way length ft: 1000
Wire ohm/kft: 1
Other loop ohm: 0.5
Device min volts: 100
Loop R ohm = 2.5
Drop V = 12.5
Drop % = 10.0
Device V = 112.5
Margin V = 12.5
Loop loss W = 62.5
Max one-way ft = 2250.0
ENTERED DUTY MEETS
Check OEM coil duty
```

## PQSUM — Signed real/reactive power aggregation

**Inputs in order:** Bus kV LL; number of items 1-30; signed MW and Mvar for each.

**Equations:** `P=sum Pi; Q=sum Qi; |S|=sqrt(P^2+Q^2); I=1000 |S|/(sqrt(3) kV); |PF|=|P|/|S|.`

**Outputs and interpretation:** Positive P is real consumption; positive Q inductive consumption; generation/capacitors have negative signs. Outputs net exchange only. Internal feeder currents can remain high even when net power cancels. Zero net S produces undefined PF. No invented leading/lagging label for reverse power.


### Worked run

```text
3PH P-Q SUM
Load P+, generation P-
Inductive Q+, cap Q-
Bus kV LL: 34.5
Number of items: 2
Item 1
Signed MW: 30
Signed Mvar: 20
Item 2
Signed MW: 20
Signed Mvar: -5
Net MW = 50.0
Net Mvar = 15.0
Net MVA = 52.2015
Bus current A = 873.582
PF magnitude = 0.95783
Net exchange only
Check each branch duty
```

## WENNER — Wenner apparent resistivity

**Inputs in order:** Equal probe spacing m; insertion depth m; measured resistance ohm.

**Equations:** `rho=2 pi a R for shallow probes.`

**Outputs and interpretation:** Only reports rho when depth<=0.1 spacing. Otherwise withholds the shallow result. Output is ohm-m apparent resistivity, not a soil-layer fit or grid resistance. Repeat spacings/axes; measurement interference, season and instrument resolution are outside this arithmetic.


### Worked run

```text
WENNER APPARENT RHO
Equal spacing m: 5
Probe depth m: 0.1
Measured R ohm: 10
Depth/spacing = 0.02
App rho ohm-m = 314.159
Shallow-probe estimate
Repeat spacings/axes
Not grid resistance
```

## UNBAL — Line-voltage magnitude unbalance

**Inputs in order:** Three RMS line-line voltage magnitudes in matching units; entered permitted deviation percent.

**Equations:** `Average=(Vab+Vbc+Vca)/3; unbalance%=100 max(|Vi-average|)/average.`

**Outputs and interpretation:** This is a magnitude-deviation metric, not V2/V1. No fixed allowable percentage or motor-derating rule. Zero average invalid; missing phase zero values remain calculable for fault diagnosis.


### Worked run

```text
LL VOLTAGE UNBALANCE
Vab RMS: 100
Vbc RMS: 100
Vca RMS: 103
Allowed deviation %: 2
Average V = 101.0
Max deviation V = 2.0
Unbalance % = 1.9802
ENTERED LIMIT MEETS
Not V2/V1 sequence
Same units for all V
```

## BUSAMP — Bus conductor heat-balance check

**Inputs in order:** Hot DC R ohm/m; Rac/Rdc factor >=1; convection, radiation, conduction losses and solar gain, all W/m; duty A; kV LL.

**Equations:** `Ithermal=sqrt[(qc+qr+qconduction-qs)/(Rdc F)]; MVA=sqrt(3) kV I/1000.`

**Outputs and interpretation:** All heat terms and resistance must describe the SAME conductor temperature, geometry and weather. No weather correlation, heat-transfer coefficients, conductor table or joint ampacity is invented. Negative net cooling means no feasible current at the specified temperature. Conduction=0 is allowed when no credit justified. This inverse balance is useful for checking a full conductor heat-balance worksheet; it is not a complete bus design.


### Worked run

```text
BUS HEAT BALANCE
All heat in W/m
Hot DC R ohm/m: 0.0001
Rac/Rdc factor: 1
Convection loss W/m: 60
Radiation loss W/m: 30
Conduction loss W/m: 0
Solar gain W/m: 10
Duty current A: 800
Bus kV LL: 34.5
Hot AC R ohm/m = 0.0001
Net cooling W/m = 80.0
Duty Joule W/m = 64.0
Thermal current A = 894.427
Thermal MVA = 53.447
Current margin A = 94.427
HEAT BALANCE MEETS
Use common temp/weather
Check joints/apparatus
```

## REACTOR — Radial series-reactor impedance sizing

**Inputs in order:** Bus kV LL; existing fault kA at 1pu; source X/R; target fault kA; maximum voltage pu; Hz; load A.

**Equations:** `Zs=V/(sqrt(3) Isc at 1pu); R=Zs/sqrt(1+(X/R)^2); X=R(X/R); required |Z|=c V/(sqrt(3) Ilimit); added X=max(0,sqrt(max(0,|Zreq|^2-R^2))-X); L=X/(2 pi f).`

**Outputs and interpretation:** Outputs source R/X, minimum added reactance ohm/phase, mH/phase, resulting fault kA, load Mvar and IX volts/phase. One radial upstream path through a lossless added reactor. All bypass/downstream sources require another model. No tolerance/headroom applied automatically, and IX is not actual regulation. Thermal/mechanical withstand, insulation, magnetic clearance, losses and voltage performance need OEM/study work.


### Worked run

```text
SERIES REACTOR CHECK
One radial source path
Bus base kV LL: 34.5
Source fault kA at 1pu: 25
Source X/R: 10
Target fault kA: 12.8
Max voltage pu: 1.05
Frequency Hz: 60
Load current A: 1000
Source R ohm = 0.07928
Source X ohm = 0.79279
Min added X ohm = 0.83923
Inductance mH/ph = 2.22613
Calculated fault kA = 12.8
Load reactive Mvar = 2.5177
Load IX volts/ph = 839.233
No tolerance applied
OEM/voltage study HOLD
```
