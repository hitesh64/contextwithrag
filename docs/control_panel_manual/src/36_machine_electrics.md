# 36. Electrical Maintenance of Machine Control Cabinets

The production machines of the plant have their own electrical cabinets with CNC controllers, servo drives, PLCs, power supplies and safety relays. This chapter covers the electrical maintenance that is common to all of them.

## 36.1 Cabinet condition

| Check | Interval | Standard |
|---|---|---|
| Cabinet door closed and gaskets intact | Daily (operator) | Closed; no gaps |
| Cabinet cooling (fan filters or air conditioner) | Weekly clean filters; monthly check air conditioner | Air flows freely; inside temperature below 40 degrees C |
| Dust and oil mist inside | Monthly | Clean; source of contamination corrected |
| Thermal imaging of terminals and drives | Quarterly | No hot spots (Chapter 24.6.2) |
| Terminal tightness of power connections | Yearly (under LOTO) | Torqued to maker's value |
| Earth connections and shield clamps | Yearly | Tight, clean |

!! CAUTION: Never leave a machine cabinet door open to "cool it down". Dust and metal particles from the shop enter, and the cabinet air conditioner or fans are designed for a closed cabinet. If the cabinet is hot, find out why (blocked filter, failed fan or air conditioner, overloaded drive).

### 36.1.1 Cabinet air conditioners

- Clean the condenser filter (outside air side) weekly in dusty areas.
- Check the condensate drain: blocked drains cause water to enter the cabinet.
- Set point 35 degrees C (not lower): a lower setting causes condensation on cold components.
- Check that the door switch stops the air conditioner when the cabinet is open (prevents condensation).

## 36.2 Servo drives and motors

CNC axes are driven by servo motors with encoders and servo drives (amplifiers). The CNC sends position commands; the drive controls the motor current to follow them, using the encoder feedback.

| Fault | Typical cause | Action |
|---|---|---|
| Following error (axis does not follow the command) | Mechanical obstruction, lack of lubrication, worn mechanics, drive or motor fault, wrong load (heavy sheet) | Move axis by hand under LOTO (if possible) to check friction; check lubrication; read drive alarm |
| Encoder error | Encoder cable damaged (drag chain), connector, encoder failure | Check cable along the drag chain, connector pins; swap cable if a spare is available |
| Overcurrent / overload | Mechanical binding, short circuit in motor cable, brake not releasing | Check brake release voltage (24 V DC), motor cable IR (disconnect from drive first) |
| Over-voltage (regeneration) | Fast deceleration of heavy axis, braking resistor failed | Check braking resistor resistance and connection |
| Motor brake does not release | No 24 V to brake, brake coil failed, air gap worn | Measure brake voltage at motor connector; replace motor brake / motor |

!! WARNING: Vertical axes (laser Z axis, press brake ram where electrically driven, crane hoist) have holding brakes. Before working on a vertical axis motor or drive, secure the axis mechanically so that it cannot fall when the brake is released or the motor is removed.

### 36.2.1 Replacing a servo drive or motor

1. Save the drive parameters (to the CNC, a memory card or a laptop) before any replacement, if the drive still works.
2. LOTO the machine; wait for the drive DC bus discharge time; measure.
3. Replace with the identical type (check the full type code, including firmware version where required).
4. Load the saved parameters; for motor replacement, the encoder may need to be adjusted (commutation offset) as per the maker's procedure.
5. Reference the axis; check positioning accuracy (Chapter 6 to 9 monthly tests).
6. Record the replacement in the machine history card.

## 36.3 Cables in drag chains

Cables to moving axes (back gauges, laser gantry, turret carriage) run in drag chains (cable carriers) and bend millions of times. They are the most common cause of intermittent electrical faults on CNC machines.

- Use only highly flexible cables designed for drag chains as replacements.
- Inspect drag chains monthly: broken links, cables twisted or crossed inside, cable sheaths worn, separators missing.
- Cables must lie loosely side by side, not on top of each other, with the strain relief at both ends.
- An intermittent encoder or sensor fault that appears only at certain axis positions points to a cable breaking inside the drag chain.

## 36.4 CNC and PLC data backup

| Data | Backup interval | Where kept |
|---|---|---|
| CNC machine parameters | After any change; at least every 6 months | Maintenance server and a labelled USB stick in the maintenance office safe |
| PLC program of the machine | After any change; every 6 months | As above |
| Part programs and tool libraries | Weekly (automatic where possible) | Programming office server |
| Drive parameters | After commissioning and after any change | As above |
| Laser cutting parameter library | Monthly | As above |

The backup log records date, machine, data type, file name and who made it. Before any repair that involves the controller, check that a current backup exists.

### 36.4.1 Memory batteries

Some CNCs, PLCs and absolute encoders keep data with a battery. When the battery low alarm appears, change the battery **with the control powered on** (unless the maker says otherwise), so that data is not lost. Replace batteries preventively at the interval given by the maker (often 2 to 4 years) and record the date on a sticker inside the cabinet.

## 36.5 Safety circuits of machines

| Safety device | Function test (interval) | Who |
|---|---|---|
| Emergency stops | Daily (operator) | Operator, check sheet |
| Light curtains | Daily (operator); stopping time measurement yearly | Operator; technician with stopping time meter |
| Interlocked guards | Daily or weekly per check sheet | Operator |
| Two-hand controls | Daily | Operator |
| Safety relays | Proof test yearly (both channels, feedback) | Technician |
| Laser guard of press brake | Daily (test rod) | Operator |

**Light curtain safety distance**: the curtain must be far enough from the hazard that the machine stops before a hand reaches it. The yearly stopping time measurement checks that the machine still stops in time (worn brakes, slow valves increase stopping time). If the measured stopping time increased by more than 10 % or exceeds the value used to calculate the mounting distance, the cause is repaired before use.

## 36.6 Power supply problems on machines

| Symptom | Possible cause | Check |
|---|---|---|
| CNC resets or loses reference during the day | Voltage dips (welding, compressor starting), loose neutral, failing 24 V power supply | Power quality logger; check 24 V supply output under load (24 V +/- 5 %) |
| Random sensor faults on several sensors at once | 24 V supply overloaded or failing; short circuit in one sensor cable pulling the supply down | Measure 24 V; disconnect sensor groups one at a time |
| Drive trips on undervoltage | Supply dips, loose input terminals, input fuse | Thermal image of input terminals; check fuses |
| Machine earth leakage trips | Moisture in motor or cable, damaged cable, drive filter leakage | IR test of motors and cables; check RCD type suits drives (type B) |

## 36.7 Machine history card

Every machine has a history card (in the maintenance system) with:

- Asset data: maker, model, serial number, year, location, criticality.
- Major spare part numbers.
- Every breakdown and repair, with date, cause and action.
- Every PM, replacement of major parts (motors, drives, pumps, valves), and modification.
- Backup records and software versions.

Before starting a repair, look at the history: the same fault may have occurred before with a known cause.

!! HINGLISH: Machine ke electrical cabinet ka darwaza hamesha band rakho, filter saaf rakho, andar 40 degree se kam. Servo drive ya motor badalne se pehle parameter ka backup lo; vertical axis ko mechanically rok ke kaam karo. Drag chain ki cable sabse zyada tootti hai; kisi khaas position par fault aaye to wahi cable check karo. CNC aur PLC ka backup har 6 mahine aur har badlav ke baad. Battery badalni ho to control on rakh ke badlo.
