# 32. Panel Design Basics for Production and Testing Staff

This chapter explains the design decisions behind a panel, so that production and testing staff understand why the drawing says what it says, and can recognise a design question that must go back to the design team. Production staff never change a design on their own.

## 32.1 Design inputs

| Input | Source | Used for |
|---|---|---|
| System voltage, frequency, earthing system (TN-S, TN-C-S, TT) | Customer specification | Ratings, neutral and PE arrangement |
| Prospective short-circuit current at the panel | Customer / electrical consultant, transformer data | Icw, Ipk of busbars; breaking capacity of breakers |
| Single line diagram | Customer | Feeders, ratings, metering |
| Load list | Customer | Feeder ratings, starters |
| Installation conditions: indoor / outdoor, ambient temperature, altitude, dust, humidity | Customer | IP, ventilation, derating |
| Space and access | Customer layout | Panel dimensions, front / rear access, cable entry |
| Standards and specification | Customer | Forms, colours, makes, testing |

## 32.2 Short-circuit current

When a short circuit happens near the panel, the current is limited mainly by the transformer impedance. A quick estimate for a fault at the LT terminals of a transformer:

**Isc (kA) = transformer rating (kVA) / (1.732 x LT voltage (kV) x impedance (per unit))**

Example: 500 kVA, 433 V, 5 % impedance: Isc = 500 / (1.732 x 0.433 x 0.05) = 13.3 kA. Two such transformers in parallel feeding the same busbar double it. Motors running at the time add their contribution. The design team uses a proper calculation; the estimate helps to understand why a small factory panel may be rated 25 kA while a large plant's PCC is rated 50 or 65 kA.

The **peak current** (Ipk) in the first half cycle depends on the power factor of the fault: for 50 kA the peak factor is 2.1, so Ipk = 105 kA. The peak current decides the mechanical forces on the busbars and their supports: force between two parallel bars is proportional to the square of the current and inversely proportional to their spacing. This is why the drawing fixes support spacing and insulator types, and why fitters must not change them.

## 32.3 Busbar sizing

Busbar size depends on:

- **Current rating**: temperature rise must stay within limits (IEC 61439 allows up to 70 K rise on busbars in normal service, but the plant designs for lower rises to give margin); the first estimate uses current density (Chapter 1.3.2: 1.6 A/mm2 copper, 1.0 A/mm2 aluminium).
- **Short-time rating**: the bar must not overheat during the fault: for copper, a cross-section of about 7 mm2 per kA for 1 second as a guide (50 kA for 1 s needs about 350 mm2 minimum, which a 1600 A bar already exceeds).
- **Mechanical strength**: support spacing and bar size as per verified design.
- **Arrangement**: several thin bars per phase with gaps (e.g. 2 x 10 x 100 mm with 10 mm gap) carry more current than one thick bar of the same area because of better cooling and less skin effect.

| Copper busbar (one bar per phase, painted or sleeved, in enclosure, guide values for 35 degrees C ambient) | Approximate rating |
|---|---|
| 25 x 5 mm | 250 A |
| 40 x 5 mm | 400 A |
| 50 x 10 mm | 800 A |
| 80 x 10 mm | 1250 A |
| 100 x 10 mm | 1600 A |
| 2 x 100 x 10 mm | 2500 A |
| 3 x 100 x 10 mm | 3200 A |

!! NOTE: These values are guide values only. The rating of the actual panel is fixed by its design verification (tests or calculation per IEC 61439-1 clause 10.10) and is shown on the drawing.

## 32.4 Temperature rise and heat dissipation

Every device dissipates heat (power loss). The panel must remove this heat so that the air inside stays within the temperature that the devices are rated for (often 40 to 55 degrees C inside the panel).

| Device | Typical power loss |
|---|---|
| MCB 16 A (per pole at rated current) | 2 to 3 W |
| MCCB 250 A (3 poles at rated current) | 30 to 40 W |
| ACB 1600 A | 150 to 250 W |
| Contactor 40 A (3 poles plus coil) | 10 to 15 W |
| VFD 22 kW | 500 to 700 W |
| Busbar 1600 A, per metre of three phases | 100 to 150 W |
| 24 V DC power supply 10 A | 20 to 30 W |

The design team adds the losses of each section (with the diversity factor) and checks the temperature rise by calculation or by comparison with a tested design. If the losses are too high, the design adds louvres, fans, larger enclosure or air conditioning. Production must therefore not block louvres, omit filters or add devices not in the BOM.

## 32.5 Cable and wire selection

Inside the panel, wire sizes follow Chapter 17.2. For outgoing cables (site), the cable size is chosen by the consultant for current capacity, voltage drop (typically below 3 % for power, 5 % for motor starting), and short-circuit withstand. The panel's terminal size and gland plate must suit the cable sizes on the cable schedule: a 3.5-core 300 mm2 aluminium cable needs large lugs and space; if the terminals or space on the drawing seem too small for the cable, report it before the panel is wired.

## 32.6 Selectivity (discrimination)

Selectivity means that, when a fault occurs, only the breaker nearest to the fault trips, and the rest of the plant stays on. It is achieved by:

- **Current selectivity**: the upstream breaker's instantaneous setting is above the maximum fault current at the downstream breaker.
- **Time selectivity**: the upstream breaker (ACB with S function) waits a short time (tsd, e.g. 0.2 to 0.4 s) to let the downstream breaker clear the fault.
- **Energy selectivity**: current-limiting downstream breakers that the maker's tables confirm.

Protection settings are therefore planned as a chart for the whole panel. The testing engineer applies exactly these settings; changing one setting (for example raising a feeder's instantaneous setting "to avoid nuisance tripping") can destroy the selectivity of the whole system.

## 32.7 Earthing systems

| System | Description | Effect on the panel |
|---|---|---|
| TN-S | Separate neutral and protective earth conductors from the transformer | Separate N and PE busbars; N insulated from frame |
| TN-C-S | Combined PEN conductor up to the main panel, then separated | Link between PEN and PE at the main panel only, as shown on drawing |
| TT | Installation earth separate from the supply earth | Earth leakage protection (RCD) required on circuits |
| IT | Supply not earthed or earthed through high impedance | Insulation monitoring device; first fault does not trip |

The N-PE link is the most important detail: it is made at one point only (usually in the main LT panel). An unintended second link (for example a neutral bar fixed without insulators) causes neutral current to flow in the earth system, which upsets earth leakage protection and can cause interference.

## 32.8 Derating

Device ratings are for a reference temperature (often 40 degrees C ambient around the device for breakers, or the temperature stated by the maker). Inside a hot panel, or at altitudes above 2000 m, devices must be derated. The design accounts for this; production must place devices exactly as drawn, because moving a breaker closer to a drive or into an upper compartment can raise its temperature and cause nuisance tripping.

## 32.9 When to stop and ask the design team

- A device does not fit in the space on the drawing.
- A device delivered is different from the BOM (make, type, rating), even if "equivalent".
- Clearances cannot be achieved as per Table 16-2.
- Cable lugs, terminals or gland plates seem too small for the specified cables.
- Busbar or wire size on the drawing seems inconsistent with the breaker rating.
- The customer at FAT asks for a change.
- Any doubt about a safety function (interlock, emergency stop, earthing).

Record the question on the job card with a "design query" mark and wait for a written answer (revised drawing or design concession).

!! HINGLISH: Design ka har faisla soch samajh kar hota hai: busbar ka size, support ki doori, bolt ki length, device ki jagah, louvre aur fan. Production apne man se design nahi badalta. Device fit na ho, BOM se alag device aaye, doori (clearance) na bane, ya cable ke liye jagah kam lage to "design query" likh ke design team se likhit jawaab lo. Protection setting chart ke hisaab se hi setting lagao.
