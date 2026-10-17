# 23. Plant Utilities: Compressed Air, Power Supply and Cranes

## 23.1 Why utilities matter

When the compressor stops, PUNCH-02, LASER-03, CRIMP-12, the powder booth and the clamps of several machines stop within minutes. When the power supply has a dip, CNC machines lose their reference and the paint oven burners lock out. When the crane fails, no panel can be moved in Bays 5 and 6. Utilities are therefore maintained with the same care as the production machines.

## 23.2 Screw air compressor (COMP-15)

### 23.2.1 How it works

[[fig:compressor|Figure 23-1. Oil-injected screw compressor with refrigerated dryer and receiver|470]]

An oil-injected rotary screw compressor has two meshing helical rotors (male and female) in a casing. Air enters through the **inlet filter** and the **inlet (unloader) valve**, is trapped in the spaces between the rotors and the casing, and is compressed as these spaces become smaller towards the discharge end. **Oil** is injected into the compression chamber to seal the clearances, cool the air and lubricate the rotors. The air-oil mixture goes to the **oil separator tank**, where most oil falls out, and through the **separator element**, which removes the remaining fine oil mist. The oil returns through the **oil cooler**, the **thermostatic valve** and the **oil filter** to the compressor. The compressed air passes through the **minimum pressure valve** and the **after-cooler**, then to the **receiver**, the **refrigerated dryer** and the **filters** before entering the plant air network.

The controller runs the compressor in **load / unload** mode: when the pressure reaches the **unload pressure** (8.0 bar), the inlet valve closes and the motor runs unloaded; when the pressure falls to the **load pressure** (7.0 bar), the inlet valve opens and compression resumes. If the compressor runs unloaded for longer than the set time (5 minutes), the motor stops and restarts automatically when the pressure falls.

### 23.2.2 Technical data

| Item | Value |
|---|---|
| Type | Oil-injected rotary screw, air-cooled |
| Motor | 15 kW, 415 V, star-delta start |
| Free air delivery | 2.5 m3/min at 7.5 bar |
| Load / unload pressure | 7.0 / 8.0 bar |
| Maximum working pressure | 10 bar |
| Oil | Synthetic compressor oil as per maker, 10 litres |
| Normal discharge temperature | 75 to 95 degrees C |
| Receiver | 1000 litres, with safety valve set at 10 bar, pressure gauge, auto drain |
| Refrigerated dryer | Pressure dew point +3 degrees C, with auto drain |
| Filters after dryer | General purpose filter 1 micron, oil removal filter 0.01 micron (for paint booth and laser air) |

### 23.2.3 Daily checks (utility operator)

| Check | Normal |
|---|---|
| Discharge pressure | Cycling between 7.0 and 8.0 bar |
| Discharge temperature | 75 to 95 degrees C |
| Oil level (sight glass, when stopped or as per maker) | Between marks |
| Alarms on controller | None |
| Receiver auto drain and dryer drain | Working (water discharges at intervals) |
| Dryer dew point indicator | Green zone |
| Leaks, unusual noise or vibration | None |
| Compressor room temperature and ventilation | Below 40 degrees C, louvres open |

### 23.2.4 Maintenance

| Interval (running hours) | Task |
|---|---|
| Weekly | Clean inlet filter by blowing from inside to outside (replace if damaged); clean cooler fins |
| 2000 h | Replace inlet air filter element; replace oil filter |
| 4000 h | Replace oil (or per oil analysis); replace separator element; check belt (if belt driven) |
| 8000 h | Check minimum pressure valve and thermostatic valve; check motor bearings; check safety valve operation |
| Yearly | Safety valve test and receiver inspection (statutory, by competent person); dryer condenser cleaning and refrigerant check |

### 23.2.5 Troubleshooting

| Symptom / alarm | Likely cause | Remedy |
|---|---|---|
| CP-01 High discharge temperature (trip at 110 degrees C) | Dirty cooler, low oil, high room temperature, thermostatic valve stuck, blocked oil filter | Clean cooler, check oil level, ventilate room, check valve, replace filter |
| CP-02 Motor overload | Low voltage, high pressure, bearing problem | Check supply voltage, pressure settings, bearings |
| CP-03 Phase failure / reversal | Supply fault | Check incoming supply; never run reversed (rotor damage) |
| CP-04 Separator differential pressure high | Separator element blocked | Replace separator |
| CP-05 Pressure sensor fault | Sensor or cable | Check sensor |
| Oil in the air lines | Separator damaged, oil level too high, scavenge line blocked | Replace separator, correct level, clean scavenge orifice |
| Pressure falls although compressor is loaded | Air demand higher than capacity, leaks, inlet filter blocked, inlet valve not opening fully | Check leaks, filter, inlet valve; check demand |
| Water in air lines | Dryer not working, drains blocked | Check dryer, drains |

### 23.2.6 Compressed air leaks

Leaks waste energy: a single 3 mm hole at 7 bar leaks about 0.6 m3/min, which is about a quarter of the compressor's output. A leak survey is done every month on a Sunday (when production is stopped) by listening (and with an ultrasonic leak detector), and every leak is tagged and repaired. The compressor's load hours with no production give a simple measure of total leakage.

### 23.2.7 Air quality for each user

| User | Required air quality |
|---|---|
| Machine clamps, cylinders (PUNCH-02, CRIMP-12, PEM-07 feeder) | Dry (dew point +3 degrees C), filtered 1 micron, lubricated by machine FRL if required |
| Powder coating (fluidising, guns) | Dry, oil-free (0.01 micron oil filter), dew point +3 degrees C or lower |
| Laser assist air (LASER-03) | Dry, oil-free, 16 bar from a separate booster with its own dryer and filters |
| Blow guns for cleaning | Limited to 2 bar at the nozzle (safety nozzles) |

!! WARNING: Never point compressed air at a person or use it to clean clothes or skin. Air entering the skin or an eye causes serious injury. Use the safety blow guns only for cleaning parts and machines.

## 23.3 Electrical supply of the plant

### 23.3.1 Distribution

The plant receives power from the utility at 11 kV through a transformer of 500 kVA, 11 kV / 433 V, Dyn11. The main LT panel in the utility room has the incomer ACB, a DG incomer with mechanical and electrical interlock, the APFC panel, and outgoing feeders to the bay distribution boards and the large machines. A 250 kVA diesel generator supplies critical loads (compressor, paint shop conveyor, lighting, test bay) during power cuts.

| Feeder | Load |
|---|---|
| PDB Bay 1 | SHEAR-01, PUNCH-02, LASER-03 |
| PDB Bay 2 | BRAKE-04, WELD-05, WELD-06, PEM-07, sockets |
| Paint shop PCC | PTL-08 pumps, PCL-09 booth, ovens, conveyor |
| PDB Bay 4 | BUS-10, WIRE-11, CRIMP-12, MARK-13 |
| PDB Bays 5 and 6 | Assembly sockets, CRANE-16, TEST-14 |
| Utility | COMP-15, dryer, effluent plant |
| Lighting DB | All lighting, emergency lighting |

### 23.3.2 Power quality and machine sensitivity

- CNC machines (LASER-03, BRAKE-04, PUNCH-02, BUS-10) are supplied through isolation transformers with voltage stabilisers and surge protection. A voltage dip below 85 % can make a CNC lose position: after any power dip, re-reference the machine before restarting.
- LASER-03 has an online UPS for the CNC and the chiller controls.
- The paint oven burners lock out on power dips: the paint operator checks the oven after each power interruption and removes parts from the oven if the stoppage exceeds 10 minutes.

### 23.3.3 Maintenance of electrical distribution

| Interval | Task |
|---|---|
| Daily | Read the main meter (kWh, max demand, PF); check APFC relay PF display (target above 0.98) |
| Monthly | Thermal imaging of main LT panel and bay PDBs under load; check DG battery and fuel; DG test run 15 minutes on load |
| Every 6 months | Earth pit resistance test (target below 1 ohm for the system earth grid, below 5 ohm for individual electrode pits); RCCB test |
| Yearly | Shutdown maintenance of main LT panel (torque, cleaning, ACB maintenance); transformer oil test (BDV, moisture); relay testing |

## 23.4 EOT crane (CRANE-16)

### 23.4.1 Description

CRANE-16 is a double girder electric overhead travelling crane of 5 tonne safe working load (SWL), spanning Bays 5 and 6. It has three motions: **hoist** (up / down, two speeds), **cross travel** (trolley along the girders), and **long travel** (bridge along the bay). It is operated from a pendant push button station hanging from the trolley (or by radio remote).

### 23.4.2 Safety devices

| Device | Function |
|---|---|
| Hoist upper limit switch (and ultimate limit) | Stops hoisting before the hook block reaches the drum |
| Hoist lower limit switch | Stops lowering before the last 2 turns of rope leave the drum |
| Overload limiter | Prevents lifting more than 110 % of SWL |
| Cross and long travel limit switches | Slow down and stop at ends of travel |
| Brakes (hoist, travel) | Electromagnetic fail-safe brakes: apply when power is off |
| Emergency stop on pendant | Removes power from all motions |
| Hook safety latch | Prevents the sling from slipping off the hook |
| Warning horn and travel warning light | Warn people in the bay |

### 23.4.3 Daily pre-use check (crane operator)

1. Check the pendant: buttons work and spring back; emergency stop works; cable undamaged.
2. Check the hook: latch present and working; no cracks, no opening of the throat.
3. Check the wire rope as far as visible: no broken wires, kinks, crushing, birdcaging.
4. Test the upper limit switch: hoist slowly with no load until the limit stops the hook.
5. Test brakes: lift a light load, stop: the load must not slip.
6. Test the horn.
7. Record the check in the crane log book. Do not use the crane if any check fails; tag it "Out of service" and inform maintenance.

### 23.4.4 Maintenance

| Interval | Task |
|---|---|
| Weekly | Check limit switches; check brake operation; check rope lubrication |
| Monthly | Inspect wire rope along its full length (broken wires, diameter reduction); lubricate rope; check gearbox oil levels; check wheel and rail condition; check pendant cable |
| Every 6 months | Brake lining wear and adjustment; check electrical panel, contactors and resistors; check hook bearing |
| Yearly | Statutory load test and thorough examination by competent person (certificate kept); change gearbox oil |

**Wire rope discard criteria** (summary): replace the rope when the number of visible broken wires in a length of 6 x rope diameter reaches the limit given by the rope maker (typically 6 broken wires for common 6 x 36 ropes), when the diameter has decreased by 10 % of nominal, or on any kink, birdcage, crushing, heat damage or severe corrosion.

### 23.4.5 Crane troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| No motion at all | Main isolator off, emergency stop pressed, control fuse, phase failure | Check isolator, reset emergency stop, check fuses and supply |
| Hoist up does not work, down works | Upper limit switch operated or faulty; overload limiter active | Lower slightly; check limit switch; check load |
| Load creeps down after stopping | Hoist brake worn or out of adjustment | Stop use; adjust or replace brake lining |
| Crane jerks or travels skewed | Wheel wear, rail misalignment, one travel motor not working | Check motors, brakes, wheels |
| Motor overheats | Too frequent inching, brake dragging, low voltage | Check brake release, voltage, operating practice |

## 23.5 Operator quick card

!! HINGLISH: COMP-15 ka pressure 7 se 8 bar ke beech chalna chahiye, temperature 75-95 degree. Har din receiver aur dryer ka drain check karo. Compressed air kabhi kisi insaan ki taraf ya kapde saaf karne ke liye mat chalao. Bijli jaane ke baad CNC machine ko dobara reference (home) karo. Crane chalane se pehle roz pendant, hook latch, rope, upper limit aur brake check karo aur log book mein likho. Load ke neeche kabhi khade mat ho.
