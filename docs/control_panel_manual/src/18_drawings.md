# 18. Reading Panel Drawings

## 18.1 The drawing set of a panel

Every panel is built from a set of drawings. The fitter, the wireman, the testing engineer and the maintenance technician must be able to read them. The set contains:

| Drawing | What it shows | Who uses it most |
|---|---|---|
| Single line diagram (SLD) | The power circuit in one line per circuit: incomers, busbars, feeders, ratings | Everyone; testing; customer |
| General arrangement (GA) | Front view, side view, plan, dimensions, door layout, cable entry, foundation details | Fabrication, assembly, site |
| Busbar drawing | Busbar sizes, routing, supports, joints, clearances | Busbar shop, assembly |
| Mounting plate layout | Device positions, ducts, DIN rails on each plate | Assembly, wiring |
| Power wiring diagram (three-line) | Each phase, neutral and earth of the power circuit, with device terminals | Wiring, testing |
| Control (schematic) diagram | Control circuits in ladder form: coils, contacts, lamps, PLC I/O | Wiring, testing, maintenance |
| Terminal plan | Every terminal strip with internal and external connections | Wiring, site cabling |
| Wire list / wire schedule | Every wire with number, size, colour, from, to | Wire preparation |
| Bill of materials (BOM) | Every item with tag, description, make, type, quantity | Stores, assembly, testing |
| Cable schedule (for site) | External cables with size and route | Site, customer |
| Nameplate / labels list | Text of every label | Engraving / printing |

## 18.2 Title block and revisions

Each sheet has a title block at the bottom right with: customer and project, panel name, drawing number, sheet number and total sheets, revision letter, date, names of drawn / checked / approved, and the "released for manufacturing" stamp.

Changes are shown with a **revision cloud** (a wavy line around the changed area) and a triangle with the revision letter. The revision table lists each revision, its date, a short description and the approver. When you receive a new revision, check every cloud and inform the people who already worked on the changed area.

## 18.3 Device designation

The drawings use letter codes for devices (based on IEC 81346-2), followed by a number. The same tag appears on the device label inside the panel.

| Letter code | Device type | Examples |
|---|---|---|
| Q | Switching power circuits | Q1 ACB, Q11 MCCB, Q12 MPCB, Q21 power contactor (in some standards K is used for contactors) |
| K | Relays and contactors in control circuits, timers | K1 auxiliary relay, K11 contactor, K5T timer |
| F | Protective devices | F1 fuse, F2 control MCB, F11 overload relay, F20 protection relay |
| T | Transformers | T1 control transformer, T11 CT |
| P | Measuring and indicating instruments | P1 multifunction meter, P2 ammeter |
| S | Manual switches and push buttons | S1 start button, S2 stop button, S3 selector switch |
| H | Indicating lamps, horns | H1 "ON" lamp, H2 "TRIP" lamp |
| X | Terminals and connectors | X1 terminal strip, X1:5 terminal 5 of X1 |
| M | Motors | M1 pump motor |
| A | Assemblies and electronic units | A1 PLC, A2 HMI |
| B | Sensors and transducers | B1 pressure switch, B2 level sensor |
| G | Power supplies | G1 24 V DC supply |
| U | Converters | U1 VFD, U2 soft starter |
| R | Resistors | R1 space heater |
| C | Capacitors | C1 capacitor bank step |
| E | Lighting, heating | E1 panel lamp |

## 18.4 Symbols

| Symbol (description) | Meaning |
|---|---|
| Two parallel lines with a line through (circuit breaker symbol with cross) | Circuit breaker (ACB, MCCB, MCB) |
| Square with a line through and a small semicircle | Contactor main contact |
| Rectangle with A1 / A2 | Coil of a contactor or relay |
| Contact with the moving blade open, numbered 13-14 | Normally open (NO) contact |
| Contact with the moving blade closed, numbered 21-22 | Normally closed (NC) contact |
| Rectangle with a zig-zag or thermal symbol, 95-96 / 97-98 | Overload relay; 95-96 NC trip contact, 97-98 NO alarm contact |
| Circle with a cross | Indicating lamp |
| Circle with M and 3~ | Three-phase motor |
| Two circles overlapping | Transformer |
| Circle on a line with S1/S2 (or a thick line through a ring) | Current transformer |
| Rectangle with a line through (fuse) | Fuse |
| Push button with a mushroom head | Emergency stop (latching) |
| Three horizontal lines decreasing (earth) | Protective earth connection |

## 18.5 Reading a control diagram

### 18.5.1 Layout

Control diagrams are drawn as **ladders**: the supply lines run along the top (phase, L or +24 V) and bottom (neutral, N or 0 V); each circuit is a vertical "rung" from top to bottom. The sheet is divided into **columns** numbered 0 to 9 along the top, so that every element has an address such as "sheet 12, column 4", written 12.4.

Contacts of a relay or contactor can be on different sheets from its coil. Under each coil a **contact mirror** (cross-reference table) lists its contacts and where they are used: for example under coil K11 on sheet 12.4, "13-14 / 12.5" means the NO contact 13-14 is used on sheet 12, column 5. Next to each contact, the reference shows where its coil is.

### 18.5.2 Contact numbering

| Number | Meaning |
|---|---|
| 1-2, 3-4, 5-6 (or L1-T1, L2-T2, L3-T3) | Main (power) contacts of contactors and breakers |
| A1 - A2 | Coil terminals |
| x3 - x4 | Normally open auxiliary contact (second digit 3-4); first digit is the position: 13-14, 23-24, 43-44 |
| x1 - x2 | Normally closed auxiliary contact: 21-22, 31-32 |
| x5 - x6 | Normally closed contact of a timer or overload: 95-96 (overload trip, NC), 55-56 (timer NC) |
| x7 - x8 | Normally open contact of a timer or overload: 97-98 (overload alarm, NO), 67-68 (timer NO) |
| 15-16-18 | Changeover contact of a timer (15 common, 16 NC, 18 NO) |
| 11-12-14 | Changeover contact of a relay (11 common, 12 NC, 14 NO) |

### 18.5.3 Example: DOL starter

[[fig:dol|Figure 18-1. Power and control circuit of a direct-on-line (DOL) starter|470]]

The DOL starter connects the motor directly to the supply through a contactor, with an overload relay for protection. Reading the control rung from top to bottom:

1. The control supply comes from the control MCB F2.
2. It passes through the **stop push button S2** (NC, 1-2) and the **emergency stop** (NC), so pressing either breaks the circuit.
3. It passes through the **overload relay NC contact F11 95-96**, so an overload trip breaks the circuit.
4. The **start push button S1** (NO, 3-4) is in series. In parallel with S1 is the **holding (self-latching) contact K11 13-14**.
5. Then the **contactor coil K11 A1-A2** to neutral.

Pressing S1 energises K11; K11 closes its main contacts (motor runs) and its auxiliary 13-14, which bypasses S1 so the motor keeps running after S1 is released. Pressing S2 or the emergency stop, or an overload trip, de-energises K11, which opens and drops its holding contact; the motor stays off until S1 is pressed again. Indicating lamps: H1 "RUN" through K11 23-24 (NO); H2 "TRIP" through F11 97-98 (NO).

### 18.5.4 Example: star-delta starter

A star-delta starter reduces the starting current of a large motor to about one third of the DOL starting current by starting the motor with its windings in star, then switching to delta when it has accelerated. It needs a motor with six terminals (U1 V1 W1, U2 V2 W2) rated for delta at the supply voltage.

| Contactor | Function | Closed during |
|---|---|---|
| KM1 (main / line) | Connects supply to U1, V1, W1 | Star and delta |
| KM3 (star) | Shorts U2, V2, W2 together (star point) | Star only |
| KM2 (delta) | Connects the winding ends to the supply so that the windings form a delta (W2 to L1, U2 to L2, V2 to L3) | Delta only |
| Timer KT | Sets the time in star (typically 5 to 10 s depending on load) | - |

Interlocks: KM2 and KM3 must never close together (that is a direct short circuit). The control circuit has an electrical interlock (NC contact of KM2 in KM3 coil circuit and NC of KM3 in KM2 circuit) and, on larger starters, a mechanical interlock between KM2 and KM3. The overload relay is placed in the line of the windings (phase current), set at 0.58 x motor full load current.

## 18.6 Reading the power diagram and SLD

On the SLD, check for each feeder: feeder number and name, device type and rating (for example "MCCB 160 A, 4P, 36 kA, TM release"), CT ratio and meter, cable size to the load, and starter type. The three-line power diagram shows each phase and terminal number: use it to wire and to test phase sequence and continuity.

| SLD item | Example | Meaning |
|---|---|---|
| Incomer | ACB 1600 A, 4P, EDO, 50 kA, microprocessor release LSIG | 4-pole air circuit breaker, electrically operated, draw-out, 50 kA breaking, release with long-time, short-time, instantaneous and ground fault protection |
| Busbar | 1600 A Cu, 50 kA / 1 s, TPN | Copper busbar, rated 1600 A, 50 kA short time 1 s, three phase and neutral |
| Feeder | MCCB 250 A, 3P, 36 kA, ETU | 3-pole moulded case breaker with electronic trip unit |
| Motor feeder | 30 kW, S/D, MPCB 63 A + KM 3 x 40 A + OLR 25-40 A | 30 kW motor star-delta starter |
| Metering | CT 1600/5 A, Cl 1.0, 15 VA; MFM | Current transformer ratio 1600 to 5 A, accuracy class 1.0, burden 15 VA; multifunction meter |

## 18.7 Terminal plan and wire list

The terminal plan shows, for each terminal, the internal wire (with its number and destination inside the panel) on one side and the external cable core (with the cable number and core number) on the other side. The wire list (from the design software) lists every wire with: wire number, size, colour, from (device:terminal), to (device:terminal), length. The wire preparation cell uses it to make kits (Chapter 15) and the testing engineer uses it for point-to-point checks.

## 18.8 Common mistakes when reading drawings

- Mixing up the NO and NC symbols, or reading a contact in its operated state. Drawings always show contacts in the **de-energised, unoperated** state (no power, breakers off, push buttons not pressed).
- Ignoring cross-references and assuming a contact belongs to the nearest coil.
- Working from an old revision.
- Confusing the device tag (K11) with the wire number (11).
- Overlooking notes on the drawing (for example "shield earthed at field end only").

## 18.9 Operator quick card

!! HINGLISH: Drawing hamesha "released for manufacturing" stamp aur sahi revision wali honi chahiye. Q matlab breaker, K contactor ya relay, F fuse ya overload, X terminal, S push button, H lamp, T transformer ya CT. 13-14 NO contact, 21-22 NC contact, 95-96 overload ka NC trip contact. Drawing mein contacts hamesha bina power wali halat mein dikhaye jaate hain. Coil ke neeche cross-reference dekho ki uske contacts kis sheet aur column par hain. DOL starter mein start button ke parallel K11 13-14 holding contact hota hai.
