# Appendix C. Reference Tables and Formulas

## C.1 Electrical formulas

| Quantity | Formula | Example |
|---|---|---|
| Ohm's law | V = I x R | 230 V across 46 ohm: I = 5 A |
| Power, DC or resistive AC | P = V x I | 24 V x 2 A = 48 W |
| Single-phase power | P = V x I x PF | 230 V x 10 A x 0.9 = 2.07 kW |
| Three-phase power | P = 1.732 x V(line) x I x PF | 1.732 x 415 x 50 x 0.85 = 30.5 kW |
| Three-phase apparent power | S (kVA) = 1.732 x V(line) x I / 1000 | 1.732 x 415 x 100 / 1000 = 71.9 kVA |
| Current from kW (three-phase) | I = P x 1000 / (1.732 x V x PF x efficiency) | 15 kW, 415 V, PF 0.85, eff 0.9: 27.3 A |
| Current from kVA (three-phase) | I = S x 1000 / (1.732 x V) | 500 kVA at 433 V: 667 A |
| Phase voltage from line voltage (star) | V(phase) = V(line) / 1.732 | 415 / 1.732 = 240 V |
| Resistance of a conductor | R = resistivity x length / area | 100 m of 2.5 mm2 copper: 0.0175 x 100 / 2.5 = 0.7 ohm |
| Voltage drop, three-phase (approx.) | Vd = 1.732 x I x (R cos phi + X sin phi) x L | Use cable maker's mV/A/m tables |
| Capacitor reactive power | Q (kVAr) = V2 x 2 x 3.14 x f x C (three-phase delta: per phase) | Use APFC maker's tables |
| Required kVAr for PF correction | Q = P x (tan phi1 - tan phi2) | 100 kW from PF 0.8 to 0.98: 100 x (0.75 - 0.203) = 54.7 kVAr |
| Motor synchronous speed | n = 120 x f / poles | 4 poles, 50 Hz: 1500 rpm |

## C.2 Conductor data

| Property | Copper | Aluminium |
|---|---|---|
| Resistivity at 20 degrees C (ohm mm2 / m) | 0.0175 | 0.0283 |
| Density (kg / dm3) | 8.9 | 2.7 |
| Conductivity relative to copper | 100 % | 61 % |
| Temperature coefficient of resistance (per K) | 0.0039 | 0.0040 |
| Melting point (degrees C) | 1083 | 660 |

### C.2.1 AWG and metric wire sizes

| AWG | Area (mm2) | Nearest metric size |
|---|---|---|
| 20 | 0.52 | 0.5 |
| 18 | 0.82 | 0.75 |
| 16 | 1.31 | 1.5 |
| 14 | 2.08 | 2.5 |
| 12 | 3.31 | 4 |
| 10 | 5.26 | 6 |
| 8 | 8.37 | 10 |
| 6 | 13.3 | 16 |
| 4 | 21.2 | 25 |
| 2 | 33.6 | 35 |
| 1/0 | 53.5 | 50 |
| 2/0 | 67.4 | 70 |
| 4/0 | 107 | 95 or 120 |

## C.3 Threads, holes and spanners (metric coarse threads)

| Thread | Pitch (mm) | Tap drill (mm) | Clearance hole, medium (mm) | Spanner size (mm) | Allen key, socket head (mm) |
|---|---|---|---|---|---|
| M3 | 0.5 | 2.5 | 3.4 | 5.5 | 2.5 |
| M4 | 0.7 | 3.3 | 4.5 | 7 | 3 |
| M5 | 0.8 | 4.2 | 5.5 | 8 | 4 |
| M6 | 1.0 | 5.0 | 6.6 | 10 | 5 |
| M8 | 1.25 | 6.8 | 9.0 | 13 | 6 |
| M10 | 1.5 | 8.5 | 11.0 | 16 (or 17) | 8 |
| M12 | 1.75 | 10.2 | 13.5 (busbars: 14) | 18 (or 19) | 10 |
| M16 | 2.0 | 14.0 | 17.5 | 24 | 14 |
| M20 | 2.5 | 17.5 | 22.0 | 30 | 17 |

### C.3.1 Bolt property classes

| Marking on head | Tensile strength (N/mm2) | Use |
|---|---|---|
| 4.6 | 400 | Not used in this plant except non-structural |
| 8.8 | 800 | Standard for structures and busbars |
| 10.9 | 1000 | Machine parts where the maker specifies |
| 12.9 | 1200 | Machine parts, socket head cap screws, as specified |
| A2-70 / A4-70 | 700 (stainless) | Stainless steel panels, outdoor |

## C.4 Torque values used in this manual

| Application | Table | Values |
|---|---|---|
| Structure bolts (8.8) | Table 16-1 | M5 5, M6 8, M8 20, M10 40, M12 70 Nm |
| Busbar joints (8.8 with washers) | Table 16-3 | M6 10, M8 22, M10 44, M12 75, M16 160 Nm |
| Insulator inserts | Chapter 16.4.3 | M8 20 Nm, M10 30 Nm (or insulator maker's value) |
| Device terminals | Device maker | Device maker's value always applies |
| Terminal blocks | Chapter 17.5.1 | Maker's value (typical 0.5 to 1.5 Nm) |

## C.5 Sheet metal

### C.5.1 Sheet thickness and gauges

| SWG | mm | Common use |
|---|---|---|
| 18 | 1.2 | Light covers (rare in panels) |
| 16 | 1.6 | Covers, partitions |
| 14 | 2.0 | Frames, doors |
| 12 | 2.6 (2.5 used) | Mounting plates |
| 10 | 3.2 (3.0 used) | Gland plates, base channels |

### C.5.2 Weight of steel sheet (kg per m2)

| Thickness (mm) | 1.0 | 1.2 | 1.6 | 2.0 | 2.5 | 3.0 | 4.0 | 5.0 | 6.0 |
|---|---|---|---|---|---|---|---|---|---|
| Steel (kg/m2) | 7.85 | 9.42 | 12.56 | 15.70 | 19.63 | 23.55 | 31.40 | 39.25 | 47.10 |
| Aluminium (kg/m2) | 2.70 | 3.24 | 4.32 | 5.40 | 6.75 | 8.10 | 10.80 | 13.50 | 16.20 |

### C.5.3 Material strengths (typical)

| Material | Tensile strength (N/mm2) | Shear strength (N/mm2) | Bending force factor vs. MS |
|---|---|---|---|
| CRCA / mild steel | 350 to 450 | 280 to 350 | 1.0 |
| GI sheet | 350 to 450 | 280 to 350 | 1.0 |
| Stainless steel 304 | 600 to 700 | 450 to 550 | 1.5 |
| Aluminium 5052-H32 | 210 to 260 | 140 to 200 | 0.5 |
| Copper ETP half hard | 240 to 300 | 160 to 200 | 0.6 |

## C.6 Units and conversions

| From | To | Multiply by |
|---|---|---|
| inch | mm | 25.4 |
| foot | m | 0.3048 |
| bar | kPa | 100 |
| bar | psi | 14.5 |
| MPa | bar | 10 |
| kgf | N | 9.81 |
| tonne-force | kN | 9.81 |
| kgf/mm2 | N/mm2 | 9.81 |
| Nm | kgf m | 0.102 |
| lbf ft | Nm | 1.356 |
| kW | hp | 1.341 |
| litre per minute | m3/h | 0.06 |
| CFM | m3/min | 0.0283 |
| Degrees F | Degrees C | (F - 32) / 1.8 |

## C.7 Motor insulation classes

| Class | Maximum winding temperature | Typical allowed rise (at 40 degrees C ambient) |
|---|---|---|
| B | 130 degrees C | 80 K |
| F | 155 degrees C | 105 K (often used with class B rise for life) |
| H | 180 degrees C | 125 K |

## C.8 Standards referred to in this manual

| Standard | Subject |
|---|---|
| IEC 61439-1 / -2 / -3 (IS/IEC 61439) | Low-voltage switchgear and controlgear assemblies |
| IEC 60947 series | Low-voltage switchgear devices (breakers, contactors, starters, relays) |
| IEC 60898-1 | MCBs for household and similar installations |
| IEC 61008 / 61009 | RCCBs / RCBOs |
| IEC 60529 | Degrees of protection (IP code) |
| IEC 60204-1 | Electrical equipment of machines |
| IEC 81346-2 | Reference designations (device letter codes) |
| IEC 60073 | Coding principles for indicators and actuators (colours) |
| IS 694 | PVC insulated cables up to 1100 V |
| IS 513 | Cold rolled steel sheets |
| ISO 2409 | Paint adhesion: cross-cut test |
| ISO 9227 | Salt spray test |
| ISO 4406 | Hydraulic oil cleanliness code |
| ISO 4414 / ISO 4413 | Pneumatic / hydraulic fluid power safety |
| ISO 12100 | Safety of machinery: risk assessment |
| ISO 13849-1 | Safety-related parts of control systems |

!! NOTE: Standards are revised from time to time. The design and quality departments keep the current editions; this list gives the subjects only.

## C.9 Common colours

| Item | Colour / code |
|---|---|
| Standard panel enclosure | RAL 7035 light grey |
| Base frame | RAL 2000 orange or black (as customer) |
| Mounting plates (painted) | RAL 2000 orange or white RAL 9010 (as customer) |
| Phase sleeves | Red, yellow, blue; neutral black; PE green-yellow |
| Emergency stop | Red mushroom on yellow background |
| Safety signs: prohibition / mandatory / warning / safe condition | Red / blue / yellow / green |

!! HINGLISH: M6 ke liye 5.0 mm drill aur 10 mm spanner, M8 ke liye 6.8 drill aur 13 spanner, M10 ke liye 8.5 drill aur 16-17 spanner, M12 ke liye 10.2 drill aur 18-19 spanner. Three-phase power = 1.732 x volt x ampere x PF. Copper aluminium se zyada achha conductor hai (aluminium 61 %). 1 bar = 14.5 psi, 1 tonne = 9.81 kN.
