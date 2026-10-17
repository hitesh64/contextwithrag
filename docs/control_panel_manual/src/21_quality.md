# 21. Quality Control, Non-conformance and Calibration

## 21.1 Quality plan of a panel

The quality plan sets the inspection points from material receipt to dispatch. Each point names what is checked, by whom, how much (100 % or sample), and the record. The table is the standard plan; a customer's inspection and test plan (ITP) may add hold points witnessed by the customer.

| Stage | Inspection | By | Extent | Record |
|---|---|---|---|---|
| Receipt of sheet and busbar | Thickness, size, surface, certificates (Chapter 5) | Store and quality | Each lot | Goods receipt inspection report |
| Receipt of bought-out devices | Make, type, rating, damage, quantity against purchase order | Store and quality | 100 % | Goods receipt inspection report |
| Cutting | First-off dimensions | Operator, inspector | First part of each program and shift | Job card stamp |
| Bending | First-off angles and dimensions | Operator, inspector | First part of each program | Job card stamp |
| Welding | Visual, dimensions | Inspector | 100 % visual | Job card stamp |
| Fabrication before paint | Dimensions, hardware, burrs (Chapter 11.5) | Inspector | 100 % of sub-assemblies | Green "OK for paint" tag |
| Pre-treatment | Bath control, coating weight | Paint shop operator, quality | Per shift / daily | Bath log |
| Powder coating | DFT, appearance, adhesion, cure | Paint shop inspector | Sample as per Chapter 13 | Paint inspection report |
| Busbars | Dimensions, bends, sleeving | Busbar inspector | First-off and sample | Busbar inspection report |
| Wire kits | Crimp checks, pull test | Wire cell supervisor | First-off and sample | Crimp log |
| Assembly | Assembly inspection (Chapter 16.6) | Assembly inspector | 100 % | Assembly checklist |
| Wiring | Self-check, then testing | Wireman, tester | 100 % | Wiring checklist |
| Testing | Routine tests (Chapter 20) | Testing engineer | 100 % | Routine test report |
| Final | Packing, documents | Quality | 100 % | Dispatch clearance |

## 21.2 First-off approval

The first part made after any set-up (new program, new tool, new material lot, start of shift, after a repair) is checked completely against the drawing before the batch continues. The operator measures and the inspector or supervisor approves by stamping the job card. If the first-off fails, the set-up is corrected and a new first-off is made. Parts made before the first-off was approved are held until checked.

## 21.3 Non-conforming product

A non-conforming product is any part, sub-assembly or panel that does not meet the drawing, specification or this manual.

1. **Identify**: put a red "HOLD" tag on it with the defect described.
2. **Segregate**: move it to the red quarantine area (or, for a large panel, mark it clearly and inform the supervisor).
3. **Report**: the inspector raises a non-conformance report (NCR) with: job number, part, quantity, defect, where found, who found it, photos.
4. **Decide** (quality manager with production and, if needed, design): rework, repair, use as is (concession, only with design approval and, if it affects the customer's requirements, with the customer's written approval), or scrap.
5. **Act**: carry out the decision; re-inspect reworked parts.
6. **Find the cause**: for repeated or serious defects, find the root cause (section 21.4) and take corrective action.
7. **Close** the NCR when the action is done and verified.

## 21.4 Root cause analysis

A defect fixed without finding its cause will come back. Two simple tools are used.

### 21.4.1 Five whys

Ask "why" until you reach a cause that you can act on. Example:

| Question | Answer |
|---|---|
| Why did the panel fail the earth continuity test? | The earth reading on door 3 was 2.5 ohm. |
| Why was it 2.5 ohm? | The earth braid was fixed to the door stud over paint. |
| Why was there paint on the stud? | The masking cap was missing during powder coating. |
| Why was it missing? | The cap fell off in the pre-treatment tunnel. |
| Why did it fall off? | The silicone caps of the new lot are one size too large for M6 studs. |

Action: return the cap lot; add a cap fit check in the receiving inspection; add an earth stud bare-metal check at the paint unloading point.

### 21.4.2 Fishbone (cause and effect) diagram

Write the problem at the head of the "fish" and list possible causes on six bones: **Man** (training, skill), **Machine** (condition, settings), **Method** (procedure, drawing), **Material** (lot, supplier), **Measurement** (gauge, calibration), **Environment** (temperature, humidity, light, dust). Then check which causes are true with data.

## 21.5 Calibration of measuring instruments

Every instrument used to accept or reject a product, or to set a machine that decides quality, is calibrated at a fixed interval against standards traceable to national standards (via an accredited laboratory).

| Instrument | Interval | By |
|---|---|---|
| Vernier calipers, micrometers, height gauges | 12 months | Accredited laboratory or in-house against gauge blocks |
| Steel tapes and rules | 12 months | In-house against a calibrated master tape |
| Digital protractors, squares | 12 months | In-house against master |
| Torque wrenches and torque screwdrivers | 6 months | Accredited laboratory |
| Crimping tools (hand and hydraulic) | 12 months | Tool maker or accredited laboratory |
| DFT gauges | 12 months (foils checked daily) | Accredited laboratory |
| Multimeters, clamp meters, IR testers, HV tester, earth continuity tester | 12 months | Accredited laboratory |
| Secondary injection set, micro-ohmmeter | 12 months | Accredited laboratory |
| Pull tester and crimp force monitor | 12 months | Maker or laboratory |
| Oven thermocouples and data logger | 12 months | Accredited laboratory |
| Pressure gauges on machines (critical) | 12 months | In-house against master gauge |

Each instrument has an ID number and a calibration sticker showing the due date. An instrument that is overdue, damaged or out of tolerance is removed from use and tagged. When an instrument is found out of tolerance, the quality manager checks which products were accepted with it since the last good calibration and decides whether they must be re-checked.

## 21.6 Customer complaints

Complaints from site (for example "MCCB terminal overheated after two months", "door gasket missing", "wrong CT ratio set") are recorded in the complaint register with the job number. The quality manager checks the job records (test report, torque records, NCRs) and the root cause, and replies to the customer with the corrective action. Repeated complaint types are reviewed monthly with the plant head.

## 21.7 Documentation supplied with a panel

| Document | Prepared by |
|---|---|
| As-built drawings (all revisions corrected after testing) | Design |
| Bill of materials | Design |
| Routine test report | Testing |
| FAT report (if witnessed) | Testing / customer |
| Device manuals and catalogues (breakers, relays, drives, PLC) | Purchase / design |
| Protection setting chart | Design / testing |
| Installation, operation and maintenance instructions for the panel | Design |
| Packing list | Dispatch |
| Warranty certificate | Sales |

## 21.8 Records retention

| Record | Kept for |
|---|---|
| Job cards, inspection reports, test reports | 10 years |
| Calibration records | 10 years |
| NCRs and complaint records | 10 years |
| Bath logs, oven profiles | 5 years |
| Training records | Employment period plus 5 years |

!! HINGLISH: Har setup ke baad pehla part (first-off) inspector se approve karao. Kharab part par laal HOLD tag lagao aur red area mein rakho, phir NCR bharo. Galti ka asli kaaran "paanch kyon" se dhundho, sirf part theek karna kaafi nahi. Jis instrument ka calibration sticker expire ho gaya ho, use istemaal mat karo.
