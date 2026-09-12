# ZSIZE — transformer impedance sizing

Revision: 2026-09-12. Standalone TI-84 Evo Python program: `ZSIZE.py`.

## Purpose and result

Work backward from a downstream symmetrical three-phase fault-current limit to a minimum actual transformer impedance, a minimum nominal specification allowing for negative manufacturing tolerance, and an upward-rounded procurement candidate. Check an OEM proposal against the same inputs. All percentages refer to the entered **MVA base per transformer**, with HV/LV voltage bases at the stated tap.

The model uses an infinite HV source, equal two-winding transformers feeding the studied LV bus, and an entered upper bound for other fault contributions. It does not credit utility, cable, or reactor impedance. `PROCUREMENT HOLD` remains on every candidate: limited inputs establish a fault-current sizing bound, but cannot establish the acceptable upper impedance, voltage performance, full breaker duty, or a released purchase specification.

## Inputs, in calculator order

| Prompt | Meaning |
|---|---|
| Z base MVA/unit | MVA base on which the requested/OEM impedance is specified, per transformer; not aggregate plant MVA |
| HV base kV LL | Rated HV line-line kV for that tap/base |
| LV base kV LL | Corresponding LV line-line kV; breaker fault current is evaluated here |
| Breaker sym kA | Verified permissible symmetrical duty at the applicable voltage and interruption condition; not merely a reported available-fault result |
| Max voltage pu | Maximum prefault voltage on the stated base; 1.0–2.0 accepted; no assumed default |
| Duty headroom % | Reserve below the breaker limit, defined as `target = limit × (1 − headroom/100)`; a planning choice, not an IEEE-mandated margin |
| Other fault kA | Conservative sum of magnitudes of additional contributions through the studied breaker for the same duty/time; zero explicitly assumes none |
| Units on SAME LV | Equal units simultaneously feeding this faulted LV bus. Enter **1 for each isolated 34.5 kV bus**, even with multiple units connected to a common HV bus. Enter 2 only for two contributing units on a closed common LV bus |
| Minus Z tol % | Relative negative deviation from nominal, e.g. 7.5 means a factor of 0.925, not subtraction of 7.5 percentage points |
| Z step pct points | Upward rounding increment for a candidate: 1 means whole percentage points; 0.5 means half points. It is not a catalog rating list |
| OEM Z% (0=auto) | Optional nominal OEM proposal on exactly the same base; 0 checks the calculated rounded candidate |

No input may be blank or nonfinite. Count must be an integer. Headroom and tolerance must be below 100%. The program stops without a candidate if other sources consume all of the allocated duty. Practical input bounds are software guards, not equipment design limits.

## Equations and units

Let `S` be per-unit-transformer MVA, `V` LV kV, `N` equal transformers on the same LV bus, `c` maximum prefault voltage pu, `m` headroom fraction, and `t` negative tolerance fraction.

```text
Ibase,kA = S / (sqrt(3) V)
IHV,A = 1000 S / (sqrt(3) VHV)
Zbase,LV,ohm = V^2 / S
Itarget = Ilimit (1 - m)
Ibudget = Itarget - Iother
Zactual,min,% = 100 c N Ibase,kA / Ibudget
Znominal,min,% = Zactual,min,% / (1 - t)
Zcandidate,% = ceil(Znominal,min,% / step) step
Zlowest,% = Zselected,% (1 - t)
Iscreen,kA = 100 c N Ibase,kA / Zlowest,% + Iother
```

The displayed minima are rounded for readability; selection uses unrounded values and always rounds the candidate upward. Do not copy a rounded-down displayed minimum into a purchase specification. The selected value is a nominal impedance, and the minimum delivered value must also be specified on the same base/tap/reference temperature. For a different MVA or voltage base, derive `Znew,pu = Zold,pu (Snew/Sold) (Vold/Vnew)^2` before comparing values.

The other-source magnitude sum is a bounding assumption for the specified case, not a phasor or inverter-control model. Finite-source calculations need complex impedances on a common base; this module deliberately takes no finite-source credit. HV voltage supplies HV FLA and the base context; it does not independently change the LV fault result with matched transformer voltage bases.

## Reproduce the linked calculation

Enter in order:

```text
100, 138, 34.5, 12.8, 1.0, 0, 0, 1, 7.5, 1, 0
```

Expected: LV FLA 1673.48 A; HV FLA 418.37 A; LV base impedance 11.9025 ohm; minimum actual impedance **13.0741%**; minimum nominal **14.1341%**; rounded candidate **15%**; lowest actual **13.875%**; screened current approximately **12.0611 kA**. All impedances are on a **100 MVA, 138/34.5 kV base per transformer**.

Repeat with OEM Z = 14: approximately **12.9226 kA**, so `REVISE CANDIDATE/BASIS`. Repeat with voltage 1.05 pu and OEM Z = 15: approximately **12.6642 kA**, leaving little room below 12.8 kA. Higher voltage, reserved headroom, additional sources, and a closed LV tie can increase the required nominal impedance.

## Procurement use

Use the output to draft: “Proposed nominal positive-sequence impedance ___%, on ___ MVA per transformer and ___/___ kV at the specified tap/reference temperature, with negative tolerance ___% and minimum delivered impedance ___%. Subject to approved short-circuit and voltage-performance studies and OEM confirmation.” This is a draft input, not a complete purchase requirement.

Before release, establish the maximum source configuration and current actually interrupted by each breaker; applicable fault types/grounding; generation and motor contributions; prefault voltage and tap range; impedance tolerances on the correct base; X/R and asymmetrical/peak duty; TRV; and the acceptable impedance range from voltage regulation, motor starting, reactive requirements, losses and OEM capability. A higher Z that meets the current screen can still be unsuitable for operation. Approval cannot be inferred from the arithmetic.

## Verified technical basis

- **IEEE Std C57.12.00-2021, §7.1.5.1, Equation (6), printed p. 47 (PDF p. 48):** transformer and system impedance relation on a common apparent-power base and given tap. The infinite-source simplification and inverse sizing above are derived circuit calculations. §7.1.4.3, same page, includes system impedance in the relevant category duty calculation.
- **IEEE Std C57.12.00-2021, §9.2(a), printed p. 62 (PDF p. 63):** two-winding transformer tolerance is ±7.5% for specified impedance above 2.5%, and ±10% at 2.5% or below. The program requires an entered tolerance; a candidate at/below 2.5% with less than 10% raises a check flag. Tighter contractual tolerances need separate justification. This tool is limited to two-winding units; other configurations need a suitable model and tolerance basis.
- The manufacturer's scope and project adoption must be checked. [IEEE's official catalog](https://standards.ieee.org/ieee/C57.12.00/6962/) lists the 2021 edition as active, verified 2026-09-12. Exact breaker-standard clauses and OEM application corrections were not reviewed for this module; no correction factor or compliance certification is implied.


## Run and verify

Transfer only `ZSIZE.py` using TI Connect Evo and run it in Python. No third-party packages are required. Run the worked case on the physical calculator before daily use; desktop regression does not establish firmware compatibility. This revision has not been transferred or run on the calculator by the authoring agent.
