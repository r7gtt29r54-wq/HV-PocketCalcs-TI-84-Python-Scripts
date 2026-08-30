# TI-84 Evo High-Voltage Engineering Check Suite - Instruction Manual

## 1. Purpose

This suite is a set of transparent, daily-use independent checks for a high-voltage substation engineer. Each program calculates multiple intermediate quantities so the user can identify where a design package diverges, rather than merely seeing a final pass/fail label.

The programs are not substitutes for ETAP, ASPEN, CDEGS, CYMCAP, an IEEE 485 worksheet, an IEEE 605 bus calculation, a three-dimensional lightning model, an insulation-coordination study, or an approved OEM curve. Pocket calculators are excellent at arithmetic and notably poor at assuming responsible charge.

## 2. Before every use

Record:

- project and exact asset;
- one-line revision and operating case;
- study/vendor/source revision for each input;
- units and per-unit base;
- program filename and revision date;
- result, reviewer, and disposition.

Any `MEETS` result means only that the entered duty did not exceed the entered limit under the program's stated model. `HOLD` means necessary information was intentionally not inferred.

## 3. Program index

| Program | Daily review use |
|---|---|
| ARREST | Review MCOV, TOV, and insulation protective margins from study/OEM values |
| BUSCHK | Convert power flow to bus current and check continuous, short-time, and peak duty |
| CAPBANK | Check ideal and selected bank size, actual PF, capacitance, voltage rise, and resonance |
| CTBURD | Check CT loop burden and symmetrical/transient secondary voltage demand |
| DCLOAD | Reconstruct a compact DC duty and charger check from load and tripping schedules |
| FAULT3 | Recalculate 3PH, SLG, and L-L currents from sequence Thevenin impedances |
| NGR | Check NGR ohms, charging current, total fault current, power, and energy |
| SPHERE | Check single-mast or equal-mast 2-D rolling-sphere geometry |
| VDROP | Check exact balanced three-phase voltage drop with temperature and parallel runs |
| XFMR | Estimate total transformer-bank MVA and HV/MV FLA at 10% design |

## 4. ARREST.py - arrester coordination

### What it calculates

- required continuous line-ground voltage from maximum line-line voltage and an entered line-ground multiplier;
- selected MCOV margin;
- actual TOV in per unit of MCOV and OEM TOV capability margin at an entered duration;
- lightning-impulse margin from equipment BIL and arrester LIPL;
- switching-impulse margin when both SIWL and SSPL are supplied.

### Inputs

| Prompt | Enter |
|---|---|
| Max system kV LL | Maximum continuous system line-line RMS voltage, not nominal voltage |
| Cont LG multiplier | `VLG,max / VLL,max` for the applicable grounding and contingency case |
| Selected MCOV kV | Proposed arrester MCOV, RMS kV |
| System TOV kV LG | Maximum study TOV at the arrester location, RMS kV |
| OEM TOV cap kV | OEM-permitted TOV at the entered duration and prior-duty condition |
| TOV duration sec | Applicable clearing/overvoltage duration |
| Equipment BIL kV | Protected equipment lightning impulse withstand, crest kV |
| Arrester LIPL kV | Arrester lightning impulse protective level for the selected current wave |
| Switch withstand kV | Applicable switching impulse withstand; enter 0 with SSPL 0 to hold |
| Arrester SSPL kV | Arrester switching surge protective level; enter 0 with SIWL 0 to hold |

### Equations

`Required MCOV = VLL,max x entered LG multiplier`

`MCOV margin % = 100 x (selected MCOV / required MCOV - 1)`

`TOV margin % = 100 x (OEM capability / system TOV - 1)`

`LI margin % = 100 x (BIL / LIPL - 1)`

The program does not declare a required percentage. Compare the calculated margins to the adopted Owner/EOR insulation-coordination criterion.

### Worked check

Inputs: `36.5, 0.57735, 24.4, 30, 32, 10, 200, 80, 150, 100`.

Expected key outputs: required MCOV `21.073 kV`, MCOV margin `15.79%`, TOV margin `6.67%`, LI margin `150%`, SI margin `50%`.

### Hold points

Confirm grounding contingency, TOV duration and prior duty, actual lead length, energy duty, pressure-relief rating, contamination/creepage, separation distance, and the exact OEM curve. Current product-standard scope: IEEE C62.11-2020. See [CALCULATION_BASIS.md](./CALCULATION_BASIS.md), Items 10 and 11.

## 5. BUSCHK.py - bus electrical duty

### What it calculates

- normal and contingency current from entered MVA and bus kV;
- MVA corresponding to the entered continuous ampere rating;
- continuous loading percentages;
- symmetrical short-time `I^2t` duty and use of entered `kA-for-seconds` capability;
- peak current from an entered asymmetry/peak multiplier and use of the entered peak rating.

### Inputs

| Prompt | Enter |
|---|---|
| Bus kV LL | Operating line-line voltage for the power-flow case |
| Normal MVA | Maximum normal bus-section apparent power |
| Contingency MVA | Maximum credible contingency bus-section apparent power |
| Continuous rating A | Approved ampacity for the exact conductor, joints, and environment |
| Sym fault kA | Maximum applicable symmetrical RMS fault current |
| Fault duration sec | Backup-clearing duration used for the thermal duty |
| Bus ST rating kA | Approved short-time current rating |
| ST rating sec | Time associated with that short-time rating |
| Peak multiplier | Project/study factor converting symmetrical RMS to peak current |
| Peak rating kA | Approved peak withstand rating |

### Equations

`I(A) = MVA x 1000 / (sqrt(3) x kV)`

`I2t duty = Isym^2 x clearing time`

`I2t capacity = Ishort-time^2 x rated time`

`Peak duty = entered multiplier x Isym`

### Worked check

Inputs: `230, 500, 600, 2000, 40, 0.25, 63, 1, 2.6, 104`.

Expected key outputs: normal current `1255.1 A`, contingency current `1506.1 A`, bus capacity `796.74 MVA`, I2t use `10.1%`, peak duty `104.0 kA`.

### Hold points

This program does not calculate ampacity, terminal/joint hot spots, short-circuit forces, conductor temperature, sag, or insulator/structure loads. IEEE Std 605-2023 Clause 5.2 identifies the broader design inputs; Annexes B, I, and J contain the full thermal/mechanical workflows. See calculation-basis Item 6.

## 6. CAPBANK.py - capacitor-bank design check

### What it calculates

- initial reactive load;
- ideal Mvar required to reach target PF;
- integer number of selected steps required;
- actual selected bank Mvar and resulting PF, including leading/lagging indication;
- ideal capacitance per phase per step for delta or grounded/ungrounded wye geometry as entered;
- first-order voltage-rise and parallel-resonance-order screens when source short-circuit MVA is supplied.

### Inputs

| Prompt | Enter |
|---|---|
| Load MW | Real load at the correction condition |
| Initial PF | Initial PF magnitude, greater than 0 and less than 1 |
| Target PF | Target PF magnitude, greater than initial PF and no greater than 1 |
| Bank kV LL | Bank line-line RMS voltage |
| Frequency Hz | System frequency |
| 1=DELTA 2=WYE | Physical capacitor connection |
| Selected step Mvar | Nameplate Mvar of one equal step at entered voltage |
| Number of steps | Selected installed/energized equal steps |
| Source SC MVA | Thevenin short-circuit MVA at bank bus; enter 0 to hold screens |

### Equations

`Qinitial = P tan(acos(PFinitial))`

`Qideal = P[tan(acos(PFinitial)) - tan(acos(PFtarget))]`

`PFactual = P / sqrt(P^2 + (Qinitial - Qbank)^2)`

For one delta step: `Cphase = Qstep / (3 omega VLL^2)`.

For one wye step: `Cphase = Qstep / (omega VLL^2)`.

The program reports `100 Qbank/Ssc` as a first-order voltage-rise screen and `sqrt(Ssc/Qbank)` as a parallel-resonance-order screen.

### Worked check

Inputs: `50, 0.90, 0.98, 34.5, 60, 1, 5, 3, 1000`.

Expected key outputs: ideal bank `14.063 Mvar`, required steps `3`, actual PF `0.98343 lagging`, per-phase/step capacitance `3.714 uF`, approximate voltage rise `1.5%`, resonance order `8.165`.

### Hold points

Perform load flow, harmonic scan, switching transient/inrush, back-to-back switching, unbalance, fuse, reactor/filter, discharge-device, protection, and equipment-duty checks. Source basis: Glover et al., 7th ed., Section 2.3, pp. 55-57.

## 7. CTBURD.py - CT burden and saturation-voltage screen

### What it calculates

- secondary current at maximum primary fault;
- round-trip lead resistance;
- equivalent device impedance from burden VA at rated secondary current;
- rated-current VA burden;
- symmetrical terminal and internal CT voltage;
- class-voltage use for symmetrical current;
- conservative `(1+X/R)` offset voltage demand and effective-class use.

### Inputs

| Prompt | Enter |
|---|---|
| Primary fault kA | Maximum primary fault current through the CT |
| CT tap primary A | Primary ampere rating of the connected tap |
| CT rated sec A | Rated secondary current, normally 1 A or 5 A per nameplate |
| One-way lead ft | CT to relay one-way routed length |
| Lead ohm/kft | Resistance of one lead conductor at applicable temperature |
| Relay burden VA | Connected relay burden at rated secondary current |
| Other burden VA | Test switches, transducers, meters, and other series burden |
| CT winding ohm | Secondary winding resistance on the connected tap |
| Effective C class V | Effective terminal accuracy-class voltage for the connected tap |
| Primary X/R | X/R at the CT for the studied through-fault |

### Equations

`If,sec = If,primary x Isec,rated / Iprimary,tap`

`Rlead = 2 x one-way length x ohm/kft / 1000`

`Zdevice = total device VA / Isec,rated^2`

`Vterminal,sym = If,sec(Rlead + Zdevice)`

`Vrequired,offset = If,sec(1 + X/R)(Rlead + Zdevice + RCT)`

### Worked check

Inputs: `40, 2000, 5, 500, 0.2, 2, 1, 0.5, 400, 20`.

Expected key outputs: fault secondary `100 A`, lead loop `0.2 ohm`, rated burden `8 VA`, symmetrical terminal voltage `32 V`, offset demand `1722 V`. The output correctly calls for an excitation-curve check.

### Hold points

The device VA-to-ohm conversion is a magnitude approximation. Verify actual complex burden, CT connection, full-winding/tap class scaling, excitation curve/knee point, remanence, ratio error, relay algorithm, time to saturation, and internal/external fault cases. The calculation form follows the locally reviewed C37.110-2007; the active edition is C37.110-2023 and must govern when adopted. See calculation-basis Item 8.

## 8. DCLOAD.py - DC duty and charger screen

### What it calculates

- continuous Ah over the selected autonomy period;
- incremental Ah for two non-overlapping events whose entered currents are total bus current;
- a factor-adjusted nameplate-Ah screen;
- charger current using removed Ah, recharge factor/time, continuous load, design factor, and charger correction;
- utilization of an entered selected battery.

### Inputs

| Prompt | Enter |
|---|---|
| Continuous load A | Total steady DC load at applicable battery voltage |
| Autonomy hours | Required charger-outage standby duration |
| Event 1 total A | Total DC bus current during event 1 |
| Event 1 minutes | Event 1 duration |
| Event 2 total A | Total DC bus current during event 2 |
| Event 2 minutes | Event 2 duration |
| OEM rate factor | Explicit conversion from arithmetic Ah to applicable rate/cell screen |
| Temperature factor | Approved temperature correction factor |
| Aging factor | Approved end-of-life factor |
| Design factor | Approved growth/design factor as a multiplier |
| Recharge factor | Battery recharge efficiency factor |
| Recharge hours | Required recharge time |
| Charger corr factor | OEM altitude/temperature/other charger correction |
| Selected battery Ah | Proposed nameplate Ah; enter 0 to hold selection check |

### Event convention

Each event current is the **total** current during that event. The script adds only `max(0, event current - continuous current)` for the event duration, preventing the continuous load from being counted twice. The two events are assumed not to overlap. If operations can overlap, combine them into the governing event or use a full minute-by-minute worksheet.

### Equations

`Removed Ah = Icontinuous x hours + sum[(Ievent - Icontinuous)+ x minutes/60]`

`Factored screen Ah = removed Ah x rate x temperature x aging x design`

`Charger A = [(removed Ah/recharge h) x recharge factor + Icontinuous] x design x charger correction`

### Worked check

Inputs: `10, 8, 50, 1, 30, 1, 1.1, 1.15, 1.25, 1.1, 1.1, 8, 1, 200`.

Expected key outputs: duty removed `81.0 Ah`, factored screen `140.889 Ah`, charger output `23.251 A`, selected use `70.4%`.

### Hold points

Final battery sizing requires the full duty sequence, minimum system/end voltage, actual coil voltage-current behavior, breaker-failure and restoration logic, DC ties, manufacturer discharge tables, and the adopted IEEE 485/1115 method as applicable. IEEE 1818-2017 Annex C, pp. 85-92, demonstrates why the simple Ah total alone is not a cell selection. See calculation-basis Item 7.

## 9. FAULT3.py - sequence fault-current check

### What it calculates

- base current;
- bolted or impedance fault three-phase current;
- SLG current from series positive-, negative-, and zero-sequence impedances;
- line-to-line current from positive- and negative-sequence impedances;
- three-phase fault MVA and positive-sequence X/R.

### Inputs

| Prompt | Enter |
|---|---|
| System base MVA | Common MVA base for all sequence impedances |
| Fault bus kV LL | Common voltage base at faulted bus |
| Prefault voltage pu | Thevenin positive-sequence prefault voltage magnitude |
| R1, X1 pu | Positive-sequence Thevenin impedance on common base |
| R2, X2 pu | Negative-sequence Thevenin impedance on common base |
| R0, X0 pu | Zero-sequence Thevenin impedance on common base |
| Fault R, X pu | Fault impedance on common base; enter zero for bolted faults |

### Equations

`Ibase(kA) = MVA / [sqrt(3) kV]`

`I3PH,pu = Vpu / |Z1 + Zf|`

`ISLG,pu = 3Vpu / |Z1 + Z2 + Z0 + 3Zf|`

`ILL,pu = sqrt(3)Vpu / |Z1 + Z2 + Zf|`

### Worked check

Inputs: `100, 34.5, 1.0, 0.01, 0.10, 0.01, 0.10, 0.03, 0.30, 0, 0`.

Expected key outputs: base `1.6735 kA`, 3PH `16.6517 kA`, SLG `9.9910 kA`, L-L `14.4208 kA`, positive X/R `10.0`.

### Hold points

All sequence impedances must describe the same topology, fault location, voltage base, MVA base, and study case. Do not use this result as breaker duty without the applicable interrupting/closing/latching method, decrement, asymmetry, TRV, minimum/maximum cases, motor/generator/IBR contribution, and approved utility model. Source: Glover et al., Sections 8.3, 10.2, and 10.3; see calculation-basis Items 4 and 5.

## 10. NGR.py - NGR and charging-current check

### What it calculates

- line-ground voltage;
- ideal NGR resistance for the entered resistive current;
- system capacitive charging current for the entered total per-phase capacitance;
- quadrature total ground-fault current and resistive-to-capacitive ratio;
- resistor MW and MJ duty.

### Inputs

| Prompt | Enter |
|---|---|
| System kV LL | RMS line-line voltage of the grounded island |
| Resistive GF A | Intended in-phase resistor contribution |
| Duty time sec | Required resistor thermal duty duration |
| Frequency Hz | System frequency |
| Total C/phase uF | Total phase-to-ground capacitance per phase for the studied island; 0 holds charging check |

### Equations

`VLG = VLL/sqrt(3)`

`RNGR = VLG/IR`

`IC = 3 omega Cphase VLG`

`Itotal = sqrt(IR^2 + IC^2)`

`MW = VLG x IR / 1,000,000`; `MJ = MW x seconds`

### Worked check

Inputs: `34.5, 400, 10, 60, 2`.

Expected key outputs: `49.7965 ohm`, charging current `45.055 A`, total fault current `402.529 A`, IR/IC `8.878`, energy `79.6743 MJ`.

### Hold points

Confirm transformer vector group and neutral availability, all connected cables/equipment for each switching case, zero-sequence network, NGR tolerance and hot resistance, voltage rating, time rating, protection sensitivity/coordination, transient recovery, harmonics, enclosure, and OEM selection. The calculator does not decide whether resistance grounding is appropriate.

## 11. SPHERE.py - two-dimensional rolling-sphere geometry

### Mode 1: single mast

Calculates the maximum horizontal offset at the entered equipment height for a mast and a selected sphere radius. For single-mast geometry, mast height above the radius is capped at the radius because the reviewed IEEE 998-2012 Clause 6.3.1 notes that excessive single-mast height above striking distance adds no additional protection in that model.

Inputs: mode `1`, sphere radius, mast height, equipment height, and target offset. Use one consistent distance unit.

`Xmax = sqrt(2RHmast - Hmast^2) - sqrt(2RHequip - Hequip^2)`

### Mode 2: two equal-height masts

Calculates maximum equal-mast spacing for a target at the midpoint and the bottom-of-sphere arc height at the actual midpoint.

Inputs: mode `2`, sphere radius, equal mast height, equipment height at the midpoint, and mast spacing.

`Dmax = 2 sqrt[2R(Hmast-Hequip) - (Hmast-Hequip)^2]`

`Harc,mid = Hmast + sqrt[R^2 - (D/2)^2] - R`

When the mast/equipment height difference is at least `2R`, the program limits maximum spacing to `2R`, the geometric support limit for that cross section.

### Worked checks

- Single mast inputs `1, 150, 60, 20, 40` produce maximum offset `45.1669` and `BELOW 2D ARC`.
- Equal masts inputs `2, 150, 60, 20, 150` produce maximum spacing `203.9608`, midpoint arc height `39.9038`, and vertical margin `19.9038`.

### Hold points

Touching the sphere is reported as outside. Complete design requires the current adopted method, selected stroke current/radius, three-dimensional plan and elevation geometry, multiple/mixed supports, shield wires and sag, side-stroke assessment, shielding-failure basis, and field coordinates. IEEE 998-2012 was the local calculation source; IEEE 998-2026 is current and must be reviewed/adopted before reliance. See calculation-basis Item 9.

## 12. VDROP.py - exact balanced three-phase voltage drop

### What it calculates

- receiving-end current from MW, kV, and PF;
- AC resistance corrected from base to operating temperature with an entered coefficient;
- equivalent R/X for route length and parallel runs;
- exact sending-end phase-voltage phasor and line-line magnitude;
- signed voltage change and three-phase conductor loss.

### Inputs

| Prompt | Enter |
|---|---|
| Receiving load MW | Three-phase real power at receiving end |
| Receiving kV LL | Receiving-end line-line RMS voltage |
| PF | PF magnitude |
| 1=LAG 2=LEAD | Receiving-load current angle |
| One-way length ft | Electrical route length |
| R ohm/kft at base C | Approved AC conductor resistance at base temperature |
| X ohm/kft | Approved positive-sequence reactance for actual geometry |
| Base temp C | Temperature associated with entered resistance |
| Operating temp C | Studied conductor operating temperature |
| R alpha per C | Approved resistance temperature coefficient; enter 0 if R already matches operating condition |
| Parallel runs/phase | Equal current-sharing runs per phase |

### Equations

`Rop = Rbase[1 + alpha(Top - Tbase)]`

`I = MW x 1000 / [sqrt(3) kV PF]`

`Vs,phase = Vr,phase + (R + jX)Iphasor`

`Vs,LL = sqrt(3)|Vs,phase|`

`Loss kW = 3I^2R/1000`

### Worked check

Inputs: `50, 34.5, 0.95, 1, 10000, 0.1, 0.08, 75, 90, 0.00393, 2`.

Expected key outputs: current `880.78 A`, operating R `0.10590 ohm/kft`, sending voltage `35.45941 kV`, exact voltage change `2.7809%`, loss `1232.254 kW`.

### Hold points

Confirm whether R is AC or DC, conductor temperature, skin/proximity effects, cable bonding/sheath effects, spacing and transposition, parallel-run current sharing, transformer taps, shunt capacitance, harmonic current, unbalance, and load model. For long lines/cables or voltage-controlled resources, use a load-flow/cable model. Source: Qcells go-by printed p. 4 plus the receiving-end phasor model; see calculation-basis Item 1.

## 13. XFMR.py - transformer 10% capacity check

### What it calculates

- estimated total transformer-bank MVA from plant MWac, PF, and planning margin;
- arithmetic planning MVA per installed transformer;
- total parallel-bank FLA at the HV bus;
- total arithmetic MV FLA and MV FLA per separate transformer secondary;
- an impedance-only, stiff-HV-source secondary-fault screen for each separate MV bus.

### Inputs

| Prompt | Enter |
|---|---|
| Plant MWac | Maximum plant real-power export/import used for this conceptual sizing case |
| Plant PF | PF magnitude for the plant sizing condition |
| Planning margin % | Explicit 10%-design margin |
| HV kV LL | Nominal line-line voltage at the common, parallel transformer HV bus |
| MV kV LL | Nominal line-line voltage at each separate transformer secondary bus |
| Transformer Z % | Positive-sequence impedance magnitude on the transformer base; used only for the secondary-fault screen |
| Installed units | Number of equal transformers sharing the total planning MVA |

### Equations

`Required total MVA = Plant MWac/PF x (1 + margin)`

`Planning MVA/unit = Required total MVA / installed units`

`FLA = MVA x 1000 / [sqrt(3) x kV LL]`

`MV fault/unit = MV FLA/unit / (Z%/100)`

### Worked check

Inputs: `300, 0.95, 10, 230, 34.5, 10, 2`.

Expected key outputs: required total `347.368 MVA`, planning allocation `173.684 MVA/unit`, HV bank FLA `872.0 A`, aggregate MV FLA `5813.1 A`, MV FLA per transformer `2906.6 A`, and MV fault screen `29.066 kA`.

### Hold points

The HV FLA represents the common HV bus with the transformer banks in parallel. The `MV total FLA` is only the arithmetic sum of separate transformer-secondary currents; it is not a rating for one closed MV bus. For normal split 34.5 kV operation, use `MV FLA/unit`. The MV fault screen assumes a stiff HV source and one transformer feeding one isolated MV bus; it excludes utility/source impedance, inverter contribution, motors, cables, reactors, and breaker duty. Confirm load duration, reactive requirements, ultimate cooling stages, ambient, LTC/tap range, impedance tolerance, zero-sequence paths, losses, and OEM guarantees. This is planning support, not an equipment rating or a short-circuit study. IEEE C57.12.00-2021 is a general requirements standard, not a calculator-selected rating. See calculation-basis Items 3 and 11.

## 14. Required disposition after a run

Use one of these dispositions in the design-review record:

- **MATCH:** independent result agrees with the governing calculation within the stated rounding/model tolerance.
- **CLARIFICATION:** arithmetic is reproducible but an input, basis, operating case, or acceptance limit is not traceable.
- **DEVIATION:** supplier/EOR result conflicts with an explicit governing requirement.
- **HOLD:** current edition, project authority, OEM data, study case, or accountable approval is unavailable.

Never turn `MATCH` into `APPROVED` without the responsible review and release workflow.
