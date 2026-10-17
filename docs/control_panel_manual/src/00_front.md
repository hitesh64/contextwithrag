# About This Manual

## Purpose

This manual describes how the demonstration factory builds low-voltage electrical control panels, from the moment a sheet of steel arrives at the store to the moment a tested, packed panel leaves the dispatch bay. It explains how each machine in the plant works, how an operator starts, runs and stops it, how a technician maintains and repairs it, and how the assembly, wiring and testing teams turn fabricated enclosures into finished panels.

The manual is written for the people who do the work: machine operators, panel fitters, wiremen, testing engineers, quality inspectors, maintenance technicians and shift supervisors. It is also written to be searched. Each machine chapter follows the same order, so that a question such as "what is the daily check on the press brake" or "why does the busbar punch show alarm BB-07" finds one clear answer.

!! DANGER: This is a sample document for the ContextBasedRAG demonstration factory. The factory, its machines, their asset codes and every value in this manual are invented and written from general industry practice. Do not use this manual to operate, adjust or repair a real machine. On a real site always follow the original equipment manufacturer's manual and the site's own approved procedures.

## Who should read which part

| Reader | Read first | Then read |
|---|---|---|
| New operator (any machine) | Chapter 3 Safety, Chapter 4 Roles and shift working | The chapter of the machine you are assigned to, the Hinglish quick card at the end of it |
| Sheet metal operator | Chapters 5 to 11 | Chapter 24 Preventive maintenance |
| Powder coating operator | Chapters 12 and 13 | Chapter 3 sections on chemicals and fire |
| Busbar and wiring operator | Chapters 14 and 15 | Chapter 17 Wiring practice |
| Panel fitter and wireman | Chapters 16, 17, 18 | Chapter 19 Components |
| Testing engineer | Chapters 19, 20, 21 | Chapter 18 Reading drawings |
| Maintenance technician | Chapters 3, 24, 25, 26 | Every machine chapter, Appendix A fault codes |
| Supervisor and manager | Chapters 2, 4, 21, 24 | All chapters as needed |

## How each machine chapter is arranged

Every machine chapter uses the same headings in the same order. Once you have read one, you can find your way in any other.

1. **Purpose and position in the process** - what the machine makes and where its work goes next.
2. **Main parts and how it works** - the working principle in plain words, with a diagram.
3. **Technical data** - capacity, power, air and other figures of the machine at this factory.
4. **Controls and indicators** - what each button, lamp and screen does.
5. **Safety devices and specific hazards** - guards, light curtains, interlocks, and the dangers special to this machine.
6. **Start-up procedure** - the steps at the beginning of a shift.
7. **Normal operation** - setting up a job, running it and checking the parts.
8. **Shutdown procedure** - the steps at the end of a shift or before maintenance.
9. **Quality checks** - what to measure and how often.
10. **Preventive maintenance** - daily, weekly, monthly and yearly tasks with who does them.
11. **Troubleshooting** - symptoms, likely causes and remedies, including the alarm codes.
12. **Spare parts** - the parts kept in stock.
13. **Operator quick card (Hinglish)** - a short summary in simple Hinglish for the shop floor.

## Signal words used in this manual

The boxes below are used throughout. Read every box before you carry out the step it belongs to.

!! DANGER: An immediate hazard that will cause death or serious injury if the instruction is not followed. Example: working inside a panel that has not been isolated and proved dead.

!! WARNING: A hazard that could cause death or serious injury. Example: reaching past a press brake light curtain that has been muted.

!! CAUTION: A hazard that could cause minor injury or damage to the machine or the product. Example: bending a sheet thicker than the tooling is rated for.

!! NOTE: Information that helps the job go right but is not a safety instruction.

!! TIP: Practical advice from experienced operators and technicians.

!! HINGLISH: Shop floor ke liye chhota summary, simple Hinglish mein. English instruction aur Hinglish note mein farak lage to English instruction hi follow karo aur supervisor ko batao.

## Document control

| Item | Value |
|---|---|
| Document number | CPM-MAN-001 |
| Title | Control Panel Manufacturing: Plant, Machines and Technician Manual |
| Revision | A (first issue) |
| Owner | Maintenance Manager, demonstration factory |
| Approved by | Plant Head, demonstration factory |
| Review period | Every 12 months, or earlier when a machine, a process or a standard changes |
| Applies to | All production, maintenance, quality and stores staff of the demonstration factory |

A printed copy of this manual is uncontrolled. The controlled copy is the one in the document system. Before you follow a printed copy, check that its revision letter matches the controlled copy. When this manual and a machine maker's manual disagree on a value for the machine itself, the maker's manual applies and the difference must be reported to the maintenance manager so that this manual can be corrected.

## Revision history

| Revision | Date | Description | Prepared by |
|---|---|---|---|
| A | 2026-10-17 | First issue for the demonstration factory | Maintenance department |

## Asset register of the plant

The table lists every machine covered in this manual with its asset code. The asset code is painted on the machine, printed on its history card and used in every work order and breakdown record.

| Asset code | Machine | Area | Criticality |
|---|---|---|---|
| SHEAR-01 | CNC hydraulic guillotine shear, 3100 x 6 mm | Sheet metal shop, Bay 1 | High |
| PUNCH-02 | CNC turret punch press, 30 t, 32 stations | Sheet metal shop, Bay 1 | High |
| LASER-03 | Fiber laser cutting machine, 3 kW, 3000 x 1500 mm | Sheet metal shop, Bay 1 | Critical |
| BRAKE-04 | CNC hydraulic press brake, 135 t x 3100 mm | Sheet metal shop, Bay 2 | Critical |
| WELD-05 | Pedestal spot welding machine, 35 kVA | Welding area, Bay 2 | Medium |
| WELD-06 | MIG/MAG welding set, 400 A | Welding area, Bay 2 | Medium |
| PEM-07 | Hardware insertion press, 6 t | Sheet metal shop, Bay 2 | Medium |
| PTL-08 | Seven-tank pre-treatment line with dry-off oven | Paint shop, Bay 3 | High |
| PCL-09 | Powder coating booth, recovery unit and curing oven | Paint shop, Bay 3 | Critical |
| BUS-10 | CNC busbar processing machine (punch, shear, bend) | Busbar shop, Bay 4 | High |
| WIRE-11 | Automatic wire cut and strip machine | Wiring preparation, Bay 4 | Medium |
| CRIMP-12 | Pneumatic crimping press with applicators | Wiring preparation, Bay 4 | Medium |
| MARK-13 | Thermal transfer wire marker and ferrule printer | Wiring preparation, Bay 4 | Low |
| TEST-14 | Panel routine test bench (HV, IR, functional) | Testing bay, Bay 6 | Critical |
| COMP-15 | Screw air compressor 15 kW with refrigerated dryer | Utility room | High |
| CRANE-16 | EOT crane, 5 t, double girder | Assembly hall, Bays 5 and 6 | High |

## Abbreviations

| Abbreviation | Meaning |
|---|---|
| ACB | Air circuit breaker |
| APFC | Automatic power factor correction (panel) |
| BOM | Bill of materials |
| CNC | Computer numerical control |
| CRCA | Cold rolled close annealed (steel sheet) |
| CT | Current transformer |
| DFT | Dry film thickness (of paint) |
| DOL | Direct on line (starter) |
| EOT | Electric overhead travelling (crane) |
| FAT | Factory acceptance test |
| GA | General arrangement (drawing) |
| GI | Galvanised iron (sheet) |
| HMI | Human machine interface (touch screen) |
| HV test | High voltage (dielectric) test |
| IP | Ingress protection (degree of protection, IEC 60529) |
| IR | Insulation resistance |
| LOTO | Lockout and tagout |
| LT | Low tension (low voltage, up to 1000 V AC) |
| MCB | Miniature circuit breaker |
| MCC | Motor control centre |
| MCCB | Moulded case circuit breaker |
| MS | Mild steel |
| NCR | Non-conformance report |
| OEM | Original equipment manufacturer |
| PCC | Power control centre |
| PDB | Power distribution board |
| PE | Protective earth |
| PLC | Programmable logic controller |
| PM | Preventive maintenance |
| PPE | Personal protective equipment |
| PT | Potential (voltage) transformer |
| RCCB | Residual current circuit breaker |
| SLD | Single line diagram |
| SOP | Standard operating procedure |
| SS | Stainless steel |
| TDC / BDC | Top dead centre / bottom dead centre |
| VFD | Variable frequency drive |
