# 17. Electrical Wiring Practice

## 17.1 Purpose

Wiring connects the devices of the panel into the circuits shown on the power and control drawings. Good wiring is correct (every wire where the drawing says), safe (right size, right insulation, protected from damage), reliable (terminations that stay tight for decades), and easy to maintain (neat, numbered, traceable). This chapter is the plant standard for wiring; the customer's specification may add requirements, and those are written on the job card.

## 17.2 Wire sizes

### 17.2.1 Control and auxiliary circuits

| Circuit | Minimum wire size (copper, class 5, PVC 1100 V) |
|---|---|
| Control circuits 230 V / 110 V AC (contactor coils, lamps, push buttons) | 1.5 mm2 |
| Control circuits 24 V DC to PLC inputs and outputs | 0.75 mm2 (1.0 mm2 where specified) |
| Analogue signals (4-20 mA, 0-10 V, thermocouple extension as specified) | 0.5 or 0.75 mm2 shielded twisted pair |
| CT secondary circuits | 2.5 mm2 (4 mm2 for runs longer than 10 m or as specified) |
| PT / voltage sensing circuits | 1.5 mm2, protected by fuses or MCB at the tapping point |
| Control supply from busbar to control transformer or control MCB | 2.5 mm2, protected by fuse or MCB close to the tapping point |
| Space heater and lighting inside panel | 1.5 mm2 |
| Door earthing | 6 mm2 green-yellow or braid |

### 17.2.2 Power wiring inside the panel

Power connections from busbars to outgoing breakers and from breakers to outgoing terminals are made with single-core flexible copper cable, PVC insulated, 1100 V, when a busbar link is not used. The table is the plant minimum for an ambient of 50 degrees C inside the panel, cables in free air or in ducts with spacing; the drawing may require larger sizes.

| Protective device rating | Minimum copper cable size |
|---|---|
| Up to 16 A | 2.5 mm2 |
| 20 A and 25 A | 4 mm2 |
| 32 A | 6 mm2 |
| 40 A | 10 mm2 |
| 63 A | 16 mm2 |
| 80 A | 25 mm2 |
| 100 A | 35 mm2 |
| 125 A | 50 mm2 |
| 160 A | 70 mm2 |
| 200 A | 95 mm2 |
| 250 A | 120 mm2 |
| 315 A and above | Busbar links, or 2 x 150 mm2 per phase as per drawing |

!! CAUTION: Wire size follows the rating of the protective device upstream of the wire, not the actual load current. A 2.5 mm2 wire fed from a 32 A MCB is not protected against overload even if the load takes only 5 A today.

## 17.3 Colour code

The plant standard colours are below. The customer's specification may require a different code; the code of the job is always written on the wiring drawing's first sheet.

| Circuit | Colour |
|---|---|
| Power phases L1, L2, L3 | Red, yellow, blue |
| Power neutral | Black |
| Protective earth (PE) | Green-yellow |
| AC control circuits (phase side) | Red (or grey where specified) |
| AC control circuits (neutral side) | Black |
| DC control circuits, positive (+24 V) | Blue with plus marker or blue |
| DC control circuits, negative (0 V) | Blue with white stripe or white / grey as specified |
| Interlock circuits fed from an external source (remain live when the panel incomer is off) | Orange |
| CT secondary circuits | Phase colours with black for the star point, or as specified |
| Analogue signals | Shielded cable colours as supplied |

!! WARNING: Orange wires are live from another panel even when this panel's incomer is OFF. Every terminal strip carrying such wires has a warning label "Live from external source". Isolate the external source before working on these terminals.

## 17.4 Routing rules

1. **Follow the duct**: wires run inside slotted ducts on the mounting plate and leave the duct through the nearest slot opposite the terminal. No wire crosses diagonally over devices.
2. **Fill**: a duct is filled to at most 70 % of its cross-section. If a duct is full, ask for a larger duct; do not force the cover.
3. **Segregation**: keep power wiring, control wiring and signal (analogue, communication) wiring in separate ducts. Where they must cross, cross at right angles. Keep at least 100 mm between drive output (motor) cables and signal wires.
4. **Bending radius**: at least 4 x the outside diameter for single-core wires and flexible cables up to 10 mm2, and at least 6 x for larger cables.
5. **Slack**: leave enough length at each termination for one re-termination (about 50 mm hidden in the duct), but no loops outside the duct.
6. **Protection at edges**: where wires pass through metal (partitions, frames) use grommets or edge protectors; where they pass near sharp edges, add spiral wrap.
7. **Hot surfaces**: keep wires at least 50 mm away from resistors, heaters, and the heat sinks of drives.
8. **Busbars**: wires do not run on or touch busbars; keep at least the clearance in Table 16-2 and fix wires so they cannot move closer.
9. **No joints**: wires are continuous from terminal to terminal. Joints (twisting, soldering, connectors) in the middle of a wire are not allowed.
10. **Bunches outside ducts** (for example on doors or to devices outside the ducts) are tied with cable ties every 100 to 150 mm, with the cut end of the tie trimmed flush and facing away from hands.

### 17.4.1 Door wiring

Wires to door-mounted devices run as a flexible bundle from the duct on the mounting plate (or the frame) to the door, across the hinge side.

- Use extra-flexible wire (class 5 or class 6) for the hinge loop.
- Protect the bundle with spiral wrap or a flexible conduit over the hinge loop.
- Fix both ends of the loop with cable tie mounts (adhesive mounts plus screws), so that the bundle twists rather than bends sharply when the door opens.
- Check: open the door fully (beyond 110 degrees if possible) and close it. The bundle must not be pinched, stretched or rub on edges.
- Add an earth wire for the door (Chapter 16.3.3).

## 17.5 Terminations

### 17.5.1 General rules

- Every stranded wire end in a screw or spring terminal gets a ferrule or pin terminal of the right size (Chapter 15).
- One wire per terminal clamp unless the terminal is approved for two wires of the same size; in that case use a twin ferrule, never two ferrules in one clamp.
- Ring lugs on stud terminals: maximum two lugs per stud, back to back, with a washer and a spring washer under the nut.
- Insert the ferrule fully into the terminal so that no bare copper is visible outside the terminal and the insulation of the ferrule touches the terminal body.
- Tighten screws with a torque screwdriver to the device maker's value. Typical values for terminal blocks: 0.5 Nm (2.5 mm2 blocks, M3 screws), 0.8 Nm (4 mm2, M4), 1.2 to 1.5 Nm (6 to 10 mm2), but the maker's value applies.
- Pull test each wire by hand after tightening ("tug test"): a moderate pull must not move the wire.
- Spring-clamp terminals: insert the screwdriver into the release slot, insert the ferruled wire fully, remove the screwdriver, tug test.

### 17.5.2 Heavy cable lugs

For cables of 16 mm2 and above:

1. Strip the insulation to the barrel length of the lug plus 2 mm, without nicking strands.
2. Insert the conductor fully into the lug until it touches the bottom of the barrel.
3. Crimp with the hydraulic crimping tool using the hexagonal die marked with the cable size and lug type. Start the first crimp near the palm and work towards the open end; number of crimps as marked on the lug (normally 2 for 16 to 70 mm2, 3 for 95 mm2 and above).
4. Check: hexagonal shape fully formed, flash (thin fin at the die edge) small and even, no cracks in the lug, die marking (cable size) embossed on the barrel.
5. Cover the barrel and the end of the insulation with heat-shrink sleeve in the phase colour.
6. Connect with bolt, flat washers both sides and spring washer, tighten to Table 16-3 or to the device maker's value.

### 17.5.3 CT circuits

!! DANGER: Never open the secondary circuit of a current transformer while current flows in the primary. The secondary voltage rises to thousands of volts, which can kill and destroys the CT. Before disconnecting a meter or relay on a CT circuit, short the CT secondary with the shorting link on the CT test terminal block.

- CT secondary wires: 2.5 mm2 minimum, ring lugs on CT terminals and meters (no fork lugs).
- Every CT circuit passes through a **CT test (shorting) terminal block** with sliding links, so that meters can be changed and tested while the panel is live.
- The CT star point (S2 terminals) is earthed at one point only, at the CT test terminal block, with a green-yellow 2.5 mm2 wire.
- CT polarity: P1 faces the supply (source side), P2 faces the load. S1 and S2 are connected to meter terminals as per drawing. Wrong polarity gives negative power readings and wrong protection relay operation.

### 17.5.4 PT and voltage sensing circuits

- Voltage sensing taps from busbars are protected by fuses or MCBs placed as close as possible to the tapping point (within 300 mm), with 2.5 mm2 wire up to the fuse.
- Voltage circuits are wired in phase sequence L1-L2-L3-N to meters and relays; the testing engineer checks the phase sequence.

### 17.5.5 Shielded cables

- Terminate the shield (screen) at one end only (normally at the panel end) on the shield earth bar, unless the drawing says both ends.
- Strip the outer sheath only as far as needed; keep the unshielded length below 50 mm.
- Use shield clamps on the shield earth bar for drive and encoder cables (360 degree contact).

## 17.6 Terminal blocks for outgoing connections

| Item | Plant standard |
|---|---|
| Terminal type | DIN rail mounted screw or spring terminals, 2.5 mm2 to 16 mm2 for control; power terminals or direct breaker connection above 16 mm2 |
| Grouping | Separate strips for power, control (AC), control (DC), signals, CT, PT; each strip with end plates and end clamps |
| Spare terminals | 10 % spare terminals on each control strip (minimum 2) |
| Separators | Partition plates between groups of different voltages |
| Labelling | Strip number at the start (e.g. X1, X2) and each terminal numbered |
| Fuse and disconnect terminals | For PT circuits and where drawing shows |
| Earth terminals (green-yellow) | Mounted on the rail; connected to the earth bar |
| Distance from gland plate | At least 200 mm from the gland plate to allow spreading of field cores |

## 17.7 Wiring sequence at the panel

1. Read the wiring drawings and the wire list; check the wire kit against the kit card.
2. Wire the power circuits first (busbar droppers to breakers, breakers to contactors and overloads, to outgoing terminals), because they are the stiffest and take the most space.
3. Wire the CT and PT circuits.
4. Wire the control circuits sheet by sheet; on the drawing, mark each wire with a highlighter as you install it ("yellowing" the drawing). Any wire you could not install is circled in red.
5. Wire the door devices last.
6. Fit the duct covers only after self-check (section 17.8).

## 17.8 Wireman's self-check

Before handing over to the testing department, the wireman checks his or her own work:

| Check | How |
|---|---|
| All wires installed | Drawing fully yellowed; red circles explained on the punch list |
| Wire numbers | Both ends of every wire carry the correct number, readable from the front |
| Terminations | Tug test of every wire; no bare copper visible; ferrules correct size |
| Torque | Power terminations marked with torque seal |
| Routing | No wires over devices, ducts closed, bundles tied, door loop free |
| Earthing | All earth wires connected, door earths fitted |
| Cleanliness | Insulation slugs, cable tie ends and ferrule offcuts removed (vacuum the panel) |
| Labels | Device labels, terminal labels, feeder plates fitted |

## 17.9 Common wiring errors found at testing

| Error | Effect | Prevention |
|---|---|---|
| Wire to the wrong terminal of a contactor auxiliary (NO instead of NC) | Circuit works in reverse | Check contact numbering: 13-14 / 23-24 NO, 21-22 / 31-32 NC |
| Coil wire to A2 instead of A1 (on coils with polarity, DC) | Coil or diode damaged | Check DC coils with suppression diodes |
| Missing wire in a series chain (e.g. one emergency stop not wired) | Safety function does not work | Yellowing method; continuity test |
| CT wires S1 and S2 crossed | Wrong power reading, wrong relay operation | Polarity check, primary injection test |
| Loose ferrule (wrong size) | Intermittent fault, overheating | Correct ferrule size, tug test |
| Neutral of control circuit taken from wrong source | Mixed sources, fuse blowing | Follow drawing; label neutral links |
| Shield earthed at both ends | Interference on analogue signals | Follow shield rule |
| Wire insulation trapped under terminal clamp | No contact, intermittent fault | Strip length correct, check visually |

## 17.10 Operator quick card

!! HINGLISH: Control wire kam se kam 1.5 mm2, PLC DC wire 0.75 mm2, CT wire 2.5 mm2. Rang: R-Y-B phase, black neutral, green-yellow earth, orange matlab bahar se live wire, dhyan rakho. Wire duct ke andar chalao, duct 70 % se zyada mat bharo. Har stranded wire par ferrule, ek clamp mein ek hi wire (do ho to twin ferrule). Har wire ko kheench ke check karo. CT ka secondary kabhi khula mat chhodo, pehle shorting link lagao. Drawing par jo wire lag gaya use peela highlight karo. Ant mein panel ko vacuum se saaf karo.
