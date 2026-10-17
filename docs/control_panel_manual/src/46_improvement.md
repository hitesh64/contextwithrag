# 46. Continuous Improvement on the Shop Floor

## 46.1 Kaizen: small improvements by everyone

Kaizen means continuous small improvements made by the people who do the work. Every worker can propose an improvement on the kaizen sheet at the bay notice board: the problem, the idea, and the expected benefit. The supervisor reviews proposals weekly; simple ones are implemented at once by the team. Implemented kaizens are displayed on the board with the name of the proposer.

| Example kaizen | Benefit |
|---|---|
| Shadow board for press brake tools with segment lengths marked | Tool change time reduced from 25 to 12 minutes |
| Colour-coded bins for ferrules matching ferrule colours | Wrong ferrule size errors eliminated |
| Contact numbering card (NO / NC) at wiring benches | Fewer wiring errors on auxiliary contacts |
| Magnetic job card holders on panel frames | Job card no longer lost during assembly |
| Earth stud check gauge at paint unloading | Painted earth studs found before assembly |

## 46.2 OEE: overall equipment effectiveness

OEE shows how well a machine is used in the planned time. It multiplies three factors:

- **Availability** = running time / planned production time (losses: breakdowns, set-ups, waiting for material).
- **Performance** = (ideal cycle time x total count) / running time (losses: slow running, small stops).
- **Quality** = good count / total count (losses: rejects, rework).

**OEE = Availability x Performance x Quality**

### 46.2.1 Example: BRAKE-04 in one shift

| Item | Value |
|---|---|
| Shift length | 480 minutes |
| Planned breaks | 30 minutes |
| Planned production time | 450 minutes |
| Breakdown (PB-12 back gauge, case in Chapter 24.5) | 45 minutes |
| Set-ups (tool changes) | 60 minutes |
| Running time | 450 - 45 - 60 = 345 minutes |
| Ideal cycle time (average bend with handling) | 0.5 minutes per bend |
| Bends made | 600 |
| Good bends (12 rejected for wrong angle) | 588 |
| Availability | 345 / 450 = 76.7 % |
| Performance | (0.5 x 600) / 345 = 87.0 % |
| Quality | 588 / 600 = 98.0 % |
| OEE | 0.767 x 0.870 x 0.980 = 65.4 % |

The biggest loss here is availability (set-ups and the breakdown). Reducing tool change time (section 46.3) and fixing the back gauge cable problem permanently give the largest gains.

### 46.2.2 Typical OEE values

| OEE | Meaning |
|---|---|
| Below 40 % | Poor: large losses, often unrecorded |
| 40 to 60 % | Typical for job-shop machines with many set-ups |
| 60 to 85 % | Good |
| Above 85 % | World class (for repetitive production) |

## 46.3 SMED: quick changeover

SMED (single minute exchange of die) is a method to reduce set-up time.

1. **Observe and record** the current changeover step by step with times (video helps).
2. **Separate internal and external work**: internal steps can only be done with the machine stopped (removing and fitting tools); external steps can be done while the machine still runs (fetching the next tools, reading the drawing, loading the program).
3. **Move internal to external**: prepare tools on a trolley in the order of use before the machine stops; preload the next program; pre-check the material.
4. **Simplify internal steps**: quick clamps, standard tool heights, marked tool positions, fewer bolts.
5. **Standardise** the new method in a work instruction and train.

| Press brake changeover step | Before | After |
|---|---|---|
| Find drawing and program | Internal, 8 min | External (prepared by supervisor) |
| Fetch tools from cabinet | Internal, 10 min | External (tool trolley prepared during previous job) |
| Remove old tools | 6 min | 4 min (tools returned to trolley, not cabinet) |
| Fit new tools | 8 min | 5 min (stations marked on beam, segments pre-sorted) |
| Enter tool setup in CNC | 3 min | 1 min (setup saved in program) |
| Test bend and correction | 6 min | 4 min (corrections saved from last batch) |
| Total internal time | 41 min | 14 min |

## 46.4 Poka-yoke: error proofing

Poka-yoke means designing the process so that a mistake cannot happen, or is detected immediately.

| Mistake | Poka-yoke |
|---|---|
| Wrong ferrule size | Colour-coded ferrules, bins and crimp dies |
| Contactor with wrong coil voltage fitted | Coil voltage variants in separate bins with large labels; BOM line shows coil voltage in bold; inspection line in checklist |
| Busbar joint not torqued | Paint mark after torquing; 100 % visual check of marks |
| Wrong program on machine | Program header checked against job card; barcode on job card read at the machine |
| Fastener inserted on wrong side | Fixture with locating pins that only fits the part one way |
| Earth stud painted | Masking cap fit gauge at receiving; check at paint unloading |
| Missing earth strap on a door | Earth strap kits counted per panel; continuity test is 100 % |
| Forgotten device after HV test | Disconnection tags hung on the panel door, listed and removed one by one at reconnection |

## 46.5 Problem solving in teams

For larger problems (repeated defects, chronic breakdowns), a small team (operator, technician, supervisor, quality) follows the PDCA cycle:

1. **Plan**: define the problem with data; find the root cause (five whys, fishbone, Chapter 21.4); plan the countermeasure.
2. **Do**: implement on a trial basis.
3. **Check**: measure the result against the original data.
4. **Act**: standardise if it works (update this manual, check sheets, programs); otherwise go back to Plan.

## 46.6 Visual management

- Production boards (Chapter 38.2).
- Machine status lamps (andon).
- Floor markings (Chapter 2.1.1).
- Min / max marks on gauges and levels.
- Shadow boards for tools.
- Red tags for defects (Chapter 24.8), HOLD tags for quality.
- Kaizen and safety boards.

Anyone walking through the bay should be able to see in a minute whether things are normal or not.

!! HINGLISH: Kaizen matlab har din chhota sudhaar, har koi idea de sakta hai. OEE = availability x performance x quality; press brake ke example mein 65 % aaya, sabse bada nuksaan setup aur breakdown se. SMED se setup time kam karo: jo kaam machine chalte hue ho sakta hai (tool trolley, drawing, program) wo pehle kar lo. Poka-yoke matlab aisa intezaam ki galti ho hi na: rang wale ferrule bin, torque ke baad paint mark, program header milana.
