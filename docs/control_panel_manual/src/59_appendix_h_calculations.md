# Appendix H. Worked Calculations for Technicians

Each example uses the formulas and values of this manual. Work through them in training; the answers show each step.

## H.1 Sheet weight

**Problem**: weight of a 1500 x 3000 mm sheet of 3.0 mm CRCA?
**Solution**: 1.5 m x 3.0 m x 3.0 mm x 7.85 = 106 kg. Handle with the vacuum lifter only (Chapter 5.4.1).

## H.2 Punching force

**Problem**: can PUNCH-02 punch a 96 x 96 mm meter cut-out in one hit in 2.0 mm CRCA?
**Solution**: perimeter 4 x 96 = 384 mm. Force = 384 x 2.0 x 350 / 1000 = 268.8 kN = about 27.4 tonnes. This is above the 80 % limit (24 t), so the cut-out is nibbled with a smaller tool or cut on LASER-03 (Chapter 7.7.2).

## H.3 Press brake force

**Problem**: force to bend a 1.6 mm CRCA side cover, 2000 mm long, with a V12 die?
**Solution**: force per metre = 64 x 1.6 x 1.6 / 12 = 13.7 t/m. Total = 13.7 x 2.0 = 27.3 tonnes. Well within 135 t; check the die rating (t/m) printed on the die (Chapter 9.7.1).

**Problem**: same part in stainless steel 304?
**Solution**: 13.7 x 1.5 = 20.5 t/m; total 41 tonnes.

## H.4 Flat length of a bent part

**Problem**: a door return profile in 2.0 mm CRCA has outside dimensions 20 + 600 + 20 mm with two 90 degree bends. Flat length?
**Solution**: 640 - 2 x 3.8 = 632.4 mm (Chapter 9.7.2).

**Problem**: a Z-bracket in 1.6 mm CRCA, outside dimensions 30 + 50 + 30 mm, two bends?
**Solution**: 110 - 2 x 3.0 = 104.0 mm.

## H.5 Busbar flat length

**Problem**: a U-shaped copper link 10 x 50 mm with outside dimensions 120 + 200 + 120 mm (two flat bends, radius 10 mm)?
**Solution**: 440 - 2 x (1.8 x 10) = 404 mm (Chapter 14.7.3).

## H.6 Busbar current density

**Problem**: first estimate of copper size for 800 A?
**Solution**: 800 / 1.6 = 500 mm2, for example 50 x 10 mm (guide rating 800 A in Chapter 32.3). The final size comes from the verified design.

## H.7 Motor current

**Problem**: full load current of a 22 kW motor at 415 V, PF 0.86, efficiency 0.92?
**Solution**: I = 22 000 / (1.732 x 415 x 0.86 x 0.92) = 22 000 / 568.7 = 38.7 A. The table in Chapter 19.6.2 gives 41 A as a typical value; use the nameplate for settings.

## H.8 Star-delta overload setting

**Problem**: a 37 kW motor with nameplate current 67 A on a star-delta starter with the overload relay in the winding circuit?
**Solution**: 0.58 x 67 = 38.9 A; set at 39 A (Chapter 19.6.1).

## H.9 Cable resistance and CT burden

**Problem**: CT 5 A secondary, meters 15 m away (30 m loop) with 2.5 mm2 copper. Wire burden?
**Solution**: R = 0.0175 x 30 / 2.5 = 0.21 ohm. Burden = I squared x R = 25 x 0.21 = 5.25 VA. Add the meter burden (for example 1 VA): total about 6.3 VA; a 10 VA CT is suitable, a 5 VA CT is not (Chapter 19.8.1).

## H.10 Power factor correction

**Problem**: plant load 300 kW at PF 0.82. kVAr to reach 0.98?
**Solution**: tan(acos 0.82) = 0.698; tan(acos 0.98) = 0.203. Q = 300 x (0.698 - 0.203) = 148.5 kVAr. Select an APFC panel of 150 kVAr in steps (for example 6 x 25 kVAr), detuned if the plant has many drives (Appendix C.1, Chapter 19.15).

## H.11 Short-circuit level

**Problem**: prospective fault current at the LT terminals of a 1000 kVA, 433 V, 5.5 % transformer?
**Solution**: 1000 / (1.732 x 0.433 x 0.055) = 24.2 kA. A panel near this transformer needs breakers and busbars rated for at least 25 kA plus motor contribution; the design team calculates the exact value (Chapter 32.2).

## H.12 IDMT relay operating time

**Problem**: standard inverse relay, current setting 200 A, TMS 0.2, fault current 2000 A. Trip time?
**Solution**: I / Is = 10. t = 0.14 x 0.2 / (10^0.02 - 1) = 0.028 / 0.0471 = 0.59 s (Chapter 19.10).

## H.13 Panel ventilation

**Problem**: a VFD panel has 1200 W of losses; allowed temperature rise 10 K. Required fan airflow?
**Solution**: 3.1 x 1200 / 10 = 372 m3/h at the actual filter pressure drop (Chapter 19.17).

## H.14 Hydraulic cylinder force and speed

**Problem**: cylinder bore 100 mm, pressure 180 bar, pump 30 l/min. Force and extend speed?
**Solution**: area = 3.1416 x 5 x 5 = 78.5 cm2. Force = 180 x 78.5 x 10 = 141 300 N, about 14.4 t. Speed = 30 / 78.5 x 10 = 3.8 m/min, about 64 mm/s (Chapter 26.1).

## H.15 Pneumatic clamp force

**Problem**: 50 mm bore clamp cylinder at 6 bar, efficiency 0.9?
**Solution**: area = 3.1416 x 2.5 x 2.5 = 19.6 cm2. Force = 6 x 19.6 x 10 x 0.9 = 1060 N. At 4.5 bar: 795 N (Chapter 27.1.2).

## H.16 Compressed air leak cost

**Problem**: leaks total 0.6 m3/min in a plant whose compressor gives 2.5 m3/min with 15 kW. If the compressor runs 6000 hours per year and electricity costs 8 per kWh, what do the leaks cost?
**Solution**: leak share = 0.6 / 2.5 = 24 %. Energy = 0.24 x 15 kW x 6000 h = 21 600 kWh. Cost = 21 600 x 8 = 172 800 per year (Chapter 23.2.6).

## H.17 OEE

**Problem**: LASER-03: planned 450 min, downtime 30 min, set-ups 20 min; ideal time per sheet 4 min; 90 sheets cut, 2 rejected. OEE?
**Solution**: running time 400 min. Availability = 400 / 450 = 88.9 %. Performance = 4 x 90 / 400 = 90.0 %. Quality = 88 / 90 = 97.8 %. OEE = 0.889 x 0.900 x 0.978 = 78.2 % (Chapter 46.2).

## H.18 Phosphate coating weight

**Problem**: test panel 100 x 150 mm weighs 54.3120 g before stripping and 54.2550 g after. Coating weight?
**Solution**: difference 0.0570 g; area of both faces 0.03 m2. Coating weight = 0.057 / 0.03 = 1.9 g/m2, within 1.5 to 2.5 (Chapter 12.8.1).

## H.19 Earth fault loop

**Problem**: C32 MCB on a 230 V circuit. Maximum earth fault loop impedance for instantaneous tripping?
**Solution**: a C curve trips instantly at up to 10 x In = 320 A. Zs maximum = 230 / 320 = 0.72 ohm (Chapter 45.6).

!! HINGLISH: Ye examples training ke liye hain: sheet ka wazan, punch aur press brake ka force, flat length, motor current, overload setting, CT burden, kVAr, short circuit, relay time, fan airflow, hydraulic force, air leak ka kharcha, OEE. Har formula manual ke chapter se hai; khud hal karke jawab milao.
