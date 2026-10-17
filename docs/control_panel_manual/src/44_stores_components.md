# 44. Stores and Handling of Bought-out Components

Bought-out components (breakers, contactors, relays, meters, PLCs, drives, terminals, cables, glands, accessories) are about half the value of a panel. Wrong, damaged or missing components are the most common cause of delays at assembly and of failures at testing.

## 44.1 Receiving

| Check | How |
|---|---|
| Quantity | Count against the purchase order and delivery note |
| Identity | Make, type code (full catalogue number), rating, coil voltage, number of poles, accessories |
| Condition | Packaging intact, no visible damage, no moisture |
| Documents | Test certificates where required (ACBs, CTs, capacitors, cables), warranty cards |
| Date codes | For capacitors and batteries: manufacturing date (age affects life) |
| Counterfeit risk | Only from authorised distributors; check holograms and labels; doubtful items quarantined |

!! CAUTION: Compare the full catalogue number, not just the description. Two contactors with the description "contactor 3 pole 25 A" can differ in coil voltage (24 V DC, 110 V AC, 230 V AC), auxiliary contacts and frame. Case study 28.6 shows what happens when the coil voltage is not checked.

## 44.2 Storage

| Item | Storage rule |
|---|---|
| Breakers, contactors, relays | Original boxes, racks by type and rating; coil voltage variants in separate labelled bins |
| ACBs | On their pallets, covered, not stacked |
| PLCs, drives, meters, electronic relays | Antistatic packaging; dry cabinet; temperature 5 to 40 degrees C |
| Capacitors | Upright, dry, away from heat; first in, first out |
| Cables and wires | Drums on drum stands or racks; ends sealed; not in direct sunlight |
| Terminals and small items | Labelled bins, one item per bin; the label shows catalogue number and description |
| Glands and lugs | Labelled bins by size |
| Batteries (UPS, PLC) | Cool place; charge as per maker during storage |

## 44.3 Kitting for jobs

1. Planning releases the BOM of the job with the required date.
2. The store picks the components per BOM line and places them in job-labelled crates per vertical or per module.
3. Shortages are listed on a shortage sheet and sent to purchase and the assembly supervisor the same day.
4. The assembly supervisor checks the kit against the BOM (identity checks of 44.1) before assembly starts and signs the kit card.
5. Substitutions (a different make or type) are allowed only with written design approval and, if the customer specified makes, with customer approval.

## 44.4 Handling

- Lift heavy devices (ACBs, large MCCBs, drives) with lifting aids, by their designated lifting points.
- Do not carry breakers by their handles or terminals.
- Keep electronic devices in their antistatic bags until mounting; touch the earthed panel frame before handling.
- Do not stack loose devices on top of each other on benches.
- Return unused components to the store with the job number and reason; do not keep "spare" components at the workplace.

## 44.5 Traceability

For important components, the serial numbers are recorded on the job record: ACBs, MCCBs with electronic releases, protection relays, drives, PLC CPUs, meters (energy meters), CTs for metering. These numbers are needed for warranty claims and for the customer's asset records.

## 44.6 Returns and rejections

- Components found faulty at assembly or testing are tagged red with the job number and fault description, returned to the store and recorded.
- The store returns them to the supplier with the fault report and claims replacement.
- Repeated faults of the same component type are reported to the quality manager for supplier action.

!! HINGLISH: Component aate hi poora catalogue number, rating, coil voltage aur poles purchase order se milao. Coil voltage ke alag-alag bin. PLC, drive aur meter antistatic bag mein, sookhi jagah. Job ka kit BOM ke hisaab se crate mein; kami ho to usi din shortage sheet. Doosri company ka ya alag type ka component bina design (aur customer) ki likhit permission ke mat lagao. ACB, relay, drive, PLC ke serial number job record mein likho.
