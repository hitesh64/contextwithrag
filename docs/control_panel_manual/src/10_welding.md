# 10. Welding: Spot Welder (WELD-05) and MIG Welder (WELD-06)

## 10.1 Welding in panel manufacturing

Welding joins the bent sheet metal parts into rigid assemblies. Two processes are used:

- **Resistance spot welding (WELD-05)** for thin sheet joints that must look clean: door corners, door stiffeners, cover reinforcements, partition brackets and frame gussets. Spot welding is fast, needs no filler wire, and leaves only small marks that disappear under powder coating.
- **MIG/MAG welding (WELD-06)** for heavy and structural joints: base frames, lifting brackets, channel frames of large PCCs, and parts thicker than 2.5 mm. It gives a continuous, strong seam, but heat causes distortion and the seam must often be ground.

Welded parts go to grinding and finishing (Chapter 11), then to the paint shop.

## 10.2 Resistance spot welding machine (WELD-05)

### 10.2.1 How it works

[[fig:spot_weld|Figure 10-1. Resistance spot welding: electrodes, current path and the weld nugget|420]]

Two copper alloy **electrodes** press the two sheets together with a controlled force. The welding **transformer** then passes a very high current (8 to 15 kA) at low voltage (a few volts) through the electrodes and the sheets for a short time, measured in **cycles** of the 50 Hz supply (1 cycle = 20 milliseconds). The highest electrical resistance in the path is at the contact between the two sheets, so the heat is generated there. The steel melts locally and forms a lens-shaped **nugget**. The electrodes keep pressing while the current stops (**hold time**), so the nugget solidifies under pressure. The electrodes are water-cooled so that they do not overheat and stick to the sheet.

The weld cycle has four steps:

| Step | What happens | Typical time |
|---|---|---|
| Squeeze | Electrodes close and build up force; no current | 20 to 30 cycles |
| Weld | Current flows; nugget forms | 10 to 22 cycles depending on thickness |
| Hold | Current off, force maintained; nugget solidifies | 10 to 20 cycles |
| Off / release | Electrodes open | - |

### 10.2.2 Main parts

| Part | Function |
|---|---|
| Pedestal frame with upper and lower arms | Carries the electrodes; arm length (throat) 500 mm |
| Pneumatic cylinder | Moves the upper electrode and creates the electrode force |
| Pressure regulator and gauge | Sets the electrode force |
| Welding transformer 35 kVA | Converts 415 V to low voltage, high current |
| Weld timer / controller (microprocessor) | Sets squeeze, weld, hold times and current (phase shift heat control) |
| Electrodes and caps | Cu-Cr-Zr alloy, replaceable caps |
| Water cooling circuit | Cools the transformer, arms and electrodes |
| Foot switch (two-stage) | First stage closes the electrodes, second stage starts the weld |

### 10.2.3 Technical data

| Item | Value |
|---|---|
| Rated power at 50 % duty | 35 kVA |
| Supply | 415 V, 2 phase, 50 Hz |
| Maximum short-circuit current | 18 kA |
| Capacity, mild steel | 2.5 + 2.5 mm |
| Throat depth / gap between arms | 500 mm / 300 mm |
| Maximum electrode force at 6 bar | 6.0 kN |
| Cooling water | 4 litres per minute, inlet below 30 degrees C |
| Compressed air | 6 bar |

### 10.2.4 Weld schedule for mild steel (CRCA)

| Thickness (each sheet) | Electrode face diameter | Electrode force | Weld time (cycles) | Current (approx.) | Minimum nugget diameter |
|---|---|---|---|---|---|
| 1.0 + 1.0 mm | 5.0 mm | 2.2 kN | 10 | 9.0 kA | 4.0 mm |
| 1.6 + 1.6 mm | 6.3 mm | 3.5 kN | 14 | 11.0 kA | 5.1 mm |
| 2.0 + 2.0 mm | 7.1 mm | 4.5 kN | 18 | 12.5 kA | 5.7 mm |
| 2.5 + 2.5 mm | 7.9 mm | 5.5 kN | 22 | 14.0 kA | 6.3 mm |

The electrode face diameter is about 5 x the square root of the thickness; the minimum nugget diameter is about 4 x the square root of the thickness. Galvanised sheet needs about 20 to 30 % more current and more frequent tip dressing, because the zinc alloys with the copper.

| Spot spacing and edge distance (mild steel) | 1.0 mm | 1.6 mm | 2.0 mm | 2.5 mm |
|---|---|---|---|---|
| Minimum pitch between spots | 20 mm | 25 mm | 30 mm | 35 mm |
| Minimum distance from spot centre to edge | 8 mm | 10 mm | 11 mm | 13 mm |
| Standard pitch used on doors | 50 mm | 50 mm | 60 mm | 75 mm |

!! NOTE: Spots placed too close together lose current through the previous spot (shunting), so the new nugget is small. Keep at least the minimum pitch, and increase the current by one step when the pitch is close to the minimum.

### 10.2.5 Safety

!! WARNING: The electrodes close with up to 6 kN, enough to crush a finger. Keep fingers away from the electrodes; hold the part from the edges. Use the two-stage foot switch correctly: first stage to close and check position, second stage to weld.

- Molten metal can be expelled (expulsion) as sparks: wear safety glasses, leather gloves and a leather apron.
- People with pacemakers or other implanted medical devices must not work near the spot welder or MIG welder, because of the strong magnetic field.
- Never weld with the cooling water off: the electrodes overheat, and the transformer can be damaged.

**LOTO points of WELD-05**: electrical isolator (lockable); air valve with exhaust; cooling water valve (only for work on the water circuit).

### 10.2.6 Start-up, operation and shutdown

1. Open the cooling water valve; check the flow indicator shows flow at the drain.
2. Open the air; set the pressure for the thickness (pressure chart on the machine).
3. Switch on the isolator and the timer; select the weld programme number for the thickness.
4. Check electrode alignment: close the electrodes on a piece of paper and carbon paper; the print should be a full circle of the right diameter.
5. Make two test welds on scrap strips of the same material and do a peel test (section 10.2.7).
6. Weld the parts: position the part, press the first stage, check the position, press the second stage. Hold until the electrodes open.
7. At the end of the shift switch off the timer and isolator, close the air and, after 5 minutes, close the water.

### 10.2.7 Quality checks for spot welds

| Test | How | When | Accept if |
|---|---|---|---|
| Peel test | Weld two strips 30 x 100 mm; peel apart in a vice with pliers | Start of shift, after tip dressing, after changing programme | A button (nugget) pulls out of one strip, with diameter at least the minimum nugget diameter |
| Chisel test | Drive a chisel between sheets next to a spot (on a sample part) | Weekly on a sample | Spot does not break at the interface |
| Visual | Look at each spot | Every part | Even round marks, no cracks, no burn-through, indentation below 20 % of thickness |
| Position | Check spot positions against the drawing marks | First-off | Within 5 mm of the marked position |

### 10.2.8 Electrode maintenance (tip dressing)

The electrode tips flatten and grow ("mushroom") with use, so the contact area increases and the current density falls: welds become weak. Tips must be dressed back to the correct face diameter.

- Dress the tips every 300 welds on mild steel, every 100 welds on galvanised sheet, or whenever the peel test shows a small nugget.
- Use the tip dresser (a hand dresser or cutter) to restore the dome or flat face to the diameter in the weld schedule.
- Replace the cap when it is worn below the minimum length marked on the cap holder.
- Never file the tips with a coarse file, which leaves an irregular face.

### 10.2.9 Troubleshooting WELD-05

| Symptom | Likely cause | Remedy |
|---|---|---|
| Weak welds, small nugget in peel test | Mushroomed tips, low current, low force, shunting | Dress tips, check programme, check air pressure, increase pitch |
| Expulsion (heavy sparks) | Too much current, too little force, dirty or rusty sheet | Reduce current or increase force; clean sheet |
| Electrode sticks to the sheet | Poor cooling, too much current, galvanised sheet | Check water flow; dress tips; reduce current |
| Deep indentation | Too much force or current, small tip face | Check force and face diameter |
| Burn-through hole | Too much current or time, misaligned tips | Reduce, align tips |
| No current, electrodes close | Timer fault, second stage of foot switch, thermal switch tripped | Check timer alarm, pedal, transformer temperature |
| Electrodes do not close | Air off, solenoid valve, foot switch | Check air and valve |

| Code | Message | Action |
|---|---|---|
| SW-01 | Cooling water flow low | Open water, clean strainer, check drain |
| SW-02 | Transformer over-temperature | Wait; check water flow; reduce duty cycle |
| SW-03 | Air pressure low | Check air supply and regulator |
| SW-04 | No current detected | Check secondary connections, electrodes, part contact |
| SW-05 | Current outside limit | Check programme, tips, part; dress tips |
| SW-06 | Thyristor fault | Call electrical technician |
| SW-07 | Tip dressing counter reached | Dress tips, reset counter |

## 10.3 MIG/MAG welding set (WELD-06)

### 10.3.1 How it works

[[fig:mig|Figure 10-2. MIG/MAG welding: wire feed, gas shield and arc|430]]

In MIG/MAG (metal inert gas / metal active gas) welding an electric **arc** burns between a continuously fed **wire electrode** and the workpiece. The arc melts the wire and the edges of the joint; the molten wire becomes the filler metal of the weld. A **shielding gas** flowing from the nozzle around the wire protects the molten pool from the air, which would otherwise cause porosity and brittle welds. The welding machine is a **constant voltage** power source: the welder sets the voltage, and the current follows from the **wire feed speed**.

For steel the plant uses a mixture of 82 % argon and 18 % CO2 (MAG). It gives less spatter and a smoother bead than pure CO2. On thin sheet the arc works in **short-circuit transfer**: the wire touches the pool many times per second, which keeps the heat low and is good for sheet and positional welding.

### 10.3.2 Main parts

| Part | Function |
|---|---|
| Inverter power source 400 A | Gives constant voltage DC output |
| Wire feeder (4-roll drive) | Pushes the wire through the torch cable at set speed |
| Torch with cable (3 m) | Carries wire, current and gas; trigger switch |
| Contact tip | Transfers current to the wire; must match wire size |
| Gas nozzle | Directs the shielding gas |
| Liner | Guides the wire inside the cable |
| Gas cylinder, regulator and flowmeter | Supplies gas at set flow |
| Earth (return) clamp and cable | Completes the circuit through the workpiece or welding table |
| Fume extraction arm | Removes welding fumes at the source |

### 10.3.3 Technical data

| Item | Value |
|---|---|
| Output | 30 to 400 A, 15 to 34 V |
| Duty cycle | 400 A at 60 %, 310 A at 100 % |
| Supply | 415 V, 3 phase, 25 kVA |
| Wire | ER70S-6, 0.8 mm and 1.0 mm (1.2 mm for heavy frames) |
| Gas | Ar 82 % / CO2 18 %, 12 to 15 litres per minute |

### 10.3.4 Welding parameters (mild steel, Ar/CO2)

| Thickness | Wire | Voltage | Current | Wire speed | Gas flow | Joint |
|---|---|---|---|---|---|---|
| 1.6 mm | 0.8 mm | 17 to 18 V | 90 to 110 A | 4 to 5 m/min | 12 l/min | Stitch welds 20 mm every 100 mm, tacks |
| 2.0 mm | 0.8 mm | 18 to 19 V | 110 to 130 A | 5 to 6 m/min | 12 l/min | Fillet and corner joints |
| 3.0 mm | 1.0 mm | 19 to 20 V | 140 to 170 A | 5 to 6.5 m/min | 14 l/min | Base frame channels |
| 5.0 mm | 1.0 mm | 22 to 24 V | 180 to 220 A | 7 to 9 m/min | 15 l/min | Lifting brackets, heavy frames |
| 6.0 mm | 1.2 mm | 24 to 26 V | 220 to 260 A | 6 to 7.5 m/min | 15 l/min | Heavy base frames; multi-pass for butt joints |

### 10.3.5 Safety

!! WARNING: The arc emits strong UV light that burns the eyes (arc eye) and the skin within seconds. Always use a helmet with the correct filter (shade 10 to 12), keep your sleeves down and collar closed, and put up welding screens so that other workers are not exposed.

- **Fumes**: position the extraction arm 20 to 30 cm from the arc; never weld galvanised sheet without extraction (zinc fume causes metal fume fever).
- **Fire**: remove flammable material within 10 metres; keep an extinguisher at the welding bay; never weld near the paint shop without a hot work permit.
- **Electric shock**: keep the earth clamp close to the weld; do not stand on wet floor; replace damaged cables.
- **Gas cylinders**: chained upright, valve closed after work, cap fitted when moved.
- **Hot parts**: mark hot parts with a "HOT" chalk mark.

**LOTO points of WELD-06**: electrical isolator (lockable); gas cylinder valve closed.

### 10.3.6 Operation

1. Check the cables, torch and earth clamp; check the contact tip matches the wire size and is not worn (oval hole).
2. Open the gas cylinder slowly; set the flow on the flowmeter (12 to 15 l/min).
3. Switch on the power source; set voltage and wire speed for the thickness (table above), or select the synergic programme.
4. Clean the joint: remove oil, paint, rust and mill scale for 20 mm on both sides.
5. Fit the parts in the welding jig; check squareness and gaps (gap up to 1 mm on sheet).
6. Tack weld at both ends and every 100 to 150 mm, check squareness again, then weld.
7. To control distortion: weld in short stitches alternately on both sides (back-step), let the part cool between passes, and clamp in the jig until cool.
8. After welding: remove spatter, check the weld (section 10.3.7), and grind visible welds flush where the drawing requires a smooth finish.
9. At the end: close the gas cylinder, switch off, hang the torch on its holder, clean the nozzle.

### 10.3.7 Weld quality

| Defect | Appearance | Cause | Remedy |
|---|---|---|---|
| Porosity | Small holes in the bead | Gas flow low or high, draught, dirty surface, nozzle blocked by spatter | Check flow, shield from draught, clean joint and nozzle |
| Excessive spatter | Many metal drops around the weld | Voltage too low or high, wrong gas, long stick-out | Adjust voltage, keep stick-out 10 to 15 mm |
| Undercut | Groove melted at the edge of the weld | Too much current or voltage, wrong torch angle, too fast | Reduce, angle torch 10 to 15 degrees, slow down |
| Lack of fusion | Weld sits on the surface | Too little current, too fast, cold joint | Increase current, slow down, correct angle |
| Burn-through | Hole through thin sheet | Too much heat, gap too large | Reduce current, stitch weld, backing bar |
| Cracks | Lines in or next to the weld | High restraint, fast cooling, wrong wire | Report to supervisor; grind out and re-weld |
| Distortion | Part bent or twisted | Too much heat, wrong sequence | Stitch weld, balance welding sides, use jigs |

Visual inspection is done on every weld. Fillet weld size is checked with a fillet weld gauge on the first-off and on every lifting bracket (lifting brackets are 100 % checked: full length weld, leg length as per drawing, no cracks or porosity).

### 10.3.8 Maintenance of WELD-06

| Frequency | Task |
|---|---|
| Daily | Clean the nozzle and contact tip with anti-spatter spray; check cables and earth clamp; check gas hose for leaks (soap solution) |
| Weekly | Blow out the liner with dry air; check drive rolls for wear; clean the power source air inlet |
| Monthly | Replace the liner if wire feed is jerky; check torch cable insulation; check the earth cable lugs for tightness |
| Yearly | Calibration check of the power source (voltage and current readings); internal cleaning by electrical technician |

### 10.3.9 Troubleshooting WELD-06

| Symptom | Likely cause | Remedy |
|---|---|---|
| Wire feeds jerkily | Dirty or worn liner, wrong drive roll pressure, worn contact tip | Clean or replace liner, adjust pressure, replace tip |
| Wire burns back into the tip | Tip too close to work, wire feed too slow, poor earth | Increase stick-out, check feed and earth |
| Arc unstable | Poor earth connection, worn tip, wrong parameters | Clean and tighten earth clamp, replace tip |
| No gas | Cylinder empty, solenoid valve, kinked hose | Change cylinder, check valve and hose |
| Machine trips on overheating | Duty cycle exceeded, blocked air inlet | Let it cool, clean inlet |

| Code | Message | Action |
|---|---|---|
| MG-01 | Over-temperature | Allow cooling; check fan and inlet |
| MG-02 | Supply phase missing | Check supply fuses and isolator |
| MG-03 | Wire feed motor overload | Check liner and drive rolls |
| MG-04 | Gas flow low (with sensor) | Check cylinder and hose |
| MG-05 | Output short circuit at start | Check torch for spatter bridge between tip and nozzle |

## 10.4 Spare parts kept in stock

| Part | Quantity |
|---|---|
| Spot welding caps (each type) | 20 |
| Cap holders | 2 |
| Tip dresser cutter | 2 |
| Water hoses and connectors | 1 set |
| Foot switch | 1 |
| MIG contact tips 0.8, 1.0, 1.2 | 50 each |
| Gas nozzles | 10 |
| Liners | 3 |
| Drive rolls 0.8 / 1.0 / 1.2 | 1 set each |
| Torch complete | 1 |

## 10.5 Operator quick card

!! HINGLISH: Spot welder (WELD-05): pehle cooling water kholo aur flow check karo, phir air aur programme number set karo. Shift start mein do test weld karke peel test karo: ek strip mein se pura button nikalna chahiye. Har 300 weld par tip dressing karo (GI sheet par har 100). Ungliyan electrode ke beech mat rakho. MIG welder (WELD-06): helmet shade 10-12, gloves, apron pehno; screen lagao. Gas 12-15 litre per minute. Joint saaf karo, pehle tack, phir chhote stitch weld dono taraf baari-baari. Lifting bracket ka weld 100 % check hota hai.
