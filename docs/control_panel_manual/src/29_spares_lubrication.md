# 29. Spare Parts, Lubrication and Maintenance Stores

## 29.1 Spare parts policy

| Category | Definition | Stock rule | Examples |
|---|---|---|---|
| Critical (insurance) spares | Long lead time, failure stops a critical machine | Keep 1 always, even if rarely used | BRAKE-04 servo valve, laser guard set, LASER-03 protective windows and nozzles, COMP-15 separator |
| Consumable spares | Used regularly | Minimum / maximum stock based on consumption | Filters, nozzles, contact tips, punch springs, blades |
| Common spares | Used across many machines | Standardised items kept in stock | Proximity sensors M12 and M18, contactors, MCBs, fuses, relays, push buttons |
| Non-stock | Cheap or quick to buy | Bought when needed | Uncommon fasteners, special cables |

### 29.1.1 Minimum and reorder levels

For consumables, the store sets:

- **Minimum stock** = average consumption per week x supplier lead time in weeks + safety stock.
- **Reorder level** = minimum stock + one week's consumption.
- **Maximum stock** = reorder level + economic order quantity.

The maintenance planner reviews the consumption and the levels every quarter.

### 29.1.2 Issuing spares

1. The technician issues a spare against a work order number (breakdown or PM) in the store register or system.
2. Defective parts that can be repaired (servo valves, drives, PCBs, motors) are returned to the store with a red "repairable" tag and the fault description, and are sent for repair.
3. Parts removed for testing and found good are returned with a green tag.
4. The store informs the planner when an item falls below the reorder level.

### 29.1.3 Storage of spares

- Electronic spares (drives, PLC modules, PCBs, sensors) in antistatic bags, in a dry cabinet, away from heat.
- Bearings in their original packing, lying flat; first in, first out.
- Rubber parts (seals, belts, hoses) away from light, heat and ozone sources (motors, welding); note the date of manufacture: seals and hoses age even in storage.
- Hydraulic and pneumatic components with port caps fitted.
- Spare motors: shafts turned by hand every 3 months to redistribute grease; space heaters connected if long storage.

## 29.2 Lubrication

### 29.2.1 Lubricant list

To avoid mixing errors, the plant uses a short list of lubricants. Each lubrication point is marked with a coloured symbol matching the lubricant.

| Code | Lubricant | Colour mark | Used for |
|---|---|---|---|
| H46 | Hydraulic oil ISO VG 46 HLP | Blue circle | SHEAR-01, PUNCH-02, BRAKE-04, BUS-10 hydraulic systems |
| H32 | Hydraulic oil ISO VG 32 HLP | Blue square | PEM-07 |
| P32 | Pneumatic lubricator oil ISO VG 32 | Light blue | FRL lubricators where fitted |
| G2 | Lithium complex EP grease NLGI 2 | Green triangle | Machine guides, bearings with nipples, crane wheels |
| GL | Linear guide grease (maker specified) | Green square | Linear guides and ball screws of CNC axes |
| W68 | Way oil ISO VG 68 | Yellow circle | Central lubrication tanks (PUNCH-02) |
| G220 | Gear oil ISO VG 220 EP | Red triangle | Gearboxes, crane hoist gearbox |
| CO | Compressor oil (maker's synthetic) | Black circle | COMP-15 |
| HT | High-temperature chain oil | Orange circle | Paint line conveyor chain (oven section) |

### 29.2.2 Lubrication chart (summary)

| Asset | Point | Lubricant | Interval | By |
|---|---|---|---|---|
| SHEAR-01 | Beam guides (4 nipples) | G2 | Weekly | Operator |
| SHEAR-01 | Back gauge ball screws and guides | GL | Weekly | Operator |
| PUNCH-02 | Central lubrication tank | W68 | Check daily, fill as needed | Operator |
| PUNCH-02 | Turret bearing | G2 | Monthly | Technician |
| LASER-03 | Rack and pinion, guides (automatic system) | Maker's grease | Check tank weekly | Operator |
| BRAKE-04 | Ram gibs | G2 | Weekly | Operator |
| BRAKE-04 | Back gauge screws and guides | GL | Weekly | Operator |
| BUS-10 | Carriage guides and rack | G2 / GL | Weekly | Operator |
| BUS-10 | Punch lubrication | W68 | Daily check | Operator |
| PCL-09 / PTL-08 | Conveyor chain | HT (oven), G2 trolleys | Weekly (automatic oiler check daily) | Technician |
| COMP-15 | Motor bearings (if nipples) | G2 | As per motor plate | Technician |
| CRANE-16 | Wire rope | Rope lubricant | Monthly | Technician |
| CRANE-16 | Hoist gearbox | G220 | Check monthly, change yearly | Technician |
| All motors with nipples | Bearings | G2 | As per motor plate | Technician |

### 29.2.3 Good lubrication practice

- Clean the nipple before greasing; dirt pushed into a bearing destroys it.
- Use the grease gun of the colour code: one gun per grease type.
- Give the specified number of shots; do not over-grease.
- Wipe off old grease that comes out.
- Record lubrication on the machine's lubrication card.
- Store lubricants in the lubrication room in labelled, closed containers; use dedicated transfer containers for each oil.

## 29.3 Maintenance tools and instruments

| Tool / instrument | Location | Control |
|---|---|---|
| Electrical tool kits (insulated 1000 V) | Each electrical technician | Monthly inspection; insulation damage = replace |
| Mechanical tool kits | Each mechanical technician | Monthly inspection |
| Multimeters, clamp meters, insulation testers | Maintenance tool room | Calibrated yearly; issued against signature |
| Thermal camera, vibration meter, ultrasonic detector | Maintenance office | Calibrated yearly |
| Hydraulic test gauges and hoses | Tool room | Gauges calibrated yearly |
| Bearing heater and pullers | Workshop | - |
| Laser alignment tool | Tool room | Checked yearly |
| Torque wrenches (maintenance) | Tool room | Calibrated every 6 months |
| LOTO locks, hasps, tags | LOTO station at each bay | Checked monthly; missing locks reported |
| Portable earthing sets | Electrical room | Inspected before use |

## 29.4 Maintenance workshop

The workshop has a bench drill, bench grinder, vice benches, a hydraulic press for bearing work, a hose crimping machine, a parts washer, and an electrical repair bench with a variable supply. Work on electrical items (contactors, small motors, PCBs) is done on the electrical bench with ESD mats for electronics.

!! HINGLISH: Critical spare (jaise BRAKE-04 ka servo valve, laser ki window aur nozzle) hamesha stock mein. Spare part sirf work order number par nikalo. Kharab repair hone wala part laal tag ke saath store mein wapas. Har lubrication point par rang ka nishaan hai, usi rang ki grease gun aur oil use karo. Nipple pehle saaf karo, phir grease. Grease zyada mat bharo.
