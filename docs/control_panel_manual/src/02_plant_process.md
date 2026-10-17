# 2. Plant Layout and Process Flow

## 2.1 Layout of the factory

The factory is arranged so that material moves in one direction, from the raw material store at one end to the dispatch bay at the other, with as little back-tracking as possible. The building has six bays and a utility room.

| Bay | Area | Main equipment | Crane / handling |
|---|---|---|---|
| Store | Raw material and bought-out components | Sheet racks, busbar racks, component bins | Forklift, sheet trolley |
| Bay 1 | Sheet metal cutting | SHEAR-01, PUNCH-02, LASER-03 | Vacuum sheet lifter, pallet trucks |
| Bay 2 | Bending, welding, hardware | BRAKE-04, WELD-05, WELD-06, PEM-07, grinding benches | Jib crane 1 t |
| Bay 3 | Paint shop | PTL-08 pre-treatment line, PCL-09 powder booth and oven | Overhead conveyor |
| Bay 4 | Busbar and wiring preparation | BUS-10, WIRE-11, CRIMP-12, MARK-13 | Busbar trolleys |
| Bay 5 | Panel assembly and wiring | Assembly stands, torque tools, wiring benches | CRANE-16 |
| Bay 6 | Testing, inspection, packing | TEST-14, inspection area, packing area | CRANE-16 |
| Utility room | Compressed air and power | COMP-15, air dryer, receiver, main LT panel | - |

[[fig:plant_flow|Figure 2-1. Material flow through the factory, from store to dispatch|470]]

### 2.1.1 Marked areas on the floor

The floor is marked with painted lines. Every worker must know the meaning of the colours.

| Floor marking | Meaning |
|---|---|
| Yellow continuous line | Walkway and aisle boundary; do not place material on the line or across it |
| White line | Work area and machine boundary |
| Red and white hatching | Keep clear: in front of fire extinguishers, electrical panels and emergency exits |
| Black and yellow hatching | Physical hazard: crane lifting zone, press brake back gauge zone, step or edge |
| Green area | Finished goods and approved parts |
| Red area | Rejected or held parts waiting for decision (quarantine) |
| Blue area | Work in progress waiting for the next operation |

## 2.2 Process flow in detail

### 2.2.1 Stores and material issue

Sheets arrive in bundles with a mill test certificate. The store checks thickness, size, grade and surface (no rust, pits or deep scratches), records the heat number and stacks the sheets flat on racks by thickness and grade. Copper busbars arrive in straight lengths of 3 to 4 metres and are stored horizontally on racks with wooden separators so that the surface is not scratched.

Material is issued against the cutting list (nesting report) of each job. The store writes the job number on the issue slip, and the sheet metal supervisor signs for it.

### 2.2.2 Cutting

Blanks are cut in Bay 1:

- **LASER-03** cuts complex parts with many holes and cut-outs, doors with meter cut-outs, and parts in stainless steel. It works from a nested program in which many parts are arranged on one sheet.
- **PUNCH-02** punches parts with standard holes and louvres from sheets up to 3 mm, where punching is faster than laser cutting, and forms louvres and knock-outs that a laser cannot make.
- **SHEAR-01** cuts sheets into rectangular strips and blanks for simple parts such as covers, base channels and gland plates, and trims sheets to size before punching.

Every cut part receives a tag with the job number, part number and quantity, and goes to the deburring table.

### 2.2.3 Bending, welding and hardware

In Bay 2 the parts are bent on **BRAKE-04** following the bending sequence in the program, then welded where the drawing calls for it. Doors and frames are spot welded on **WELD-05**; base frames and heavy brackets are MIG welded on **WELD-06**. Threaded inserts, studs and nuts are pressed into sheet with **PEM-07** before painting, so that the paint is not damaged later.

After welding, weld spatter is removed and welds are ground smooth where they will be visible. Each sub-assembly is checked against the drawing (first-off inspection, then sample checks) before it moves to the paint shop.

### 2.2.4 Paint shop

Parts are hung on the overhead conveyor and pass through **PTL-08**, the seven-tank pre-treatment line (degreasing, rinsing, derusting, activation, phosphating and passivation) and the dry-off oven. They then pass through the **PCL-09** booth where polyester or epoxy-polyester powder is sprayed electrostatically, and through the curing oven. Standard shade is RAL 7035 (light grey) for the enclosure and RAL 2000 (orange) for the base frame and some mounting plates, unless the customer specifies otherwise.

### 2.2.5 Busbar and wire preparation

In Bay 4 copper and aluminium bars are cut, punched and bent on **BUS-10**, then deburred, cleaned and, if the drawing calls for it, tinned or sleeved with heat-shrink sleeve in phase colours. Wire is cut to length and stripped on **WIRE-11**, crimped on **CRIMP-12**, and ferrules are printed on **MARK-13**. Wire kits are prepared per panel and per wiring diagram so that the wireman receives a complete set.

### 2.2.6 Assembly and wiring

In Bay 5 the painted parts are assembled into the panel structure. The busbar system is erected and torqued, devices are fixed to the mounting plates, ducts and DIN rails are fixed, and the panel is wired according to the power and control drawings.

### 2.2.7 Testing, inspection and dispatch

In Bay 6 every panel undergoes the routine tests of IEC 61439 on **TEST-14**: inspection, continuity of protective circuit, dielectric test, insulation resistance, wiring check and functional test. The customer may witness the factory acceptance test. Finally, the panel is cleaned, the shipping sections are separated, and the panel is packed and dispatched.

## 2.3 Typical cycle times

The table below gives typical times for a standard 6-vertical MCC with 24 feeders. They are used by planning to fix delivery dates and by supervisors to spot delays.

| Stage | Typical duration | Resource |
|---|---|---|
| Design and drawing approval | 5 to 10 working days | Design team, customer |
| Material availability | 2 to 15 days depending on devices | Purchase |
| Sheet metal cutting | 1 to 2 shifts | LASER-03 / PUNCH-02 / SHEAR-01 |
| Bending and welding | 2 to 3 shifts | BRAKE-04, WELD-05, WELD-06 |
| Pre-treatment and powder coating | 1 shift plus 1 shift cooling and unloading | PTL-08, PCL-09 |
| Busbar fabrication | 1 to 2 shifts | BUS-10 |
| Assembly | 3 to 4 shifts | Assembly team of 2 fitters |
| Wiring | 5 to 8 shifts | Wiring team of 2 to 3 wiremen |
| Testing and rectification | 1 to 2 shifts | Testing engineer |
| Packing and dispatch | 1 shift | Packing team |

## 2.4 Job card and traceability

The job card travels with the job. Each operation is signed by the operator who did it and stamped by the inspector who checked it. When a defect is found later, the job card shows who did the operation, on which machine and in which shift, so that the cause can be found and corrected.

| Field on the job card | Filled by |
|---|---|
| Job number, customer, panel name | Planning |
| Drawing numbers and revisions | Planning |
| Operation list with machine codes | Planning |
| Operator name and date for each operation | Operator |
| Quantity produced and rejected | Operator |
| Inspection stamp for each stage | Quality inspector |
| Remarks (deviations, concessions) | Supervisor or quality |

!! CAUTION: Never work from a drawing that does not carry the "released for manufacturing" stamp, and never work from an older revision. If the revision on the job card and the revision on the drawing differ, stop and ask the planning department.

## 2.5 Handling material between stages

- Sheets are lifted with the vacuum lifter or by two persons wearing cut-resistant gloves. A single person must not carry a sheet larger than 1250 x 2500 mm.
- Bent parts are moved on trolleys with rubber-lined shelves to avoid scratches.
- Painted parts are stacked with foam or cardboard separators, never metal to metal.
- Busbars are carried on busbar trolleys with separators; bent busbars are hung on racks so that their bends are not disturbed.
- Assembled panels are moved only with CRANE-16 using the lifting hooks or the base frame, or with a pallet truck under the base frame. Never lift a panel by its door, by a busbar or by a mounting plate.

## 2.6 Key performance figures

The plant tracks a small set of figures every week. Each machine chapter states which of these figures the operator affects.

| Figure | How it is calculated | Target |
|---|---|---|
| On-time delivery | Panels dispatched on or before the promised date / panels dispatched | 95 % |
| First-pass yield at testing | Panels passing routine test without rectification / panels tested | 90 % |
| Sheet metal rework | Rejected or reworked parts / parts produced | Below 2 % |
| Paint rejection | Parts recoated / parts coated | Below 3 % |
| Machine availability | Running time available / planned time | Above 95 % for critical machines |
| Mean time between failures (MTBF) | Running hours / number of breakdowns | Rising trend |
| Mean time to repair (MTTR) | Total repair time / number of breakdowns | Below 2 hours |
| PM compliance | PM tasks done in the month / PM tasks due | 100 % |
| Lost time injuries | Injuries causing loss of a shift or more | Zero |

!! HINGLISH: Material ek hi direction mein chalta hai: store se cutting, bending, welding, paint, busbar, assembly, wiring, testing aur dispatch. Job card har stage par sign karna zaroori hai. Purane revision ki drawing se kaam bilkul mat karo.
