# 7. CNC Turret Punch Press (PUNCH-02)

## 7.1 Purpose and position in the process

PUNCH-02 punches holes, slots, louvres, knock-outs and cut-outs in sheets up to 3 mm thick. In panel manufacturing it is used for parts with many standard holes: mounting plates with fixing holes, side covers with ventilation louvres, gland plates with knock-outs, and DIN rail and duct mounting patterns. Punching a standard round or square hole takes a fraction of a second, so for parts with hundreds of holes the turret is faster and cheaper than the laser. The turret is also the only machine in the plant that can **form** sheet: louvres, emboss, countersinks, extrusions for tapping, and half-shear marks.

Its parts go to deburring and then to BRAKE-04 for bending.

## 7.2 Main parts and how it works

[[fig:turret|Figure 7-1. Turret punch press: turrets, ram and sheet positioning (top view)|430]]

The machine has two rotating discs, the **upper turret** holding the punches and the **lower turret** holding the matching dies. Both turrets rotate together so that the selected tool comes under the **ram**. The sheet is held by **clamps** on a **carriage** that moves the sheet in X (along) and Y (across) on a table with brushes and balls. For each hit, the carriage positions the sheet so that the hole position is exactly under the ram, the ram strikes the punch, and the punch shears a slug out of the sheet into the die. The slug falls through the die into the slug chute.

A **stripper** around the punch holds the sheet down while the punch returns, so that the sheet does not lift with the punch. **Auto-index stations** can rotate the tool to any angle, so one rectangular tool can punch slots at any angle.

Large or irregular contours are made by **nibbling**: many overlapping hits of a small tool along the contour. Parts are held in the skeleton by small uncut tabs called **micro-joints**, and are broken out after the sheet is finished.

| Part | Function |
|---|---|
| Frame (O-type or bridge) | Carries the turrets and the ram, resists the punching force |
| Ram (hydraulic or servo-electric) | Drives the punch down; stroke and speed controlled by the CNC |
| Upper turret | Holds punches in stations of different sizes |
| Lower turret | Holds the dies, aligned with the punches |
| Auto-index stations | Rotate tool to programmed angle |
| X / Y carriage | Positions the sheet with servo motors and ball screws or rack and pinion |
| Clamps (3) | Pneumatic jaws holding the sheet edge |
| Repositioning cylinders | Hold the sheet while the clamps move to a new grip, to punch sheets longer than the X travel |
| Table with brushes / balls | Supports the sheet and prevents scratches |
| Slug chute and conveyor | Carries slugs out of the machine |
| Lubrication system | Lubricates the punch and the ram guide, and sprays oil on the punch for stainless steel |
| Light curtain / safety fence | Protects the area of the moving carriage |
| CNC controller | Reads the program, controls axes, ram, turret and clamps |

### 7.2.1 Turret stations and tool sizes

| Station size | Maximum tool diameter | Typical tools in this plant |
|---|---|---|
| A (1/2 inch) | 12.7 mm | Round holes 3.5 to 12.7 mm, small slots |
| B (1-1/4 inch) | 31.7 mm | Round holes up to 31.7 mm, square, oblong, DIN rail slots |
| C (2 inch) | 50.8 mm | Large rounds, rectangles for nibbling |
| D (3-1/2 inch) | 88.9 mm | Knock-outs, louvre tool, large squares |
| E (4-1/2 inch) | 114.3 mm | Meter cut-outs 72 x 72 and 96 x 96 mm (by nibbling or special tool) |
| Auto-index B and C | As above | Rectangular tools at any angle |

## 7.3 Technical data

| Item | Value |
|---|---|
| Punching force | 30 tonnes (300 kN) |
| Number of stations | 32, of which 2 auto-index |
| Sheet size without repositioning | 1250 x 2500 mm |
| Maximum thickness, mild steel | 6.35 mm (normally used up to 3 mm) |
| Maximum sheet weight | 150 kg |
| Hit rate at 1 mm stroke, 25 mm pitch | 400 hits per minute |
| Nibbling rate | 900 hits per minute |
| Positioning accuracy | +/- 0.1 mm |
| Axis speed X / Y | 100 m/min combined |
| Main power | 30 kVA |
| Compressed air | 6 bar, 400 litres per minute |
| Ram drive | Hydraulic, servo-valve controlled |
| Hydraulic oil | ISO VG 46, 200 litres |

## 7.4 Controls and indicators

| Control | Function |
|---|---|
| Main isolator | Machine power; lockable |
| CNC panel | Program selection, tool table, offsets, axis jog, alarms |
| Cycle START (green) | Starts or resumes the program |
| Cycle STOP / feed hold (yellow) | Stops at the end of the current hit |
| Emergency stops | On CNC panel, at the loading table, at the rear |
| Clamp open/close foot switch | Opens and closes the clamps for loading |
| Turret rotation key (jog) | Rotates the turret in manual mode for tool changes, only with the turret door closed |
| Turret door | Interlocked access door to the turret for tool change |
| Lamp tower | Green running, yellow stopped / waiting, red alarm |

## 7.5 Safety devices and specific hazards

!! WARNING: The carriage and the clamps move fast and without warning when the program runs. The pinch point between the carriage and the frame can crush a hand or a body. Stay outside the light curtain while the machine runs. Load and unload only when the machine has stopped at the end of the program or in feed hold.

- **Perimeter light curtain and fence** around the carriage area.
- **Interlocked turret door**: opening it stops the turret and the ram.
- **Ram guard** around the punching point; fingers cannot reach the punch.
- **Two-pressure clamps**: low pressure during movement, full pressure while punching.
- **Noise**: punching produces 90 to 95 dB(A); ear protection is compulsory.
- **Slugs**: small slugs are sharp and slippery on the floor; empty the slug bin before it overflows.

### 7.5.1 LOTO points of PUNCH-02

| Energy | Isolation point | How to verify |
|---|---|---|
| Electrical | Main isolator, lockable | Display dark, no response to Cycle START |
| Hydraulic | Pump off | Ram pressure gauge zero |
| Pneumatic | Lockable ball valve at the machine air inlet with exhaust | Clamp pressure gauge zero; open clamps by hand to confirm |
| Gravity | Ram resting at bottom stop or blocked | Visual |

## 7.6 Start-up procedure

1. Check air pressure at the inlet: at least 6 bar.
2. Check hydraulic and lubrication oil levels.
3. Switch on the main isolator and wait for the CNC to start.
4. Reset emergency stops; start the hydraulics.
5. Reference all axes (X, Y, turret, auto-index, C-axis) as asked by the controller.
6. Carry out the daily checks (section 7.10.1).
7. Load the program of the first job; check the tool table against the tools actually in the turret.

## 7.7 Normal operation

### 7.7.1 Punch and die clearance

The clearance is the difference between the die opening and the punch size (total clearance, both sides together). It must suit the material and thickness. Too small a clearance makes a double shear edge, needs more force and wears the tool quickly; too large a clearance gives a large burr and a rough, rolled edge.

| Material | Total clearance as % of thickness | Example: 2.0 mm sheet |
|---|---|---|
| Mild steel / CRCA | 20 to 25 % | 0.40 to 0.50 mm |
| Galvanised sheet | 20 to 25 % | 0.40 to 0.50 mm |
| Stainless steel 304 | 25 to 30 % | 0.50 to 0.60 mm |
| Aluminium | 15 to 20 % | 0.30 to 0.40 mm |
| Copper (soft) | 15 to 20 % | 0.30 to 0.40 mm |

!! TIP: Look at the slug. A good slug has a shiny burnish band over about one third of its edge and a clean, even fracture zone. A slug with a very narrow burnish band means the clearance is too large; a slug with two burnish bands means it is too small.

### 7.7.2 Punching force

The force needed for one hit is calculated as:

**Force (kN) = cut perimeter (mm) x thickness (mm) x shear strength (N/mm2) / 1000**

Use a shear strength of 350 N/mm2 for mild steel, 550 N/mm2 for stainless steel 304 and 200 N/mm2 for aluminium 5052.

Example: a 40 x 40 mm square in 2 mm mild steel: perimeter 160 mm, force = 160 x 2 x 350 / 1000 = 112 kN, or about 11.4 tonnes. Well within the 30 tonne capacity. The same hole in 3 mm stainless steel needs 160 x 3 x 550 / 1000 = 264 kN, about 27 tonnes, which is above the 80 % limit below, so that cut-out is made with a smaller tool by nibbling or on LASER-03.

!! CAUTION: Never program a tool that needs more than 80 % of the machine force (24 tonnes). Also check the maximum force of the tool itself: small punches (below 6 mm) can break if the thickness is more than the punch diameter.

### 7.7.3 Loading the tools

1. Select the tool in the tool table of the program; the turret rotates the station to the tool change position.
2. Open the turret door (the turret and ram are now locked).
3. Take out the old punch with the punch holder; put it in its marked place in the tool cabinet.
4. Fit the new punch with the correct orientation key, and fit the matching die with the correct clearance in the lower station.
5. Check the punch length with the tool length gauge; enter the length in the tool table if the controller uses it.
6. Close the door and confirm the tool change on the screen.

### 7.7.4 Running a job

1. Load the sheet: open the clamps, place the sheet on the table against the clamp jaws and against the X-stop (origin pin), close the clamps.
2. Retract the origin pin (the program normally does this).
3. Run the first sheet in single-block mode at reduced speed if the program is new.
4. Check the first part against the drawing (section 7.9). Get first-off approval.
5. Run the rest of the sheets. Unload the sheets when the program ends; break out the parts at the break-out table.
6. Watch the clamps: the program must keep holes and forming tools out of the clamp dead zone. If a hit is too close to a clamp, the controller gives an alarm.

### 7.7.5 Forming operations

| Operation | Tool | Notes |
|---|---|---|
| Louvre | Louvre tool, D station | Punched upwards; program at reduced speed; leave the louvres for the last operations |
| Knock-out | KO tool with tabs | For gland plates: the knock-out remains held by 2 or 4 small tabs |
| Countersink | Countersink tool | For flush screws on covers |
| Extrusion for tapping | Extrusion tool | Raises a collar so that an M4 to M6 thread has enough length in thin sheet |
| Embossing / marking | Emboss or mark tool | Part numbers, earth symbols |

Forming tools strike upwards from the die side in some designs; check the tool data sheet and the program for the correct station and direction.

## 7.8 Shutdown procedure

1. Finish the sheet in progress; unload all sheets and parts.
2. Return the carriage to the park position (program end or button on CNC).
3. Empty the slug bin.
4. Stop the hydraulics; switch off the main isolator.
5. Close the air valve if the plant air system is stopped overnight.
6. Clean the table, remove slugs from the brushes, record production.

## 7.9 Quality checks

| Check | Tool | Frequency | Tolerance |
|---|---|---|---|
| Hole position from reference edge | Vernier or height gauge | First-off, then every 10th sheet | +/- 0.2 mm |
| Hole size | Plug gauge or vernier | First-off | +0.1 / -0 mm |
| Pitch of hole patterns | Vernier | First-off | +/- 0.15 mm |
| Burr | Visual, touch with gloved finger | Every sheet | Below 10 % of thickness |
| Louvre height and shape | Template, vernier | First-off | As per drawing +/- 0.3 mm |
| Sheet flatness after punching | Flat table | First-off | Below 2 mm per metre |
| Scratches and marks | Visual | Every part | None on visible faces |

## 7.10 Preventive maintenance

### 7.10.1 Daily (operator)

- Test emergency stops, light curtain and turret door interlock.
- Check air pressure (6 bar) and drain the air filter bowl.
- Check hydraulic oil level and lubrication oil level.
- Clean the table brushes and the clamp jaws.
- Empty the slug bin; check that slugs fall freely (no slug build-up in dies).
- Clean the turret stations of the tools used.

### 7.10.2 Weekly

- Lubricate X and Y linear guides and ball screws as per the lubrication chart.
- Check punches for wear: an edge radius of 0.25 mm or more means the punch must be sharpened.
- Check strippers for cracks.
- Check clamp jaw teeth for wear.

### 7.10.3 Monthly

- Check the alignment of upper and lower turret stations with the alignment mandrel at stations 1, 9, 17 and 25.
- Check positioning accuracy with a test sheet: punch a grid of 10 mm holes and measure.
- Clean the electrical cabinet filters and check cabinet cooling.
- Check the clamp air cylinders and the repositioning cylinders for leaks.

### 7.10.4 Every 6 months and yearly

- Change the hydraulic filters (6 months), oil every 4000 hours or according to analysis.
- Check the backlash of the X and Y axes; adjust or compensate.
- Check turret bushings and keys for wear; check the turret indexing pin.
- Check the ram guide and ram stroke calibration.

### 7.10.5 Tool sharpening

A sharp tool punches clean holes with low force and low noise. A dull tool makes burrs, deforms the sheet and loads the machine.

1. Sharpen when the cutting edge radius reaches 0.25 mm, or when burrs exceed 10 % of thickness.
2. Grind on a surface grinder with a fine wheel (grit 46 to 60), removing 0.05 to 0.1 mm per pass with coolant. Never let the punch turn blue from heat.
3. Remove 0.1 to 0.2 mm in total per sharpening, just enough to restore a sharp edge.
4. Demagnetise the punch after grinding, and stone a small 0.02 to 0.05 mm edge to remove the grinding burr.
5. Grind the die by the same amount if needed, and record the new tool length. A tool has a total regrind life of about 3 to 4 mm; below the minimum length, it is scrapped.

## 7.11 Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Heavy burr | Dull punch or die; clearance too large | Sharpen; check die size for material |
| Slug pulling (slug comes back up with the punch) | Dull punch, vacuum, short die land, no slug-retaining die | Sharpen; use slug-free die; oil punch |
| Sheet sticks to punch, lifts | Stripper worn or weak spring; dull punch | Replace stripper or spring; sharpen |
| Holes out of position | Clamp slipping, origin pin not touched, axis backlash | Clean jaws, reload correctly, check backlash |
| Sheet deformed / warped | Too many hits close together; dull tools; forming not in last operation | Change punching sequence, sharpen, move forming to end |
| Scratches on sheet bottom | Worn brushes, slug on table | Replace brushes, clean table |
| Punch breaks | Overload, misalignment, thickness above tool limit | Check alignment, check tool limits, program larger tool |
| Turret does not index | Indexing pin, air pressure, sensor | Check air, sensor, pin lubrication |
| Repeated clamp alarm | Hole programmed too close to clamp | Change program; use repositioning |

### 7.11.1 Alarm codes

| Code | Message | Cause | Action |
|---|---|---|---|
| TP-01 | Emergency stop | Button pressed | Reset, restart hydraulics |
| TP-02 | Light curtain interrupted | Person in machine zone | Leave the zone, reset |
| TP-03 | Turret door open | Door not closed or switch fault | Close door; check switch |
| TP-04 | Air pressure low | Below 5 bar | Check compressor, valve, leaks |
| TP-05 | Clamp not closed | Clamp sensor | Check sheet position, clamp air |
| TP-06 | Clamp dead zone violation | Hit inside clamp zone | Edit program; reposition |
| TP-07 | X axis following error | Obstruction, heavy sheet, drive | Remove obstruction, check sheet weight, check drive |
| TP-08 | Y axis following error | As TP-07 | As TP-07 |
| TP-09 | Turret index error | Pin not engaged, sensor | Jog turret to reference, check pin and sensor |
| TP-10 | Auto-index position error | Index motor or encoder | Reference C-axis; check drive |
| TP-11 | Ram overload | Force above limit | Check tool, thickness, material in program |
| TP-12 | Ram not at top | Ram stopped mid-stroke (punch stuck) | Lift ram in manual; free the punch under LOTO |
| TP-13 | Hydraulic oil temperature high | Cooler, heavy nibbling | Allow cooling, clean cooler |
| TP-14 | Hydraulic filter clogged | Filter dirty | Replace element |
| TP-15 | Lubrication level low | Lube tank empty | Fill with recommended oil |
| TP-16 | Software limit X / Y | Program outside travel | Check program origin and sheet size |
| TP-17 | Tool not in tool table | Program calls missing tool | Load tool and update table |
| TP-18 | Slug detected / slug sensor | Slug lying on die | Stop; clean die and check slug chute |

## 7.12 Spare parts kept in stock

| Part | Quantity kept |
|---|---|
| Punches and dies of the 20 most used tools | 1 spare set each |
| Strippers for A and B stations | 4 each |
| Punch springs | 6 |
| Clamp jaws | 1 set |
| Table brushes | 10 |
| Hydraulic filter elements | 2 |
| Proximity sensors | 3 |
| Air solenoid valves (clamp) | 1 |
| Turret indexing pin | 1 |

## 7.13 Operator quick card

!! HINGLISH: PUNCH-02 ek baar mein bahut saare chhed, slot aur louvre banati hai. Start se pehle air 6 bar, oil level aur light curtain check karo. Program ki tool table aur turret mein lage tool milao. Sheet clamp aur origin pin dono se lagao. Machine chalte waqt light curtain ke andar mat jao, carriage bahut tez chalta hai. Pehla sheet naap ke approve karao. Burr zyada ho to punch tez (sharpen) karwao. Kaan mein ear plug zaroor lagao.
