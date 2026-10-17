# 13. Powder Coating Booth and Curing Oven (PCL-09)

## 13.1 Purpose and position in the process

Powder coating gives the panel its finished colour and its long-term protection against corrosion. Dry powder made of resin, hardener and pigment is sprayed electrostatically onto the pre-treated parts and then melted and cured in an oven into a hard, continuous film. Compared with liquid paint it gives a thicker and tougher film in one coat, uses no solvents, and the overspray can be recovered and reused.

The standard finish for indoor panels is a **polyester or epoxy-polyester powder in RAL 7035**, structure (textured) or smooth semi-gloss, with a dry film thickness of **60 to 80 microns**. Base frames are coated in **RAL 2000** orange or black as the customer requires; outdoor panels use pure polyester (UV resistant) powder, often at 80 to 100 microns.

Parts arrive from the dry-off oven of PTL-08 on the overhead conveyor, are coated in the booth, cured in the oven, and unloaded after cooling for inspection and dispatch to assembly.

## 13.2 How it works

[[fig:powder|Figure 13-1. Electrostatic powder spraying, recovery and curing|470]]

### 13.2.1 Electrostatic spraying

The powder is stored in a **fluidising hopper**: compressed air passes through a porous plate at the bottom and makes the powder behave like a liquid. A **venturi injector** sucks the powder and blows it through a hose to the **spray gun**. At the gun tip a high-voltage **electrode** (up to 100 kV) charges the air around it and the powder particles pick up a negative charge (corona charging). The parts are **earthed** through the hooks and the conveyor. The charged particles are attracted to the earthed part and stick to it, even wrapping around the edges. The charge holds the powder on the part until it is melted in the oven.

### 13.2.2 Recovery

Powder that misses the part (overspray) is drawn by the booth exhaust fan into a **cyclone**, which separates most of the powder and returns it through a **sieve** to the hopper. The fine particles that pass the cyclone are caught by **cartridge filters**, which are cleaned by reverse air pulses. The cleaned air returns to the shop through **after-filters**. The airflow also keeps the powder concentration in the booth well below the lower explosion limit.

### 13.2.3 Curing

The **curing oven** is a gas-fired, recirculating hot air oven. The powder first melts and flows into a smooth film, then the resin and hardener react (cross-link) to form a hard, chemically resistant film. Curing depends on the **metal temperature** and time, not on the air temperature: a thick base channel takes much longer to heat up than a 1.6 mm cover.

| Cure schedule (standard polyester powder) | Metal temperature | Time at that temperature |
|---|---|---|
| Normal | 180 degrees C | 10 minutes |
| Alternative | 200 degrees C | 8 minutes |
| Low-bake powders (on request) | 160 degrees C | 15 minutes |

The oven air set point is 200 degrees C and the conveyor gives about 20 minutes in the oven, which brings 1.6 to 3 mm parts to 180 degrees C for at least 10 minutes. Base frames of 5 mm and above need a slower conveyor speed or a separate batch (section 13.7.4).

## 13.3 Technical data

| Item | Value |
|---|---|
| Booth | Open-front booth with two automatic gun positions (reciprocators) and two manual stations |
| Guns | 6 automatic corona guns on 2 reciprocators, 2 manual corona guns |
| Gun voltage | 0 to 100 kV, set 60 to 80 kV for normal work |
| Recovery | Cyclone with sieve + cartridge after-filter, recovery fan 15 kW |
| Air velocity at booth openings | 0.4 to 0.5 m/s |
| Compressed air | 6 bar, dry (dew point +3 degrees C or lower), oil-free |
| Curing oven | Gas-fired (PNG) indirect, 350 kW, recirculating, set point 200 degrees C |
| Oven length / time at 1.5 m/min | 30 m path / 20 minutes |
| Cooling zone | Forced air cooling, 10 minutes |
| Conveyor | Shared with PTL-08, 1.0 to 2.0 m/min |
| Flame detection | Infrared flame detectors in the booth, shut down guns and fan |

## 13.4 Controls

| Control | Function |
|---|---|
| Booth control panel | Gun on/off, kV and µA settings, powder flow, air flow, reciprocator stroke and speed, recovery fan |
| Manual gun controls | Trigger, kV and powder output selection on the gun control unit |
| Oven HMI | Zone temperature set points, burner status, fan status, chart recorder |
| Conveyor master control | Speed and start / stop for the whole paint line |
| Emergency stops | Booth, oven entry and exit, loading and unloading points |

## 13.5 Safety and specific hazards

!! WARNING: Powder in air can explode when it reaches its explosive concentration and meets a spark. Sparks come from unearthed objects or people, from a gun held too close to an earthed part, or from hot work. The booth airflow, earthing and cleanliness prevent this. Never switch off the recovery fan while the guns are spraying, and never spray in the booth with the fan off.

- **Earthing**: every part must be earthed through clean hooks (resistance of part to earth below 1 megohm). The operator wears antistatic (conductive) shoes and holds the manual gun with a bare hand or a conductive glove so that the operator is earthed through the gun handle.
- **Gun distance**: keep the manual gun at least 150 mm from the part.
- **No ignition sources**: no mobile phones, lighters, hot work or non-approved electrical equipment in the booth zone.
- **Dust**: wear a FFP2 mask during manual spraying and cleaning; do not blow powder off clothes with compressed air (use a vacuum cleaner).
- **Oven**: hot surfaces and hot parts; flue gases; only trained persons reset burners.
- **Cleaning**: clean with antistatic brushes and an approved (dust explosion-protected) vacuum cleaner.

### 13.5.1 LOTO points of PCL-09

| Energy | Isolation point |
|---|---|
| Electrical | Booth panel main isolator; oven panel main isolator; reciprocator drives |
| High voltage | Gun control units off (included in booth isolator); discharge the gun electrodes against an earthed part |
| Gas | Oven gas train manual valve closed and locked |
| Compressed air | Booth air inlet valve locked with exhaust |
| Conveyor | Conveyor drive isolator; pull cords |
| Thermal | Oven cooled below 50 degrees C before entry (confined space permit for oven entry) |

## 13.6 Start-up procedure

1. Start the oven heating 45 minutes before production; wait until all zones are at set point.
2. Check the compressed air: pressure 6 bar, water separator drained, dryer running.
3. Check the hopper powder level and colour; fluidise for 5 minutes before spraying (the powder surface should "boil" gently, without craters or spouts).
4. Check the hooks on the conveyor: clean (burnt-off) hooks give good earth. Replace coated hooks.
5. Start the recovery fan; check the pressure drop of the cartridge filters.
6. Switch on the gun control units; set kV and powder output for the job (section 13.7.1).
7. Spray a test panel; check film thickness after curing (or with an uncured-powder thickness comb as a quick check).
8. Start the conveyor with the pre-treatment line.

## 13.7 Normal operation

### 13.7.1 Gun settings

| Situation | kV | Current limit (microamps) | Powder output | Gun distance |
|---|---|---|---|---|
| Flat panels, covers | 70 to 80 | 30 to 50 | Medium | 200 to 250 mm |
| Recessed areas, inside corners (Faraday cage) | 30 to 50 | 10 to 20 | Low to medium, higher air velocity | 150 to 200 mm |
| Second coat / recoat | 40 to 50 | 10 to 15 | Low | 200 to 250 mm |
| Edges and small brackets | 60 to 70 | 20 to 30 | Low | 200 mm |

!! TIP: Inside corners of a panel frame are hard to coat because the electric field lines go to the outer edges and not into the corner (Faraday cage effect). Coat the inside corners first with the manual gun at lower kV, pointing the gun straight into the corner, then let the automatic guns coat the flat faces.

### 13.7.2 Manual touch-up

The manual operator stands at the station after the automatic guns and coats areas the automatic guns cannot reach: the inside of frames, the back of door returns, the inside of louvres. Keep the gun moving; spraying too long in one place builds a thick layer that will run or crack, and causes back-ionisation (rough, star-shaped spots).

### 13.7.3 Masking

Areas that must remain bare (earth studs and earth nuts, threads, contact faces for earthing of doors and mounting plates, and busbar support faces if the drawing says so) are masked before pre-treatment or before coating:

- Silicone plugs and caps for threads and studs.
- High-temperature masking tape (polyester, 200 degrees C) for flat contact areas.
- Remove the masking after curing while the part is still warm (the tape comes off cleaner).

### 13.7.4 Heavy parts

Base frames and parts of 5 mm and thicker absorb heat slowly. Run them in a separate batch at 1.0 m/min (30 minutes in the oven) or use the oven in batch mode. The curing of heavy parts is verified with the **oven temperature data logger** (section 13.8.2) at least once a month and whenever a new type of heavy part is introduced.

### 13.7.5 Colour change

1. Stop spraying; run the conveyor empty for one hook spacing.
2. Clean the guns: blow out the powder hoses and gun with clean air; clean the gun nozzle and electrode.
3. Empty the hopper; clean it and the fluidising plate with a vacuum cleaner.
4. Clean the booth walls and floor from top to bottom with an antistatic squeegee and vacuum.
5. Clean the cyclone and sieve (or change to the dedicated cyclone for that colour if fitted).
6. Fill the hopper with the new powder; spray a test panel.
7. Colour change takes about 45 minutes from RAL 7035 to another light colour, longer from dark to light colours. Planning groups parts by colour to reduce changes.

## 13.8 Quality checks

| Test | Method | Frequency | Requirement |
|---|---|---|---|
| Dry film thickness (DFT) | Magnetic induction gauge, 5 readings per part face | First part of each type, then 1 in 20 parts | 60 to 80 microns (indoor); 80 to 100 microns (outdoor) |
| Appearance | Visual at 1 m in daylight or 800 lux | Every part | Uniform colour and texture; no runs, pinholes, craters, inclusions, bare spots |
| Adhesion | Cross-cut test (ISO 2409), 6 cuts 2 mm apart each way, tape pull | Daily on test panel | Class 0 or 1 (less than 5 % flaked) |
| Cure | Solvent rub test: 30 double rubs with MEK-soaked cloth | Daily on test panel and heavy parts | Slight dulling allowed; no softening or removal to metal |
| Hardness | Pencil hardness | Weekly | H or harder |
| Impact | Falling weight (reverse impact) on test panel | Weekly | No cracking or loss of adhesion at the value of the powder data sheet |
| Gloss | Gloss meter at 60 degrees (smooth finishes only) | Each powder lot | Within +/- 5 units of the specification |
| Colour | Visual against master plate; colour meter for critical jobs | Each powder lot | Matches master plate |
| Salt spray | Sample panels sent to an external laboratory (ISO 9227) | Every 3 months and for customer orders that require it | Typically 500 hours: creep from scribe below 2 mm, no blisters |

### 13.8.1 Measuring film thickness

1. Calibrate the gauge on a bare, flat steel sample of the same thickness, using the foils supplied with the gauge.
2. Take readings at least 25 mm from edges, on flat areas.
3. Take 5 readings per face and record the average and the lowest value.
4. No single reading below 50 microns is accepted on indoor parts (below 65 microns on outdoor parts).

### 13.8.2 Oven temperature profile

Monthly, a data logger with thermocouples (one in the air, three clamped to parts of different thickness) is passed through the oven with the production load. The curve must show that the thickest part reaches 180 degrees C for at least 10 minutes and no part exceeds 220 degrees C. The profile is kept in the quality file.

## 13.9 Shutdown

1. Stop spraying after the last loaded parts; run the conveyor until the oven is empty (the oven must not be shut down with parts inside, they will be under-cured).
2. Switch off guns; leave the recovery fan running for 10 minutes to clear the booth.
3. Clean guns and nozzles; cover the hopper.
4. Switch off the oven burners; the circulation fan runs until the oven is below 80 degrees C (automatic).
5. Clean the booth floor; empty the waste powder container into the closed waste bin.
6. Record the oven chart, DFT readings and powder consumption.

## 13.10 Maintenance

| Frequency | Task | By |
|---|---|---|
| Daily | Clean guns, nozzles and electrodes; clean booth; drain air filter; check hooks; check filter pressure drop | Operator |
| Weekly | Clean the sieve; check powder hoses for wear and blockage; replace worn hoses; clean the injector venturi; check earth resistance of conveyor and hooks (below 1 megohm) | Operator, technician |
| Monthly | Replace venturi inserts if worn; check reciprocator belts and limit switches; check flame detector function with test lamp; strip hooks (burn-off or chemical) | Technician |
| Every 3 months | Replace after-filters as needed; check cartridge filter condition; clean oven ducts and fans | Technician |
| Yearly | Burner service; oven insulation and door seals check; recalibration of oven thermocouples and gun kV display; airflow measurement at booth openings | Contractor, quality |

## 13.11 Troubleshooting

| Defect | Appearance | Likely cause | Remedy |
|---|---|---|---|
| Poor wrap / thin coating at edges | Edges and back thinly coated | Bad earth (dirty hooks), low kV | Clean hooks; check earth below 1 megohm; raise kV |
| Faraday cage | Inside corners bare | High kV repels powder from corners | Lower kV, use deflector nozzle, coat corners first |
| Back-ionisation | Rough "orange peel" with star-shaped craters, film limited | Too long spraying, high kV, film already thick | Lower kV and current limit; keep gun moving |
| Orange peel (heavy texture on smooth powder) | Wavy surface | Film too thick, slow heat-up, powder too coarse | Reduce DFT; check oven heat-up; check powder |
| Pinholes | Tiny holes in film | Moisture, gas from the substrate (welds, porous parts), film too thick | Dry parts fully; pre-heat (degas) welded parts; reduce DFT |
| Craters / fish-eyes | Round depressions | Oil or silicone contamination (air, hands, spray products) | Check compressed air for oil; no silicone sprays in plant; clean |
| Inclusions / dirt | Bumps with particles | Dirty booth, contaminated recovered powder, dirty oven | Clean booth and oven; check sieve |
| Under-cure | Soft film, fails solvent rub, poor impact | Oven temperature low, conveyor too fast, heavy parts | Check profile; slow conveyor; batch heavy parts |
| Over-cure | Yellowing, loss of gloss, brittle | Too high temperature or too long (stoppage in oven) | Check set point; remove parts quickly after a stoppage |
| Poor adhesion | Film peels at cross-cut | Poor pre-treatment, under-cure, contamination | Check PTL-08 records and cure; check for oil |
| Colour mismatch | Different shade | Powder lot change, over-cure, contamination from previous colour | Check lot and master plate; clean properly at colour change |
| Powder spits from gun | Lumps on part | Moist air, worn venturi, blocked hose, damp powder | Check air dryer; replace venturi; store powder correctly |

| Code | Message | Action |
|---|---|---|
| PC-01 | Emergency stop | Reset |
| PC-02 | Flame detected | All guns and fan stopped automatically; check booth; follow fire procedure; investigate cause before restart |
| PC-03 | Recovery fan off / airflow low | Guns blocked; check fan and filters |
| PC-04 | Filter differential pressure high | Pulse clean; replace cartridges if pressure stays high |
| PC-05 | Gun high voltage fault | Check gun cable and electrode; replace cascade if faulty |
| PC-06 | Hopper level low | Fill powder |
| PC-07 | Fluidising air pressure low | Check air supply and regulator |
| PC-08 | Reciprocator fault | Check drive, belt, limit switches |
| PC-09 | Oven burner lockout | Trained person only; check gas; reset once; call burner service if repeated |
| PC-10 | Oven temperature out of range | Check burner, circulation fan, thermocouple; hold parts until temperature is in range |
| PC-11 | Oven circulation fan failure | Burner stops automatically; check fan motor and belt |
| PC-12 | Conveyor stopped | Check drive and pull cords; remove parts from the oven if the stop is longer than 10 minutes |

## 13.12 Powder storage and handling

- Store powder boxes in a cool, dry room below 30 degrees C and away from direct sunlight, oven heat and water.
- Keep boxes closed; use powder within its shelf life (12 months for most polyester powders), first in, first out.
- Mix recovered powder with fresh powder in a ratio of about 1 part recovered to 3 parts fresh to keep the particle size balanced.
- Do not use powder that is lumpy (exposed to heat or moisture); sieve or reject it.
- Record powder lot numbers on the job card for traceability.

## 13.13 Operator quick card

!! HINGLISH: PCL-09 mein powder electrostatic gun se lagta hai aur oven mein 180 degree metal temperature par 10 minute pakta hai. Hooks saaf hone chahiye, warna earth nahi milta aur powder nahi chipakta. Antistatic joote pehno, manual gun ko kam se kam 150 mm door rakho. Fan band karke kabhi spray mat karo. DFT 60-80 micron hona chahiye, har 20 part mein ek naapo. Mobile phone booth mein nahi. Oven mein parts chhod ke line band mat karo. Earth stud ki masking cap curing ke baad garam halat mein hatao.
