# 37. Site Service and Commissioning Support

Service engineers of the factory visit customer sites to supervise installation, commission panels, and attend complaints during the warranty period. This chapter is their guide.

## 37.1 Before going to site

- Collect the as-built drawings, the routine test report, the protection setting chart, the BOM, the device manuals and the VFD parameter lists of the job.
- Carry the service kit: insulated tool kit, CAT III / IV multimeter, clamp meter, insulation tester, phase sequence meter, torque wrenches (with calibration valid), thermal camera, laptop with device software, spare fuses and common spares of the job, LOTO locks and tags, PPE including arc-rated face shield.
- Confirm with the customer: site readiness (foundation, cables laid, earthing ready), permit system, contact person, working hours.

## 37.2 Working at a customer site

!! WARNING: At a customer site, you work under the customer's permit-to-work and LOTO rules in addition to this manual. Never work on equipment that the customer's authorised person has not isolated and handed over under a permit. Apply your own personal lock on the isolation point as well.

- Attend the site safety induction.
- Do not operate the customer's switchgear (upstream breakers, transformers) yourself; ask the customer's authorised person.
- Keep a site diary: date, work done, persons present, problems, materials used.
- Get every test and handover document signed by the customer's representative.

## 37.3 Commissioning sequence

1. **Mechanical completion check**: panel positioned and fixed, sections joined, busbar links torqued and marked, earth connected at two points, cables terminated and glanded, covers fitted (Chapter 22.5).
2. **Pre-commissioning tests**: IR of busbars and incoming cable, IR of outgoing cables (each feeder, with the motor disconnected or included as agreed), continuity of earth, check of terminations torque (sample), check settings against the setting chart.
3. **Control supply energisation**: control circuits tested feeder by feeder without main power (as at FAT), now with the field devices connected: remote push buttons, interlocks from process, PLC signals.
4. **Main supply energisation** (by customer's authorised person): incomer closed, voltage and phase sequence checked.
5. **Motor feeders**: bump test for direction, then no-load run, then load run; record currents; check overload settings against actual motor nameplates (motors at site may differ from the design list).
6. **VFD feeders**: motor data from actual nameplate, auto-tune, direction, speed range, process signals.
7. **APFC**: CT connection and polarity checked at the actual incomer; relay set; steps switched in under real load; PF achieved.
8. **Thermal check**: after 24 hours of load, thermal imaging of all joints and terminations.
9. **Handover**: commissioning report signed, customer operators shown the operation and the safety points, spare keys and handles handed over.

## 37.4 Common site complaints and their causes

| Complaint | Usual causes | What to check |
|---|---|---|
| Breaker trips on motor start | Instantaneous setting too low for motor inrush; motor larger than design; wrong starter type | Settings, motor nameplate, starting current with clamp meter (peak hold) |
| Overload trips after some time | Setting lower than motor FLC; star-delta relay setting not 0.58 x FLC; motor overloaded; supply voltage low | Setting, actual current, voltage |
| Meter shows wrong current or negative power | CT ratio setting in meter, CT polarity, CT on wrong phase, voltage phase sequence | Meter setup, wiring at CT and meter |
| Contactor chatters | Low control voltage (long control cables), voltage drop when large motors start | Coil voltage during the event |
| Panel hot inside | Fans not running, filters blocked, ambient higher than design, louvres covered by site material | Fans, filters, ambient |
| Water inside outdoor panel | Gland plate not sealed, unused entries open, canopy missing, condensation without heater | Seals, heater, hygrostat |
| Earth leakage trips | Insulation fault in field cable or motor, wrong RCD type for drives, neutral-earth link in wrong place | IR of cables and motors, RCD type, N-PE link |
| VFD trips | See Chapter 19.13.4 | Fault log of the drive |
| APFC not improving PF | CT location or polarity, relay settings, failed capacitors, blown step fuses | CT and relay, capacitance of steps, fuses |
| Hot joint found by thermal survey | Link not cleaned or torqued at site, paint on contact surfaces, loose cable lug | Under LOTO: open, clean, re-torque (Chapter 16.4.4; case study 28.5) |

## 37.5 Warranty claims

1. Record the complaint with the job number, panel, feeder, description and photos.
2. Investigate on site: is it a product defect (factory) or a site cause (installation, operation, supply, environment)?
3. For a product defect: replace or repair under warranty; send the failed part to the factory with a red tag and the description; raise a customer complaint record (Chapter 21.6).
4. For a site cause: explain to the customer with evidence (readings, photos); offer chargeable service if requested.
5. Write the service report and get it signed.

## 37.6 Service report contents

| Section | Content |
|---|---|
| Customer, site, job number, panel | - |
| Date and duration of visit | - |
| Reason for visit | Commissioning / complaint / preventive service |
| Observations | With measurements and photos |
| Work done | Steps, tests, settings changed (old and new values) |
| Parts used | With warranty / chargeable |
| Pending points | With responsibility (factory / customer) and target date |
| Customer's signature | - |

!! HINGLISH: Site par customer ke permit aur LOTO niyam bhi maano, apna lock bhi lagao. Customer ki upar wali switchgear khud mat chalao. Commissioning kram: mechanical check, IR test, control supply test, main supply on, motor ki direction aur current, VFD, APFC, 24 ghante baad thermal check, handover report par sign. Shikayat aaye to pehle naapo aur photo lo, phir decide karo factory ki galti hai ya site ki.
