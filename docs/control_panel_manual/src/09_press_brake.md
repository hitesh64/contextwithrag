# 9. CNC Hydraulic Press Brake (BRAKE-04)

## 9.1 Purpose and position in the process

BRAKE-04 bends flat blanks into the three-dimensional shapes of the panel: frame channels, door returns, cover flanges, mounting plate stiffening flanges, base channels and brackets. Nearly every sheet metal part of a panel passes through it, many with four to eight bends. Accurate bending decides whether the panel can be assembled square and whether doors close and seal properly. BRAKE-04 is therefore a critical machine, and its operators need the highest skill level in the sheet metal shop.

Its parts go to welding (WELD-05, WELD-06), to hardware insertion (PEM-07), or directly to the paint shop.

## 9.2 Main parts and how it works

[[fig:press_brake|Figure 9-1. Air bending in a V-die and the axes of the press brake|450]]

The press brake bends sheet by pressing it with a long **punch** (upper tool) into a **V-die** (lower tool). In **air bending**, which is the method used in this plant, the sheet touches only the punch tip and the two shoulders of the die. The bend angle is set by how deep the punch goes into the V: deeper gives a smaller (sharper) angle. Because the angle depends only on depth, one set of tools makes any angle from about 88 degrees to 180 degrees, and the CNC controls the angle by controlling the depth to a hundredth of a millimetre.

The **ram (upper beam)** is driven by two hydraulic cylinders, one at each side, called **Y1** and **Y2**. Each has a linear scale and is controlled separately by a proportional servo valve, so the beam can be kept parallel or tilted on purpose. The **back gauge** has fingers that the operator pushes the sheet against; the back gauge axes are **X** (front-back distance, giving the flange length), **R** (finger height) and, on this machine, **Z1 and Z2** (side position of each finger). The **crowning** system in the lower beam bends the table slightly upwards in the middle to compensate for the deflection of the beams under load, so that the angle is the same along the whole length.

| Part | Function |
|---|---|
| Frame (two side frames, upper beam, lower beam) | Carries the forces; the side frames have a throat depth for the part flanges |
| Ram with Y1 and Y2 cylinders | Moves the punch down and up |
| Linear scales | Measure the ram position at each side, accuracy 0.01 mm |
| Hydraulic power pack | Pump, motor, tank, servo valve block, filters |
| Upper tool clamping | Hydraulic or quick clamps holding the punches |
| Lower tool holder with crowning | Holds the dies; motorised wedge crowning |
| Back gauge (X, R, Z1, Z2) | Positions the sheet for each bend |
| Front sheet supports | Support large sheets on linear guides |
| Laser safety guard (optical blocking device) | Protects the operator's fingers at the punch tip |
| Foot pedal (with emergency stop) | Down / up control |
| CNC controller with graphic programming | Bend sequence, angle calculation, crowning, back gauge, tool library |

### 9.2.1 Speeds of a bending stroke

A bending stroke has four phases. The change from fast approach to slow bending speed happens at the **speed change point**, set 6 to 10 mm above the sheet. Below this point the ram moves at a safe speed of 10 mm per second or less, which is why the operator can hold the sheet.

| Phase | Speed (typical) |
|---|---|
| Fast approach | 180 mm/s |
| Bending (working) | 10 mm/s |
| Decompression | Short pause at the bottom |
| Fast return | 160 mm/s |

## 9.3 Technical data

| Item | Value |
|---|---|
| Nominal force | 135 tonnes (1350 kN) |
| Bending length | 3100 mm |
| Distance between side frames | 2600 mm |
| Throat depth | 410 mm |
| Stroke (Y) | 200 mm |
| Open height (daylight) | 500 mm |
| Axes | Y1, Y2, X, R, Z1, Z2 and motorised crowning (V axis) |
| Y positioning accuracy | +/- 0.01 mm |
| X positioning accuracy | +/- 0.05 mm |
| Back gauge X travel | 650 mm |
| Main motor | 11 kW |
| Hydraulic oil | ISO VG 46, 220 litres |
| Upper tool system | European style (Promecam), hydraulic clamping |
| Safety | Laser optical guard on the ram, rear light curtain, side guards |

## 9.4 Controls and indicators

| Control | Function |
|---|---|
| Main isolator | Machine power; lockable |
| CNC touch screen | Program, graphic sequence, angle correction, tool library, manual axis control |
| Pump START / STOP | Hydraulic pump |
| Foot pedal: DOWN, UP, emergency stop | Ram movement during bending |
| Mode selector | Adjust (inch), single stroke, automatic sequence |
| Muting / box bending mode | Special mode for boxes, set by CNC, with slow speed only |
| Emergency stops | Pedal, CNC panel, rear |
| Tool clamp buttons | Release and clamp upper and lower tools |

## 9.5 Safety devices and specific hazards

!! DANGER: The punch closes on the die with up to 135 tonnes. Fingers caught between punch and sheet or die are crushed. Never place fingers between the punch and the sheet. Hold the sheet from the front, from the sides, with fingers below the sheet away from the die and with thumbs on top well outside the punch line.

!! WARNING: When a long flange is bent upwards, the sheet whips up quickly ("sheet follow"). Keep your face and body out of the path of the rising sheet, and hold large sheets loosely and follow the movement. For heavy or long parts use the sheet follower supports or a second operator.

- **Laser optical guard**: a laser transmitter and receiver mounted on the ram project a beam a few millimetres below the punch tip. If anything (a finger) interrupts the beam during the fast approach, the ram stops. Below the speed change point, the guard is muted and the ram moves at safe speed only.
- **Rear light curtain** stops the back gauge and ram when someone enters behind the machine.
- **Side guards** (fixed and interlocked) prevent access from the sides.
- **Foot pedal with three positions**: release stops the ram; pressing hard to the third position also stops it (panic position).
- **Emergency stops** on pedal, panel and rear.

### 9.5.1 Daily test of the laser guard

1. Select single stroke mode with a punch fitted.
2. Place the test piece (a 14 mm test rod) on the die under the punch, at the left end.
3. Press DOWN: the ram must stop before touching the test rod while in fast approach, and the screen must show the guard alarm.
4. Repeat at the centre and at the right end.
5. If the ram does not stop, switch off, report to the supervisor and maintenance. Do not use the machine.

### 9.5.2 LOTO points of BRAKE-04

| Energy | Isolation point | How to verify |
|---|---|---|
| Electrical | Main isolator, lockable | CNC dark, pump does not start |
| Hydraulic | Pump stopped; pressure released | Gauge zero |
| Gravity (ram) | Ram lowered onto the tools with wooden blocks, or locked by the maker's ram support | Ram cannot drift: mark position and check after 5 minutes |

## 9.6 Start-up procedure

1. Check the oil level; check for leaks under the cylinders and the valve block.
2. Switch on the main isolator; the CNC starts.
3. Start the pump; let it warm up for 10 minutes (the CNC may run a warm-up cycle). Accurate angles need oil at working temperature, 35 to 50 degrees C.
4. Reference the axes.
5. Do the daily checks including the laser guard test (section 9.5.1).
6. Load the program and the tools for the first job.

## 9.7 Normal operation

### 9.7.1 Selecting the die opening

The V-die opening is chosen from the sheet thickness. The rule for mild steel is a V of about 8 times the thickness. The V decides the inside radius, the force needed and the shortest flange that can be bent.

| Thickness, mild steel (mm) | V-die (mm) | Force for 1 metre (tonnes) | Inside radius (mm) | Minimum flange (mm) |
|---|---|---|---|---|
| 1.0 | 8 | 8 | 1.3 | 6 |
| 1.5 | 12 | 12 | 1.9 | 9 |
| 1.6 | 12 | 14 | 1.9 | 9 |
| 2.0 | 16 | 16 | 2.6 | 11 |
| 2.5 | 20 | 20 | 3.2 | 14 |
| 3.0 | 24 | 24 | 3.8 | 17 |
| 4.0 | 32 | 32 | 5.1 | 22 |
| 5.0 | 40 | 40 | 6.4 | 28 |
| 6.0 | 50 | 46 | 8.0 | 35 |

The force column is for mild steel of 450 N/mm2 tensile strength, from the formula **Force (tonnes per metre) = 64 x thickness2 / V**. For stainless steel 304 multiply by 1.5; for aluminium 5052 multiply by 0.5.

!! CAUTION: Check the total force before bending. Force per metre multiplied by the bend length must be below the machine capacity (135 tonnes) and below the rated load of the tools printed on them (tonnes per metre). Example: 6 mm mild steel over 3 m needs 46 x 3 = 138 tonnes, which is more than the machine capacity: such a part must be shortened or bent with a larger V.

!! CAUTION: Never bend a short part at one end of the machine with high force. Concentrated load damages the tools and the beam. Bend short parts in the centre, or use two identical parts at both ends to balance the load.

### 9.7.2 Flat length and bend deduction

When a sheet is bent, the outside of the bend stretches and the inside compresses. The flat blank must therefore be shorter than the sum of the outside dimensions of the bent part. The amount to subtract for each 90 degree bend is the **bend deduction (BD)**.

**Flat length = sum of outside flange lengths - (number of 90 degree bends x BD)**

| Thickness, CRCA (mm) | V-die (mm) | Bend deduction for 90 degrees (mm) |
|---|---|---|
| 1.0 | 8 | 1.9 |
| 1.5 | 12 | 2.8 |
| 1.6 | 12 | 3.0 |
| 2.0 | 16 | 3.8 |
| 2.5 | 20 | 4.7 |
| 3.0 | 24 | 5.6 |

Example: a U-channel in 2.0 mm CRCA, outside dimensions 40 + 100 + 40 mm, has two bends. Flat length = 180 - (2 x 3.8) = 172.4 mm.

The values come from a K-factor of 0.42 and the inside radius of the table above. They are a starting point. The CNC and the CAD system use the same values, and every new tool or material lot is confirmed by a test bend: bend a 100 x 100 mm blank in the middle and measure both flanges.

### 9.7.3 Bending sequence

The CNC proposes a bending sequence and shows it graphically. The operator checks that:

- every flange can be gauged against the back gauge fingers;
- the part does not collide with the punch, the beam or the frame in any bend (the CNC shows collisions in red);
- the part can be handled and turned safely;
- inside bends are done before outside bends that would close the part around the punch;
- the longest and heaviest flanges are bent last when possible, so that the part is easy to hold.

For panel doors and covers with four sides, the short sides are bent first, then the long sides; corners are left open (relief cuts) for welding.

### 9.7.4 Bending a part

1. Fit the punch and die of the program; check that both are the same height type and seated in the clamps. Clamp them.
2. Check the tool positions on the screen match the actual stations.
3. Place the blank on the die, push it against both back gauge fingers. Both fingers must touch.
4. Hold the blank as described in section 9.5.
5. Press DOWN. The ram approaches fast, stops at the speed change point, then bends slowly.
6. Release the pedal at the end of the bend (or the ram returns automatically in automatic mode).
7. Remove the part; for the next bend the back gauge moves automatically.
8. Check the first part (section 9.9): measure angles with a protractor and flanges with a vernier.
9. Correct the angle on the CNC (angle correction) if needed, not by changing the depth by hand.

!! TIP: Springback: after bending the sheet springs open a little. The CNC calculates the extra depth needed. If the angle is still off, enter the measured angle in the correction field. A new lot of material may need a new correction: check the first part of every new lot.

### 9.7.5 Common panel parts

| Part | Material | Notes |
|---|---|---|
| Frame vertical channel (9-fold profile) | 2.0 mm CRCA | Many bends with close flanges; use gooseneck punch; strict sequence |
| Door with return flanges | 2.0 mm CRCA | Four sides, corner reliefs, then spot-welded corners |
| Side cover with flanges | 1.6 mm CRCA | Long part: use two operators or front supports |
| Mounting plate with stiffening flanges | 2.5 mm GI | Check flatness after bending |
| Base channel | 3.0 mm CRCA or HR | V24 die, heavy part, two operators |
| Gland plate | 3.0 mm CRCA | Usually flat; flanges only on some designs |
| Busbar support brackets | 2.5 to 3.0 mm | Small parts, centre of machine |

### 9.7.6 Hemming

A hem is a flange folded flat onto itself to give a safe edge and stiffness. It is made in two steps: first bend to 30 degrees with an acute (30 degree) punch and die, then flatten with a flattening die. Allow a hem flange length of at least 4 times the thickness.

## 9.8 Shutdown procedure

1. Finish the part in progress.
2. Lower the ram onto the tools in adjust mode with a block of wood between punch and die, or leave the tools clamped with the ram at top and the maker's ram support engaged (this plant: ram at top, tools left in the machine only if the next job uses them).
3. Stop the pump; switch off the main isolator.
4. Clean the tools with a dry cloth; put unused tools back in the tool cabinet in their marked places.
5. Record production and alarms in the shift log.

## 9.9 Quality checks

| Check | Tool | Frequency | Tolerance |
|---|---|---|---|
| Bend angle | Digital protractor | First-off, then 1 in 10 | +/- 0.5 degrees |
| Flange length | Vernier | First-off, then 1 in 10 | +/- 0.2 mm (one bend), +/- 0.5 mm (accumulated) |
| Angle consistency along length | Protractor at both ends and centre | First-off of long parts | Difference below 0.5 degrees |
| Squareness and diagonals of frames | Tape | Every frame | Diagonal difference below 1.5 mm |
| Tool marks on visible faces | Visual | Every part | None deep enough to show through paint |
| Cracks at bend (thick or hard material) | Visual | First-off | None |

!! NOTE: If the angle is good at the ends but open in the middle, the crowning is too low; if it is closed in the middle, the crowning is too high. Adjust crowning in the CNC, not by shims.

## 9.10 Preventive maintenance

### 9.10.1 Daily (operator)

- Test the laser guard at three points (section 9.5.1), the emergency stops and the rear light curtain.
- Check hydraulic oil level and leaks.
- Clean the tools and the tool holders; remove scale and dirt that would mark the parts.
- Clean the back gauge fingers and the ball screw covers.
- Check the oil temperature on the CNC during work (35 to 50 degrees C).

### 9.10.2 Weekly

- Lubricate the ram guides (gibs), back gauge guides and ball screws.
- Check the tool clamps for correct clamping force.
- Check the pedal cable and connector.

### 9.10.3 Monthly

- Check the parallelism of the ram to the table with gauge blocks at both ends (difference below 0.02 mm).
- Check the back gauge X accuracy at three positions, and the finger heights.
- Check the alignment of the laser guard transmitter and receiver.
- Clean the oil cooler and cabinet filters.

### 9.10.4 Every 6 months and yearly

- Replace hydraulic filters (6 months).
- Take an oil sample (6 months); replace oil every 4000 hours or on analysis.
- Check linear scales and their cleanliness (yearly).
- Check cylinder seals for internal leakage: ram drift test, ram must not drift more than 0.1 mm in 10 minutes at top with the pump off and valves closed.
- Check tools for wear: a worn punch tip or die shoulders give angle variation along the length.

## 9.11 Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Angle varies from part to part | Material thickness or strength varies; oil not warm | Check thickness; warm up; correct angle per lot |
| Angle open in the middle | Crowning too low | Increase crowning |
| Angle different left and right | Y1 / Y2 not parallel; tool wear at one end; material not centred | Check Y1/Y2 calibration; turn tools; centre the part |
| Flange length wrong | Back gauge X error; part not touching fingers; wrong BD | Check X calibration; train operator; check BD value |
| Flange length different left and right | Fingers not at same X; part not square | Check finger alignment; check blank squareness |
| Cracks at bend | Radius too small for material; grain direction; hard material | Use larger V; bend across grain; check material |
| Marks on part | Dirty or damaged die shoulders | Clean or polish dies; use protective film or urethane |
| Ram does not move down | Guard interrupted, pedal fault, pump off, Y axis error | Check guard and alarms, pedal, pump |
| Ram stops at speed change point and does not bend | Guard still interrupted below mute point; pressure low | Check guard alignment; check pressure |
| Back gauge not moving | Rear curtain interrupted, axis not referenced, drive fault | Clear rear, reference, check drive (alarm PB-12) |

### 9.11.1 Alarm codes

| Code | Message | Cause | Action |
|---|---|---|---|
| PB-01 | Emergency stop | Button pressed | Reset |
| PB-02 | Laser guard interrupted | Object in beam during fast approach | Remove obstruction; check guard alignment |
| PB-03 | Laser guard test not done | Daily test not performed after power on | Perform test |
| PB-04 | Rear light curtain interrupted | Person behind machine | Clear area, reset |
| PB-05 | Side guard open | Guard door open | Close; check switch |
| PB-06 | Y1 / Y2 synchronisation error | Difference between cylinders above limit | Stop; check scale, servo valve; call maintenance |
| PB-07 | Y axis linear scale error | Dirty or damaged scale, cable | Clean scale, check cable |
| PB-08 | Hydraulic oil temperature high | Cooler, heavy use | Cool down; clean cooler |
| PB-09 | Hydraulic pressure too low | Pump, relief valve, leak | Check pressure; call maintenance |
| PB-10 | Hydraulic filter clogged | Filter dirty | Replace element |
| PB-11 | Tool clamp not closed | Clamp pressure, sensor | Clamp tools; check pressure |
| PB-12 | Back gauge X axis fault | Drive, encoder, obstruction | Remove obstruction; reset drive; check encoder |
| PB-13 | Back gauge R axis fault | As PB-12 | As PB-12 |
| PB-14 | Crowning axis fault | Motor, sensor | Reference crowning; check motor |
| PB-15 | Force limit exceeded | Bending force above programmed limit | Check material, V-die, program |
| PB-16 | Collision warning | Sequence collides with tool or machine | Change sequence or tools |

## 9.12 Spare parts kept in stock

| Part | Quantity kept |
|---|---|
| Punches 88 degree standard, R0.8, 835 mm segments | 1 set |
| Dies V12, V16, V24 segments | 1 set each |
| Laser guard transmitter and receiver | 1 set (shared spare with critical spares) |
| Hydraulic filter elements | 2 |
| Pedal assembly | 1 |
| Back gauge finger set | 1 |
| Servo valve (Y1/Y2) | 1 (critical) |
| Proximity and limit switches | 4 |
| Cylinder seal kit | 1 |

## 9.13 Operator quick card

!! HINGLISH: BRAKE-04 sheet ko mod (bend) karti hai. Shuru mein pump 10 minute garam karo aur laser guard ko test rod se teen jagah check karo; ram na ruke to machine mat chalao. Ungliyan kabhi punch aur sheet ke beech mat rakho. Lambi flange upar uthti hai, chehra door rakho. Pehla piece angle aur flange naap ke approve karao. Angle galat ho to CNC mein correction dalo. Chhota part machine ke beech mein mod karo, kinare par nahi. Force table check karo, machine ki capacity se zyada load mat do.
