# 40. Standard Operating Procedures for Common Maintenance Tasks

Each SOP below gives the steps of one task that technicians and trained operators do often. All SOPs assume that the person is trained and authorised for the machine, wears the PPE of the area, and applies LOTO where the SOP says so.

## SOP-01 Changing the nozzle of LASER-03

| Item | Detail |
|---|---|
| Who | Trained laser operator |
| LOTO | Laser off and key removed; axes stopped (no full LOTO needed for nozzle change at the service position) |
| Tools | Nozzle wrench, magnifier, clear tape, lint-free gloves |
| Time | 5 minutes |

1. Finish or pause the program; switch the laser off; move the head to the service position.
2. Let the nozzle cool (1 to 2 minutes after cutting).
3. Unscrew the nozzle by hand or with the nozzle wrench; do not use pliers.
4. Inspect the ceramic ring: no cracks, no loose fit. Replace if damaged (then do the height calibration).
5. Screw in the new nozzle of the type and size in the parameter set, hand tight.
6. Do the centring test with clear tape (Chapter 8.7.3).
7. Run the height sensor calibration (Chapter 8.7.4).
8. Record the nozzle change in the shift log.

## SOP-02 Changing press brake tools on BRAKE-04

| Item | Detail |
|---|---|
| Who | Trained press brake operator |
| LOTO | Not required for tool change in the CNC tool change mode with the ram at top and the pump stopped; full LOTO for any work under the ram with tools removed |
| Tools | Tool trolley, gloves, cleaning cloth |
| Time | 10 to 30 minutes depending on tool length |

1. Select tool change mode on the CNC. Raise the ram to the top; stop the pump.
2. Release the upper tool clamps; slide punch segments out sideways (do not drop them down: the safety pins hold them, but long segments are heavy). Use the tool trolley.
3. Release the lower tool holder; lift out the die segments.
4. Clean the clamps and holder seats; check for dents and burrs.
5. Fit the new die segments; align and clamp.
6. Fit the punch segments; clamp; check that each segment is seated (safety tongue engaged).
7. Enter the tool positions in the CNC exactly as fitted.
8. Restart the pump; reference; do the laser guard test (Chapter 9.5.1) because the guard height depends on the punch.
9. Make a test bend.

## SOP-03 Changing a hydraulic return filter (SHEAR-01, PUNCH-02, BRAKE-04, BUS-10)

| Item | Detail |
|---|---|
| Who | Maintenance technician |
| LOTO | Full LOTO: electrical, hydraulic (pressure zero), gravity (ram / beam blocked) |
| Tools | Filter wrench, drip tray, rags, new element and seal, clean gloves |
| Time | 30 minutes |

1. Apply LOTO; verify zero pressure on the gauge.
2. Clean the outside of the filter housing.
3. Place the drip tray; open the housing slowly to release any trapped pressure.
4. Remove the element; inspect the dirt on it (metal particles indicate wear: report and take an oil sample).
5. Clean the housing bowl with lint-free cloth; do not use cotton waste.
6. Fit the new element and new O-ring, lightly oiled with clean hydraulic oil.
7. Close the housing to the maker's torque.
8. Remove LOTO, start the pump, check for leaks, check the clogging indicator is green.
9. Top up oil through the filter cart if needed. Record in the PM work order.

## SOP-04 Making a busbar joint

| Item | Detail |
|---|---|
| Who | Trained panel fitter |
| LOTO | New panel: not energised. In service: full isolation and earthing of the busbar under permit |
| Tools | Calibrated torque wrench, abrasive pad, isopropyl alcohol, lint-free cloth, yellow paint marker |
| Time | 10 minutes per joint |

1. Check bar sizes, hole pattern, bolts (property class 8.8, length per drawing) and washers.
2. Clean the faces (copper: abrasive pad then alcohol; tin-plated: alcohol only; aluminium: wire brush and jointing compound).
3. Assemble with flat washers both sides and spring or disc spring washer under the nut.
4. Insert all bolts finger tight; align; check clearances (Table 16-2), especially at bolt ends.
5. Torque in a cross pattern in two stages to Table 16-3.
6. Mark each bolt with the paint marker.
7. Record the joint in the torque record.

## SOP-05 Dielectric (HV) test of a panel

| Item | Detail |
|---|---|
| Who | Authorised testing engineer |
| Preconditions | Visual inspection, earth continuity and IR tests passed; sensitive devices disconnected |
| Tools | TEST-14 HV tester, earthing stick |
| Time | 30 to 60 minutes |

1. Check the test bay: one panel only, no person inside, gates working, beacons working.
2. Close all breakers of the circuits to be tested; connect phases together as per the combination.
3. Connect the HV lead to the circuit and the return lead to the PE terminal.
4. Set the test voltage (Chapter 20.8.1) and the trip current.
5. Leave the bay; close the gate; announce the test.
6. Raise the voltage smoothly to the full value, hold for the duration, reduce to zero, switch off.
7. Discharge with the earthing stick; then enter.
8. Repeat for each combination; record results.
9. Repeat the IR test; reconnect all disconnected devices and record their reconnection.

## SOP-06 Compressor oil and separator change (COMP-15)

| Item | Detail |
|---|---|
| Who | Maintenance technician |
| LOTO | Electrical isolation; air isolated from receiver and system pressure released (gauge zero); compressor cooled below 50 degrees C |
| Tools | Spanners, filter wrench, drain hose, container, new oil, oil filter, separator element, seals |
| Time | 2 hours |

1. Stop the compressor at the end of the day so that it is cool in the morning (oil drains better slightly warm, about 40 degrees C).
2. Apply LOTO; verify that the separator tank pressure is zero (open the tank pressure gauge test or the manual vent).
3. Drain the oil from the drain valve into the container; record the quantity.
4. Replace the oil filter (oil the new seal lightly).
5. Open the separator tank cover; replace the separator element and gaskets as per maker; ensure the earthing staple in the separator gasket (if fitted) is in place.
6. Clean the scavenge line orifice.
7. Refill with the specified oil to the correct level.
8. Remove LOTO; run for 10 minutes; check for leaks; check the oil level again and top up.
9. Reset the service counter; record in the PM work order.

## SOP-07 Changing a crimp die on CRIMP-12

| Item | Detail |
|---|---|
| Who | Trained wire cell operator |
| LOTO | Air isolated with exhaust valve; press at rest |
| Time | 5 minutes |

1. Close the air valve; operate the pedal once to exhaust remaining air.
2. Remove the die cover; unscrew the die holder screws; remove the die set.
3. Fit the new die set with its coding pin; tighten screws.
4. Refit the cover; open air.
5. Teach the reference curve on the crimp force monitor with 5 good crimps (check them visually and by crimp height).
6. Do a pull test on the first crimp.

## SOP-08 Replacing a light curtain

| Item | Detail |
|---|---|
| Who | Maintenance technician (electrical) |
| LOTO | Full machine LOTO |
| Tools | Same type light curtain (transmitter and receiver), alignment aid, test rod, stopping time meter |
| Time | 1 to 2 hours |

1. Apply LOTO. Record the mounting position (distance from hazard) before removal: mark the brackets.
2. Replace with exactly the same type and resolution (finger or hand protection). A curtain with a different resolution or response time needs a new safety distance calculation by the maintenance engineer.
3. Connect as per the wiring diagram; set the same configuration (blanking, muting, restart interlock) as the old curtain, using the configuration record.
4. Align transmitter and receiver (alignment LEDs).
5. Remove LOTO. Test with the test rod at the top, middle and bottom, at both edges: the hazardous motion must stop each time.
6. Measure the stopping time; check against the safety distance.
7. Record the replacement and test, signed by the supervisor.

## SOP-09 Racking an ACB out to the disconnected position

| Item | Detail |
|---|---|
| Who | Authorised electrical technician |
| PPE | Arc-rated face shield and clothing, insulated gloves |
| Time | 10 minutes |

1. Get the permit; inform the area; check the downstream load can be switched off.
2. Open the ACB (press OFF); check the indicator shows "O" (open).
3. Insert the racking handle; turn until "test", then "disconnected".
4. Remove the handle; padlock the cradle and the shutters as required.
5. Apply your personal lock and tag.
6. If work is needed on the downstream circuit, also prove dead and earth it as per the permit.

## SOP-10 Replacing a contactor in an MCC feeder (de-energised)

| Item | Detail |
|---|---|
| Who | Electrical technician |
| LOTO | Feeder isolated at its MCCB or MPCB (locked), control supply of the feeder isolated; proved dead on power and control terminals |
| Time | 30 minutes |

1. Apply LOTO; prove dead on the contactor main terminals and coil terminals (orange external circuits: isolate separately).
2. Photograph the wiring before removal; check wire numbers.
3. Disconnect wires; remove the contactor from the rail.
4. Check the new contactor: rating, coil voltage, auxiliary contacts, same as the BOM.
5. Mount, reconnect, torque terminals to the maker's value.
6. Remove LOTO; test the feeder: start, stop, emergency stop, overload trip, indications.
7. Record in the work order with the reason for failure (burnt coil, welded contacts, mechanical).

## SOP-11 Powder colour change (PCL-09)

Follow Chapter 13.7.5. Key points: run the conveyor empty for one hook spacing; clean guns, hoses, hopper, booth walls and floor, cyclone and sieve; fill new powder; spray a test panel and compare it with the master plate before releasing production.

## SOP-12 Replacing the degreaser bath (PTL-08 stage 1)

| Item | Detail |
|---|---|
| Who | Paint shop technician with supplier support |
| LOTO | Stage 1 pump and heater isolated; tank below 40 degrees C |
| PPE | Chemical goggles, gauntlets, apron, gumboots; face shield while adding chemicals |
| Time | 1 shift |

1. Pump the spent bath to the effluent treatment plant holding tank (never to the drain).
2. Remove sludge from the tank bottom into drums for hazardous waste.
3. Clean the tank, spray risers and nozzles; inspect lining.
4. Fill with water to 80 % of the level; start circulation.
5. Add the degreaser chemical slowly as per the supplier's make-up quantity; fill to level.
6. Heat to 60 degrees C; titrate; adjust to 14 to 18 points.
7. Record the bath change, chemicals and titration in the bath log.

## SOP-13 Thermographic survey of panels

| Item | Detail |
|---|---|
| Who | Technician trained in thermography |
| Conditions | Panel under at least 40 % of normal load for 1 hour |
| PPE | Arc-rated face shield and clothing when opening live panel doors (only doors designed to be opened live, with permit) |

1. Prefer viewing windows or covers that can be opened safely; never remove barriers in front of live busbars.
2. Set emissivity (painted surfaces 0.95; bare copper is reflective, measure on lugs, sleeves or insulated parts).
3. Scan all joints and terminations; record images of any spot warmer than similar points.
4. Record the load current at the time.
5. Classify by temperature difference (Chapter 24.6.2) and raise work orders.

## SOP-14 Replacing a VFD

1. Save parameters from the old drive if possible (keypad copy or laptop).
2. Apply LOTO; wait for the discharge time; measure DC bus below 50 V DC.
3. Photograph wiring; disconnect power, motor, control and shield clamps.
4. Remove the drive (heavy drives: two persons or lifting device).
5. Fit the new drive (same type and rating); reconnect all wiring and shield clamps; torque power terminals.
6. Remove LOTO; power on; load parameters; check motor data; auto-tune if required.
7. Test run: direction, speed range, start / stop, faults, signals to the PLC.
8. Record the new serial number in the asset record.

## SOP-15 Weekly lubrication round

1. Collect the lubrication route card of the week.
2. Take the colour-coded grease guns and oil cans for the round.
3. For each point: clean the nipple, apply the specified amount, wipe excess, tick the card.
4. Report any point that does not take grease (blocked nipple) or shows leaks.
5. Return the card to the maintenance planner.

!! HINGLISH: Har SOP mein likha hai kaun karega, LOTO chahiye ya nahi, kaun se tool aur kitna samay. Kadam kram se karo, beech mein koi kadam mat chhodo. Laser nozzle badalne ke baad centring test aur height calibration zaroori. Press brake tool badalne ke baad laser guard test dobara. Light curtain sirf same type se badlo aur test rod se test karke supervisor se sign karao.
