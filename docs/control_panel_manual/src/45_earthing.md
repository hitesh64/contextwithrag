# 45. Earthing and Bonding in Detail

## 45.1 Why earthing matters

Earthing has three jobs:

1. **Protection against electric shock**: if a live conductor touches a metal enclosure, the fault current flows through the protective earth (PE) conductor back to the source and trips the protective device quickly, before the enclosure voltage can hurt someone.
2. **System earthing**: the neutral (star point) of the transformer or generator is connected to earth, which fixes the system voltages relative to earth and allows earth faults to be detected.
3. **Functional earthing and EMC**: clean reference for electronics, shield earthing, and discharge of static (powder booth hooks).

## 45.2 Earthing inside a panel

| Element | Requirement |
|---|---|
| Main PE busbar | Full length of the panel; size as per drawing (for example 50 x 6 mm copper for a 1250 A MCC) |
| PE terminal for incoming earth conductors | At least two points (one at each end of long panels) |
| Section-to-section PE links | Bolted, torqued (Table 16-3) |
| Frames, doors, mounting plates, gland plates | Bonded to PE (Chapter 16.3.3) |
| Outgoing feeder PE terminals | One per feeder for the cable's protective conductor or armour |
| Cable armour | Earthed through glands and earth tags |
| CT star point | Earthed at one point at the CT terminal block |
| Control transformer secondary | One side earthed (protective earthing of control circuits) |
| 24 V DC 0 V | Earthed at one point (unless floating system is designed) |
| Shields | Shield earth bar (Chapter 17.5.5) |
| Neutral | Insulated from PE except at the designed N-PE link (Chapter 32.7) |

### 45.2.1 Size of protective conductors

Inside panels, the protective conductor of an outgoing feeder is sized as per the drawing; a common rule of IEC 60364-5-54 is:

| Phase conductor cross-section S | Minimum protective conductor (same material) |
|---|---|
| S up to 16 mm2 | S |
| 16 to 35 mm2 | 16 mm2 |
| Above 35 mm2 | S / 2 |

## 45.3 Plant earthing system

The plant earth system consists of earth electrodes (pits) connected by a buried copper or galvanised steel grid to the main earth bar in the utility room. Separate pits are provided for the transformer neutral (two pits), the transformer body, the DG neutral and body, the lightning protection system (connected to the grid at ground level), and the electronic (clean) earth if specified, bonded to the main grid.

| Earth | Number of pits (this plant) | Target resistance |
|---|---|---|
| Transformer neutral | 2 | Below 1 ohm combined with grid |
| Transformer body and LT panel | 2 | Below 1 ohm combined |
| DG neutral and body | 2 + 2 | Below 1 ohm combined |
| Machine earthing grid (bays) | 8 | Grid below 1 ohm |
| Lightning protection | 4 | Below 10 ohm each |

## 45.4 Testing earth electrodes

### 45.4.1 Fall of potential method (three-point)

1. Disconnect the electrode under test from the grid at its test link (only with the permit and when the installation's other earths keep the system safe).
2. Drive the current spike (C) into the ground at a distance of at least 10 times the electrode length (for a 3 m electrode, 30 m or more) and the potential spike (P) at 62 % of that distance, in a straight line.
3. Connect the earth tester (E to the electrode, P and C to the spikes) and measure.
4. Move P by 10 % closer and further; the readings should be nearly the same. If not, increase the C distance.
5. Reconnect the test link and tighten.

### 45.4.2 Clamp-on method

A clamp-on earth tester measures the resistance of an electrode in a multi-electrode grid without disconnection. It is quick for routine checks but requires a parallel earth path; it cannot be used on a single isolated electrode.

### 45.4.3 Records

The earth pit register records each pit's number, location, type, date, method, reading, soil condition (dry / wet) and action. Readings rising over time show corrosion of the electrode or connection; pits are improved (watering is a temporary measure; adding electrodes or chemical earthing is the permanent one).

## 45.5 Bonding

Equipotential bonding connects metal parts that could become live or that could introduce different potentials, so that no dangerous voltage appears between parts that can be touched at the same time:

- Machine frames to the earth grid (two connections per machine, Chapter 3.5.3).
- Metal pipes (water, compressed air, gas) at their entry into the building.
- Cable trays (bonded along their length and at both ends).
- Structural steel of the building.
- Powder booth, conveyor and hooks (static discharge, Chapter 13.5).
- Test bay fence and floor plates.

## 45.6 Earth fault loop and protection

For an earth fault to trip the protective device quickly, the earth fault loop impedance (from the source, through the phase conductor, the fault, the protective conductor and back) must be low enough. The required maximum loop impedance depends on the device (for example, a C16 MCB needs a current of at least 160 A to trip instantly, which at 230 V allows a loop impedance of at most about 1.4 ohm). Long cables with small protective conductors may not reach this; RCDs are then used. The design engineer checks this; the site engineer measures loop impedance on final circuits with a loop tester where required.

## 45.7 Common earthing faults

| Fault | Effect |
|---|---|
| Earth strap on painted surface | High resistance; doors can become live in a fault (Chapter 28.4) |
| Second N-PE link | Neutral current flows in PE, nuisance RCD trips, interference |
| Shield earthed at both ends in a signal circuit with earth potential difference | Circulating current, noise on signals |
| Armour not earthed at the gland | Armour can become live; no fault path |
| Corroded test link at the earth pit | High resistance of the whole earth |
| Lightning earth isolated from the main grid | Dangerous potential differences during a strike |

!! HINGLISH: Earthing se fault aane par breaker turant trip hota hai aur body par current nahi aata. Panel mein PE busbar, har door aur plate ka earth, cable armour ka earth gland par. Neutral aur earth ka link sirf ek jagah. Earth pit har 6 mahine test karo (fall of potential method) aur register mein likho. Paint par earth strap aur do jagah N-PE link sabse aam galtiyan hain.
