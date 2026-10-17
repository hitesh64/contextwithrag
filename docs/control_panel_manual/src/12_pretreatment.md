# 12. Pre-treatment Line (PTL-08)

## 12.1 Purpose and position in the process

Powder coating sticks well and protects against corrosion only on a clean, chemically prepared surface. Sheet steel arrives with rolling oil, drawing lubricants, fingerprints, laser oxide and sometimes light rust. The pre-treatment line removes them and forms a thin crystalline **zinc phosphate** layer on the steel. The phosphate layer anchors the powder and stops rust from creeping under the paint at scratches. A panel coated without proper pre-treatment may look perfect at dispatch and start peeling or rusting at the customer's site within a year.

PTL-08 is a seven-stage spray tunnel through which the overhead conveyor carries the parts hung on hooks. After the last stage, parts pass through the **dry-off oven** and then to the powder booth PCL-09 (Chapter 13).

## 12.2 How it works

[[fig:pretreatment|Figure 12-1. Seven stages of the pre-treatment tunnel and dry-off oven|480]]

Each stage has a **tank** under the tunnel, a **pump** that sends the solution to **spray risers** with nozzles on both sides of the conveyor, and drains back into the same tank. Between stages there are **drip zones** where the solution drains back so that it is not carried into the next tank. Hot stages are heated by **heat exchangers** (from a hot water or gas-fired heater). Each tank has a level float, a temperature sensor and a sampling point.

| Stage | Process | Purpose | Chemical | Temperature | Spray time |
|---|---|---|---|---|---|
| 1 | Alkaline degreasing | Removes oil, grease, dirt | Alkaline degreaser with surfactants | 55 to 65 degrees C | 3 minutes |
| 2 | Water rinse | Removes degreaser | Tap water, overflow | Ambient | 1 minute |
| 3 | Acid pickling (de-rusting) | Removes light rust and laser oxide | Inhibited hydrochloric / phosphoric acid based | Ambient | 2 minutes |
| 4 | Water rinse | Removes acid | Tap water, overflow | Ambient | 1 minute |
| 5 | Surface activation | Seeds fine phosphate crystals | Titanium phosphate activator | Ambient | 1 minute |
| 6 | Zinc phosphating | Forms the zinc phosphate conversion coating | Zinc phosphate with nitrite accelerator | 45 to 55 degrees C | 3 minutes |
| 7 | DM water rinse and passivation | Removes salts; seals pores of the coating | De-mineralised water with chrome-free passivator | Ambient | 1 minute |
| Oven | Dry-off | Removes water before powder | - | 110 to 120 degrees C | 10 minutes |

### 12.2.1 Why each stage matters

- **Degreasing** must be complete; phosphate does not form on oily areas. A water-break test after stage 2 shows whether the surface is clean.
- **Rinses** prevent chemicals from one stage poisoning the next. Carry-over of alkali into the phosphate bath, or of acid into the activation, quickly spoils the bath.
- **Activation** makes the phosphate crystals small and dense. Without it the coating is coarse and porous.
- **Phosphating** is a controlled chemical reaction; the bath strength, the acid ratio, the accelerator and the temperature all decide the coating weight and quality.
- **Final DM rinse** removes soluble salts. Salts left under the powder draw moisture through the film later and cause blisters.

## 12.3 Technical data

| Item | Value |
|---|---|
| Line type | 7-stage spray tunnel, stainless steel 304 tunnel, mild steel tanks with FRP lining |
| Conveyor | Overhead monorail, shared with PCL-09, speed 1.0 to 2.0 m/min (normal 1.5 m/min) |
| Maximum part size | 2400 mm high x 1000 mm wide x 600 mm deep |
| Tank volume | 4000 litres each (stages 1, 3, 6); 3000 litres others |
| Spray pumps | 7 pumps, 5.5 kW each (stage 1 and 6: 7.5 kW) |
| Spray pressure | 1.0 to 1.5 bar at the riser |
| Heating | Indirect, hot water generator 300 kW (PNG fired) |
| Dry-off oven | 110 to 120 degrees C, PNG fired, recirculating air |
| Exhaust | Fume exhaust fans for stages 1 and 6 |
| DM water plant | Mixed bed, conductivity below 10 microsiemens per cm |

## 12.4 Controls

| Control | Function |
|---|---|
| Main control panel with PLC and HMI | Start / stop of pumps, heating, oven, conveyor; set temperatures; alarms |
| Individual pump selector switches | Auto / off / manual (manual only for maintenance) |
| Heater start | Starts the hot water generator and the circulation pumps |
| Conveyor start / stop and speed | Shared with paint shop; master control at the paint shop HMI |
| Emergency stops | At the loading point, along the tunnel, at the unloading point, at the panel |
| Gas train valves | Manual valve, safety shut-off valves (controlled by burner management) |

## 12.5 Safety and specific hazards

!! WARNING: The chemicals are corrosive. The degreaser is a strong alkali and the pickling chemical is an acid; both cause serious burns to the eyes and skin. Wear chemical goggles, PVC gauntlets, PVC apron and gumboots for any work at the tanks, including taking samples. Know where the emergency shower and eye wash are.

- Never mix chemicals; add chemicals slowly to the tank with the pump running for mixing. Add acid to water, never water to acid.
- Nitrite accelerator must never be mixed with acid outside the tank: it releases toxic gases.
- Confined space: entry into a tank or the tunnel for cleaning needs a confined space permit, gas test, ventilation and a standby person.
- Hot surfaces: heat exchanger pipes, the oven and parts leaving the oven.
- Slippery floor: keep the floor around the tunnel dry; report leaks at once.
- Gas burners: only trained persons may reset burner lockouts; never bypass the flame failure device.

### 12.5.1 LOTO points of PTL-08

| Energy | Isolation point |
|---|---|
| Electrical | Main isolator of the pre-treatment control panel; pump motor isolators near each pump |
| Thermal | Hot water generator off; heating valve of the stage closed and locked; wait until below 40 degrees C |
| Gas | Gas train manual valve closed and locked |
| Chemical | Pump isolated, suction and delivery valves closed and locked |
| Conveyor (mechanical) | Conveyor drive isolator locked; conveyor emergency pull cord |

## 12.6 Start-up procedure

1. Check tank levels; top up with water if below the mark (rinse tanks fill automatically).
2. Start the hot water generator about 60 minutes before production (heating 4000 litres from 30 to 60 degrees C takes about 45 minutes).
3. Start the spray pumps of all stages; check spray pressure and that no nozzles are blocked (look through the inspection windows).
4. Start the DM water plant; check conductivity.
5. Do the chemical tests of the shift (section 12.8) and make additions if needed.
6. Start the dry-off oven; wait until it reaches 110 degrees C.
7. Start the conveyor with the paint shop; start loading parts.

## 12.7 Loading parts

- Hang parts so that solution and water drain freely: holes and open sides down, no cups or pockets that hold water. If a part holds water, it will carry chemicals into the next tank and leave water marks.
- Use clean hooks; burnt or coated hooks cause poor earth in the powder booth (Chapter 13).
- Space parts at least 100 mm apart and keep large flat faces parallel to the spray risers.
- Do not touch parts with bare hands after degreasing; wear clean cotton gloves at unloading.
- Mask threads and earth points that must stay bare (masking plugs fitted at PEM-07 must still be in place).

## 12.8 Bath control

Chemical baths change during work: chemicals are consumed and carried out, and dirt and oil collect. Baths are tested by titration twice per shift (start and middle) and the results are recorded in the bath log. Additions are made according to the supplier's chart.

| Stage | Test | Method | Range | If low | If high |
|---|---|---|---|---|---|
| 1 Degreaser | Total alkalinity | 10 ml sample, phenolphthalein, titrate with 0.1 N acid | 14 to 18 points | Add degreaser per chart | Dilute with water |
| 1 Degreaser | Oil content | Visual, skimmer | No floating oil layer | - | Skim oil; replace bath when emulsion is heavy |
| 2 Rinse | pH | pH paper or meter | 7 to 9 | - | Increase overflow |
| 3 Pickling | Acid strength | 10 ml sample, titrate with 1 N NaOH | 8 to 12 points | Add acid chemical | Dilute |
| 3 Pickling | Iron content | Titration with permanganate | Below 2 % | - | Partial or full replacement |
| 4 Rinse | pH | pH paper | 5 to 7 | - | Increase overflow |
| 5 Activation | pH | pH meter | 8.0 to 9.5 | Add activator | - |
| 6 Phosphate | Total acid (TA) | 10 ml sample, phenolphthalein, 0.1 N NaOH | 18 to 22 points | Add phosphate chemical | Dilute |
| 6 Phosphate | Free acid (FA) | 10 ml sample, bromophenol blue, 0.1 N NaOH | 0.8 to 1.2 points | Add neutraliser | Add phosphate chemical |
| 6 Phosphate | Acid ratio TA / FA | Calculation | 18 to 22 | - | - |
| 6 Phosphate | Accelerator (nitrite) | Saccharometer gas test | 2.0 to 3.0 ml gas | Add accelerator | Reduce dosing |
| 7 DM rinse | Conductivity of drip from parts | Conductivity meter | Below 50 microsiemens per cm | - | Increase DM overflow; check DM plant |

!! NOTE: "Points" is the number of millilitres of titrant used for a 10 ml sample. The supplier's technical service checks the baths weekly and adjusts the ranges if needed. The values in the bath log are the controlled reference for the plant.

### 12.8.1 Coating weight test

The phosphate coating weight is checked once per day on a test panel (100 x 150 mm CRCA) hung with the parts.

1. Weigh the coated, dry test panel (W1) to 0.1 mg.
2. Strip the phosphate coating in the stripping solution (chromic acid free stripping agent of the supplier) as per its method, rinse, dry.
3. Weigh again (W2).
4. Coating weight (g per m2) = (W1 - W2) in grams / area of both faces in m2 (0.03 m2 for a 100 x 150 mm panel).

The target is **1.5 to 2.5 g per m2** for powder coating. A higher weight gives a brittle coating that reduces paint adhesion; a lower weight reduces corrosion protection.

### 12.8.2 Visual checks on parts

| After stage | Check | Good result |
|---|---|---|
| 2 (rinse after degreasing) | Water-break test: water should form a continuous film on the surface for 30 seconds | No breaks or beads (beads mean oil left) |
| 4 (rinse after pickling) | Surface colour | Uniform grey metal, no rust or black smut |
| 6 / 7 (after phosphating) | Coating appearance | Uniform light grey, fine and even crystals; no powdery deposit, no bare patches, no rust |
| Oven exit | Dryness | Completely dry, including folds and pockets; no water marks |

## 12.9 Shutdown procedure

1. Stop loading 20 minutes before the end of the shift; allow the last parts to leave.
2. Stop the spray pumps.
3. Stop the heater and the dry-off oven burners; keep the oven fan running until below 60 degrees C (the control does this automatically).
4. Record the bath log, chemical additions and the conveyor counter.
5. Clean the drip zones and the floor; check for leaks.

## 12.10 Maintenance

| Frequency | Task | By |
|---|---|---|
| Daily | Check spray nozzles through the windows; clean blocked nozzles; check pump seals for leaks; skim oil from degreaser | Operator |
| Weekly | Clean pump suction strainers; clean nozzles of all risers; check tank temperatures against a reference thermometer | Operator, technician |
| Monthly | Desludge the phosphate tank (sludge settles at the bottom); clean heat exchanger of stage 6; check pump motor currents and bearings | Technician |
| Every 3 months | Replace degreaser bath (or as per oil content); descale heat exchangers; check tunnel for corrosion | Technician, supplier |
| Every 6 months | Replace pickling bath (or on iron content); full cleaning of rinse tanks; regenerate or replace DM plant resin as required | Technician |
| Yearly | Burner service of hot water generator and dry-off oven (by burner service company); tank lining inspection | Contractor |

### 12.10.1 Effluent

Spent baths and overflow rinse water are not discharged to drains. They go to the effluent treatment plant (neutralisation, precipitation, filter press) of the factory, and the sludge is disposed of through the authorised hazardous waste agency with a manifest. Effluent pH and the discharge parameters are recorded daily.

## 12.11 Troubleshooting

| Defect | Likely cause | Remedy |
|---|---|---|
| Water breaks after degreasing | Degreaser weak or cold; heavy oil; bath loaded with oil | Check alkalinity and temperature; skim oil; replace bath |
| Rust after pickling or between stages | Line stopped with parts inside; rinse carries acid; long drip time | Avoid stops with parts in tunnel; increase rinse; check timings |
| No or patchy phosphate coating | Oil left on part; bath weak; temperature low; free acid high | Check degreasing, titrate phosphate, check temperature |
| Powdery (loose) coating | Free acid low, accelerator high, high sludge, coating too heavy | Adjust FA and accelerator; desludge |
| Coarse crystals, poor paint adhesion | Activation weak or contaminated; no activation stage | Check activation pH; replace bath |
| Yellow or blue stains | Accelerator too high; drying too slow | Reduce accelerator; check oven |
| Water marks or salt deposits | Final rinse conductivity high; part holds water | Check DM plant, overflow; change hanging |
| Blisters after powder coating (later) | Soluble salts left; poor rinse | Check final rinse conductivity; improve rinsing |

| Code | Message | Action |
|---|---|---|
| PT-01 | Emergency stop | Find and reset |
| PT-02 | Tank level low (stage number shown) | Top up; check for leak; pump stops to protect itself |
| PT-03 | Tank temperature low | Check heater, valve, heat exchanger |
| PT-04 | Tank temperature high | Check control valve; stop heating |
| PT-05 | Pump motor overload | Check pump for blockage; reset; call electrician if repeated |
| PT-06 | Spray pressure low | Clean strainer and nozzles; check pump |
| PT-07 | Burner lockout (hot water generator) | Trained person only: check gas pressure, reset once; call burner service if repeated |
| PT-08 | Oven burner lockout | As PT-07 |
| PT-09 | Oven temperature out of range | Check burner, fan, thermocouple |
| PT-10 | DM water conductivity high | Regenerate or replace resin |
| PT-11 | Exhaust fan failure | Stop line; check fan |
| PT-12 | Conveyor stopped | Check conveyor drive and pull cords (common alarm with PCL-09) |

## 12.12 Operator quick card

!! HINGLISH: PTL-08 mein 7 stage hain: degreasing, rinse, acid se zang hatana, rinse, activation, zinc phosphate, DM water rinse; phir dry-off oven. Tank ke paas goggles, gauntlet, apron aur gumboot zaroori. Shift mein do baar titration karo aur bath log mein likho. Degreasing ke baad water-break test: paani ki parat tootni nahi chahiye. Parts aise latkao ki paani bahar nikal jaye. Line rukne par parts andar mat chhodo, zang lag jaata hai. Acid mein paani nahi, paani mein acid daalo.
