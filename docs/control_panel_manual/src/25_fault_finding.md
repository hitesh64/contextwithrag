# 25. Fault Finding: Methods and Instruments

## 25.1 A systematic method

Good technicians are not lucky; they are systematic. The same six steps work for a press brake that does not bend, a panel feeder that does not start, and a compressor that trips.

1. **Collect information**: talk to the operator. What exactly happened? When? Any alarm code, noise, smell? What was the machine doing? Has it happened before (check the breakdown history)? Has anything been changed recently (new program, new tool, repair, power cut)?
2. **Observe safely**: look at the machine, the alarm screen, the indicator lamps, PLC LEDs. Do not start dismantling yet.
3. **Think of possible causes**: use the drawings and this manual. List the causes from the most likely and easiest to check to the least likely and hardest.
4. **Test to narrow down**: measure, do not guess. Use the half-split method (section 25.2). Each test should rule out half of the remaining possibilities.
5. **Repair and test**: fix the cause, not only the symptom. Check that the machine works in all modes, and that the safety functions work.
6. **Record and prevent**: write the breakdown record (Chapter 24.5). Ask why it happened and how to prevent it.

!! WARNING: Fault finding often needs measurements on live circuits. Measure live only when the measurement cannot be done dead, with a permit, correct PPE, CAT III instruments and insulated probes with finger guards and short exposed tips (4 mm or less). Every repair is done dead, under LOTO.

## 25.2 The half-split method

When a signal must pass through a chain of elements (a control circuit with ten contacts in series, a hydraulic line with several valves, a long cable with several terminals), test in the middle of the chain first. If the signal is present in the middle, the fault is in the second half; if not, in the first half. Then test in the middle of the faulty half, and so on. A chain of 16 elements is reduced to the faulty element in at most 4 measurements, instead of up to 16 when testing one by one from the start.

## 25.3 Fault finding in control circuits

### 25.3.1 Voltage method (live)

With the control supply on and the start command given, measure the voltage from the neutral (or 0 V) to points along the circuit, starting at the supply.

[[fig:voltage_method|Figure 25-1. Voltage method: measuring from neutral along a control rung|440]]

- Voltage present before a contact and absent after it, with the contact supposed to be closed: that contact is open (faulty or not operated).
- Voltage present at A1 of the coil but the coil does not pull in: measure between A1 and A2. If full voltage is across the coil, the coil is open or the contactor is mechanically jammed. If no voltage across A1-A2 but voltage at A1 to neutral, the neutral connection at A2 is open.

### 25.3.2 Resistance method (dead)

With the circuit isolated and locked, check continuity of each contact and wire with the ohmmeter, operating the push buttons and contacts by hand. This method is safe but cannot find faults that appear only under voltage or load.

### 25.3.3 Common control circuit faults

| Fault | Typical cause |
|---|---|
| Control MCB trips immediately on closing | Short circuit or earth fault in control wiring (pinched wire, water in a field push button station), faulty coil |
| Control MCB trips when a particular device operates | That device's coil is shorted, or a wire downstream of its contact is shorted |
| Contactor chatters | Low voltage on coil, loose wire in holding circuit, bad contact in emergency stop chain |
| Motor starts but stops when start button is released | Holding contact (13-14) not wired or faulty |
| Motor cannot be stopped | Stop button contact welded or bypassed, contactor main contacts welded, wrong wiring (stop button in wrong rung) |
| Intermittent stopping | Loose terminal in series chain, vibration on a limit switch, failing overload relay |

## 25.4 Measuring instruments

### 25.4.1 Measurement categories

Instruments are rated by measurement category (CAT). Use an instrument rated for the place you measure:

| Category | Where | Minimum for this plant |
|---|---|---|
| CAT II | Plug-in equipment, sockets | - |
| CAT III | Distribution boards, machine panels, motors, fixed installation | CAT III 600 V for all panel work |
| CAT IV | Origin of installation: incoming supply, main LT panel incomer, outdoor cables | CAT IV 600 V for main LT panel incomer |

### 25.4.2 Multimeter

| Measurement | Notes |
|---|---|
| AC voltage | Use the V AC range; true RMS meters read correctly on drive outputs and distorted waveforms |
| DC voltage | Polarity: red lead on positive; useful for 24 V DC circuits and VFD DC bus (with care) |
| Resistance / continuity | Only on dead circuits; disconnect parallel paths (other circuits) or the reading is misleading |
| Diode test | Checks diodes, freewheeling diodes on DC coils |
| Current (with leads) | Avoid; use a clamp meter. Never put a multimeter on the current range across a voltage: it shorts the supply |

Before each use, check the leads for damage and do the "test - test - test" (Chapter 3.4.2) when proving dead.

### 25.4.3 Clamp meter

A clamp meter measures current without breaking the circuit, by clamping around one conductor.

- Clamp one conductor only: clamping a whole cable (phase and neutral) gives zero.
- Compare the three phase currents of a motor: a difference of more than 10 % between phases indicates a supply unbalance, a high-resistance connection, or a winding fault.
- Leakage measurement: clamping all live conductors (L1, L2, L3, N) of a circuit together with a leakage clamp meter shows the earth leakage current.

### 25.4.4 Insulation resistance tester (megger)

| Equipment | Test voltage | Minimum (guide) |
|---|---|---|
| 415 V motors | 500 V DC (1000 V DC for new motors) | 10 megohm (new: above 100 megohm) |
| 415 V cables | 1000 V DC | 100 megohm per km (higher for new cables) |
| Control circuits | 500 V DC | 2 megohm in service |
| New panels (factory test) | 1000 V DC main circuits | 100 megohm (Chapter 20) |

Procedure: isolate and lock; disconnect electronics (drives, PLCs, meters, SPDs); test; record the 1-minute value; discharge. For motors, also compare the **polarisation index** (PI = 10-minute reading / 1-minute reading) when the 1-minute value is doubtful: PI above 2 indicates dry, clean insulation; below 1.5 indicates moisture or contamination.

### 25.4.5 Other instruments

| Instrument | Use |
|---|---|
| Phase sequence indicator | Check L1-L2-L3 rotation before starting motors; wrong sequence reverses motors |
| Non-contact voltage detector | Quick check only; never use it alone to prove a circuit dead |
| Two-pole voltage tester (with LED and vibration) | Proving dead (approved tester with self-test) |
| Infrared thermometer / thermal camera | Hot connections, bearings, motors |
| Loop calibrator | Simulate and measure 4-20 mA signals |
| Tachometer | Motor and spindle speed |
| Vibration pen | Bearing and unbalance checks |
| Pressure gauges with test couplings | Hydraulic and pneumatic pressures |

## 25.5 Motors

### 25.5.1 Motor does not start

| Check | How |
|---|---|
| Supply at the starter output | Voltage on all three phases at the contactor output, when commanded |
| Contactor operation | Contactor pulls in? If not, see control circuit section |
| Overload relay | Tripped? Find why before resetting (Chapter 19.6) |
| Motor terminal connections | Isolate, check terminals in the motor box for burnt or loose connections |
| Winding resistance | Compare the three windings (U1-U2, V1-V2, W1-W2): equal within 5 % |
| Insulation | Megger each winding to earth |
| Mechanical | Isolate, turn the shaft by hand: free? Jammed load, seized bearing |

### 25.5.2 Motor runs hot or trips on overload

- Measure the current under load and compare with the nameplate. Higher current: mechanical overload, low voltage, single phasing, winding fault.
- Check the voltage balance at the motor terminals (difference below 2 %). A 3 % voltage unbalance can increase motor heating by about 18 %.
- Check the cooling: fan cover clean, fins clean, fan not broken.
- Check the bearings: noise, temperature, vibration.

### 25.5.3 Bearings

Most motor failures start as bearing failures. Signs: increasing noise (rumble, squeal, clicking), vibration, temperature above 80 degrees C at the bearing housing, grease leakage. Re-grease motors with grease nipples at the interval on the motor plate with the specified grease quantity: over-greasing causes overheating as much as under-greasing.

## 25.6 Sensors and encoders

### 25.6.1 Inductive proximity sensors

Machines use 3-wire DC inductive sensors (brown = +24 V, blue = 0 V, black = output) to detect positions (back gauge home, turret index, ram top dead centre).

| Test | Normal |
|---|---|
| Supply between brown and blue | 24 V DC (20 to 30 V) |
| Sensor LED | Lights when metal is in front |
| Output (PNP) between black and blue | About 24 V when target present, 0 V when absent |
| Output (NPN) between brown and black | About 24 V when target present |
| Sensing distance | Target within the rated distance (e.g. 2 mm for an M12 flush sensor); sensor not damaged by impact |

Common faults: sensor face damaged by a part, metal chips stuck on the face (reading always "present"), cable cut or crushed, connector loose or full of coolant, sensor loose in its bracket (distance changed).

### 25.6.2 Encoders and linear scales

Encoders measure the position of CNC axes. Faults show as following error alarms, position loss after power-on, or jerky movement. Check: connector and cable (shield intact, no oil inside connector), mechanical coupling between motor and encoder (loose coupling gives position errors), scale cleanliness (linear scales on BRAKE-04 must be kept free of oil mist and dust). Replace encoders only with the same type, and re-reference the axis after replacement.

## 25.7 Safety circuits

Light curtains, safety mats, interlocked guards and emergency stops are connected to **safety relays** or **safety PLCs** with redundant (dual-channel) circuits and monitoring. When a safety device is faulty, the machine will not start. The fault must be found and repaired; it must never be bypassed.

| Symptom | Check |
|---|---|
| Safety relay does not reset | Both channels closed? (Check each emergency stop and guard switch.) Feedback loop (EDM) closed, i.e. the contactors controlled by the relay are really off? Reset button wired and pressed after channels closed? |
| Light curtain red LED stays on | Alignment (transmitter and receiver facing each other at the same height), dirty lenses, damaged cable, an object in the field, mounting moved |
| Light curtain fault code | Read the code from the receiver display or LED pattern in the light curtain manual |
| Safety relay faults after a contactor change | Wrong contactor type (needs mirror contacts for feedback) |

After any repair of a safety device, carry out the full functional test of that device and record it with the supervisor's signature.

## 25.8 PLC-controlled machines

1. Look at the HMI alarm list and the alarm history (time, code, text).
2. Check the PLC status LEDs (Chapter 19.12.3).
3. Use the input LEDs as a "map": when the operator presses a button or a sensor is operated, the matching input LED should light. If not, the fault is in the field (device, wiring, supply). If yes, the signal reaches the PLC.
4. Use the output LEDs: if the program commands an output (LED on) but the actuator does not work, the fault is outside the PLC: fuse, wiring, interface relay, valve coil, contactor.
5. If inputs are correct and outputs are not commanded, the program is waiting for a condition (interlock, safety, step sequence). Check the HMI diagnostic page or, with authorisation, the program online (read only).

## 25.9 Intermittent faults

Intermittent faults are the hardest. Methods:

- Record every occurrence with time, machine state, temperature and what else was running (welding sets, compressor starting): patterns show the cause (for example a fault when the compressor starts suggests a voltage dip; a fault only in the afternoon suggests heat).
- Wiggle test: with the circuit monitored, gently move cables and connectors and tap relays; a change in signal shows the loose point.
- Thermal effect: heat (hair dryer) or cool (freeze spray) a suspected component while monitoring.
- Swap test: exchange a suspected plug-in relay or module with an identical one from a non-critical place: if the fault moves, the part is faulty.
- Check earthing and shields: many intermittent electronic faults are caused by interference from drives and welding.

## 25.10 Operator quick card

!! HINGLISH: Fault dhundhne ke 6 kadam: operator se poocho, dhyan se dekho, sambhavit kaaran socho, naap ke check karo (beech se aadha-aadha), theek karke test karo, record likho. Live measurement sirf permit, PPE aur CAT III meter ke saath; repair hamesha LOTO mein. Clamp meter se teeno phase ka current milao, 10 % se zyada farak matlab problem. Motor ka IR 500 V par 10 megohm se zyada hona chahiye. Light curtain ya E-stop kharab ho to bypass kabhi nahi, theek karo aur test karke supervisor se sign karao.
