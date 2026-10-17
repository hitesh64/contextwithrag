# 6. CNC Hydraulic Guillotine Shear (SHEAR-01)

## 6.1 Purpose and position in the process

SHEAR-01 cuts sheets in straight lines. It trims full sheets to the width needed by the turret punch, cuts strips for base channels and gland plates, and cuts rectangular blanks for covers and partitions. Its cut parts go to PUNCH-02, to BRAKE-04 for bending, or directly to deburring when no further cutting is needed.

## 6.2 Main parts and how it works

[[fig:shear|Figure 6-1. Working principle of the guillotine shear (side view)|430]]

A guillotine shear cuts the sheet between two long blades: the **lower blade**, fixed to the table, and the **upper blade**, fixed to the blade holder (the beam) that moves down. The upper blade is set at a small angle to the lower blade, called the **rake angle**, so that it cuts progressively along the sheet like a pair of scissors. A larger rake angle needs less force but twists and bows narrow strips; a smaller rake angle gives straighter strips but needs more force.

Before the blade moves, the **hold-down cylinders** press the sheet against the table so that it cannot move or lift during the cut. The **back gauge**, driven by a servo motor and a ball screw, positions a stop bar behind the blades at the programmed distance; the operator pushes the sheet against it, so that the cut strip has exactly that width. The **blade gap** (clearance) between the upper and lower blade is set according to the sheet thickness and material.

The beam is driven by two **hydraulic cylinders** fed by a pump and a valve block. The **CNC controller** sets the back gauge position, the blade gap, the rake angle and the stroke length, counts the parts, and controls the hydraulic valves.

| Part | Function |
|---|---|
| Frame | Welded steel frame carrying the table, side frames and cylinders |
| Upper blade and holder (beam) | Moves down to cut; carries the upper blade |
| Lower blade | Fixed to the table; four cutting edges, can be turned when worn |
| Hydraulic cylinders (2) | Drive the beam down and up |
| Hydraulic power pack | Motor, pump, tank, filters, valve block, pressure relief valve |
| Hold-downs | Hydraulic pads that clamp the sheet before the cut |
| Back gauge | CNC-driven stop for the strip width, with ball screws and linear guides |
| Front support arms | Support the sheet in front of the table, with a measuring scale and a squaring arm |
| Squaring arm | Stop at the left side of the table at 90 degrees to the blade |
| Shadow line light | Projects a line on the sheet showing the cutting line for cutting to a marked line |
| Finger guard | Fixed guard in front of the hold-downs that keeps fingers out of the blade area |
| Rear light curtain | Protects the area behind the machine |
| Foot pedal | Starts the cut; has a cover against accidental operation |
| CNC controller | Programs, back gauge, blade gap, rake angle, counter |

## 6.3 Technical data

| Item | Value |
|---|---|
| Maximum cutting length | 3100 mm |
| Maximum thickness, mild steel (450 N/mm2) | 6 mm |
| Maximum thickness, stainless steel (700 N/mm2) | 4 mm |
| Maximum thickness, aluminium | 8 mm |
| Rake angle range | 0.5 to 2.5 degrees |
| Back gauge travel | 20 to 1000 mm |
| Back gauge positioning accuracy | +/- 0.1 mm |
| Strokes per minute (at minimum stroke) | 8 to 18 |
| Main motor | 11 kW, 415 V, 3 phase |
| Hydraulic oil | ISO VG 46 anti-wear hydraulic oil, tank 250 litres |
| Maximum system pressure | 210 bar |
| Number of hold-downs | 14 |
| Machine weight | About 9.5 tonnes |

## 6.4 Controls and indicators

| Control | Function |
|---|---|
| Main isolator (on the electrical cabinet) | Switches the machine supply; lockable in OFF for LOTO |
| Control ON push button (white) | Switches on the control circuit after the emergency stops are reset |
| Pump START (green) / STOP (red) | Starts and stops the hydraulic pump motor |
| Emergency stop (red mushroom) | On the control panel, on the foot pedal and at the rear; stops all movement |
| Foot pedal | Starts a cut in single-stroke mode; must be released between strokes |
| Mode selector | Single stroke / continuous (continuous is disabled by key, used only for strips) / adjust (inch) |
| CNC screen | Program selection, back gauge position, blade gap, rake angle, counter, alarms |
| Shadow line lamp switch | Switches on the cutting line light |
| Lamps on the cabinet | Power on (white), pump running (green), alarm (red) |

## 6.5 Safety devices and specific hazards

!! DANGER: The blade and the hold-downs can amputate fingers. Never put your hands past the finger guard. If a strip is stuck between the blades, stop the pump, lock out the machine and remove the strip with a tool, never with your fingers.

- **Finger guard**: fixed bar in front of the hold-downs. The gap under it is at most 8 mm, so that fingers cannot reach the hold-downs. It must never be raised for "thick sheet" jobs; thick sheets up to 6 mm pass under it.
- **Rear light curtain**: stops the machine and the back gauge if somebody enters the area behind the machine, where the cut parts fall.
- **Side guards**: fixed guards at both ends of the blade, removed only by maintenance under LOTO.
- **Foot pedal cover**: prevents accidental operation by a falling object or a foot.
- **Two-pressure hold-down**: the hold-downs come down first with low pressure; the blade moves only after full clamping.
- **Emergency stops**: three, tested daily.

**Specific hazards**: the cut strips fall behind the machine with sharp edges; long strips can spring and whip; the back gauge moves without warning when the program runs; hydraulic oil at 210 bar can penetrate the skin through a pin-hole leak.

### 6.5.1 LOTO points of SHEAR-01

| Energy | Isolation point | How to verify |
|---|---|---|
| Electrical | Main isolator on the electrical cabinet, lockable | Press pump START: nothing must happen; check display dark |
| Hydraulic | Pump stopped; beam lowered onto the wooden block or to bottom position | Pressure gauge on valve block reads zero |
| Gravity | Beam resting on the lower stop or on two wooden blocks placed on the table under the beam | Visual |

## 6.6 Start-up procedure

1. Check the area: no tools or material on the table, behind the machine or near the back gauge.
2. Check the hydraulic oil level in the sight glass: between MIN and MAX.
3. Switch on the main isolator. The CNC starts and shows the home screen.
4. Reset the emergency stops and press Control ON.
5. Start the pump. Let it run for 5 minutes without cutting so that the oil warms up (in winter, 10 minutes).
6. Reference the back gauge (home) as asked by the controller. Keep away from the rear area while it moves.
7. Carry out the daily check sheet (section 6.10.1), including the emergency stops, the light curtain and the pedal.
8. Select the program for the first job, or enter the dimensions in manual mode.

## 6.7 Normal operation

### 6.7.1 Setting the blade gap

The blade gap is the horizontal clearance between the upper and lower blade at the moment of cutting. Too small a gap wears the blades quickly and needs more force; too large a gap gives a rough edge with a large burr and bends thin sheet into the gap. The controller sets the gap automatically from the material and thickness entered in the program. For manual setting, use the table.

| Material | Thickness (mm) | Blade gap (mm) | Rake angle (degrees) |
|---|---|---|---|
| Mild steel / CRCA | 1.0 | 0.05 | 0.8 |
| Mild steel / CRCA | 1.6 | 0.08 | 1.0 |
| Mild steel / CRCA | 2.0 | 0.10 | 1.0 |
| Mild steel / CRCA | 3.0 | 0.15 | 1.3 |
| Mild steel / HR | 5.0 | 0.25 | 1.8 |
| Mild steel / HR | 6.0 | 0.30 | 2.0 |
| Stainless steel | 1.5 | 0.06 | 1.2 |
| Stainless steel | 2.0 | 0.08 | 1.5 |
| Aluminium | 2.0 | 0.12 | 0.8 |
| Aluminium | 3.0 | 0.18 | 1.0 |

!! TIP: A good cut edge shows a smooth, shiny band (the shear zone) over about one third of the thickness and a dull fracture zone over the rest, with a small burr. A burr higher than 10 % of the thickness means the gap is too large or the blades are blunt.

### 6.7.2 Cutting to the back gauge

1. Enter or select the strip width and quantity; check the back gauge position on the display.
2. Place the sheet on the front support arms and push it against the squaring arm on the left.
3. Slide the sheet forward against the back gauge stop fingers. Both fingers must touch.
4. Keep hands on the sheet surface, well in front of the finger guard.
5. Press the foot pedal. The hold-downs clamp, the blade cuts and returns.
6. Release the pedal. The cut strip falls on the rear chute or the rear conveyor.
7. Measure the first strip (first-off): width at both ends and in the middle, and the squareness with a square or by diagonals.
8. If correct, continue; check one piece in every 20.

### 6.7.3 Cutting to a marked line

For a single part marked with a scriber, switch on the shadow line lamp and move the back gauge to its rear position. Align the scribed line with the shadow line and cut. Accuracy is about +/- 0.5 mm, so use this only for parts without tight tolerance.

### 6.7.4 Narrow strips

Narrow strips (less than 10 times the thickness) twist and bow. Use the smallest rake angle allowed by the thickness, reduce the stroke length, and support the strip at the back with the strip support device. Strips narrower than 15 mm must not be cut on SHEAR-01; they are cut on LASER-03.

## 6.8 Shutdown procedure

1. Finish the cut in progress; do not leave a sheet under the hold-downs.
2. Lower the beam to the bottom position in adjust mode, or leave it at the top as the maker recommends for overnight stops (this plant: top position).
3. Stop the pump.
4. Remove the cut parts and scrap from the rear chute; clean the table with a brush (never by hand over the blade).
5. Switch off the main isolator.
6. Fill the production record and shift log.

## 6.9 Quality checks

| Check | Tool | Frequency | Tolerance |
|---|---|---|---|
| Strip width | Steel tape or vernier | First-off, then 1 in 20 | +/- 0.3 mm up to 1000 mm |
| Squareness | Square or diagonal measurement | First-off, then 1 in 20 | Diagonal difference below 1 mm per 1000 mm |
| Straightness of cut | Straight edge | First-off | 0.5 mm per metre |
| Burr height | Visual, burr gauge | First-off, then hourly | Below 10 % of thickness |
| Bow and twist | Flat table | Narrow strips, first-off | Below 2 mm per metre |

## 6.10 Preventive maintenance

### 6.10.1 Daily (operator)

| Task | Standard |
|---|---|
| Check hydraulic oil level | Between MIN and MAX |
| Test each emergency stop | Machine stops, pump stops |
| Test the rear light curtain | Interrupt with hand while back gauge moves: movement stops |
| Check the pedal cover | Fitted and free |
| Check for oil leaks | No drops under the cylinders or the valve block |
| Clean the table, back gauge area and rear chute | No scrap, no slugs |
| Listen to the pump | No new noise, no whining |

### 6.10.2 Weekly (operator and technician)

- Lubricate the beam guides and the back gauge linear guides (grease gun, 2 shots per nipple, EP2 grease).
- Clean the ball screws of the back gauge and apply a thin film of oil.
- Check the hold-down pads for wear and oil leaks.
- Check the blade edges for chips and dullness.

### 6.10.3 Monthly (maintenance)

- Check the blade gap at both ends and at the centre with feeler gauges; compare with the CNC value.
- Check the oil temperature during work: below 60 degrees C.
- Clean the oil cooler fins and the electrical cabinet filter.
- Check tightness of the blade bolts.
- Check the back gauge accuracy with a test cut at 100, 500 and 900 mm.

### 6.10.4 Every 6 months and yearly (maintenance)

- Change the return filter element (every 6 months, or when the clogging indicator shows red).
- Take an oil sample for analysis yearly; change the oil every 4000 running hours or when the analysis shows contamination.
- Turn or regrind the blades as needed (section 6.11.2).
- Check the parallelism of the beam and the synchronisation of the two cylinders.
- Check the accumulator pre-charge pressure, if fitted.
- Inspect all hoses for cracks, swelling and abrasion; replace hoses older than 6 years.

## 6.11 Troubleshooting

### 6.11.1 Symptoms and remedies

| Symptom | Likely cause | Remedy |
|---|---|---|
| Large burr on cut edge | Blade gap too large; blunt blades | Check gap setting for the material; turn or regrind blades |
| Burr only at one end | Blade gap not parallel | Adjust gap at the adjustment screws; check beam guides |
| Sheet bends into the gap (thin sheet) | Gap too large | Reduce gap; check material selected in program |
| Strips are twisted or bowed | Rake angle too large; narrow strip | Reduce rake angle; use strip support |
| Cut not square | Squaring arm not at 90 degrees; back gauge not parallel | Check squaring arm with a large square; adjust back gauge parallelism |
| Width varies along the strip | Back gauge fingers not at the same position | Re-align the back gauge bar; check both ball screws |
| Beam does not move down | Hold-downs not reaching pressure; pedal fault; light curtain interrupted | Check hold-down pressure switch, pedal contacts, light curtain alignment |
| Beam moves slowly | Low oil, worn pump, relief valve leaking, cold oil | Check oil level and temperature; check pressure at the gauge |
| Machine stops in the middle of the cut | Thickness above capacity; pressure switch tripped | Check sheet thickness and grade; reset and reverse the beam in adjust mode |
| Noisy pump | Air in the oil, low oil, clogged suction strainer | Check level, check suction line for leaks, clean strainer |
| Oil temperature high | Cooler dirty, continuous heavy work, wrong oil | Clean cooler, reduce strokes, check oil grade |

### 6.11.2 Blade care

The lower blade has four cutting edges and the upper blade has two or four. When an edge is dull, the blade is turned to use a new edge. When all edges are dull, the blades are reground by a qualified grinding shop; regrinding removes 0.5 to 1.0 mm and the blade gap must be reset with shims after refitting.

1. Lock out the machine (section 6.5.1). Place wooden blocks under the beam.
2. Remove the blade bolts from one end to the other, holding the blade with the blade lifting device. A 3100 mm blade weighs about 45 kg; it must be handled by two persons with the lifting device.
3. Clean the blade seat; remove all burrs and dirt.
4. Turn the blade to a new edge, fit it, and tighten the bolts from the centre outwards to the torque on the maker's sheet.
5. Set the blade gap with feeler gauges at five points along the length.
6. Make a test cut on 1 mm sheet over the full length: the cut must be clean along the whole length.

### 6.11.3 Alarm codes

| Code | Message | Cause | Action |
|---|---|---|---|
| SH-01 | Emergency stop pressed | One of the three emergency stops is pressed | Find and reset the button, press Control ON |
| SH-02 | Rear light curtain interrupted | Person or object behind the machine; curtain misaligned | Clear the area; check alignment of transmitter and receiver |
| SH-03 | Pump motor overload | Motor overload relay tripped | Check oil temperature and pressure; reset overload; if it trips again call electrical technician |
| SH-04 | Oil temperature high | Oil above 65 degrees C | Stop work, let it cool, clean cooler, check cooler fan |
| SH-05 | Oil level low | Float switch in tank | Find and repair the leak, top up with ISO VG 46 |
| SH-06 | Return filter clogged | Clogging indicator | Replace filter element |
| SH-07 | Back gauge not referenced | Power was switched off or encoder lost position | Run the reference (home) cycle |
| SH-08 | Back gauge following error | Mechanical obstruction, ball screw dry, drive fault | Check for obstruction, lubricate, check servo drive alarm |
| SH-09 | Back gauge limit switch | Gauge reached end of travel | Check program dimension; move gauge in manual mode |
| SH-10 | Blade gap motor fault | Gap adjusting motor overload or encoder error | Check motor, limit switches, reference gap |
| SH-11 | Rake angle not reached | Valve or sensor fault | Check rake angle sensor; check proportional valve |
| SH-12 | Hold-down pressure not reached | Low pressure, hold-down leak | Check pressure switch, hold-down seals |
| SH-13 | Beam not at top dead centre | Beam stopped in middle of stroke | Return beam in adjust mode, check TDC sensor |
| SH-14 | Cylinder synchronisation error | Two cylinders not moving together | Stop; call maintenance; check synchronisation valve and cylinder seals |
| SH-15 | CNC communication error | Cable, connector or controller fault | Switch off and on; check cables; call electrical technician |

## 6.12 Spare parts kept in stock

| Part | Quantity kept |
|---|---|
| Lower blade set (one blade) | 1 |
| Upper blade set (one blade) | 1 |
| Return filter element | 2 |
| Suction strainer | 1 |
| Hold-down seal kit | 2 |
| Pedal switch | 1 |
| Back gauge proximity sensors | 2 |
| Pump motor overload relay | 1 |
| Hydraulic oil ISO VG 46 | 1 barrel (210 l) |
| Hose set (beam cylinders) | 1 set |

## 6.13 Operator quick card

!! HINGLISH: SHEAR-01 seedhi line mein sheet kaatne ki machine hai. Start se pehle oil level dekho, emergency stop aur light curtain test karo. Pump 5 minute chalao, phir back gauge ko home karo. Sheet ko squaring arm aur back gauge dono se lagao, haath finger guard ke aage hi rakho. Pehla piece naap ke supervisor se approve karao. Patti phans jaye to pump band karo, LOTO karo aur tool se nikalo, ungli se kabhi nahi. Burr zyada aaye to blade gap ya blade check karao.
