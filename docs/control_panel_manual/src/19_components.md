# 19. Control Panel Components: Technician's Guide

This chapter explains how the main devices of a panel work, how they are selected and set, how they are checked, and how they fail. It is written for wiremen, testing engineers and maintenance technicians. Always check the device maker's data sheet for the exact values of the device in your hands.

## 19.1 Miniature circuit breakers (MCB)

An MCB protects a circuit against overload and short circuit. Inside it there are two releases: a **thermal release** (a bimetal strip that bends when heated by overload current and trips the mechanism after a time), and a **magnetic release** (a coil that trips the breaker instantly when a short-circuit current flows). An **arc chute** splits and cools the arc when the contacts open.

### 19.1.1 Tripping curves

The curve letter says at which multiple of the rated current (In) the magnetic release trips instantly.

| Curve | Magnetic trip range | Use |
|---|---|---|
| B | 3 to 5 x In | Resistive loads, long cables, lighting, sockets in homes |
| C | 5 to 10 x In | General loads, control circuits, small motors, lighting with ballasts (standard in panels) |
| D | 10 to 20 x In | Transformers, high inrush loads (control transformers, capacitors, large SMPS) |

### 19.1.2 Ratings on an MCB

| Marking | Meaning | Example |
|---|---|---|
| C16 | Curve C, rated current 16 A | - |
| 10000 (in a box) | Rated short-circuit capacity per IEC 60898 | 10 kA |
| Icn / Icu | Breaking capacity | Must be equal or higher than the fault level at the point of installation, or backed up by an upstream device as per maker's tables |
| 1P, 2P, 3P, 4P | Number of poles | - |
| 230/400 V | Rated voltage | - |

### 19.1.3 Checks and failures

- Check that the toggle operates firmly and that the breaker does not trip on normal load.
- Measure contact voltage drop on load if overheating is suspected (more than 0.3 V across a closed pole at rated current indicates a problem).
- An MCB that has cleared several short circuits may be weakened: replace it after a severe fault.
- Typical failures: terminal screw loose (overheating, discoloured housing), nuisance tripping due to wrong curve (B instead of C for inrush loads), welded contacts after a short-circuit beyond its capacity.

## 19.2 Residual current devices (RCCB / RCBO)

An RCCB compares the current going out on the phase(s) with the current returning on the neutral, using a **core balance transformer**. If some current leaks to earth (through insulation failure or a person), the difference (residual current) produces a signal that trips the device.

| Sensitivity (IΔn) | Purpose |
|---|---|
| 10 mA / 30 mA | Protection of persons against electric shock (sockets, wet areas) |
| 100 mA | Protection against fire and of equipment |
| 300 mA | Protection against fire caused by earth leakage |

| Type | Detects |
|---|---|
| AC | Sinusoidal AC residual current only |
| A | AC plus pulsating DC (single-phase electronic loads) |
| F | As A plus mixed frequencies (single-phase drives) |
| B | As F plus smooth DC (three-phase drives, EV chargers) |

!! NOTE: An RCCB does not protect against overload or short circuit (unless it is an RCBO). It must be backed up by an MCB or fuse. Press the test button monthly: the device must trip. At testing, the trip current and time are checked with an RCD tester (30 mA device: trip at 15 to 30 mA, within 300 ms at IΔn).

## 19.3 Moulded case circuit breakers (MCCB)

MCCBs protect feeders from 16 A to 1600 A. They have a moulded insulating case, a spring-operated mechanism, arc chutes, and a **trip unit** (release).

### 19.3.1 Trip units

| Type | Settings | Notes |
|---|---|---|
| Thermal-magnetic (TM), fixed | None | Cheapest; used for small feeders |
| Thermal-magnetic, adjustable | Ir (thermal, 0.8 to 1 x In or 0.7 to 1 x In), Im (magnetic, 5 to 10 x In) | Common in distribution |
| Electronic / microprocessor (ETU, MP) | L: Ir and tr; S: Isd and tsd; I: Ii; G: Ig and tg (LSI / LSIG) | Precise, selective, with display and communication on some types |
| Motor protection release | Ir set to motor current, class 10 / 20, high magnetic | Used with a contactor; may replace a separate overload relay |

**L (long time)**: overload protection, tripping after a time that decreases as the current increases. **S (short time)**: delayed short-circuit protection for selectivity with downstream breakers. **I (instantaneous)**: high short circuits. **G (ground fault)**: earth fault protection based on residual current measured by the release.

### 19.3.2 Ratings

| Rating | Meaning |
|---|---|
| In | Rated current of the breaker (frame or release) |
| Icu | Ultimate short-circuit breaking capacity: the breaker can break this current once, but may then need replacement |
| Ics | Service short-circuit breaking capacity (as % of Icu): the breaker can break this current and continue in service |
| Ue | Rated operational voltage |
| Ui / Uimp | Insulation voltage / impulse withstand |

Select an MCCB with Icu at least equal to the prospective short-circuit current at its point of installation (shown on the SLD).

### 19.3.3 Accessories

| Accessory | Function |
|---|---|
| Auxiliary contact (OF) | Shows breaker ON / OFF state to the control circuit |
| Alarm / trip contact (SD) | Changes over when the breaker trips (not when switched off by hand) |
| Shunt trip (MX / ST) | Trips the breaker when its coil is energised (remote trip, emergency off) |
| Under-voltage release (MN / UVR) | Trips the breaker when the supply voltage falls; breaker cannot be closed without voltage |
| Rotary handle (door-mounted) | Operates the breaker through the door with door interlock and padlocking |
| Motor operator | Remote close and open |
| Spreaders, terminal shields, phase barriers | Increase clearances, protect against contact |

### 19.3.4 Setting an MCCB

1. Read the required settings from the SLD or the protection setting chart of the job.
2. Set Ir (thermal) with the dial or keypad; check against the load: for a feeder cable rated 200 A, Ir must not be above 200 A.
3. Set Im or Isd / Ii as specified.
4. For ETUs, record the settings in the test report; seal the setting cover if the customer requires.
5. Test the trip using the test button (push to trip) and, at testing, with secondary injection (Chapter 20).

## 19.4 Air circuit breakers (ACB)

ACBs are used as incomers and bus couplers from 630 A to 6300 A. They are usually **draw-out** in PCCs.

### 19.4.1 Construction

- **Main contacts and arcing contacts**: arcing contacts open last and close first, so the arc does not damage the main contacts.
- **Arc chutes**: split, cool and extinguish the arc.
- **Spring-charged stored-energy mechanism**: a closing spring is charged by a motor or a handle; releasing it closes the breaker in a few milliseconds independent of the operator's speed. The opening spring is charged during closing.
- **Microprocessor release** with LSIG protection, display, and test socket.
- **Cradle** (for draw-out): with three positions: **connected** (main and control circuits connected), **test** (main circuit disconnected, control connected: the breaker can be closed and opened for testing), **disconnected** (both disconnected). Safety shutters cover the busbar contacts when the breaker is withdrawn.

### 19.4.2 Operating sequence

1. Check the position indicator: connected.
2. Check the spring status indicator: "charged" (yellow). If "discharged", charge with the motor (automatic when control supply is present) or with the manual handle (about 7 to 10 strokes until the indicator changes).
3. Check "ready to close" indicator.
4. Close with the close push button (or remote close coil).
5. To open, press the open push button (or trip by protection, shunt trip, or UVR).

### 19.4.3 Racking in and out

!! WARNING: Rack out only when the breaker is OPEN. Most ACBs have an interlock that prevents racking with the breaker closed; never defeat it. Wear arc-rated face protection when racking a breaker in or out of a live cradle.

1. Open the breaker.
2. Insert the racking handle (the interlock trips the breaker if closed and blocks the handle until the breaker is open).
3. Turn the handle until the position indicator shows "test", then "disconnected". The handle stops at each position.
4. Remove the handle; padlock the shutters or the cradle as required for LOTO.

### 19.4.4 ACB maintenance (yearly, or after a major fault trip)

- Rack out to disconnected position, remove from the cradle (lifting trolley).
- Inspect arc chutes: remove, check for erosion and cracks, clean soot.
- Inspect contacts: check wear indicator; clean with a dry cloth; do not file silver-plated contacts.
- Check mechanism: lubricate as per maker (special grease only), operate 5 times manually.
- Check the release with secondary injection test set; download trip history.
- Check cluster (disconnect) contacts on the breaker and cradle: no burns, spring pressure correct, apply contact grease approved by maker.
- Measure contact resistance with a micro-ohmmeter at 100 A DC (compare with maker's value, typically below 50 micro-ohm per pole for 1600 A).
- Measure insulation resistance pole to pole and pole to earth.

## 19.5 Contactors

A contactor is an electrically operated switch for frequent switching of power circuits. A **coil** energised by the control circuit pulls an armature, which closes the **main contacts** against a spring; when the coil is de-energised, the spring opens the contacts. Contactors are rated by **utilisation category**:

| Category | Load | Typical use |
|---|---|---|
| AC-1 | Non-inductive or slightly inductive (heaters, resistive) | Heaters, distribution |
| AC-3 | Squirrel-cage motors: starting, switching off while running | Normal motor starting |
| AC-4 | Motors: plugging, inching | Cranes, hoists |
| AC-6b | Capacitor banks | APFC (use capacitor duty contactors with pre-charge resistors) |
| DC-13 / AC-15 | Control of electromagnets / coils | Auxiliary contacts |

| Selection item | Check |
|---|---|
| Rated operational current (AC-3) at 415 V | At least the motor full load current |
| Coil voltage | Matches the control supply (e.g. 230 V AC, 110 V AC, 24 V DC); a 24 V DC coil on 230 V AC burns at once |
| Auxiliary contacts | Number of NO and NC as per drawing |
| Mechanical interlock | For reversing and star-delta |
| Surge suppressor | RC module on AC coils or diode on DC coils when driven by PLC outputs |

### 19.5.1 Contactor faults

| Symptom | Cause | Check |
|---|---|---|
| Humming loudly | Low coil voltage, dirt on magnet faces, broken shading ring (AC coils) | Measure coil voltage at A1-A2 (should be within 85 to 110 % of rated); clean pole faces |
| Coil burnt | Wrong coil voltage, overvoltage, armature blocked | Check voltage and mechanical freedom |
| Does not pick up | No control voltage, open circuit in control chain, coil open | Measure voltage at A1-A2 with circuit commanded; coil resistance |
| Contacts welded | Short circuit, undersized contactor, contact bounce under low voltage | Replace contactor; check rating and coordination |
| Single phasing on motor | One main contact burnt | Measure voltage drop across each contact under load |

## 19.6 Overload relays and motor protection breakers

A thermal overload relay has three bimetals (one per phase) heated by the motor current. When the current exceeds the setting for long enough, the bimetals bend and operate the trip mechanism, which opens the NC contact 95-96 (in the contactor coil circuit) and closes the NO contact 97-98 (alarm). Most relays also include **single-phasing (phase loss) sensitivity**: if one phase is lost, the differential mechanism trips faster.

### 19.6.1 Setting

- Set the dial to the motor full load current (FLC) on the motor nameplate, at the actual supply voltage.
- In a star-delta starter where the relay is in the winding circuit, set to 0.58 x FLC.
- Trip class: Class 10 (trips within 10 s at 7.2 x setting) for normal starts; Class 20 or 30 for heavy starting loads (fans with large inertia).
- Reset: manual (H) or automatic (A). The plant standard is **manual reset** so that a motor does not restart by itself after cooling.

### 19.6.2 Typical motor full load currents (415 V, 3 phase, 4 pole, approximate)

| Motor kW | FLC (A) | Motor kW | FLC (A) |
|---|---|---|---|
| 0.37 | 1.1 | 11 | 21 |
| 0.75 | 1.8 | 15 | 28 |
| 1.5 | 3.4 | 18.5 | 34 |
| 2.2 | 4.8 | 22 | 41 |
| 3.7 | 7.5 | 30 | 55 |
| 5.5 | 11 | 37 | 67 |
| 7.5 | 14 | 45 | 82 |
| 9.3 | 18 | 55 | 100 |

!! NOTE: Always use the nameplate current of the actual motor for settings. The table is for estimating component sizes when the motor data is not yet known.

### 19.6.3 MPCB

A motor protection circuit breaker combines overload (adjustable thermal), short-circuit (magnetic), and isolation in one device, for motors up to about 15 kW (32 A). It is used with a contactor for remote control. Setting is the same as the overload relay.

## 19.7 Auxiliary relays and timers

- **Auxiliary (control) relays** multiply contacts and isolate circuits: a PLC output (24 V DC, 0.5 A) drives a relay whose contact switches a 230 V coil.
- **Interface relays** with plug-in sockets and LED indicators are used between the PLC and the field. A faulty relay is replaced by unplugging.
- **Timers**: on-delay (contact changes after the set time from energising), off-delay (contact returns after the set time from de-energising), star-delta timers (with a short dead time of 50 to 100 ms between star and delta), cyclic timers.

To test a relay: apply coil voltage and check that each contact changes with a continuity tester; measure coil resistance and compare with a new relay of the same type.

## 19.8 Current and voltage transformers

### 19.8.1 Current transformers

A CT has a primary (the busbar or cable passing through it, or a primary winding) and a secondary winding that gives a current proportional to the primary current: a 400/5 A CT gives 5 A in the secondary when 400 A flow in the primary.

| Specification | Meaning | Example |
|---|---|---|
| Ratio | Primary / secondary current | 400/5 A or 400/1 A |
| Accuracy class (metering) | Maximum error at rated current | Class 0.5, 1.0 |
| Accuracy class (protection) | Composite error up to accuracy limit factor | 5P10 (5 % error up to 10 x rated current) |
| Burden | Maximum load in VA that keeps the accuracy | 5 VA, 15 VA |
| Class PS | Special protection CT with knee point voltage | Differential and restricted earth fault protection |

The burden of the connected meters plus the wires must not exceed the CT burden. With 5 A secondaries, wire resistance matters: 10 m of 2.5 mm2 copper (go and return, 20 m) has about 0.15 ohm, which at 5 A uses 3.7 VA. For long distances 1 A secondaries are preferred.

### 19.8.2 Voltage transformers

PTs (VTs) are used in LT panels only when meters or relays need a reduced voltage (110 V). Most LT meters connect directly to 415 V through fuses. A PT secondary must never be short-circuited.

## 19.9 Meters

| Meter | Measures | Notes |
|---|---|---|
| Ammeter (analogue, 96 x 96 mm) | Current via CT | Scale matched to CT ratio |
| Voltmeter with selector switch | Phase-phase and phase-neutral voltages | Selector shows R-Y, Y-B, B-R, R-N, ... |
| Multifunction meter (MFM) | V, A, kW, kVA, kVAr, PF, Hz, kWh, THD | Set CT ratio and wiring type (3P4W) in the meter setup |
| Energy meter (class 0.5S / 1.0) | kWh, kVAh | Sealed by customer or utility |

Setting an MFM: enter the CT primary and secondary (e.g. 1600/5), PT ratio if any (1 for direct connection), system type (3 phase 4 wire), and communication address if used. Errors in the CT ratio setting are a common reason for wrong readings at site.

## 19.10 Protection relays

Numerical protection relays measure currents (and voltages) through CTs and PTs and trip the breaker through its shunt trip when settings are exceeded. Common functions in LT panels (with ANSI numbers):

| ANSI code | Function |
|---|---|
| 50 | Instantaneous overcurrent |
| 51 | Time overcurrent (IDMT: inverse definite minimum time) |
| 50N / 51N | Earth fault instantaneous / time |
| 27 / 59 | Under-voltage / over-voltage |
| 47 | Negative sequence voltage (phase reversal / unbalance) |
| 81 | Under / over-frequency |
| 86 | Lock-out (master trip relay; must be reset by hand) |
| 87 | Differential (transformer, generator) |

The IDMT curve "standard inverse" (IEC) gives a trip time t = 0.14 x TMS / ((I / Is)^0.02 - 1), where Is is the current setting and TMS the time multiplier setting. At 10 times the setting with TMS 0.1, t = 0.14 x 0.1 / (10^0.02 - 1) = 0.30 s.

## 19.11 Control power: transformers and power supplies

- **Control transformers** (415/110 V or 415/230 V) separate control circuits from the power circuit and give a reduced voltage. Size: the sum of the holding VA of all coils that can be energised together, plus the inrush VA of the largest coil (or as per maker's sizing table). Protect the primary with MCB curve D (inrush) and the secondary with MCB. One side of the secondary is earthed (protective earthing of control circuits) so that an earth fault trips the MCB instead of causing unintended operation.
- **SMPS (24 V DC power supplies)**: sized for the total load plus 30 % margin. Use separate supplies or electronic circuit protectors for PLC power and for field devices so that a field short circuit does not stop the PLC. The 0 V is earthed at one point.

## 19.12 Programmable logic controllers (PLC)

### 19.12.1 Parts

| Part | Function |
|---|---|
| Power supply module | Feeds the CPU and modules from 230 V AC or 24 V DC |
| CPU | Runs the program, stores data, communicates |
| Digital input (DI) modules | Read on/off signals (push buttons, limit switches, contacts) at 24 V DC |
| Digital output (DO) modules | Switch on/off loads: transistor outputs (24 V DC, 0.5 A) or relay outputs (2 A) |
| Analogue input (AI) | Reads 4-20 mA, 0-10 V, RTD, thermocouple |
| Analogue output (AO) | Gives 4-20 mA or 0-10 V to drives and valves |
| Communication modules | Ethernet, Modbus, Profibus / Profinet |

### 19.12.2 Sinking and sourcing

- **Sourcing (PNP) input sensor**: the sensor switches +24 V to the input; the input module's common is connected to 0 V.
- **Sinking (NPN) input sensor**: the sensor switches 0 V to the input; the module common goes to +24 V.

The module type and the sensor type must match the drawing. A PNP sensor on a module wired for NPN will never switch the input.

### 19.12.3 Diagnosis with LEDs

| LED | Normal | Fault meaning |
|---|---|---|
| RUN (green) | On | Off: CPU stopped |
| ERROR / SF (red) | Off | On: program fault, module fault, or missing module |
| BATT / BF | Off | Battery low / bus fault in communication |
| Input LED | On when the signal is present | No LED when the field device is operated: check field wiring and supply |
| Output LED | On when the program commands the output | LED on but load not working: check fuse, wiring, interface relay, load |

!! CAUTION: Do not change a PLC program, force outputs or replace a CPU at site without the authorisation of the project engineer. A forced output can start a machine unexpectedly. Modules are changed with the PLC switched off unless the maker allows hot swap.

## 19.13 Variable frequency drives (VFD)

### 19.13.1 How a VFD works

A VFD controls the speed of an AC motor by changing the frequency and voltage it supplies. It has three stages: a **rectifier** (diodes) converts the AC supply to DC; a **DC bus** with large capacitors smooths it (about 560 V DC for a 415 V supply); an **inverter** of IGBT transistors switches the DC on and off thousands of times per second (pulse width modulation, PWM) to create a variable frequency, variable voltage output to the motor. The motor speed is proportional to the frequency: a 4-pole motor runs near 1500 rpm at 50 Hz and near 750 rpm at 25 Hz.

!! DANGER: The DC bus capacitors stay charged after the supply is switched off. Before touching the terminals of a drive, wait at least the time printed on the drive's warning label and measure the DC bus voltage between the + and - terminals: it must be below 50 V DC.

### 19.13.2 Basic parameters

| Parameter | Typical setting |
|---|---|
| Motor nameplate data | Voltage, current, frequency, speed, power, cos phi (entered from the motor plate) |
| Control mode | V/f for pumps and fans; vector (sensorless) for conveyors and high starting torque |
| Minimum / maximum frequency | 10 Hz / 50 Hz (pumps often 25 Hz minimum) |
| Acceleration / deceleration time | 5 to 30 s depending on load |
| Start / stop command source | Terminals (from PLC or push buttons) or communication |
| Speed reference source | Analogue 4-20 mA, keypad, communication |
| Motor overload | Set to motor current |
| Auto-tune | Run with motor connected (static or rotating as allowed) |

### 19.13.3 Wiring rules

- Use the drive's recommended input protection (fuses or MCCB) and line reactor or harmonic filter where specified.
- Motor cable: shielded (or armoured) cable with the shield earthed at both ends with 360 degree clamps; keep it away from control wires (100 mm minimum).
- Do not install contactors between the drive and the motor unless the drive is stopped before they operate (bypass schemes only with interlocks).
- Do not install power factor correction capacitors on the output of a drive.
- Keep the clearance above and below the drive for cooling; check that cabinet ventilation removes the drive losses (about 2 to 3 % of the drive power).

### 19.13.4 Common drive faults

| Fault | Common causes |
|---|---|
| Overcurrent (OC) | Acceleration too short, motor or cable short circuit, motor blocked, wrong motor data |
| Overvoltage (OV) on DC bus | Deceleration too short for a high inertia load (motor regenerates); supply over-voltage. Increase decel time or add braking resistor |
| Undervoltage (UV) | Supply dip, loose input connection, input fuse blown |
| Earth fault (GF) | Motor winding or cable insulation fault; moisture in motor terminal box |
| Overheat (OH) | Blocked fan or filter, high cabinet temperature, overload |
| Motor overload (OL) | Mechanical overload, wrong current setting, low speed operation of self-cooled motor |
| Phase loss (input / output) | Blown fuse, loose terminal, broken motor cable core |
| Communication loss | Network cable, address, timeout setting |

## 19.14 Soft starters

A soft starter uses back-to-back thyristors in each phase to raise the motor voltage gradually during starting (ramp), reducing starting current (typically to 2.5 to 4 x FLC) and mechanical shock. After starting, an internal bypass contactor usually closes. Settings: initial voltage (30 to 50 %), ramp time (5 to 20 s), current limit, soft stop time (for pumps, to avoid water hammer). Soft starters do not control speed.

## 19.15 APFC panels

### 19.15.1 Why power factor correction

Inductive loads (motors, transformers) draw reactive power, so the supply current is larger than needed for the real power. Utilities penalise a low power factor. Capacitors supply reactive power locally and raise the power factor towards 1.

### 19.15.2 Parts

| Part | Notes |
|---|---|
| APFC relay | Measures PF via a CT on one phase (and voltage), switches capacitor steps to reach the target PF (e.g. 0.99) |
| Capacitor duty contactors | With pre-charge resistors and early-make contacts that limit inrush current when a capacitor is switched |
| Capacitors (MPP, gas-filled or heavy duty) | Rated at higher voltage (e.g. 480 V or 525 V) in detuned panels; with internal discharge resistors |
| Detuned reactors (7 % or 14 %) | In series with capacitors, to avoid resonance with harmonics from drives |
| Fuses or MCCB per step | Short-circuit protection |
| Cooling fans and thermostat | Capacitors and reactors are temperature sensitive |

### 19.15.3 Safety and checks

!! WARNING: Capacitors keep their charge after disconnection. The discharge resistors reduce the voltage to below 50 V within 1 to 3 minutes. Wait at least 5 minutes after isolation, then check each capacitor terminal voltage before touching, and short the terminals with an insulated shorting rod.

- The APFC relay must not reconnect a capacitor step before it has discharged (reconnection time setting, normally 60 s or more).
- Check capacitance of each step yearly with a capacitance meter (or by measuring current at known voltage): a capacitor below 90 % of rated value is replaced.
- Check the CT connection of the APFC relay: CT on the correct phase and correct polarity; voltage taken from the other two phases as per the relay's manual. Wrong CT phase is the most common cause of APFC "hunting" or no switching.

## 19.16 Surge protective devices (SPD)

SPDs protect against lightning and switching surges by diverting the surge current to earth through metal oxide varistors or spark gaps. Type 1 SPDs are for buildings with lightning protection at the main incomer; Type 2 at distribution boards; Type 3 near sensitive equipment. SPDs need a short, straight earth connection (total lead length below 0.5 m) and a back-up fuse or MCB as specified. A status window turns red when the SPD has reached its end of life.

## 19.17 Thermal management: heaters, fans and filters

| Device | Purpose | Setting |
|---|---|---|
| Space heater with thermostat | Prevents condensation when the panel is idle or in humid climates | Thermostat about 10 degrees C above dew point; often controlled by a hygrostat at 65 % RH |
| Fan with filter (inlet at bottom) and outlet filter (top) | Removes heat from devices | Thermostat at 35 degrees C |
| Panel air conditioner | For high heat loads or hot / dusty sites | Set 30 to 35 degrees C, not lower (condensation) |

Heat removed by a fan: required airflow (m3/h) is approximately 3.1 x heat loss (W) / allowed temperature rise (K). Example: 600 W device losses, allowed rise 10 K: 3.1 x 600 / 10 = 186 m3/h; select a fan with at least 186 m3/h at the actual filter pressure drop (the free-blowing value of the fan is much higher than the value with filters).

## 19.18 Push buttons, lamps and colours

Colours for operator devices follow IEC 60204-1 / IEC 60073 practice:

| Colour | Push button meaning | Lamp meaning |
|---|---|---|
| Red | Stop / off, emergency stop (red on yellow background) | Emergency, fault, trip |
| Green | Start / on | Normal, ready / running (plant standard; some customers use red for "breaker ON") |
| Yellow / amber | Abnormal condition intervention | Warning, abnormal |
| Blue | Mandatory action (reset) | Mandatory action |
| White / grey / black | General functions (not stop) | Neutral information |

!! NOTE: Some utilities and customers in India use red lamps for "breaker ON" and green for "breaker OFF" (the opposite meaning). The lamp colour scheme of each job is shown on the drawing: follow the drawing.

## 19.19 Operator quick card

!! HINGLISH: MCB curve C panel mein normal, D transformer ke liye. RCCB 30 mA insaan ki suraksha ke liye, har mahine test button dabao. MCCB mein Ir setting cable ki rating se zyada nahi. ACB ko sirf OFF halat mein rack out karo. Contactor ki coil voltage BOM se milao, 24 V DC coil 230 V par turant jal jaati hai. Overload relay motor nameplate current par set karo (star-delta mein 0.58 guna). CT ka secondary kabhi open nahi. VFD aur capacitor band karne ke baad bhi charge rehta hai: label par likha samay ruko aur voltage naapo, 50 V se kam hona chahiye.
