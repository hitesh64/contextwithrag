# 14. CNC Busbar Processing Machine (BUS-10)

## 14.1 Purpose and position in the process

BUS-10 makes the busbars of the panel: it cuts copper and aluminium bars to length, punches holes and slots for bolted joints and device connections, and bends the bars flat-wise, edge-wise and with twists so that they reach the terminals of breakers and the droppers of each section. Busbars carry the full current of the panel and its short-circuit current, so their dimensions, hole positions, bends and surface condition directly affect the safety and temperature rise of the panel.

Busbars from BUS-10 go to deburring and cleaning, then to tin plating (when specified) or to sleeving with heat-shrink sleeves, and then to the assembly bay (Chapter 16).

## 14.2 Main parts and how it works

[[fig:busbar_machine|Figure 14-1. Three-station busbar machine: punching, shearing and bending|470]]

BUS-10 is a "three-in-one" hydraulic machine with three working stations driven by one hydraulic power pack and controlled by one CNC:

- **Punching station**: a C-frame hydraulic punch with a **tool magazine** of 8 punch-die pairs (round and oblong holes). A **CNC carriage with gripper** feeds the bar along its length (X axis) and the tool magazine selects the tool and its position across the width (Y axis), so all holes are punched in one pass.
- **Shearing station**: a hydraulic shear with a flat blade cuts the bar to length without loss of material (no saw kerf). A notching tool is also fitted for corner notches.
- **Bending station**: a horizontal hydraulic bending unit with a V-die and punch for **flat (vertical) bending** and a separate edgewise bending die for **edgewise (horizontal) bending**. A bending back gauge with an encoder sets the bend position; the angle is measured by an encoder and controlled by the CNC.

The CNC accepts busbar drawings from the design software (bar length, holes, bends) and calculates the flat length, the punching program and the bending sequence. It also checks for collisions between the bent bar and the machine.

| Part | Function |
|---|---|
| Hydraulic power pack | Motor 7.5 kW, pump, valves, cooler; feeds all three stations |
| Punching unit, 8-tool magazine | Holes and slots; tool change automatically |
| CNC feed carriage with gripper | Moves the bar in X with accuracy +/- 0.2 mm |
| Shearing unit | Cuts bar to length, flat cut |
| Notching tool | Cuts corner notches and radius corners |
| Flat bending unit | Bends bars on the flat face (up to 90 degrees and more) |
| Edgewise bending die | Bends bars on the narrow edge |
| Twist fixture | Twists the bar by 90 degrees for phase changes |
| Bending back gauge and angle encoder | Positions bar and measures bend angle |
| CNC with 3D viewer | Programs, flat length calculation, bend simulation |
| Roller conveyor tables (infeed and outfeed) | Support long bars |

## 14.3 Technical data

| Item | Value |
|---|---|
| Maximum bar size, copper | 12 x 150 mm |
| Maximum bar size, aluminium | 15 x 160 mm |
| Punching force | 35 tonnes (350 kN) |
| Shearing force | 35 tonnes |
| Bending force | 35 tonnes |
| Maximum punch size | 32 mm round, 14 x 28 mm oblong (in 10 mm copper) |
| Feed carriage travel (X) | 6000 mm with repositioning |
| Positioning accuracy (X) | +/- 0.2 mm |
| Bending angle accuracy | +/- 0.5 degrees |
| Maximum bend angle | 135 degrees (flat), 90 degrees (edgewise) |
| Power | 11 kVA total |
| Hydraulic oil | ISO VG 46, 120 litres |

## 14.4 Controls

| Control | Function |
|---|---|
| Main isolator | Machine power; lockable |
| CNC console | Program, tool table, manual positioning, alarms, part counter |
| Punch / shear foot pedal | Starts the punch or shear stroke in manual mode |
| Bending two-hand control | Starts a bend; both hands required |
| Station selector | Punching / shearing / bending |
| Emergency stops | Console, punching station, bending station |
| Pump start / stop | Hydraulic pump |

## 14.5 Safety and specific hazards

!! DANGER: Each station applies 35 tonnes. A hand under the punch, in the shear or between the bar and the bending die will be crushed or amputated. The punch has a stripper guard that leaves only the bar opening; never put fingers past it. The bending station uses two-hand control: never tie down or bridge one button.

!! WARNING: During bending, a long bar swings around as the bend forms. Stand clear of the swing path of the free end. For bars longer than 1.5 m, a second person supports the far end from the side, never in front of the bar.

- Sheared ends and punched holes have sharp burrs: handle bars with cut-resistant gloves.
- Copper bars are heavy (10 x 100 copper weighs 8.9 kg per metre): use the roller tables and two-person lifts for long bars.
- Noise during punching thick bars: ear plugs.

### 14.5.1 LOTO points of BUS-10

| Energy | Isolation point | Verify |
|---|---|---|
| Electrical | Main isolator, lockable | Console dark |
| Hydraulic | Pump stopped, pressure released | Gauge zero |
| Gravity / stored | Punch ram at bottom or blocked; bending ram retracted | Visual |

## 14.6 Start-up procedure

1. Check oil level and look for leaks.
2. Switch on the isolator and CNC; start the pump; warm up for 5 minutes.
3. Reference the X carriage and the tool magazine.
4. Daily checks (section 14.10.1).
5. Load the job program; check the tools in the magazine against the tool table (tool numbers on each punch and die).
6. Check the bar material and size against the busbar cutting list of the job.

## 14.7 Normal operation

### 14.7.1 Hole and joint standards

Busbar joints are bolted with the overlap and hole patterns of the plant standard. The overlap of a straight joint equals the bar width. Use the hole sizes below unless the drawing shows otherwise.

| Bar width (mm) | Holes in joint area | Hole size | Bolt |
|---|---|---|---|
| 20 | 1 | 11 mm | M10 |
| 25 | 1 | 11 mm | M10 |
| 30 | 2 (in line) | 11 mm | M10 |
| 40 | 2 (in line) | 14 mm | M12 |
| 50 | 2 (in line) | 14 mm | M12 |
| 60 | 2 (in line) | 14 mm | M12 |
| 80 | 4 (square pattern) | 14 mm | M12 |
| 100 | 4 (square pattern) | 14 mm | M12 |
| 120 | 4 (square pattern) | 14 mm | M12 |
| 150 | 6 (2 rows of 3) | 14 mm | M12 |

Device terminals (breakers, CT, insulators) need holes matching the device: always take these dimensions from the device data sheet, not from memory. Oblong holes (slots) of 14 x 18 mm are used at one end of long bars to allow for tolerances during assembly.

### 14.7.2 Bending rules

| Rule | Copper (ETP, half hard) | Aluminium (E91E) |
|---|---|---|
| Minimum inside radius, flat bend | 1 x thickness | 1.5 x thickness |
| Minimum inside radius, edgewise bend | 1 x width | 1.5 x width |
| Minimum straight length after a bend before a hole | 2 x thickness + hole radius | 2.5 x thickness + hole radius |
| Minimum distance between two bends | 2 x thickness + bend radius | As copper + 25 % |
| Twist length (90 degree twist) | 2 x width | 2.5 x width |

!! CAUTION: A bend tighter than the minimum radius cracks the outside of the bend. Cracks may be hidden under the sleeve and reduce the current capacity and short-circuit strength of the bar. Inspect the outside of every bend before sleeving; a cracked bar is scrapped.

### 14.7.3 Flat length of bent busbars

The CNC calculates the flat length. For a manual check, for a 90 degree flat bend with inside radius equal to the thickness:

**Flat length = sum of outside dimensions - (number of 90 degree bends x 1.8 x thickness)**

Example: an L-bar of 10 x 60 mm copper, outside dimensions 300 mm and 200 mm, one bend: flat length = 500 - (1.8 x 10) = 482 mm.

The value 1.8 x thickness is a starting point. Each new bar lot is checked with a test bend, and the correction is entered into the CNC material table.

### 14.7.4 Running a job

1. Place the bar on the infeed roller table; push it into the gripper against the reference stop. Close the gripper.
2. Start the program. The carriage feeds the bar and the punching unit punches all holes; then the shear cuts the bar to length.
3. Check the first bar (section 14.9).
4. For bending, take the cut bar to the bending station. Follow the bend sequence on the screen: it shows which end goes into the die, which face is up, and the back gauge position.
5. Place the bar against the bending back gauge; press both buttons of the two-hand control. Release at the end of the bend.
6. Measure the angle with the protractor; correct the angle in the CNC if needed.
7. Mark each finished bar with the job number, panel section and bar number (e.g. "J2617 / V3 / R-12") with a permanent marker on a hidden face or a tag.

### 14.7.5 Edgewise and twist

Edgewise bending (bending across the width) is used to turn a bar sideways in the same plane, for example where vertical droppers meet a breaker. Use the edgewise die for the bar width. The inside edge of an edgewise bend thickens and the outside edge thins: check the outside edge for cracks.

Twisting the bar by 90 degrees changes the bar from horizontal to vertical. Use the twist fixture, and keep the twist length at least 2 x width so that the bar does not crack or crease.

## 14.8 Finishing busbars

### 14.8.1 Deburring and cleaning

1. Remove all burrs from sheared ends and punched holes with a file or deburring tool. Round the corners of the bar ends with a radius of 2 to 3 mm: sharp corners concentrate the electric field and can cause partial discharge at higher voltages.
2. Clean the bar with a lint-free cloth and isopropyl alcohol to remove oil and fingerprints.
3. Clean the joint faces just before assembly (not days before) with a non-woven abrasive pad (Scotch-Brite type) to remove oxide; wipe clean. Do not use emery paper on tin-plated bars, which removes the plating.

### 14.8.2 Tin plating

When specified by the customer, copper busbars are tin plated by an approved electroplating contractor, typically 8 to 12 microns of bright or matte tin. Tin protects against oxidation, especially in humid or corrosive atmospheres. Bars are sent after all punching and bending is complete, and are checked on return: plating thickness with a gauge (sample), complete coverage including holes, no blisters or burnt areas.

### 14.8.3 Heat-shrink sleeving

Busbars are sleeved with heat-shrinkable polyolefin sleeve in phase colours, for insulation against accidental contact and to identify phases. Joint areas and device connection areas are left bare (or covered later with removable shrouds or joint covers).

| Conductor | Sleeve colour (plant standard) |
|---|---|
| Phase L1 (R) | Red |
| Phase L2 (Y) | Yellow |
| Phase L3 (B) | Blue |
| Neutral (N) | Black |
| Protective earth (PE) | Green or green-yellow, or bare tinned copper with green-yellow marking |

1. Select a sleeve size that, after shrinking, fits tightly: the expanded size must pass over the bar, and the recovered size must be smaller than the bar section.
2. Cut the sleeve to the length of the bar section to be covered, plus 10 % for shrinkage in length.
3. Slide the sleeve on. Shrink with the hot air gun starting from the middle and moving to the ends, so that no air is trapped.
4. Keep the gun moving; overheating burns or splits the sleeve.
5. Trim the sleeve at joint and connection areas with a sharp knife, cutting round the bar without cutting the copper.

## 14.9 Quality checks

| Check | Tool | Frequency | Tolerance |
|---|---|---|---|
| Length | Steel tape | First bar, then 1 in 10 | +/- 1 mm |
| Hole position from end and between holes | Vernier, tape | First bar, then 1 in 10 | +/- 0.5 mm |
| Hole diameter | Vernier, plug gauge | First bar | +0.2 / -0 mm |
| Bend angle | Protractor | Every bent bar | +/- 1 degree |
| Bend position | Tape | First bar, then 1 in 10 | +/- 1 mm |
| Cracks at bends | Visual with magnifier | Every bend | None |
| Burrs and sharp corners | Visual, gloved touch | Every bar | None |
| Surface | Visual | Every bar | No deep scratches, dents or oxide patches |
| Sleeve | Visual | Every bar | Tight, no splits, burns, or trapped air; correct colour |
| Copper weight balance | Store record | Every job | Copper issued = bars made + offcuts + scrap (within 1 %) |

## 14.10 Preventive maintenance

### 14.10.1 Daily (operator)

- Test emergency stops and the two-hand control (releasing one button must stop the bending ram).
- Check oil level and leaks.
- Clean the punch and die area of slugs; empty slug bin.
- Clean the gripper jaws and the roller tables.
- Lubricate punches with a drop of oil (or check the automatic punch lubrication).

### 14.10.2 Weekly

- Check punches and dies for wear and chipping; sharpen when holes show burrs larger than 0.3 mm.
- Lubricate carriage guides and racks.
- Check shear blade edges.
- Check the bending dies for scratches that mark the bars; polish if needed.

### 14.10.3 Monthly

- Check X positioning accuracy with a test bar: punch holes at 500 mm, 1500 mm, 3000 mm and measure.
- Check the angle encoder calibration with a test bend at 90 degrees.
- Clean the oil cooler and the electrical cabinet filters.

### 14.10.4 Six-monthly and yearly

- Replace hydraulic filters (6 months); oil every 4000 hours or on analysis.
- Check and adjust the shear blade clearance (yearly).
- Check the hydraulic hoses; replace hoses older than 6 years.

## 14.11 Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Holes out of position along the bar | Gripper slipping, wrong reference, carriage backlash | Clean jaws, check gripper pressure, re-reference, check rack |
| Holes out of position across the width | Wrong tool Y offset, bar not against side guide | Check tool table offsets and side guide |
| Large burr on holes | Dull punch, wrong die clearance (die for aluminium used on copper) | Sharpen; check die size for the material |
| Bar bends or bows during punching | Holes close to edge, punching sequence | Check drawing edge distance (at least 1 x hole diameter); change sequence |
| Bend angle not repeatable | Material hardness varies; encoder; bar not against gauge | Test bend per lot; check encoder; train operator |
| Cracks at bends | Radius too small, hard bar, bending across rolling direction with edge defects | Increase radius; check bar temper; inspect bar edges |
| Sheared end not square | Bar not against stop; blade clearance | Check stop; adjust clearance |
| Marks on bar faces | Damaged dies, dirt on dies | Polish dies; clean |

### 14.11.1 Alarm codes

| Code | Message | Cause | Action |
|---|---|---|---|
| BB-01 | Emergency stop | Button pressed | Reset |
| BB-02 | Two-hand control fault | One button pressed alone or held longer than 0.5 s before the other | Release both, press together |
| BB-03 | Hydraulic pressure low | Pump, relief valve, oil level | Check level, pressure; call maintenance |
| BB-04 | Oil temperature high | Cooler, continuous heavy punching | Allow cooling; clean cooler |
| BB-05 | Filter clogged | Return filter | Replace element |
| BB-06 | Gripper not closed | Bar missing or gripper pressure low | Check bar and gripper air / hydraulic pressure |
| BB-07 | Tool magazine index error | Magazine not at commanded tool, sensor dirty, index pin | Re-reference magazine; clean sensor; check index pin; check tool number in program |
| BB-08 | Punch not at top | Punch stuck in bar | Lift in manual mode; under LOTO free the bar and check the punch |
| BB-09 | X axis following error | Obstruction, heavy bar, drive fault | Support bar on rollers; check drive |
| BB-10 | X axis limit | Bar too long for program without repositioning | Check program; use repositioning |
| BB-11 | Bending angle not reached | Pressure, encoder, bar harder than expected | Check pressure; check encoder; increase angle correction |
| BB-12 | Bending back gauge error | Drive or encoder | Re-reference; check drive |
| BB-13 | Shear not at top | Shear blade stuck | Retract in manual; check blade |
| BB-14 | Program collision warning | Bent bar collides with machine | Change bend sequence or use manual bending |

## 14.12 Spare parts kept in stock

| Part | Quantity |
|---|---|
| Punches and dies 11, 14 mm round, 14 x 18 oblong | 2 sets each |
| Punches and dies 6.6, 9, 18, 22 mm round | 1 set each |
| Stripper plates | 2 |
| Shear blades | 1 set |
| Flat bending dies (V and punch) | 1 set |
| Gripper jaws | 1 set |
| Hydraulic filter elements | 2 |
| Encoder (bending angle) | 1 |
| Proximity sensors | 3 |

## 14.13 Operator quick card

!! HINGLISH: BUS-10 copper aur aluminium busbar ko kaatti, chhed karti aur modti hai. Program ki tool table aur magazine ke tool milao. Pehli bar ki length, chhed ki position aur angle naap ke approve karao. Bend ka radius kam se kam bar ki motai jitna (copper), warna crack aata hai; har bend ko sleeve se pehle dekho. Bending mein do haath ka button hai, kabhi bypass mat karo, aur lambi bar ke ghoomne ke raaste mein mat khade raho. Har bar par job number aur bar number likho. Copper ke tukde wapas rack ya locked bin mein.
