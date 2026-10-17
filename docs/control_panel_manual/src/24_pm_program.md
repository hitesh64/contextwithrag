# 24. Preventive Maintenance Programme

## 24.1 Maintenance strategies

| Strategy | Meaning | Used for |
|---|---|---|
| Breakdown (run to failure) | Repair only after failure | Cheap, non-critical items with spares in stock (hand tools, small fans, lamps) |
| Preventive (time-based) | Fixed tasks at fixed intervals (days, running hours, strokes) | Lubrication, filters, oil changes, safety device tests |
| Condition-based (predictive) | Measure the condition and act when it shows deterioration | Bearings (vibration), electrical joints (thermography), hydraulic oil (analysis) |
| Autonomous maintenance | Operators do basic daily care: cleaning, inspection, lubrication, tightening | All machines |
| Improvement (corrective) | Change the design or method to remove the cause of repeated failures | Repeated breakdowns found in the history |

The plant uses all of them. The aim is that most work is planned; a breakdown should be the exception.

## 24.2 Criticality of assets

Each asset has a criticality rating that decides the PM depth, the spare parts stock and the response time.

| Factor | Score 1 | Score 2 | Score 3 |
|---|---|---|---|
| Effect on production | Other machine can do the work | Partial loss | Whole flow stops |
| Effect on safety / environment | None | Minor | Serious hazard if it fails |
| Effect on quality | None | Minor rework | Defects reach the customer |
| Repair time and spares lead time | Below 4 h | 4 h to 2 days | Above 2 days |

Total score 4 to 6: low; 7 to 8: medium; 9 to 10: high; 11 to 12: critical. The criticality of each asset is shown in the asset register (About This Manual).

## 24.3 Master PM schedule

The table summarises the PM tasks of every asset. Details are in each machine chapter. "Op" = operator, "Tech" = maintenance technician, "Ext" = external service.

| Asset | Daily (Op) | Weekly | Monthly (Tech) | 6-monthly | Yearly |
|---|---|---|---|---|---|
| SHEAR-01 | Oil level, E-stops, light curtain, cleaning | Lubricate guides, back gauge screws (Op/Tech) | Blade gap, oil temp, back gauge accuracy | Return filter | Oil analysis, blades, hoses, beam parallelism |
| PUNCH-02 | Air, oil, E-stops, light curtain, slugs | Lubricate axes, punch wear check | Turret alignment, accuracy test, cabinet | Hydraulic filters | Backlash, turret bushings, ram |
| LASER-03 | Chiller, window, nozzle, height calibration, gas, slag trays | Slats, rack lubrication, chiller fins | Chiller filter, extractor filters, squareness | Chiller water change | Optics service and laser power (Ext) |
| BRAKE-04 | Laser guard test, oil, tools, oil temperature | Guides, clamps, pedal | Ram parallelism, back gauge, guard alignment | Filters, oil sample | Scales, ram drift test, tools |
| WELD-05 | Water flow, air, test welds, tip dressing | - | Tip holders, hoses | - | Transformer and timer check |
| WELD-06 | Nozzle, tip, cables, gas hose | Liner, drive rolls | Liner, cables | - | Calibration of power source |
| PEM-07 | Safety test, tooling, oil | Feeder | Force verification | - | Oil, filter, sensing circuit |
| PTL-08 | Nozzles, leaks, bath tests, skimming | Strainers, nozzles, thermometers | Desludge, heat exchanger, pump checks | Pickling bath, tank cleaning, DM resin | Burner service (Ext), lining |
| PCL-09 | Guns, booth, hooks, filter dP | Sieve, hoses, venturi, earth test | Venturi inserts, reciprocator, flame detector | After-filters, oven ducts | Burner (Ext), oven profile and calibration |
| BUS-10 | E-stops, two-hand, oil, slugs | Tools, guides, blades, dies | X accuracy, angle encoder | Filters | Oil, shear clearance, hoses |
| WIRE-11 | Cleaning | Blades, belts, length test | - | - | Service |
| CRIMP-12 | Dies, air | - | Die wear, lubrication | - | Monitor and pull tester calibration |
| MARK-13 | Head cleaning at ribbon change | Cutter | - | - | - |
| TEST-14 | Leads, beacons, gate interlocks | - | Emergency stops, earthing stick | - | Instrument calibration (Ext) |
| COMP-15 | Pressures, temperature, drains, dryer | Inlet filter, cooler | - | Per running hours: filters, oil, separator | Safety valve, receiver (statutory) |
| CRANE-16 | Pre-use check | Limits, brakes | Rope, gearbox, wheels | Brakes, electricals | Load test (statutory) |

## 24.4 PM work order process

PM tasks are issued as work orders from the maintenance system according to the schedule.

1. **Generate**: the maintenance planner generates the PM work orders for the week every Friday, with the checklist, the parts and the LOTO points.
2. **Approve**: the maintenance manager reviews and approves the work orders; a work order is not started before approval. Safety-related tasks (light curtains, interlocks, LOTO points, crane, pressure vessels) are approved only by the maintenance manager.
3. **Schedule**: the production supervisor and the maintenance planner agree on the time slot (usually the first two hours of the general shift, or on Sundays for long tasks).
4. **Execute**: the technician applies LOTO, carries out every step of the checklist, records readings (pressures, temperatures, currents, clearances), parts used and observations.
5. **Hand over**: trial run with the operator, guards refitted, LOTO removed.
6. **Close**: the technician records the completion; the maintenance manager or supervisor verifies and closes. Findings that need further work generate a corrective work order.

Work order states: **draft, pending approval, approved, in progress, completed**; a work order may also be **rejected** (with a reason) or **cancelled**.

!! NOTE: A PM checklist step that cannot be completed (for example "replace filter" without the filter in stock) is never ticked as done. It is recorded as "not done" with the reason, and a follow-up work order is raised.

## 24.5 Breakdown recording

Every breakdown is recorded, even when it is repaired in a few minutes. Good records are the only way to find repeated problems.

| Field | Example |
|---|---|
| Asset code | BRAKE-04 |
| Date and time of failure | 2026-09-14 10:20 |
| Reported by | Operator name |
| Symptom (what was seen) | Back gauge not moving, alarm PB-12 |
| Start and end time of repair | 10:32 to 11:05 |
| Downtime (minutes) | 45 |
| Cause found | X axis encoder cable connector loose at back gauge drive |
| Action taken | Connector cleaned, refitted, cable tied with strain relief |
| Parts used | None |
| Root cause known? | Yes / No; if no, write "root cause not found" |
| Technician | Name |

!! TIP: Write the symptom in the words of the operator and the cause in technical words. "Machine not working" is not a symptom; "ram does not move down, pedal LED on, alarm PB-02" is.

## 24.6 Condition monitoring

| Technique | What it finds | Assets | Interval |
|---|---|---|---|
| Vibration measurement (velocity mm/s RMS) | Bearing wear, unbalance, misalignment, looseness | Motors above 5.5 kW: compressor, hydraulic pumps, spray pumps, recovery fan, oven fans | Monthly |
| Thermography | Loose or overloaded electrical connections, blocked coolers, failing bearings | Main LT panel, PDBs, machine control cabinets, motors | Monthly for panels, quarterly for machines |
| Oil analysis | Wear metals, water, contamination, oil degradation | Hydraulic systems of SHEAR-01, PUNCH-02, BRAKE-04, BUS-10; compressor | Every 6 months |
| Motor current and insulation | Winding deterioration, overload | Motors above 5.5 kW | Every 6 months (IR at 500 V DC: above 10 megohm for 415 V motors) |
| Ultrasonic | Air leaks, bearing lubrication condition | Air network, bearings | Monthly |

### 24.6.1 Vibration limits (velocity RMS, small machines up to 15 kW on rigid foundations, guide values)

| Zone | Velocity (mm/s RMS) | Meaning |
|---|---|---|
| A | Up to 1.4 | New machine condition |
| B | 1.4 to 2.8 | Acceptable for long-term operation |
| C | 2.8 to 4.5 | Not acceptable for long-term operation: plan repair |
| D | Above 4.5 | Damage likely: repair as soon as possible |

### 24.6.2 Thermography of electrical connections (temperature rise compared with a similar connection under the same load)

| Rise above similar connection | Action |
|---|---|
| 1 to 10 degrees C | Monitor; check at next shutdown |
| 10 to 20 degrees C | Repair at next planned stop (within 1 month) |
| 20 to 40 degrees C | Repair as soon as possible (within 1 week) |
| Above 40 degrees C | Immediate repair: reduce load or shut down |

## 24.7 Maintenance performance indicators

| Indicator | Formula | Target |
|---|---|---|
| Availability (critical machines) | (planned time - downtime) / planned time | Above 95 % |
| MTBF | Total running time / number of failures | Increasing |
| MTTR | Total repair time / number of failures | Below 2 h |
| PM compliance | PM work orders completed on time / PM work orders due | 100 % (minimum 95 %) |
| Planned work ratio | Planned maintenance hours / total maintenance hours | Above 80 % |
| Repeat breakdowns | Breakdowns of the same asset with the same cause within 30 days | Zero |
| Spare part availability | Requests met from stock / total requests | Above 95 % |

The maintenance manager reviews these monthly. For each asset with repeated breakdowns, a root cause analysis is done (Chapter 21.4) and the PM checklist is improved.

## 24.8 Autonomous maintenance by operators

Operators own the basic condition of their machines:

1. **Clean**: cleaning shows defects (leaks, cracks, loose bolts) that would otherwise be hidden by dirt.
2. **Inspect**: during cleaning, look at hoses, cables, guards, gauges and listen for noise.
3. **Lubricate**: points marked with a green tag are lubricated by the operator; red tags by maintenance.
4. **Tighten**: loose bolts on guards and covers that the operator can reach without LOTO.
5. **Tag**: a defect the operator cannot fix is marked with a red defect tag (with date and description) and reported; maintenance removes the tag when repaired.

Visual aids are fitted to make abnormalities easy to see: min / max marks on oil levels, green / red zones on gauges, match marks on bolts, flow indicators on water lines.

!! HINGLISH: PM ka matlab hai kharabi aane se pehle kaam karna. Har PM work order manager ke approval ke baad hi shuru hota hai, LOTO ke saath. Checklist ka jo step nahi hua, use "done" mat likho, kaaran likho. Har breakdown record karo, chahe 5 minute ka ho: asset code, kya dikha, kya kaaran mila, kya kiya, kaunsa part laga. Operator roz machine saaf karega, dekhega, green tag wale point par oil dalega aur kharabi par red tag lagayega.
