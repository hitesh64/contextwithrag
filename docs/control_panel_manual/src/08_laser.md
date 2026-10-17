# 8. Fiber Laser Cutting Machine (LASER-03)

## 8.1 Purpose and position in the process

LASER-03 cuts any shape from flat sheet: doors with meter and HMI cut-outs, mounting plates, side covers, brackets, gland plates, and all stainless steel parts. Because it needs no tooling, it is the fastest way to make a new or one-off part. It also cuts parts that the turret cannot, such as narrow strips, small radii and thick base frame plates up to 12 mm. LASER-03 is the most critical machine of the plant: a stoppage delays almost every job. Its parts go to deburring and to BRAKE-04.

## 8.2 Main parts and how it works

[[fig:laser|Figure 8-1. Fiber laser: from source to cutting head|450]]

A **fiber laser source** produces an invisible infrared beam (wavelength about 1.07 micrometres) inside a flexible optical fibre. The fibre carries the beam to the **cutting head** on the moving gantry. In the head, a **collimator lens** makes the beam parallel and a **focusing lens** concentrates it to a spot about 0.1 mm wide. At that spot the energy is so high that the metal melts and partly vaporises.

An **assist gas** flows through the **nozzle** together with the beam and blows the molten metal out of the cut (the kerf):

- **Oxygen** with mild steel: the oxygen burns with the hot steel and adds heat, so thick mild steel can be cut with moderate power. The edge has a thin oxide layer.
- **Nitrogen** with stainless steel, aluminium and galvanised sheet, and with thin mild steel when a bright, oxide-free edge is needed for welding or painting. Nitrogen only blows; it does not burn, so it needs more power and high pressure.
- **Compressed air** (dry and oil-free) can replace nitrogen on thin sheet at lower cost, with a slightly oxidised edge.

A **capacitive height sensor** in the nozzle keeps the nozzle at a fixed distance (typically 0.5 to 1.0 mm) above the sheet, even when the sheet is not flat. A **protective window** (cover glass) below the focusing lens protects the lens from spatter. A **chiller** cools the laser source and the cutting head. A **dust and fume extractor** sucks fumes from under the cutting table. Two **exchange tables (pallets)** allow one sheet to be cut while the other is unloaded and loaded.

| Part | Function |
|---|---|
| Laser source 3 kW | Generates the beam |
| Delivery fibre | Carries the beam to the head; must not be bent tighter than its minimum radius |
| Cutting head | Collimator, focusing lens (motorised auto-focus), protective window, nozzle, height sensor |
| Gantry with X, Y, Z axes | Moves the head with servo motors and rack-and-pinion drives |
| Exchange pallets (2) | Hold the sheet on replaceable slats |
| Chiller | Two circuits: laser source and optics |
| Gas console | Pressure regulators for O2, N2 and air, proportional valve controlled by CNC |
| Fume extractor with filter | Extracts and filters cutting fumes |
| Enclosed cabin with windows | Contains the beam reflection and the fumes; laser-safe windows |
| CNC and HMI | Programs, cutting parameter library, nesting, alarms |

## 8.3 Technical data

| Item | Value |
|---|---|
| Laser power | 3 kW continuous wave |
| Working area | 3000 x 1500 mm |
| Maximum thickness, mild steel (O2) | 20 mm (this plant uses up to 12 mm) |
| Maximum thickness, stainless steel (N2) | 10 mm |
| Maximum thickness, aluminium (N2) | 8 mm |
| Positioning accuracy | +/- 0.05 mm per metre |
| Repeatability | +/- 0.03 mm |
| Maximum axis speed | 120 m/min |
| Pallet exchange time | 15 seconds |
| Total electrical power | 32 kVA |
| Chiller set points | Laser circuit 25 degrees C, optics circuit 28 degrees C |
| Gases | O2 99.5 % purity, up to 1.5 bar; N2 99.99 %, up to 20 bar; dry air 16 bar |
| Laser class | Class 1 with the cabin closed; Class 4 laser inside |

## 8.4 Controls and indicators

| Control | Function |
|---|---|
| Main isolator | Machine power; lockable |
| Laser key switch | Enables the laser source; key kept by the shift supervisor |
| Laser ON / OFF | Switches the laser source to ready state |
| Shutter indicator | Lit when the laser shutter is open |
| Cycle START / STOP / feed hold | Program control |
| Pallet exchange buttons (two-hand at the loading station) | Exchange the pallets |
| Handwheel | Manual axis movement for setting |
| Red pilot laser (visible) | Shows the beam position for setting the origin |
| Emergency stops | On HMI, at the loading station, on the cabin door |
| Beacon on the cabin | Lit while the laser is emitting |

## 8.5 Safety devices and specific hazards

!! DANGER: The laser beam is invisible and can blind instantly and burn skin, including by reflection from shiny metal. Never defeat the cabin door interlocks, never look into the head or the fibre connector, and never operate the laser with any cabin panel removed. Service work on the beam path is done only by the maker's service engineer.

!! WARNING: Laser cutting can start a fire in the slag tray, in the fume duct or in the filter. Never leave the machine cutting unattended, keep the slag trays clean, and keep the CO2 extinguisher at the cabin door. Never cut materials that are not in the parameter library (plastics, coated or painted sheet) without approval: they give toxic fumes and can catch fire.

- **Enclosed cabin** with laser-safe windows and interlocked doors.
- **Light curtain** at the loading station, and two-hand control for pallet exchange.
- **Gas safety**: oxygen cylinders and the nitrogen tank are outside the building in a ventilated cage; oxygen lines must be free of oil and grease (oil and oxygen can explode).
- **Fumes**: metal fumes are harmful; the extractor must run whenever the laser cuts.
- **Hot parts**: thick parts stay hot for minutes after cutting; use gloves.

### 8.5.1 LOTO points of LASER-03

| Energy | Isolation point | How to verify |
|---|---|---|
| Electrical | Main isolator; laser key switch removed | HMI dark; laser ready lamp off |
| Laser radiation | Laser source off, key removed | Shutter indicator off |
| Gas | Valves at the gas console closed and locked | Gauges read zero after venting |
| Compressed air | Air valve locked with exhaust | Gauge zero |
| Chiller (hot / cold water) | Chiller off (only for chiller work) | - |

## 8.6 Start-up procedure

1. Check the chiller water level and that the chiller is on; wait until the water reaches the set temperature (indicator green). The laser source must not start with warm or no cooling water.
2. Open the gas supply valves; check pressures at the gas console (O2 cylinder manifold, N2 tank pressure).
3. Switch on the main isolator; start the CNC.
4. Switch on the fume extractor.
5. Reference the axes.
6. Insert the laser key and switch the laser on; wait for "laser ready" (about 2 minutes).
7. Check the protective window (section 8.7.2) and the nozzle (section 8.7.3).
8. Calibrate the height sensor (section 8.7.4) after any nozzle change, and at the start of each shift.
9. Do the daily checks (section 8.10.1).

## 8.7 Normal operation

### 8.7.1 Cutting parameters

The parameter library in the CNC holds tested parameters for each material and thickness. The operator selects the material and thickness; the CNC loads the power, speed, gas, pressure, focus and nozzle. The table shows typical values for reference only; always use the library.

| Material | Thickness (mm) | Gas | Pressure (bar) | Nozzle (mm) | Speed (m/min) |
|---|---|---|---|---|---|
| Mild steel / CRCA | 1.0 | N2 | 12 | 1.5 single | 25 to 30 |
| Mild steel / CRCA | 2.0 | N2 or air | 14 | 2.0 single | 9 to 12 |
| Mild steel / CRCA | 2.0 | O2 | 1.0 | 1.2 double | 5 to 6 |
| Mild steel | 3.0 | O2 | 0.8 | 1.2 double | 3.5 to 4.0 |
| Mild steel | 6.0 | O2 | 0.6 | 1.5 double | 2.0 to 2.3 |
| Mild steel | 10.0 | O2 | 0.5 | 2.0 double | 1.1 to 1.3 |
| Stainless steel 304 | 1.5 | N2 | 14 | 2.0 single | 14 to 18 |
| Stainless steel 304 | 3.0 | N2 | 16 | 2.5 single | 4.5 to 5.5 |
| Aluminium 5052 | 2.0 | N2 | 14 | 2.0 single | 9 to 11 |
| GI sheet | 1.6 | N2 | 14 | 2.0 single | 12 to 15 |

### 8.7.2 Checking the protective window

The protective window is a thin glass below the focusing lens. Spatter and fumes slowly dirty it; a dirty window absorbs laser power, gets hot and can crack, and the cut becomes poor.

1. Stop the laser (laser off) and move the head to the service position.
2. Clean your hands; wear powder-free gloves. Never touch the glass with bare fingers.
3. Pull out the window drawer; hold it by the frame.
4. Inspect against a light: small dark spots or a film mean it must be cleaned; cracks, burnt spots or pits mean it must be replaced.
5. Clean with lens tissue and isopropyl alcohol, wiping in one direction only.
6. Refit the drawer immediately so that no dust enters the head; record the check.

### 8.7.3 Nozzle and centring

The nozzle must be clean, round and centred on the beam. A damaged or off-centre nozzle gives a cut that is good in one direction and bad in another.

1. Check the nozzle tip under a magnifier: no spatter, no dents, round opening.
2. Do the centring test: stick a piece of clear tape on the nozzle tip, fire a single low-power pulse; the hole in the tape must be at the centre of the nozzle print.
3. If off-centre, adjust the centring screws of the head and repeat.

### 8.7.4 Height sensor calibration

After every nozzle change and at the start of each shift, run the height calibration from the HMI with the nozzle over a clean, flat area of a sheet of the same material. The CNC records the capacitance curve. A calibration failure usually means a dirty or loose nozzle, a damaged ceramic ring, or a sheet that is not earthed (rusty slats).

### 8.7.5 Running a nest

1. Load the sheet on the free pallet; push it against the stops; check the sheet is flat on the slats.
2. Exchange pallets with the two-hand buttons.
3. Load the nest program; set the material and thickness; check the parameter set.
4. Find the sheet origin and angle: use the automatic edge detection, or the red pilot laser to touch off at two points on the sheet edge.
5. Start the program. Watch the first contours: the sparks should flow straight down below the sheet.
6. Check the first parts (section 8.9). Continue.
7. While the machine cuts, unload the finished sheet from the other pallet, separate the parts from the skeleton and remove micro-joints.

!! TIP: Watch the spark stream. Sparks going straight down and leaving the sheet cleanly mean a good cut. Sparks flying upwards or back towards the head mean the cut is not through: the speed is too high, the power too low, the focus wrong, or the window dirty. Stop before the head gets spatter.

### 8.7.6 Cut quality terms

| Term | Meaning |
|---|---|
| Kerf | Width of the cut, 0.15 to 0.4 mm |
| Dross | Molten metal stuck under the cut edge |
| Striations | Lines on the cut face; fine and straight is good |
| Burn-out | Melted corners or wide kerf, usually in thick mild steel at sharp corners |
| Taper | Cut face not square; top and bottom width differ |
| Micro-joint | Small uncut tab holding the part in the skeleton |
| Pierce | Making the start hole; takes time in thick sheet |
| Lead-in | Short cut from the pierce point to the contour, so the pierce mark is not on the part |

## 8.8 Shutdown procedure

1. Finish the program; unload both pallets.
2. Switch off the laser; remove the key and give it to the supervisor.
3. Leave the fume extractor running for 10 minutes, then switch it off.
4. Close the gas valves at the console; close the oxygen cylinder valves.
5. Move the head to the park position; switch off the CNC and the main isolator.
6. Switch off the chiller only if the machine will be off for more than one day and the room temperature is above 5 degrees C (the chiller protects against condensation and freezing; follow the maker's instruction).
7. Clean the slag trays at the end of each day.

## 8.9 Quality checks

| Check | Tool | Frequency | Tolerance |
|---|---|---|---|
| Dimensions of first part | Vernier, tape | First-off of each nest | +/- 0.1 mm for holes, +/- 0.2 mm for outside dimensions |
| Hole diameter | Plug gauge, vernier | First-off | +0.1 / -0 mm |
| Dross under edge | Visual, scraper | Every sheet | No dross that cannot be removed by hand scraper |
| Edge squareness | Square | First-off for 6 mm and above | 0.1 mm per 1 mm thickness |
| Burn marks and spatter on visible faces | Visual | Every part | None on visible door faces |
| Pierce marks | Visual | Every part | Outside the part (lead-in) |

## 8.10 Preventive maintenance

### 8.10.1 Daily (operator)

- Check chiller water level and temperature; check no alarm on the chiller.
- Check and clean the protective window; check and clean the nozzle; centring test after nozzle change.
- Calibrate the height sensor.
- Check gas pressures and the oxygen cylinder stock.
- Empty and clean the slag trays; clean the area under the pallets.
- Test emergency stops, cabin door interlocks and the light curtain.
- Check the fume extractor: filter differential pressure in the green range.

### 8.10.2 Weekly

- Clean the slats of the pallets (remove dross build-up with a slat cleaner) or turn / replace slats.
- Clean the rack and pinion of the X and Y axes and the guides; lubricate as per the chart (or check the automatic lubrication tank).
- Clean the chiller condenser fins.
- Check the fume duct for dust build-up near the table.

### 8.10.3 Monthly

- Replace the chiller water filter; check water conductivity if the chiller shows it.
- Clean the filter cartridges of the fume extractor (pulse cleaning) and empty the dust drawer.
- Check the axis squareness with a test square cut 1000 x 1000 mm: diagonals within 0.2 mm.
- Clean the electrical cabinet and laser source air filters.

### 8.10.4 Every 6 months and yearly

- Change the chiller water with distilled or de-ionised water and the maker's additive (every 6 months).
- Replace the fume extractor cartridges when pulse cleaning no longer restores the pressure drop.
- Check the focusing lens and collimator through the maker's service procedure (yearly, by service engineer).
- Check the pallet exchange chain and drives.
- Verify the laser power at the head with a power meter (yearly, by service engineer).

## 8.11 Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Cut not through, sparks upward | Speed too high, power low, wrong focus, dirty window | Check parameters; clean or replace window; check focus position |
| Heavy dross on mild steel (O2) | Oxygen pressure wrong, focus too high, nozzle damaged, impure oxygen | Check pressure and gas purity; replace nozzle; adjust focus |
| Dross on stainless (N2) | Nitrogen pressure low, focus not low enough, speed too high | Check tank pressure and regulator; adjust focus deeper |
| Burn-out at corners in thick MS | Too much heat at slow corner speed | Use corner power ramping or loop corners; check parameter set |
| Good cut in one direction only | Nozzle not centred | Centring test, adjust |
| Rough cut, yellow or blue edge on SS | Oxygen or air contamination of nitrogen | Check nitrogen purity and lines for leaks |
| Height sensor collisions | Dirty nozzle, sheet tip-up of small parts, warped sheet | Clean nozzle, add micro-joints, use avoid-cut-parts path |
| Protective window breaks often | Back-reflection, spatter, wrong focus, dirty lens | Check piercing parameters, use pierce shield, have optics checked |
| Laser does not start | Chiller not ready, door open, key off | Check chiller temperature and alarms, door switches, key |

### 8.11.1 Alarm codes

| Code | Message | Cause | Action |
|---|---|---|---|
| LS-01 | Emergency stop | Button pressed | Reset |
| LS-02 | Cabin door open | Door interlock | Close door; check switch |
| LS-03 | Chiller not ready | Water temperature out of range or flow low | Wait for temperature; check water level, filter, pump |
| LS-04 | Chiller flow alarm | Blocked filter, low level | Clean filter, top up |
| LS-05 | Laser source fault | Internal source alarm | Note the source code, switch off and on once; call service if repeated |
| LS-06 | Back-reflection warning | Reflective material, wrong parameters | Check material (brass, copper need special parameters), check focus |
| LS-07 | Protective window temperature high | Dirty or damaged window | Clean or replace window |
| LS-08 | Height sensor collision | Nozzle touched sheet | Check nozzle and ceramic; recalibrate |
| LS-09 | Height sensor calibration failed | Dirty nozzle, loose ceramic, earthing | Clean, tighten, check slats earthing |
| LS-10 | Gas pressure low | Cylinder empty, regulator, leak | Change cylinder bank; check regulator |
| LS-11 | Fume extractor not running | Extractor off or overload | Switch on extractor; check overload and filter |
| LS-12 | Pallet exchange error | Pallet not in position, sensor, chain | Check sensors, obstruction |
| LS-13 | X / Y / Z following error | Obstruction, drive fault | Remove obstruction; check drive alarms |
| LS-14 | Focus motor error | Auto-focus drive | Reference focus; call service |
| LS-15 | Cabinet temperature high | Cabinet AC or fan failed | Check cabinet cooling; clean filters |

## 8.12 Spare parts kept in stock

| Part | Quantity kept |
|---|---|
| Nozzles: 1.2 double, 1.5 single and double, 2.0 single and double, 2.5 single | 10 each |
| Protective windows | 10 |
| Ceramic ring (nozzle holder) | 3 |
| Seal rings for protective window drawer | 10 |
| Pallet slats | 1 full pallet set |
| Chiller water filter | 2 |
| Fume extractor cartridges | 1 set |
| Lens tissue and isopropyl alcohol | Ongoing |
| Height sensor cable | 1 |

## 8.13 Operator quick card

!! HINGLISH: LASER-03 plant ki sabse zaroori machine hai. Chiller ka paani aur temperature pehle check karo, chiller ready hone se pehle laser on mat karo. Har shift mein protective glass saaf karo (dastane pehen ke, glass ko ungli mat lagao), nozzle check karo aur height sensor calibrate karo. Cabin ka darwaza khol ke kabhi laser mat chalao, beam dikhti nahi aur aankh kharab kar sakti hai. Machine ko akela chhod ke cutting mat chalao, aag lag sakti hai. Sparks neeche seedhe jaane chahiye; upar aaye to rok do.
