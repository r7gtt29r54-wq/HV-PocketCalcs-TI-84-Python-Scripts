# Calculation Basis, Source Register, and Release Boundary

## Status

**Artifact status:** independent engineering check suite; not project design authority.

**Evidence date:** 2026-08-29.

The formulas below are suitable for transparent spot checks when all inputs are traceable to the exact asset and operating case. A matching calculator result only shows that the entered values are consistent with the stated model. It does not prove that the inputs, model scope, or acceptance criterion are correct.

## Formula register

| Program | Formula basis | Primary limitations |
|---|---|---|
| ARREST | Required continuous voltage `VLL,max x entered LG multiplier`; direct ratios for MCOV, TOV, BIL/LIPL, and SIWL/SSPL margins | No TOV curve interpolation, lead-length effect, energy, pressure-relief, contamination, or separation-distance study |
| BUSCHK | `I = MVA/(sqrt(3) kV)`; `I2t = I^2 t`; `Ipeak = multiplier x Isym` | Uses entered ratings and peak factor; does not create ampacity or electromechanical forces |
| CAPBANK | Power triangle `Q = P tan(acos(PF))`; three-phase capacitor reactive-power relations | Approximate voltage-rise and parallel-resonance screens are not harmonic/load-flow studies |
| CTBURD | CT ratio current; loop burden; `V = IZ`; offset screen `Vreq = If_sec(1+X/R)Ztotal` | Simplified resistive burden; excitation curve, remanence, relay algorithm, connection, and transient simulation remain required |
| DCLOAD | Continuous plus two non-overlapping event Ah; explicit adjustment factors; charger `[(A/t)e + Ic]dk` | Ah screen does not reproduce an IEEE 485 rate/plate worksheet or OEM discharge curves |
| FAULT3 | Positive-, negative-, and zero-sequence networks for 3PH, SLG, and L-L faults | One Thevenin equivalent; no machine decay, inverter controls, topology, mutual coupling, or duty-standard decrement calculation |
| NGR | `R = VLG/IR`; `IC = 3 omega Cphase VLG`; orthogonal `Itotal = sqrt(IR^2+IC^2)` | Capacitance must be total per phase for the studied island; no full zero-sequence network or relay coordination |
| SPHERE | Circle geometry for a sphere tangent to a mast/ground or supported by two equal-height masts | Two-dimensional only; no mixed supports, shield-wire sag, plan-view gaps, side strokes, risk rate, or 3-D verification |
| VDROP | Receiving-end phasor model `Vs = Vr + IZ`; temperature-corrected resistance and three-phase `I^2R` loss | Balanced constant-power receiving load; excludes shunt capacitance, taps, harmonics, unbalance, charging, and load-flow controls |
| XFMR | `MVA = MW/PF x (1 + margin)`; three-phase FLA; transformer-impedance-only MV fault screen | Conceptual bank estimate; the total MV FLA is not a closed-bus rating, and the fault screen assumes a stiff HV source |

## Technical sources actually reviewed

1. **Voltage drop and field calculation structure.** The Qcells voltage-drop go-by separates DC and AC cases, identifies one-way length, conductor R/X, phase multiplier, current, and voltage-drop percentage on printed pages 2-4. Source: [Qcells Voltage Drop Calculation Template Rev.1](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/QCells/HV Design Group/Qcells Calculations & Study Report - TEMPLATE/Qcells HV Design - Voltage Drop Calculation TEMPLATE_Rev1.pdf>), especially printed p. 4. The new `VDROP.py` goes beyond that scalar approximation by calculating the sending-end phasor magnitude and loss.

2. **Power triangle and capacitor correction.** Glover, Sarma, and Overbye, *Power System Analysis and Design*, 7th ed. (2023), Section 2.3, printed pp. 55-57, Equations 2.3.6-2.3.9 and Example 2.3, provides the `P-Q-S` and PF-correction basis. Source: [Power System Analysis and Design, 7th ed.](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/References/Books/J. Duncan Glover,  Mulukutla S. Sarma, Thomas Overbye -Power System Analysis and Design, 7th Edition - 2023.pdf>).

3. **Transformer capacity, current, and fault-current relationship.** Glover, Sarma, and Overbye, *Power System Analysis and Design*, 7th ed. (2023), Section 2.3, printed pp. 55-57, provides the apparent-power/PF relation. Example 3.8, printed p. 126, demonstrates the per-unit `Isc = V/Z` relationship for a balanced three-phase terminal fault. `XFMR.py` uses the first relationship for conceptual MVA/FLA and the second only as an infinite-HV-source screen at each separate MV secondary bus.

4. **Sequence faults.** The same text, Section 10.2, printed pp. 501-504, Equations 10.2.7-10.2.8, gives the SLG series connection and phase-a current. Section 10.3, printed pp. 505-506, Equations 10.3.10-10.3.11, gives the line-to-line result. `FAULT3.py` applies these equations to an entered common MVA base.

5. **Short-circuit workflow.** The Cooper Bussmann guide directs the reviewer to include all sources and impedances on a one-line and identifies source capability, transformer impedance, motor contribution, and voltage as variables affecting the result on printed pp. 192-194. Source: [Short Circuit Current Calculations](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/References/CALCULATORS~/REF_ P2P KAIC/bus-ele-tech-lib-short-circuit-current-calculations.pdf>). It is a 2005 secondary reference, so it is used for workflow context, not current code requirements.

6. **Bus design.** IEEE Std 605-2023, Clause 1.1 and Clause 5.2, identifies ampacity, maximum anticipated fault current, fault-clearing time, temperatures, wind, altitude, and related design inputs. Annex I, printed pp. 263-269, demonstrates conductor ampacity and short-circuit verification. Source: [IEEE Std 605-2023](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/References/IEEE/IEEE 605 - Guide for Bus Design in Air Insulated Substations.pdf>). A career go-by applies the heat balance and documents site-specific inputs on printed pp. 2-5: [Blacks Creek Bus Ampacity Calculation](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/QCells/HV Engineering/1. Projects/BLACKS CREEK/3. Design/1. HV/251003_Blacks Creek Substation 60% IFR/Calculations/Blacks Creek Substation Bus Ampacity Calc.pdf>). Project values were not copied.

7. **Station DC.** IEEE Std 1818-2017, Clause 5.1.5, lists duty cycle, charger interruption, recharge time, standby duration, redundancy, and temperature among design considerations. Clause 5.5.2, Equation 16, provides the charger-sizing relationship. Annex C, printed pp. 85-92, requires the relay/tripping sequence, DC schematic, minute-by-minute load profile, manufacturer curves, and adjustment factors. Source: [IEEE Std 1818-2017](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/References/IEEE/IEEE 1818 - Guide for the Design of Low-Voltage Auxiliary Systems for Electric Power Substations.pdf>). The Qcells DC go-by separates continuous and tripping loads and documents battery and charger criteria on printed pp. 2-5: [Qcells DC Load and Battery Sizing Template](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/QCells/HV Design Group/Qcells Calculations & Study Report - TEMPLATE/Qcells HV Design - DC Load & Battery Sizing Report TEMPLATE_Rev1.pdf>). Project/template values were not embedded.

8. **CT burden and saturation.** The locally available IEEE Std C37.110-2007, Clause 4.1.2, describes secondary voltage drops and burden; Clause 4.5.2 and Equations 8-15 discuss saturation factor; Clause 7.3.1, Equation 22, gives the `(1+X/R)` voltage-demand screen. Source: [IEEE Std C37.110-2007](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/References/IEEE/C37/C37.110 IEEE Guide for the Application of Current Transformers Used for Protective Relaying Purposes.pdf>). This local edition is superseded. The current active edition is [IEEE C37.110-2023](https://standards.ieee.org/ieee/C37.110/6175/); its licensed clause text was not available in the reviewed library. The instrument-transformer requirements standard is currently [IEEE C57.13-2016](https://standards.ieee.org/ieee/C57.13/4867/).

9. **Rolling sphere.** IEEE Std 998-2012, Clause 6.3.1 and Figures 24-25, printed pp. 31-33, describes the rolling-sphere surface and single-mast protected region; Clause 6.3.4, printed p. 36, discusses multiple electrodes. Source: [IEEE Std 998-2012](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/References/IEEE/IEEE 998 - Guide for Direct Lightning Stroke Shielding of Substations.pdf>). The Qcells calculation go-by shows single-protector and equal-support geometry on printed pp. 2-5: [Qcells Lightning Protection Template Rev.0](</Users/kubera-mac2024/Library/CloudStorage/OneDrive-Personal/Career/QCells/HV Design Group/Qcells Calculations & Study Report - TEMPLATE/Qcells HV Design - Lightning Protection Analysis Calculation TEMPLATE_Rev0.pdf>). IEEE lists [IEEE 998-2026](https://standards.ieee.org/ieee/998/6860/) as the active revision superseding 2012; the 2026 licensed text was not available for clause verification.

10. **Surge arresters.** The active product standard is [IEEE C62.11-2020](https://standards.ieee.org/ieee/C62.11/5839/). The reviewed textbook case study, printed pp. 710-715, explains MCOV, TOV-duration curves, and protective characteristics using manufacturer-specific data. `ARREST.py` therefore requires the actual OEM TOV capability and protective levels as inputs and does not contain a generic arrester table.

11. **Power transformers.** [IEEE C57.12.00-2021](https://standards.ieee.org/ieee/C57.12.00/6962/) is the active general requirements standard for liquid-immersed distribution, power, and regulating transformers within its scope. `XFMR.py` does not establish an equipment rating or demonstrate compliance with that standard.

## Edition and authority holds

- Confirm the contractual edition and project adoption before using any standard as governing.
- The current IEEE 998-2026 and IEEE C37.110-2023 licensed clause text was not available in the local library; their official status and scope were checked, but their clauses were not used as unseen authority.
- NEC, NESC, NERC, utility, Owner, EOR, OEM, and AHJ acceptance values are intentionally absent.
- Results affecting procurement, protection, personnel safety, construction, commissioning, switching, or energization require an accountable calculation and release.
