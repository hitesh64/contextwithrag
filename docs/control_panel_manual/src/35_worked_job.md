# 35. Worked Example: A Complete MCC Job (J2617)

This chapter follows one invented job through the whole factory, with the documents and numbers produced at each stage. It shows how the procedures of the earlier chapters fit together. Job J2617 is a demonstration example; the customer and all data are invented.

## 35.1 The order

| Item | Value |
|---|---|
| Job number | J2617 |
| Customer | Sample Process Industries (invented) |
| Panel | MCC-2, cooling water and process pumps |
| Configuration | 6 verticals, front access, 2 shipping sections (V1-V3, V4-V6) |
| Dimensions | 6 x 800 mm wide = 4800 mm; height 2200 mm (plus 100 mm base frame); depth 600 mm |
| Ratings | 415 V, 3 phase, 4 wire, 50 Hz; InA 1250 A; Icw 50 kA for 1 s; Ui 690 V; Uimp 8 kV; IP54; Form 3b |
| Incomer | MCCB 1250 A, 4 pole, 50 kA, electronic release LSIG, with rotary handle and door interlock |
| Main busbar | Copper 80 x 10 mm per phase, neutral 40 x 10 mm, PE 50 x 6 mm |
| Feeders | 24 (see SLD summary) |
| Control supply | 110 V AC from control transformer 415/110 V, 1 kVA; 24 V DC 10 A SMPS for PLC interface |
| Finish | RAL 7035 structured polyester, 60 to 80 microns; base frame RAL 2000 |
| Delivery | 6 weeks from drawing approval; FAT witnessed by customer |

### 35.1.1 SLD summary

| Feeder | Load | Starter | Protection | Qty |
|---|---|---|---|---|
| F01 | Incomer | - | MCCB 1250 A, 4P, LSIG | 1 |
| F02 to F09 | Pumps 5.5 kW | DOL | MPCB 9-14 A + contactor 12 A AC-3 | 8 |
| F10 to F13 | Fans 7.5 kW | DOL | MPCB 13-18 A + contactor 18 A | 4 |
| F14 to F17 | Pumps 30 kW | Star-delta | MCCB 100 A + KM 3 x 40 A + OLR 25-40 A set 32 A | 4 |
| F18 to F21 | Cooling tower fans 22 kW | VFD 22 kW | MCCB 63 A (as per drive maker) + line reactor | 4 |
| F22 | Lighting DB | - | MCCB 63 A | 1 |
| F23, F24 | Spare | - | MCCB 100 A | 2 |

## 35.2 Design and release

The design team prepared: GA, busbar drawing, mounting plate layouts (24 modules), power and control diagrams (58 sheets), terminal plan, wire list (2312 wires), BOM (412 lines) and label list. The customer approved revision B with two comments (add an ammeter on each 30 kW feeder; change lamp colours to red = running). The drawings were released for manufacturing on day 9 with revision C.

!! NOTE: The lamp colour change (red = running) is a customer requirement against the plant standard green (Chapter 19.18). It is written on the first sheet of the control drawings and on the job card, so the wire kit, the label list and the testing engineer all follow it.

## 35.3 Sheet metal

### 35.3.1 Cutting list (excerpt)

| Part | Material | Qty | Machine | Program |
|---|---|---|---|---|
| Vertical frame member 2200 mm (9-fold) | CRCA 2.0 | 28 | LASER-03 | J2617-L01 |
| Horizontal frame member 800 mm | CRCA 2.0 | 24 | LASER-03 | J2617-L01 |
| Module door 800 x 400 | CRCA 2.0 | 24 | LASER-03 | J2617-L02 |
| Cable alley door | CRCA 2.0 | 6 | LASER-03 | J2617-L02 |
| Side covers | CRCA 1.6 | 2 | SHEAR-01 then PUNCH-02 | J2617-P01 |
| Back covers 800 x 2200 | CRCA 1.6 | 6 | SHEAR-01 then PUNCH-02 (louvres) | J2617-P02 |
| Module mounting plates | GI 2.5 | 24 | PUNCH-02 | J2617-P03 |
| Horizontal partitions | CRCA 1.6 | 30 | PUNCH-02 | J2617-P04 |
| Gland plates | CRCA 3.0 | 6 | SHEAR-01 | Manual |
| Base frame channels | CRCA 3.0 | 4 | SHEAR-01 then BRAKE-04 | J2617-B05 |

The nest reports showed utilisation of 84 % (L01), 79 % (L02) and 81 % (P03). Remnants of 2.0 mm larger than 300 x 300 mm were returned to the remnant rack.

### 35.3.2 Bending

BRAKE-04 program J2617-B01 for the 9-fold frame member used a gooseneck punch and V16 die. The first-off showed angles of 90.5 degrees in the middle and 90.0 at the ends on the 2200 mm part; the operator checked the crowning (Chapter 9.9) and corrected it; the second part measured 90.0 to 90.2 degrees along the length and was approved.

### 35.3.3 Welding and hardware

Doors: corners spot welded on WELD-05 (2.0 + 2.0 mm schedule: 7.1 mm face, 4.5 kN, 18 cycles), peel test passed at start of shift (nugget 6.2 mm). Base frame MIG welded on WELD-06 (3.0 mm parameters), lifting brackets 100 % inspected. PEM-07 inserted 312 M5 nuts, 96 M6 earth studs and 48 M8 studs; push-out test on first-off of each size passed. Masking caps fitted on all 96 earth studs.

## 35.4 Paint shop

| Record | Value |
|---|---|
| Bath log (shift 1) | Degreaser 16 points, 60 degrees C; phosphate TA 20, FA 1.0, accelerator 2.5 ml; final rinse 32 microsiemens per cm |
| Coating weight | 1.9 g/m2 |
| DFT readings (doors, sample of 5) | Average 68 to 74 microns, lowest 58 microns |
| Cross-cut | Class 0 |
| Solvent rub | Pass |
| Base frame | Separate batch at 1.0 m/min; rub test pass |
| Earth studs | 96 of 96 bare after unloading (checked) |

## 35.5 Busbars

| Bar | Size | Qty | Notes |
|---|---|---|---|
| Main horizontal L1/L2/L3 | 80 x 10 Cu | 2 lengths per phase (one per shipping section) + links | 4 holes 14 mm per joint, M12 |
| Main neutral | 40 x 10 Cu | 2 + link | 2 holes 14 mm |
| Droppers | 40 x 10 Cu | 18 (3 per vertical) | Bends 90 degrees flat, R 10 mm |
| Incomer links | 80 x 10 Cu | 6 | Edgewise bend to MCCB terminals |
| PE bar | 50 x 6 Cu tinned | 2 + link | Holes 11 mm every 100 mm |

Bars marked "J2617 / V3 / R-12" style (job, vertical, phase and bar number). Copper issued 412 kg; bars made 389 kg; offcuts returned 17 kg; scrap 5 kg; difference 1 kg (0.2 %), within the 1 % limit.

## 35.6 Wire preparation

2312 wires: 1.5 mm2 (1620), 0.75 mm2 (380), 2.5 mm2 CT (96), 4 to 16 mm2 power (216). Kits prepared per vertical. Crimp pull tests: 1.5 mm2 average 196 N (minimum 150 N), 2.5 mm2 average 288 N (minimum 230 N).

## 35.7 Assembly and wiring

| Activity | Duration | Notes |
|---|---|---|
| Structure assembly and doors | 3 shifts, 2 fitters | Diagonals within 1.5 mm |
| Busbar erection | 1 shift | 36 joints torqued (M12 at 75 Nm), all marked, torque record signed |
| Devices and modules | 2 shifts | Coil voltages checked: all 110 V AC as per BOM |
| Power wiring | 2 shifts | Star-delta feeders wired as per drawing after a design query (see note) |
| Control wiring | 6 shifts, 3 wiremen | Drawing yellowed; 4 wires circled red (terminal blocks short); punch list raised |
| Self-check | 1 shift | Signed |

!! NOTE: During wiring the supervisor noticed that the drawing showed 16 mm2 between the 100 A MCCB and the star-delta contactors, while Chapter 17.2.2 requires 35 mm2 for a 100 A protective device. A design query was raised; the design team confirmed that the MCCB release is set at Ir = 63 A (motor line current 55 A) and the drawing note allowed 16 mm2 for Ir up to 63 A, with the setting sealed. The note was made more visible in revision D. This is an example of the correct handling of a doubt (Chapter 32.9).

## 35.8 Assembly inspection and testing

### 35.8.1 Findings at assembly inspection

| Punch point | Action |
|---|---|
| Door 4C gap 4 mm at top | Hinge adjusted |
| Missing earth braid on cable alley door V5 | Fitted |
| 4 terminal blocks missing (X2 strip, V6) | Fitted, wires completed |

### 35.8.2 Test results (extract of the routine test report)

| Test | Result |
|---|---|
| Earth continuity | 31 points, maximum 0.028 ohm |
| IR before HV (1000 V DC) | L1: 4.2 gigaohm, L2: 3.8 gigaohm, L3: 4.0 gigaohm, N: 5.1 gigaohm |
| HV test, main circuits, 1890 V AC, 5 s | Passed, all combinations |
| HV test, 110 V control circuits, 1500 V AC, 5 s | Passed |
| IR after HV | No significant change |
| Wiring check | 2312 wires checked; 3 errors (2 wires to wrong NC/NO contact on F07, 1 wire number swapped) corrected |
| Functional tests | 24 feeders tested; star-delta timers set 8 s; VFD parameters loaded and run with test motor |
| MCCB incomer release (secondary injection) | L, S, I, G tested at set values; times within curve |
| Overload settings | Recorded per motor list; star-delta set at 32 A (0.58 x 55 A) |
| First-pass yield | Not first pass (3 wiring errors corrected) |

### 35.8.3 FAT

The customer's inspector witnessed the tests on day 34. Observations: (1) add "spare" labels on F23, F24 doors; (2) provide a printed parameter list for each VFD inside its module door. Both closed on the same day; release signed.

## 35.9 Packing and dispatch

Two shipping sections, each in a wooden frame with plywood sides, LDPE wrap and 4 kg silica gel per section. Main busbar links and M12 bolts packed in a labelled bag inside V3 with the instruction card "clean faces, torque to Table 16-3, mark". Dispatched on day 36.

## 35.10 Lessons recorded for the job

| Observation | Action for future jobs |
|---|---|
| Crowning correction on long frame members | Program template for 2200 mm members updated with correct crowning |
| 3 wiring errors found at testing | Wiring errors on NC/NO contacts discussed in toolbox talk; contact numbering card placed at wiring benches |
| Design query on cable size with sealed setting | Drawing standard changed: cable size notes printed next to the breaker symbol, not in the general notes |

!! HINGLISH: Is example mein ek MCC job shuru se dispatch tak dikhaya gaya hai: drawing release, cutting, bending, welding, paint, busbar, wire kit, assembly, testing, FAT aur packing. Har stage ka record banta hai. Jahan drawing aur manual mein farak dikha, wahan supervisor ne design query uthayi aur likhit jawaab liya; yahi sahi tarika hai.
