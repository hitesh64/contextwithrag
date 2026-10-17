# 15. Wire Processing: Cut and Strip (WIRE-11), Crimping (CRIMP-12) and Marking (MARK-13)

## 15.1 Purpose and position in the process

A medium MCC contains 2000 to 4000 wire ends. Cutting, stripping, crimping and marking them by hand at the panel is slow and gives variable quality. The wire preparation cell in Bay 4 prepares **wire kits**: wires cut to length, stripped, crimped with the right terminal or ferrule, and marked with printed ferrules at both ends, bundled per panel and per wiring sheet. The wireman at the panel then only routes and terminates them (Chapter 17).

| Machine | Asset code | What it does |
|---|---|---|
| Automatic cut and strip machine | WIRE-11 | Feeds wire from the reel, cuts to length, strips both ends (full or half strip), counts |
| Pneumatic crimping press with applicators | CRIMP-12 | Crimps lugs, pin terminals and bootlace ferrules with the matching die |
| Thermal transfer marker printer | MARK-13 | Prints ferrules (sleeves) and heat-shrink markers with wire numbers |

## 15.2 Wire and terminal basics

### 15.2.1 Wire types used

| Wire | Construction | Use |
|---|---|---|
| PVC insulated flexible copper, 1100 V grade, class 5 conductor (IS 694) | Many fine strands | Control wiring 0.5 to 2.5 mm2, power wiring up to 6 mm2 inside the panel |
| FRLS PVC (flame retardant, low smoke) | As above with FRLS compound | Panels for buildings, metros, hospitals as specified |
| Halogen-free (LSZH / HFFR) | As above with halogen-free compound | Where specified (data centres, tunnels) |
| Single-core flexible cable, 1100 V | Class 5, larger sizes 10 to 240 mm2 | Power connections from busbar to breakers and from breakers to terminals |
| Shielded cable (twisted pair) | Copper braid or foil screen | Analogue signals 4 to 20 mA, communication |

### 15.2.2 Stranding classes

Class 5 (flexible) conductors have many fine strands: a 1.5 mm2 class 5 conductor has about 30 strands of 0.25 mm. Fine strands spread when clamped under a screw, so every class 5 conductor end in a screw terminal gets a **bootlace ferrule** (end sleeve) or a crimped pin. Bare stranded ends under a screw are not allowed in this plant.

### 15.2.3 Terminal types

| Terminal | Description | Use |
|---|---|---|
| Bootlace ferrule, insulated | Tinned copper tube with plastic collar, colour coded by size | Control wires into screw and spring terminals of devices and terminal blocks |
| Twin ferrule | Takes two wires of the same size | Where two wires must enter one terminal (looping) |
| Pin terminal | Solid pin crimped on the wire | Terminals that need a rigid pin |
| Ring terminal (lug), insulated | Ring with a hole for a stud or screw | Earth studs, CT terminals, meters with screw studs |
| Fork (spade) terminal | Open U-shaped terminal | Only where the drawing requires (allows removal without unscrewing); not for CT circuits |
| Tubular copper lug (heavy duty) | Tinned copper tube with palm, hexagonal crimp | Power cables 10 to 240 mm2 |

| Ferrule colour (insulated, plant standard - DIN 46228 colour code) | Wire size |
|---|---|
| White | 0.5 mm2 |
| Grey | 0.75 mm2 |
| Red | 1.0 mm2 |
| Black | 1.5 mm2 |
| Blue | 2.5 mm2 |
| Grey (large) | 4.0 mm2 |
| Yellow | 6.0 mm2 |
| Red (large) | 10 mm2 |

!! NOTE: Ferrule colour codes differ between manufacturers (French and DIN codes). The plant uses one supplier and one code only, the one in the table. Never mix ferrules from different suppliers in one kit.

## 15.3 WIRE-11 Automatic cut and strip machine

### 15.3.1 How it works

The wire is pulled from the reel through a **pre-straightener** by two **belt or roller feeders** driven by a stepper motor. The feeder measures the length. A **blade block** with V-shaped blades does three jobs: cut, strip the leading end, and strip the trailing end. For stripping, the blades close to a depth just through the insulation (not touching the strands), then the feeder pulls the wire back so that the insulation slug is pulled off. In **half-strip** mode the insulation is pulled only partly off and stays on the end to protect the strands until crimping.

### 15.3.2 Technical data

| Item | Value |
|---|---|
| Wire range | 0.1 to 10 mm2 |
| Length range | 1 mm to 99 m |
| Length accuracy | +/- (0.2 % + 1 mm) |
| Strip length | 0.1 to 40 mm each end |
| Output | Up to 2500 pieces per hour for 300 mm wires |
| Supply | 230 V AC, 1 phase |
| Blades | V-blades for 0.1 to 6 mm2; radius blades for 6 to 10 mm2 |

### 15.3.3 Setting a job

1. Load the reel on the de-reeler; thread the wire through the straightener and the guide tube into the feeder.
2. Enter or select: wire size, length, strip length left and right, half-strip yes / no, quantity.
3. The machine sets the blade depth from the wire size in the library. Make one test piece.
4. Check: length, strip length, and that no strands are cut or nicked (look with a magnifier; count strands on a sample for critical wires).
5. Correct the blade depth by 0.01 mm steps if strands are cut (decrease cut depth) or the insulation does not come off cleanly (increase).
6. Run the batch. Bundle and tag wires per kit.

| Wire size (mm2) | Strip length for ferrule (mm) | Strip length for ring lug (mm) |
|---|---|---|
| 0.5 | 8 | 5 |
| 0.75 | 8 | 5 |
| 1.0 | 8 | 6 |
| 1.5 | 8 | 6 |
| 2.5 | 10 | 7 |
| 4.0 | 10 | 8 |
| 6.0 | 12 | 9 |

!! CAUTION: Nicked or cut strands reduce the current capacity and break by vibration. A wire with more than one cut strand in the sample check is not accepted; the whole batch since the last good check is inspected.

### 15.3.4 Maintenance and faults

| Frequency | Task |
|---|---|
| Daily | Clean blade area and feeder belts with a brush; empty insulation slug tray |
| Weekly | Check blades for nicks; check feeder belts for wear; check length with a 1000 mm test |
| As needed | Change blades (V-blades last about 500 000 cycles on PVC) |

| Code | Message | Action |
|---|---|---|
| WR-01 | Wire end / reel empty | Load new reel |
| WR-02 | Wire slip at feeder | Clean belts; increase belt pressure; check wire size setting |
| WR-03 | Blade motor error | Check for jammed slug; reference blades |
| WR-04 | Cover open | Close cover |
| WR-05 | Strip not complete (sensor) | Check blade depth and strip length |

## 15.4 CRIMP-12 Pneumatic crimping press

### 15.4.1 How a crimp works

A crimp is a cold-pressed joint: the barrel of the terminal and the strands are compressed together so tightly that they form a gas-tight mass with no air gaps. Without air, the copper cannot oxidise inside the joint, so the resistance stays low for the life of the panel. A good crimp is as strong as the wire itself. A crimp that is too loose has air gaps and fails in pull-out; a crimp that is too tight cuts the strands and breaks under vibration.

The crimp is only right when the **terminal, the wire size and the crimping die all match**. The die profile depends on the terminal type (insulated, non-insulated, ferrule, tubular lug).

### 15.4.2 CRIMP-12 data

| Item | Value |
|---|---|
| Type | Bench-top pneumatic press with interchangeable applicators and dies |
| Crimping force | Up to 20 kN at 6 bar |
| Range | 0.25 to 16 mm2 (ferrules up to 10 mm2; insulated lugs 0.5 to 6 mm2) |
| Air | 6 bar, dry |
| Crimp force monitor | Measures each crimp curve and rejects bad crimps |
| Operation | Foot pedal with safety cover over the die |

Heavy tubular lugs (16 to 240 mm2) are crimped with the hydraulic hand crimping tool and hexagonal dies in the wiring bay (Chapter 17).

### 15.4.3 Crimping procedure

1. Select the applicator and die for the terminal (the die number is on the kit sheet and on the terminal box label).
2. Set the air pressure from the chart on the machine.
3. Insert the terminal in the die locator; insert the stripped wire fully into the terminal until the insulation touches the barrel end (for ferrules: strands visible at the tip, up to 0.5 mm protruding is allowed).
4. Press the pedal. The press completes the full stroke (the ratchet / full-cycle control prevents a half crimp).
5. Watch the crimp force monitor: green = good; red = reject, cut off the terminal and crimp again.
6. Check the first crimp of every batch and every die change (section 15.4.4).

### 15.4.4 Crimp quality checks

| Check | Method | Frequency | Accept if |
|---|---|---|---|
| Visual | Magnifier | Every 50th crimp and first of batch | Strands not outside barrel, no strands cut, insulation not inside crimp zone, crimp centred on barrel, terminal not cracked |
| Strand visibility (bell-mouth end) | Visual | As above | Strands visible at the end of the barrel, insulation 0.5 to 1 mm away from barrel |
| Crimp height | Crimp height micrometer | First of batch and die change | Within the value of the terminal maker's sheet +/- 0.05 mm |
| Pull-out test | Pull tester | First of batch, every die change, and 2 per shift | Above the minimum force in the table |

| Wire size (mm2) | Minimum pull-out force (N) |
|---|---|
| 0.5 | 60 |
| 0.75 | 85 |
| 1.0 | 108 |
| 1.5 | 150 |
| 2.5 | 230 |
| 4.0 | 310 |
| 6.0 | 360 |
| 10 | 380 |

!! NOTE: The pull-out test destroys the sample. Use a short test wire from the same batch, not a wire of the kit.

### 15.4.5 Maintenance and faults

| Frequency | Task |
|---|---|
| Daily | Clean dies with a brush; check air pressure; drain water separator |
| Monthly | Check die wear (crimp height drift); lubricate the press slide |
| Yearly | Calibrate the crimp force monitor and the pull tester |

| Code | Message | Action |
|---|---|---|
| CR-01 | Crimp force outside window | Check terminal, wire size, strip length, die; re-teach reference curve after die change |
| CR-02 | Air pressure low | Check supply |
| CR-03 | Stroke incomplete | Check for obstruction; check pedal |
| CR-04 | Die not identified | Fit the correct die with its coding pin |

## 15.5 MARK-13 Wire marker printer

### 15.5.1 Wire numbering

Every wire carries its number at both ends, as shown on the wiring diagram. The plant uses **destination marking** for control wiring when the customer specifies it, and **same number both ends** (equipotential marking) as standard: all wires connected to the same electrical point carry the same number.

| Marking system | Description | Example |
|---|---|---|
| Equipotential (standard) | Same number on all wires of one potential | Wire "A12" at both ends |
| Destination | Each end shows where the other end goes | At K1:A1, marker reads "X1:5"; at X1:5, marker reads "K1:A1" |
| Combined | Wire number plus destination | "A12 / X1:5" |

### 15.5.2 Printing

1. Export the wire list from the wiring design software as a CSV file (wire number, size, colour, length, from, to).
2. Import it into the marker software; the software sorts the markers by wire size so that the right sleeve size is used.
3. Select the sleeve: PVC profile sleeve (ferrule tube) for 0.5 to 2.5 mm2, heat-shrink sleeve for larger sizes or when specified.
4. Print. Check that the print is readable, black on white (or yellow), and not smudged. Rub test: rub 10 times with a finger; the print must remain readable.
5. Cut sleeves are delivered in the order of the wire list to the kit preparation table.

### 15.5.3 Maintenance

- Clean the print head with the cleaning pen every ribbon change.
- Replace ribbon and sleeve cassette as needed; store ribbons in a closed box away from heat.
- Check cutter sharpness weekly.

| Code | Message | Action |
|---|---|---|
| MK-01 | Ribbon end | Replace ribbon |
| MK-02 | Sleeve end or jam | Reload; clear jam |
| MK-03 | Print head temperature | Wait; check fan |

## 15.6 Kit preparation

1. The kit list shows all wires of one panel section: number, size, colour, length, terminal at each end.
2. Cut and strip on WIRE-11 in order of the list.
3. Fit marker sleeves on both ends before crimping (the sleeve cannot pass over the ferrule after crimping).
4. Crimp both ends on CRIMP-12.
5. Bundle by wiring sheet or by device group; tag the bundle with the job, section and sheet number.
6. The kit supervisor counts the wires against the list and signs the kit card before release to the wiring bay.

## 15.7 Safety

- Keep fingers out of the crimp die area; the safety cover must be in place.
- Wire reels are heavy (a 100 m reel of 6 mm2 weighs about 7 kg; a 500 m drum of 2.5 mm2 about 15 kg): lift correctly.
- Blades of WIRE-11 are sharp: blade change only with the machine switched off.
- Hot air guns for heat-shrink reach 500 degrees C: put them on their stand, never on the bench.

## 15.8 Operator quick card

!! HINGLISH: WIRE-11 wire ko length mein kaat ke dono taraf strip karti hai; pehla piece check karo ki koi strand kata nahi ho. Marker sleeve crimping se pehle daalo. CRIMP-12 par terminal, wire size aur die teeno match hone chahiye; monitor laal dikhaye to terminal kaat ke dobara crimp karo. Har batch ke pehle crimp ka pull test karo (1.5 mm2 ke liye 150 N se zyada). Screw terminal mein bina ferrule ka stranded wire kabhi nahi. Ferrule ka rang size ke hisaab se: 0.5 white, 0.75 grey, 1.0 red, 1.5 black, 2.5 blue.
