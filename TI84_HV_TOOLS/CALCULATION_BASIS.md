# Calculation models

Use the following equations with the input definitions and worked examples in the [instruction manual](./INSTRUCTION_MANUAL.md). Each calculation is limited to its stated circuit and operating assumptions. No equipment approval or universal acceptance limit is implied.

## ARREST — Arrester voltage coordination

`Required MCOV = maximum VLL times entered LG multiplier; each margin is 100(capability/duty - 1).`

## BUSCHK — Bus continuous, short-time and peak duty

`I = 1000 MVA/(sqrt(3) kV); thermal duty = Isym^2 t; peak = entered multiplier times Isym.`

## CAPBANK — Capacitor bank selection at operating voltage

`Qneed = P(tan(acos(PF1))-tan(acos(PF2))); Qstep,op = Qstep,rated (Vop/Vrated)^2; Cdelta = Q/(3 omega VLL^2); Cwye = Q/(omega VLL^2).`

## CTBURD — CT burden and internal excitation demand

`Ifsec = Ifprimary Israted/Itap; Zdev = VA/Israted^2; Rext = 2 L r/1000 + Zdev PF; Xext = Zdev sqrt(1-PF^2); Vterminal=Ifsec |Zext|; Vinternal=Ifsec |Zext+RCT|; Voffset=(1+X/R) Vinternal.`

## DCLOAD — Sequential battery duty and charger calculation

`Aremoved = sum(Ai ti/60). For each endpoint s, Fs=sum((Ap-Ap-1) Kt), with A0=0 and t measured from start of period p to end of section s. Required rated Ah=(max Fs+random-duty size Ah) temperature aging design. Charger=[Aremoved recharge/recharge-hours+continuous recharge load] charger-design altitude.`

## FAULT3 — Three-phase and sequence fault currents

`I3pu=c/|Z1+Zf|; ILGpu=3c/|Z1+Z2+Z0+3Zf|; ILLpu=sqrt(3)c/|Z1+Z2+Zf|; Ibase,kA=MVA/(sqrt(3) kV).`

## NGR — Neutral resistor and capacitive charging duty

`VLG=1000 kVLL/sqrt(3); R=VLG/IR; IC=3 omega Cphase VLG; Itotal=sqrt(IR^2+IC^2); P=VLG IR; E=P seconds.`

## SPHERE — Single-mast or equal-support rolling-sphere section

`Single: offset=sqrt(2Rh-h^2)-sqrt(2Rhe-he^2), h=min(hmast,R). Equal supports: ymid=hmast+sqrt(R^2-(d/2)^2)-R; dmax=2sqrt(2Rdh-dh^2) for dh<R, otherwise 2R.`

## VDROP — Receiving-end three-phase voltage-drop phasor

`Rhot=Rbase[1+alpha_base(Top-Tbase)]; R,X = per-kft values times length/(1000 n); I = 1000 MW/(sqrt(3) kV PF); Vs=Vr+(R+jX)I; loss=3 I^2 R.`

## XFMR — Concept transformer capacity and winding currents

`Total planning MVA=MWac/PF (1+margin/100); per-unit allocation=total/N; planning FLA=1000 MVA/(sqrt(3) kV).`

## ZSIZE — Transformer impedance from a downstream duty limit

`Ibase,kA=Sunit/(sqrt(3) kVLV); target=limit(1-headroom/100); budget=target-other; Zactual%=100 c N Ibase/budget; Znom%=Zactual/(1-tolerance/100); candidate=ceil(Znom/step) step.`

## PUBASE — Per-unit R/X base conversion

`Znew=Zold(Snew/Sold)(Vold/Vnew)^2; Zbase=kV^2/MVA; Ibase=1000 MVA/(sqrt(3) kV).`

## DCDROP — DC control-loop voltage and maximum length

`Rloop=2 L r/1000+Rother; Vdevice=Vs-I Rloop; Lmax=500[(Vs-Vmin)/I-Rother]/r.`

## PQSUM — Signed real/reactive power aggregation

`P=sum Pi; Q=sum Qi; |S|=sqrt(P^2+Q^2); I=1000 |S|/(sqrt(3) kV); |PF|=|P|/|S|.`

## WENNER — Wenner apparent resistivity

`rho=2 pi a R for shallow probes.`

## UNBAL — Line-voltage magnitude unbalance

`Average=(Vab+Vbc+Vca)/3; unbalance%=100 max(|Vi-average|)/average.`

## BUSAMP — Bus conductor heat-balance audit

`Ithermal=sqrt[(qc+qr+qconduction-qs)/(Rdc F)]; MVA=sqrt(3) kV I/1000.`

## REACTOR — Radial series-reactor impedance sizing

`Zs=V/(sqrt(3) Isc at 1pu); R=Zs/sqrt(1+(X/R)^2); X=R(X/R); required |Z|=c V/(sqrt(3) Ilimit); added X=max(0,sqrt(max(0,|Zreq|^2-R^2))-X); L=X/(2 pi f).`
