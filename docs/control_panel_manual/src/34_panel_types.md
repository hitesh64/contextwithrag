# 34. Work Instructions for Specific Panel Types

The general chapters describe how every panel is built. Some panel types have their own special points. This chapter gives the extra instructions for each type. Follow it together with Chapters 16, 17 and 20.

## 34.1 APFC panel

### 34.1.1 Special features

- High heat from capacitors and especially detuned reactors (a 50 kVAr step with 7 % reactor dissipates about 300 to 400 W).
- Inrush currents when capacitors are switched; capacitor duty contactors are mandatory.
- Stored charge in capacitors.
- Harmonic resonance risk, controlled by detuned reactors.

### 34.1.2 Assembly instructions

1. Mount reactors at the bottom or in a separate ventilated compartment, and capacitors above them only if the drawing shows a barrier or air path; capacitors must not be heated by reactors (capacitor life halves for every 7 to 10 degrees C above its rated temperature).
2. Keep at least 25 mm (or the maker's value) between capacitor cans for air circulation; never mount capacitors touching each other.
3. Fit the fans at the top (outlet) and filters at the bottom (inlet); thermostat set at 35 degrees C to start the fans, and an over-temperature thermostat at 55 degrees C to switch off capacitor steps (as per drawing).
4. Each step: fuse or MCCB, capacitor duty contactor, reactor, capacitor. Wire size of each step sized for 1.5 x the capacitor rated current (to allow for harmonics and capacitance tolerance) or as per drawing.
5. The CT for the APFC relay is installed at the main incomer of the plant (on the customer side), on the phase stated in the relay manual. The panel provides the CT terminals with shorting links and a label "APFC CT: L1, P1 towards supply" (or as per relay).
6. Label each step with its kVAr and a warning: "Capacitors: wait 5 minutes after isolation".

### 34.1.3 Testing

| Test | Method | Acceptance |
|---|---|---|
| Capacitance of each step | Capacitance meter between each pair of terminals with contactor open, capacitor isolated | Within -5 % / +10 % of nameplate (as per capacitor maker) |
| Discharge | Charge step from test supply, disconnect, measure voltage decay | Below 50 V within the maker's time (1 to 3 minutes) |
| Contactor sequence | Simulate low PF with secondary injection at the relay CT input | Steps switch in one by one with the set delay; switch out when PF leading |
| Reconnection delay | Switch a step off and command on again | Not reconnected before the set delay (60 s or more) |
| Fans and thermostats | Heat the thermostat or adjust setting | Fans start; over-temperature switches steps off |
| IR and HV | Chapter 20, capacitors disconnected for HV | As Chapter 20 |

## 34.2 PLC and automation panel

### 34.2.1 Special features

- Sensitive electronics: ESD, heat, interference.
- Many signal wires, often hundreds of I/O points.
- Software (PLC program, HMI) is supplied by the automation team or the customer.

### 34.2.2 Assembly and wiring instructions

1. Mount the PLC rack on its own DIN rail with the clearances given by the PLC maker (typically 25 to 50 mm above and below for ventilation).
2. Separate the panel into zones: power (incomer, power supplies, contactors), control (PLC, relays), field terminals. Keep the 24 V DC and analogue wiring in separate ducts from 230 V AC wiring.
3. Use interface relays (plug-in) between PLC outputs and any load above 0.5 A or any 230 V load.
4. Power supplies: separate supplies (or electronic circuit protection channels) for the PLC, for field inputs and for field outputs, so that a field short circuit does not stop the CPU.
5. Earth the 0 V of the 24 V DC system at one point to the PE bar (unless the design specifies a floating system with insulation monitoring).
6. Shields of analogue cables: shield clamp bar near the cable entry.
7. Communication cables (Ethernet, Profibus) run in their own duct, with the bend radius of the cable maker, without sharp bends at the connectors.
8. Label every I/O terminal with the PLC address (for example "I0.3") in addition to the terminal number, if the drawing requires.
9. Fit a panel light and a service socket (230 V, with RCCB 30 mA) for the commissioning laptop.

### 34.2.3 Testing

- I/O check: every input simulated at the field terminal, every output commanded (Chapter 20.10.2), recorded in the I/O test sheet signed by the testing engineer and the automation engineer.
- Analogue check at 4, 12, 20 mA.
- Communication: network devices reachable (ping test), HMI communication, remote I/O.
- Power supply redundancy (if specified): switch off one supply, the system continues.
- Program version recorded in the test report; a backup copy of the program is stored with the job file.

## 34.3 VFD panel

### 34.3.1 Special features

- High heat (2 to 3 % of drive power).
- High-frequency switching: interference, motor cable shielding, bearing currents.
- Harmonic currents on the supply side.

### 34.3.2 Assembly instructions

1. Mount the drive vertically on a metal mounting plate (bare, unpainted contact area or earthing as per drive maker for EMC).
2. Keep the clearances above and below the drive as per the drive manual; no other device in the hot air path above the drive.
3. Panel ventilation sized for the total losses (Chapter 19.17); filter fans with filters cleaned easily from outside.
4. Input reactor or harmonic filter close to the drive input, as per drawing.
5. Motor cable: shielded; 360 degree shield clamp at the panel entry and at the drive; keep motor cables separate from other cables (at least 300 mm from signal cables outside the panel, 100 mm inside).
6. Braking resistor (if any) mounted on top of the panel or outside, with a guard, because it gets very hot; wire with high-temperature cable.
7. Bypass contactor (if specified): interlocked with the drive output contactor, mechanically and electrically, so that supply voltage can never reach the drive output.

### 34.3.3 Testing

Chapter 31.6.3 commissioning steps with a test motor. Check also: fan operation, drive heat sink temperature reading after 30 minutes run at load (if a load is available), parameters saved and printed.

## 34.4 PDB and feeder pillar

### 34.4.1 Special features

- Many outgoing feeders, usually with MCCBs or MCBs; simple control.
- Feeder pillars are outdoor: IP55, canopy, corrosion protection, often stainless steel or polyester powder in a thicker coat.

### 34.4.2 Instructions

1. Outdoor enclosures: gasket all doors and covers; canopy with overhang on all sides; double-roof or sun shield where specified to reduce solar heating.
2. Use stainless steel fasteners and hinges; door stays to hold doors open in wind.
3. Bottom: gland plates with cable glands; seal gaps against insects and rodents (mesh or sealing compound).
4. Space heater with thermostat and hygrostat to prevent condensation.
5. Paint: polyester powder 80 to 100 microns; salt spray report from the powder supplier on file.
6. Earthing: two external earth bolts (M10 or M12) on the base frame, labelled.
7. Test IP features: hose test where the customer requires (water from a nozzle at the specified pressure over the enclosure for the specified time; no water inside afterwards).

## 34.5 Withdrawable MCC modules

### 34.5.1 Special features

- Each module plugs onto the vertical droppers through power stabs and connects to the control circuit through a control plug.
- Positions: service (connected), test (power disconnected, control connected), isolated (both disconnected).
- Shutters cover the dropper stabs when a module is withdrawn.

### 34.5.2 Assembly instructions

1. Assemble each module on the bench with its devices and internal wiring; test it individually (continuity, function on the test bench with control supply).
2. Check the stab alignment with the dropper using the alignment gauge before inserting a module into the panel.
3. Insert each module slowly; it must move smoothly through test to service position without force. Check the contact pressure marks on the stabs after first insertion (even marks on all three stabs).
4. Check the shutters: they close automatically when the module is withdrawn, and can be padlocked closed.
5. Check the mechanical interlocks: module cannot be withdrawn or inserted with the breaker ON; door cannot be opened with the module in service and breaker ON.
6. Modules of the same size and type must be interchangeable: test by swapping two identical modules.

### 34.5.3 Testing

In addition to Chapter 20: test of each position (service, test, isolated) with indication; interlocks; shutter operation; interchangeability; earth continuity of each module to the frame in all positions where specified (earth contact before power stab contact during insertion).

## 34.6 Control desk

- Ergonomic layout as per drawing: the most used controls within easy reach; emergency stop in a clearly visible and reachable position.
- Mimic diagrams (if specified) printed or engraved, with lamps at the correct points.
- Cable entry from the bottom with gland plates; terminal strips at the back with access doors.
- Engraved labels for every push button and lamp, checked against the label list.

!! HINGLISH: APFC panel mein reactor ki garmi capacitor tak na pahunche, capacitor ke beech jagah rakho, har step par "5 minute ruko" label. PLC panel mein 24 V DC aur 230 V AC ke wire alag duct mein, PLC ke liye alag power supply, har I/O ka test sheet. VFD panel mein drive ke upar aur neeche khaali jagah, shielded motor cable, braking resistor bahar aur guard ke saath. Outdoor feeder pillar IP55, canopy, SS bolt, heater. Withdrawable module har position aur interlock ke saath test karo.
