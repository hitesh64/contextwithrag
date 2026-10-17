# 1. Electrical Control Panels: Types and Components

## 1.1 What a control panel is

An electrical control panel is a metal enclosure that holds the switching, protection, control and measuring devices for an electrical installation or a machine. Power enters the panel through incoming cables or busbar trunking, is switched and protected by breakers, is distributed through busbars and cables to outgoing feeders, and is controlled by contactors, relays, drives and programmable controllers. The panel keeps live parts out of reach, protects the devices from dust and water, carries the heat of the devices away, and gives the operator a safe place to switch, see and adjust the installation.

The factory builds low-voltage panels, called LT panels in India: assemblies rated up to 1000 V AC and 1500 V DC, typically for 415 V three-phase, 50 Hz supplies. The design and testing of these assemblies follows IEC 61439, published in India as IS/IEC 61439. Part 1 of the standard gives the general rules, Part 2 covers power switchgear and controlgear assemblies (PSC assemblies such as PCC and MCC), and Part 3 covers distribution boards intended to be operated by ordinary persons.

## 1.2 Panel types made in the factory

| Panel type | What it does | Typical rating | Typical contents |
|---|---|---|---|
| PCC (power control centre) | Receives the main supply from the transformer or DG and distributes it to MCCs and large loads | 800 A to 4000 A | ACB incomers, bus coupler, MCCB outgoings, meters, CT, protection relays |
| MCC (motor control centre) | Starts, stops and protects motors | 400 A to 2500 A main bus | MCCB or MPCB per feeder, contactors, overload relays, DOL, star-delta, soft starter and VFD feeders |
| PDB / MLDB (power or main lighting distribution board) | Distributes power to sub-boards and lighting | 100 A to 800 A | MCCB incomer, MCB or MCCB outgoings, RCCB, energy meter |
| APFC panel | Keeps the power factor of the plant near unity by switching capacitor banks | 100 kVAr to 1000 kVAr | APFC relay, capacitor duty contactors, capacitors, detuned reactors, fuses or MCCBs |
| PLC / automation panel | Controls a machine or a process | Up to 63 A typically | PLC, I/O modules, power supplies, HMI, relays, terminals, network switch |
| VFD panel | Controls motor speed | 1 kW to 315 kW drives | VFD, line reactor or harmonic filter, input breaker, bypass contactors, cooling fans |
| Feeder pillar | Outdoor distribution in yards and streets | 100 A to 630 A | MCCB or fuse switch units, IP55 enclosure, canopy |
| Control desk | Operator station with push buttons, selectors and indicators | Control voltage only | Push buttons, lamps, selector switches, meters, HMI |

### 1.2.1 Fixed, plug-in and withdrawable designs

Panels are built in three main forms according to how a feeder can be removed.

- **Fixed design**: devices are bolted to the mounting plate. A fault in one feeder may need the whole section to be switched off for repair. This is the most economical design and suits PDBs and small MCCs.
- **Plug-in design**: a feeder unit plugs onto the vertical busbar through stabs. It can be replaced with less downtime, but only with the busbar dead or under strict procedures.
- **Withdrawable (draw-out) design**: each feeder sits in a module or drawer with service, test and isolated positions. The drawer can be pulled out to the test position, where control circuits are live but the power circuit is disconnected. Large MCCs for process plants use this design.

### 1.2.2 Forms of internal separation

IEC 61439-2 describes forms of internal separation, which say how busbars, functional units and terminals are separated from each other by barriers or partitions.

| Form | Separation provided |
|---|---|
| Form 1 | No internal separation |
| Form 2a / 2b | Busbars separated from functional units; terminals not separated from busbars (2a) or separated (2b) |
| Form 3a / 3b | Busbars separated from functional units, and each functional unit separated from the others; terminals with or without separation from busbars |
| Form 4a / 4b | As Form 3, plus terminals of each unit separated from the terminals of every other unit |

A higher form gives more safety during maintenance and stops a fault in one feeder from spreading, but needs more sheet metal, more barriers and more space. The form is written on the general arrangement drawing and must be built exactly as drawn.

## 1.3 Parts of a panel

### 1.3.1 Enclosure and structure

The enclosure is built from CRCA sheet, normally 2.0 mm for the frame and doors and 1.6 mm for covers and partitions, with 3.0 mm gland plates for heavy cables. Large panels use a frame of folded channels or a modular section system, with removable side, back and top covers. Base frames are made of 3 mm to 5 mm folded channel or ISMC section so the panel can be lifted, moved and grouted to the floor.

| Enclosure part | Purpose | Typical material |
|---|---|---|
| Frame / skeleton | Carries the weight of devices and busbars | 2.0 mm CRCA folded sections |
| Doors | Access to devices; carry meters and push buttons | 2.0 mm CRCA with neoprene gasket |
| Side, top and back covers | Close the enclosure | 1.6 mm CRCA |
| Mounting plate | Carries the devices inside a compartment | 2.0 mm or 2.5 mm GI or CRCA |
| Gland plate | Entry of cables through cable glands | 3.0 mm CRCA, or aluminium for single-core cables |
| Base frame | Lifting, levelling and floor fixing | 3.0 mm to 5.0 mm folded channel |
| Partitions and barriers | Internal separation | 1.6 mm CRCA or insulating sheet |
| Lifting hooks | Crane lifting of the shipping section | Forged eye bolts M12 to M20 |

### 1.3.2 Busbars

Busbars carry the main current through the panel. They are made from electrolytic tough pitch copper (EC grade) or aluminium alloy (E91E or equivalent). The factory's design guide uses a current density of 1.6 A per mm² for copper and 1.0 A per mm² for aluminium as a first sizing figure; the final size is always taken from the verified design of the assembly, because the allowable current depends on ambient temperature, enclosure ventilation and busbar arrangement.

- **Main horizontal busbars** run along the top or bottom of the panel line.
- **Vertical (dropper) busbars** carry current from the main bus to each feeder section.
- **Neutral busbar** is normally of the same cross-section as the phase bar up to 400 A, and of half section above that if the drawing allows it.
- **Earth (PE) busbar** runs the full length of the panel, normally at the bottom, and every section, door and mounting plate is bonded to it.

Busbars are supported on insulators made of DMC, SMC or epoxy, spaced so that the bars withstand the short-circuit forces given on the drawing (for example 50 kA for 1 second). Joints are made with high-tensile bolts, plain and spring washers, tightened to the torque values in Table 16-3.

### 1.3.3 Switching and protection devices

| Device | Function | Where used |
|---|---|---|
| ACB | Incomer and bus coupler protection, 630 A to 6300 A | PCC incomers |
| MCCB | Feeder protection, 16 A to 1600 A, adjustable thermal and magnetic releases | Outgoing feeders, MCC incomers |
| MPCB | Motor protection breaker with thermal and magnetic protection | Small motor feeders up to about 32 A |
| MCB | Small circuit protection, 0.5 A to 63 A | Control circuits, lighting, small loads |
| RCCB / ELCB | Earth leakage protection, 30 mA to 300 mA | Lighting and socket circuits |
| Switch disconnector fuse (SDF) | Isolation with fuse protection | APFC, older designs |
| Contactor | Switches a motor or load on and off many times | Motor feeders, capacitor steps |
| Overload relay | Protects a motor from overcurrent over time | With contactor in DOL and star-delta starters |
| Soft starter | Reduces starting current with thyristor control | Pumps, fans, compressors |
| VFD | Variable speed control | Conveyors, pumps, fans, machines |

Chapter 19 explains each device in detail for technicians.

### 1.3.4 Measuring and control devices

- **Current transformers (CT)** reduce line current to 1 A or 5 A for meters and relays. A CT secondary must never be opened while the primary carries current, because a very high voltage appears across the open terminals.
- **Multifunction meters** show voltage, current, power, energy, power factor and harmonics.
- **Protection relays** trip a breaker on overcurrent, earth fault, under-voltage or other abnormal conditions.
- **PLCs** read inputs (push buttons, sensors) and switch outputs (contactors, valves) according to a program.
- **Control transformers** supply 230 V or 110 V AC control circuits; **power supplies** give 24 V DC.
- **Push buttons, selector switches and indicating lamps** form the operator interface on the door.
- **Terminal blocks** connect the internal wiring to the external field cables.

## 1.4 Ratings written on every panel

Every panel carries a rating plate. The values on it are the promise the factory makes to the customer, so they must match the drawing and the routine test report.

| Rating | Meaning | Example |
|---|---|---|
| Rated operational voltage (Ue) | Voltage at which the assembly works | 415 V AC, 3 phase, 4 wire |
| Rated insulation voltage (Ui) | Voltage to which insulation tests refer | 690 V or 1000 V |
| Rated impulse withstand voltage (Uimp) | Lightning or switching surge the assembly withstands | 8 kV |
| Rated current of the assembly (InA) | Current the main busbar carries continuously | 1600 A |
| Rated short-time withstand current (Icw) | Short-circuit current the busbars withstand for a stated time | 50 kA for 1 s |
| Rated peak withstand current (Ipk) | Peak of the first short-circuit current loop | 105 kA |
| Rated frequency | Supply frequency | 50 Hz |
| Degree of protection | IP code of the enclosure | IP54 |
| Form of separation | Internal separation | Form 3b |
| Rated diversity factor | Fraction of feeder ratings that can be loaded at the same time | 0.8 |

### 1.4.1 IP codes

The IP code (IEC 60529) has two digits. The first gives protection against solid objects and dust, the second against water.

| First digit | Protection against solids | Second digit | Protection against water |
|---|---|---|---|
| 2 | Fingers, objects over 12.5 mm | 0 | No protection |
| 3 | Tools and wires over 2.5 mm | 1 | Vertically dripping water |
| 4 | Wires over 1.0 mm | 2 | Dripping water when tilted 15 degrees |
| 5 | Dust protected | 4 | Splashing water from any direction |
| 6 | Dust tight | 5 | Water jets |
| - | - | 6 | Powerful water jets |

Indoor industrial panels are commonly IP42 or IP54. Outdoor feeder pillars are IP55 with a canopy. The gaskets, door locks, cable glands and ventilation louvres together decide whether the panel reaches its IP rating; a single missing gland plug spoils the rating of the whole panel.

## 1.5 The life of a panel order

A customer order passes through the following stages. Each later chapter of this manual covers one or more of them.

1. **Enquiry and design**: the design team reads the customer's specification and single line diagram, chooses the devices, sizes the busbars and prepares the general arrangement (GA), power and control drawings and the bill of materials (BOM).
2. **Approval**: the customer approves the drawings. Production starts only on approved drawings ("released for manufacturing").
3. **Planning and purchase**: planning issues a job card and a production schedule; purchase orders devices and materials.
4. **Sheet metal fabrication**: shearing, punching or laser cutting, bending, welding and hardware insertion (Chapters 5 to 11).
5. **Surface treatment**: pre-treatment and powder coating (Chapters 12 and 13).
6. **Busbar fabrication**: cutting, punching, bending and sleeving or plating of busbars (Chapter 14).
7. **Assembly**: structure assembly, mounting of devices, busbar erection (Chapter 16).
8. **Wiring**: power and control wiring, ferruling, termination (Chapters 15 and 17).
9. **Testing**: inspection and routine tests, then customer inspection (FAT) when required (Chapter 20).
10. **Packing and dispatch** (Chapter 22).

!! NOTE: An order number (job number) is given to every panel. It is written on every job card, on every fabricated part's tag, on the busbar tags and on the test report. A part without a job number tag must not be used until the supervisor identifies it.

## 1.6 Common terms used on the shop floor

| Term | Meaning |
|---|---|
| Vertical / section | One column of a multi-section panel, usually 400 mm to 1000 mm wide |
| Shipping section | Group of verticals transported as one piece |
| Feeder | One outgoing circuit with its breaker and wiring |
| Module | A compartment of a feeder in a compartmentalised panel |
| Cable alley | Vertical space next to the modules for outgoing cables |
| Dropper | Vertical busbar that feeds the modules |
| Gland plate | Plate with holes for cable glands |
| Wire way / duct | Slotted PVC trunking that carries wires |
| Ferrule | Printed marker on the end of a wire |
| Lug | Crimped terminal at the end of a cable |
| Interlock | Mechanical or electrical arrangement that prevents a wrong operation |
| Punch list | List of open defects found at inspection |

!! HINGLISH: Control panel ek steel ki body hai jisme breaker, contactor, relay, meter aur PLC lagte hain. Power busbar se feeder tak jaata hai. Har panel ka ek job number hota hai, wo har part ke tag par likha hona chahiye. Bina tag ka part use mat karo, supervisor ko dikhao.
