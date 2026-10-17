# 20. Testing and Inspection of Panels (TEST-14)

## 20.1 Purpose

Every panel leaving the factory is tested. Testing proves that the panel was built as designed and that it is safe to energise. IEC 61439-1 calls these tests **routine verification**: they are done on every assembly, in addition to the **design verification** (type tests) that the designer has already carried out on the panel design. The testing engineer signs the routine test report, which is part of the dispatch documents and is often witnessed by the customer during the factory acceptance test (FAT).

## 20.2 Routine verification items (IEC 61439-1, clause 11)

| Item | What is verified | How in this plant |
|---|---|---|
| Degree of protection of enclosure | Gaskets, gland plates, covers, louvres as required for the IP code | Visual inspection with checklist |
| Clearances and creepage distances | Distances between live parts and to earth | Visual; measurement of doubtful points; dielectric test |
| Protection against electric shock and integrity of protective circuits | Barriers, shrouds; continuity of protective (earth) circuit | Visual; low resistance continuity test |
| Incorporation of built-in components | Devices as per BOM, correct ratings, mounted per maker's instructions | Visual against BOM and drawings |
| Internal electrical circuits and connections | Tightness of connections; correct wiring | Torque marks (100 %), random torque check (10 %), wiring check |
| Terminals for external conductors | Number, type, identification | Visual against terminal plan |
| Mechanical operation | Operation of mechanisms, interlocks, locks | Operate every device and interlock |
| Dielectric properties | Insulation withstands test voltage | Power frequency withstand (HV) test; insulation resistance |
| Wiring, operational performance and function | Complete and correct; functional | Wiring check; functional test with control supply |

## 20.3 The test bench TEST-14

[[fig:test_bay|Figure 20-1. Layout of the test bay with interlocked enclosure|440]]

The test bay in Bay 6 is a fenced area with interlocked gates. Inside, the panel under test is connected to the test equipment. Outside, at the test desk, the testing engineer controls the tests.

| Equipment | Data |
|---|---|
| AC dielectric (HV) tester | 0 to 5 kV AC, 50 Hz, 500 VA; adjustable trip current 1 to 100 mA; timer 1 to 600 s |
| Insulation resistance tester | 250, 500, 1000 V DC; range up to 100 gigaohm; CAT IV 600 V |
| Low-resistance ohmmeter (earth continuity) | Test current 10 A DC; resolution 1 milliohm |
| Micro-ohmmeter | 100 A DC, for busbar joint and contact resistance |
| Secondary injection test set | Current 0 to 100 A AC; voltage 0 to 300 V; timer; for releases and relays |
| Primary injection test set (shared) | 0 to 2000 A AC, low voltage; for CT ratio and polarity checks |
| Three-phase test supply | 415 V, 63 A, through isolating transformer and MCCB with 30 mA earth leakage relay; variable 0 to 450 V auto-transformer for control supply tests |
| DC test supply | 24 V, 110 V, 220 V DC, current limited |
| Phase sequence meter, multimeter (CAT III 1000 V), clamp meter | General |
| Calibrated torque wrenches | Random torque checks |

### 20.3.1 Safety system of the test bay

!! DANGER: The HV tester produces up to 5 kV, which is lethal. HV and live functional tests may be done only by authorised testing engineers, with the test bay gates closed and nobody inside the fence.

- The gates of the test bay are interlocked: opening a gate switches off the HV tester and the three-phase test supply.
- A red beacon and a horn on the fence operate when HV or test supply is on; a green beacon shows that the bay is safe.
- Emergency stop buttons at the test desk and at each gate.
- Insulating rubber mat (IS 15652, class for 3.3 kV) in front of the test desk.
- Earthing stick with insulated handle to discharge the panel after HV and IR tests.
- Only one panel under test at a time inside the bay.
- Test leads and clips are inspected daily; damaged leads are destroyed.

## 20.4 Order of tests

The tests are done in this order, because an earlier test can show a defect that would make a later test dangerous or misleading:

1. Visual and mechanical inspection
2. Protective circuit continuity (earth continuity)
3. Insulation resistance (before HV)
4. Dielectric (HV) test
5. Insulation resistance (after HV)
6. Wiring check (point-to-point) and control circuit IR
7. Functional tests with control supply
8. Protection device tests (releases, relays) by secondary injection, CT tests
9. Final inspection, cleaning, test report

## 20.5 Visual and mechanical inspection

Use the visual inspection checklist (Appendix B). Main points:

- Panel matches the GA: dimensions, doors, cut-outs, labels, cable entries, IP features (gaskets complete, unused holes plugged, filters on louvres).
- Devices match the BOM: make, type, rating, coil voltages, settings.
- Busbar sizes, phase order and colours, supports, shrouds, clearances (Table 16-2); torque marks on 100 % of joints.
- Random torque check: 10 % of busbar joints and power terminals with a calibrated wrench set to the specified value; the bolt must not turn. If any bolt turns, all joints of that panel are re-torqued and the assembly team is informed.
- Wiring: neat, numbered, ferrules, no damaged insulation, door loops free, no loose material inside.
- Mechanical operation: operate every breaker, switch, door lock, interlock, racking mechanism and shutter. Draw-out ACBs: rack to test, disconnected and connected positions.
- Cleanliness: no swarf, dust, wire offcuts or tools. Vacuum clean before electrical tests.

## 20.6 Protective circuit continuity

The protective circuit must be able to carry fault current from any exposed metal part to the main PE terminal with low resistance.

1. Connect one lead of the low-resistance ohmmeter (10 A DC) to the main PE terminal (the terminal where the site earth will be connected).
2. Touch the other lead on each exposed conductive part: each door (on a bare point or the door earth stud), each cover, each mounting plate, gland plates, frames of each section, earth terminals of devices (e.g. VFD PE terminals), and the PE terminals of outgoing feeders.
3. Record the readings.

**Acceptance**: each reading **0.1 ohm or less**. A higher reading means a missing or loose earth strap, paint under a contact, or a broken wire. Correct and retest.

## 20.7 Insulation resistance test

### 20.7.1 Preparation

1. Disconnect or isolate devices that could be damaged by the test voltage or that would give false low readings: electronic meters, PLCs and I/O, drives, soft starters, SPDs, power supplies, protection relays (unless the maker allows), capacitors, voltage indicators with electronic circuits, space heaters (or include them and record).
2. Close all breakers and switches so that all parts of the power circuit are tested.
3. Short together the phase bars (for the "all phases to earth" test) or test phase by phase as listed.

### 20.7.2 Test

| Measurement | Test voltage | Acceptance (plant standard) |
|---|---|---|
| L1 to (L2 + L3 + N + PE) | 1000 V DC | 100 megohm or more |
| L2 to (L1 + L3 + N + PE) | 1000 V DC | 100 megohm or more |
| L3 to (L1 + L2 + N + PE) | 1000 V DC | 100 megohm or more |
| N to PE | 1000 V DC | 100 megohm or more |
| Control circuits (230 V / 110 V) to PE | 500 V DC | 50 megohm or more |
| 24 V DC circuits to PE (with electronics disconnected) | 250 V DC | 10 megohm or more |

Apply the voltage for 60 seconds and record the value at 60 seconds. The IEC 61439-1 minimum (for the alternative insulation measurement method) is 1000 ohm per volt of the circuit's nominal voltage to earth, i.e. 0.23 megohm for 230 V; the plant standard values above are much higher because a new, clean, dry panel easily achieves them, and a lower value means a defect (damaged insulation, moisture, dirt, wrong connection).

!! WARNING: After each IR test, discharge the circuit with the earthing stick before touching it. Long cables and capacitive circuits hold a dangerous charge.

## 20.8 Dielectric (power frequency withstand) test

### 20.8.1 Test voltages

The test voltage depends on the rated insulation voltage Ui of the circuit (IEC 61439-1, Table 8).

| Rated insulation voltage Ui (line to line) | Dielectric test voltage, AC r.m.s. |
|---|---|
| Ui up to 60 V | 1000 V |
| 60 V to 300 V | 1500 V |
| 300 V to 690 V | 1890 V |
| 690 V to 800 V | 2000 V |
| 800 V to 1000 V | 2200 V |

For the main circuits of a panel with Ui = 690 V, the test voltage is 1890 V. Auxiliary circuits that are not connected to the main circuit are tested according to their own Ui (for example a 230 V control circuit with Ui 300 V: 1500 V; a 24 V DC circuit: 1000 V, or excluded where the electronics cannot be disconnected and the IR test is used instead).

**Duration**: the routine test applies the full test voltage for at least 1 second. The plant applies it for **5 seconds** as standard, and for 60 seconds when the customer specification requires.

### 20.8.2 Procedure

1. Complete the IR test with good results first. Never apply HV to a circuit with low insulation resistance.
2. Disconnect sensitive devices as for the IR test. Disconnect SPDs and capacitors.
3. Connect the HV lead to the circuit under test (phases connected together) and the return lead to the PE / frame. Test in the combinations: all phases + N to PE; each phase to the other phases + N + PE.
4. Set the trip current to 100 mA (or the value the HV tester and panel size need; large panels have higher capacitive current).
5. Leave the bay, close the gates, check the beacon, announce the test.
6. Raise the voltage smoothly from below half of the test voltage up to the full test voltage within a few seconds. Hold for the test duration. Reduce to zero smoothly and switch off.
7. Discharge with the earthing stick; then open the gates.

**Acceptance**: no flashover or breakdown (the tester does not trip and no sound or visible discharge occurs). A trip means a breakdown: find the cause (clearance too small, damaged insulation, tracking path, forgotten connection to earth, a device that should have been disconnected), correct it, and repeat IR and HV.

### 20.8.3 After HV

Repeat the IR test on the main circuits. The values must be similar to those before the HV test; a large drop shows damage from the HV test. Reconnect all disconnected devices and record this in the report (a forgotten disconnected SPD or meter fuse is a common finding at site).

## 20.9 Wiring check

1. Check every wire point-to-point against the wire list or the control drawing using a continuity tester (with the panel de-energised). Mark each checked wire on the drawing in green.
2. Check that no extra wires exist (wires not on the drawing).
3. Check wire numbers at both ends.
4. Check terminal tightness by tug test on a sample of 10 % (100 % for CT circuits).
5. Check CT shorting links: open for service (CT connected to meter) and shorting links in place for any CT whose meter is not yet fitted.

## 20.10 Functional tests

Functional tests check that the panel works as the drawings say, with the control supply connected and, where possible, the power circuit energised from the three-phase test supply without load (or with a test motor).

### 20.10.1 Control supply

1. Connect the control supply (or energise the control transformer from the test supply).
2. Measure the control voltage at the control MCB output: within +/- 5 % of nominal.
3. Measure 24 V DC at the power supply output: 24 V +/- 2 %.
4. Check the phase sequence of the voltage circuits at the meters with the phase sequence meter.

### 20.10.2 Feeder function tests

For each feeder, as per the control drawing:

- Local start / stop from the door push buttons; remote start / stop by simulating the remote contacts at the terminals; local / remote selector function.
- Indication lamps: ON, OFF, TRIP; correct colour as per drawing.
- Overload trip: operate the test button on the overload relay: contactor drops, TRIP lamp on, alarm contact closes; manual reset works.
- Emergency stop: every emergency stop stops its feeder(s) and must be reset before restart.
- Interlocks: electrical interlocks (e.g. star-delta, reversing, DG and mains changeover) checked by trying the forbidden operation: it must be prevented.
- Star-delta: check timer setting and changeover from star to delta with the dead time.
- Breaker accessories: shunt trip from the remote trip contact; UVR trips on removing voltage; auxiliary and alarm contacts change as per drawing.
- PLC panels: every input (simulate each field signal at the terminal, check the input LED and the PLC status), every output (force or command from the HMI with the project engineer, check the output LED and the relay or terminal), analogue signals (inject 4, 12 and 20 mA with a loop calibrator and read the value on the HMI).
- VFD and soft starter feeders: parameters loaded, start and stop from the panel controls, speed reference; run a test motor if available.

### 20.10.3 Meter and protection tests

- **Multifunction meters**: check CT ratio setting, PT ratio, wiring type; inject current and voltage with the secondary injection set and compare the reading.
- **ACB / MCCB electronic releases**: secondary injection through the test socket or with the maker's test kit: test the long-time (L), short-time (S), instantaneous (I) and ground fault (G) functions at the set values; check trip times against the curve.
- **Protection relays**: secondary injection of current at 2, 5 and 10 times the setting, record trip times; check output contacts and the trip of the breaker through the shunt trip.
- **CT polarity and ratio**: for important metering and protection CTs, primary injection test (inject e.g. 400 A in the primary of a 400/5 CT, measure 5 A secondary, check direction with the meter's power sign or with a polarity tester).
- **RCCBs**: trip test with RCD tester.
- **APFC**: relay settings, step switching sequence (simulate PF), contactor operation, discharge resistors (measure voltage decay), fans and thermostat.

## 20.11 Final inspection

- Re-check that all devices disconnected for testing are reconnected and all fuses fitted.
- Fit all covers, shrouds and barriers; close doors; check labels.
- Clean the panel inside and outside; touch up paint damage.
- Fix loose items (spare fuses, keys, handles, manuals) in a bag inside the panel, listed in the packing list.
- Fill in and sign the routine test report.

## 20.12 Routine test report

The report contains:

| Section | Content |
|---|---|
| Header | Customer, project, panel name, job number, drawing numbers and revisions, date |
| Ratings | Ue, Ui, Uimp, InA, Icw, frequency, IP, form |
| Visual and mechanical | Checklist results, random torque check results |
| Earth continuity | Table of points and readings (ohms) |
| IR before and after HV | Table of combinations, voltage, readings |
| HV test | Circuits, test voltage, duration, result |
| Wiring check | Done / punch points |
| Functional tests | Feeder by feeder results |
| Protection settings and tests | Settings applied and test results |
| Instruments used | Serial numbers and calibration due dates |
| Signatures | Testing engineer, quality manager, customer (if witnessed) |

## 20.13 Factory acceptance test (FAT)

When the order requires it, the customer's inspector witnesses the tests. The FAT is offered only after the internal tests are complete and passed. The testing engineer prepares: the drawings of the latest revision, the internal test report, calibration certificates of instruments, the BOM with device make lists, and the inspection and test plan (ITP) approved by the customer. Observations raised by the customer are recorded in the FAT punch list with the agreed action and target date, and the panel is released for dispatch only when the customer signs the release (or the punch points are closed and accepted).

## 20.14 Common failures at testing and their causes

| Failure | Typical cause | Responsible stage |
|---|---|---|
| Earth continuity above 0.1 ohm on a door | Earth braid missing or fixed on paint | Assembly |
| IR low on one phase | Wire insulation damaged by a sharp edge or pinched under a cover; dirt in a busbar support | Wiring, assembly |
| HV flashover | Clearance too small at a bolt end; forgotten SPD or meter; swarf | Assembly, testing preparation |
| Contactor does not pick up | Wrong coil voltage; wiring error | Stores / BOM, wiring |
| Wrong meter reading | CT ratio setting, CT polarity, wrong phase | Wiring, testing |
| Interlock not working | Mechanical interlock not adjusted; auxiliary contact wired NO instead of NC | Assembly, wiring |
| Door does not close | Device too deep, door handle hits device | Design, assembly |

Every failure is recorded in the test log with its cause. The quality department reviews the log monthly and works with the responsible stage to prevent repeats (Chapter 21).

## 20.15 Operator quick card

!! HINGLISH: Testing ka kram: visual check, earth continuity (har door aur plate 0.1 ohm se kam), IR test (1000 V DC par 100 megohm se zyada), HV test (690 V Ui ke liye 1890 V, 5 second), phir dobara IR, wiring check aur functional test. HV test sirf authorised engineer karega, gate band karke, koi andar nahi. Test ke baad earthing stick se discharge karo. Meter, PLC, drive, SPD jaise electronic saaman HV se pehle alag karo aur test ke baad wapas lagana mat bhoolo. Report par sign karo.
