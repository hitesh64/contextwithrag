# 31. Motor Control Circuits in Detail

Most feeders of an MCC control motors. This chapter describes the standard starter circuits built in the factory, how each is wired and tested, and the faults that appear most often. It complements Chapter 18 (reading drawings) and Chapter 19 (components).

## 31.1 Choosing the starting method

| Method | Starting current (x FLC) | Starting torque | Typical motor sizes | Notes |
|---|---|---|---|---|
| Direct on line (DOL) | 6 to 8 | Full | Up to 7.5 kW (larger if the supply allows) | Simplest, cheapest; high inrush and mechanical shock |
| Star-delta | About 2 to 2.7 (one third of DOL) | One third of DOL | 7.5 to 75 kW | Needs 6-terminal motor; current peak at changeover |
| Soft starter | 2.5 to 4 (adjustable) | Reduced, adjustable | 7.5 to 315 kW | Smooth start and stop; no speed control |
| VFD | 1 to 1.5 | Full torque at low speed | Any size where speed control or very soft start is needed | Speed control, energy saving on pumps and fans; harmonics |
| Reversing DOL | 6 to 8 | Full | Small motors needing two directions | Two contactors with interlocks |

## 31.2 DOL starter

The circuit is shown in Figure 18-1. Power components: MPCB or MCCB (short-circuit and overload, or short-circuit only with separate overload relay), contactor, overload relay. Control components: control MCB, emergency stop, stop and start push buttons, holding contact, lamps, local / remote selector, and the remote contacts (from the PLC or process).

### 31.2.1 Local / remote control

With a selector switch S3 (LOCAL / OFF / REMOTE):

- In LOCAL, the start and stop push buttons on the panel door control the motor.
- In REMOTE, a contact from the PLC or a remote station controls the motor (usually a maintained contact: closed = run).
- In OFF, the motor cannot be started from anywhere.
- The emergency stop and the overload trip work in every position.
- An auxiliary contact of the selector is wired to the PLC as "in remote" feedback.

### 31.2.2 Testing a DOL feeder

1. Without power circuit energised (control supply only): operate start: contactor picks up and holds; operate stop: drops. Emergency stop: drops, cannot restart until reset.
2. Overload test button: contactor drops, TRIP lamp on, PLC alarm contact closes; contactor cannot restart until the overload is reset.
3. Selector: check each position.
4. With a test motor (or at site with the actual motor): check direction of rotation (bump test: start and stop immediately), current on all three phases, no abnormal noise.

## 31.3 Star-delta starter

### 31.3.1 Sequence

1. Start command: KM1 (main) and KM3 (star) close; the motor starts in star with reduced voltage across each winding (230 V instead of 415 V).
2. Timer KT runs (set 5 to 10 s, until the motor is near full speed: watch the current falling to near no-load value).
3. KT opens KM3 (star). After a short dead time (50 to 100 ms) to let the arc in KM3 extinguish, KM2 (delta) closes.
4. The motor runs in delta at full voltage.

### 31.3.2 Interlocks

- Electrical: NC auxiliary of KM2 in the KM3 coil circuit and NC auxiliary of KM3 in the KM2 coil circuit.
- Mechanical: a mechanical interlock between KM2 and KM3 on starters above about 30 kW, as per drawing.
- The star-delta timer has a built-in dead time; a standard on-delay timer is not used for changeover.

### 31.3.3 Contactor sizing (guide)

| Contactor | Current it carries | Size (AC-3) relative to motor FLC |
|---|---|---|
| KM1 main | Phase current of the delta winding = 0.58 x FLC | 0.58 x FLC |
| KM2 delta | 0.58 x FLC | 0.58 x FLC |
| KM3 star | Star current = FLC / 3 | 0.33 x FLC |
| Overload relay (in winding circuit) | 0.58 x FLC | Set at 0.58 x FLC |

### 31.3.4 Common star-delta problems

| Symptom | Cause |
|---|---|
| Motor trips at changeover | Changeover too early (motor not near full speed): increase timer setting |
| Very high current peak at changeover | Wrong phase rotation of delta connection (motor briefly brakes): check the delta connection order (W2-L1, U2-L2, V2-L3 for this plant's standard) |
| Motor runs in star only | Delta contactor does not close: check timer output and the KM3 NC interlock contact |
| Short circuit at changeover | Missing interlock or welded star contactor; dead time too short |
| Motor hums and does not start | One winding open or one phase missing in star |

## 31.4 Reversing starter

Two contactors KM1 (forward) and KM2 (reverse) swap two phases (L1 and L3) at the motor. They must never close together, which would short-circuit two phases.

- Mechanical interlock between KM1 and KM2 (a mechanical interlock unit mounted between the two contactors).
- Electrical interlock: NC auxiliary of KM1 in the KM2 coil circuit, NC of KM2 in KM1 circuit.
- Push button interlock: forward button NC contact in the reverse circuit and vice versa (direct reversal) or a stop required before reversing, as per drawing.
- Limit switches for end positions where applicable.

**Test**: try to close both directions together: impossible. Check direction of rotation for FORWARD at site; if wrong, swap two phases at the motor terminals (not inside the starter, which would change the marking).

## 31.5 Soft starter feeder

Typical circuit: MCCB (with semiconductor fuses where specified for type 2 coordination), optional line contactor, soft starter with internal bypass, control terminals for start / stop and fault output.

| Setting | Typical value | Effect |
|---|---|---|
| Initial voltage / torque | 30 to 40 % | Too low: motor does not start turning at once |
| Ramp-up time | 10 s | Longer gives smoother start, more heating |
| Current limit | 3 x FLC | Too low: motor may stall |
| Ramp-down (soft stop) | 10 to 15 s (pumps) | Avoids water hammer |
| Motor current (overload) | Nameplate FLC | Internal motor protection |

Faults: overtemperature of the soft starter (too many starts per hour, blocked ventilation), phase loss, thyristor short circuit (shown as fault at power-on), motor stall (current limit too low or load too high).

## 31.6 VFD feeder

### 31.6.1 Power circuit

MCCB or fuses (as per drive maker for protection of the drive input), line reactor or harmonic filter (if specified), VFD, output reactor or dv/dt filter for long motor cables (above about 50 m or as per maker), shielded motor cable, optional bypass contactors with interlocks.

### 31.6.2 Control interface

| Signal | Typical connection |
|---|---|
| Run / stop | Digital input from PLC or panel push buttons (via relay) |
| Forward / reverse | Digital input |
| Speed reference | Analogue 4-20 mA from PLC or potentiometer on panel door, or communication |
| Fault reset | Digital input or keypad |
| Ready / running / fault | Relay outputs to PLC and lamps |
| Actual speed or current | Analogue output 4-20 mA to PLC or meter |
| Safe torque off (STO) | Two-channel safety input from emergency stop safety relay (where specified) |

### 31.6.3 Commissioning steps (factory functional test with test motor)

1. Check wiring; check that the drive input voltage matches the supply.
2. Power on; enter motor data from nameplate.
3. Set control source (terminals), speed reference source, min / max frequency, accel / decel.
4. Perform auto-tune (static if the motor is coupled).
5. Run at low speed; check rotation direction; then full range.
6. Check all I/O with the PLC: run, stop, fault, speed reference at 4, 12 and 20 mA (0, 50, 100 % speed).
7. Save the parameter set to the keypad memory and to a file; print the parameter list for the test report.

## 31.7 PLC-controlled motor starters

In PLC-controlled MCCs, the PLC gives the start command through an output relay to the contactor coil, and reads back:

- Contactor auxiliary contact (running feedback).
- Overload trip contact (97-98) or MPCB trip contact.
- Local / remote selector position.
- Emergency stop status (from safety relay).

The PLC raises a "fail to start" alarm if the running feedback does not appear within a set time (e.g. 2 s) after the start command, and "fail to stop" if it does not disappear after the stop command. These alarms point the technician to the starter (coil, wiring, contactor) rather than to the process.

!! WARNING: Emergency stop circuits are hard-wired through safety relays and remove power from the contactor coils directly. They must never rely only on the PLC program. Check this at testing: with the PLC in STOP or disconnected, the emergency stop must still drop every contactor it controls.

## 31.8 Coordination of motor starters

IEC 60947-4-1 defines what may happen to the starter after a short circuit:

| Type | After a short circuit |
|---|---|
| Type 1 | Starter must not cause danger to persons, but may be damaged and need repair or replacement |
| Type 2 | Starter must remain fit for further use; light welding of contacts that can be easily separated is allowed |

Type 2 coordination needs the combination of breaker, contactor and overload relay tested by the manufacturer for the given short-circuit current. The design team selects the combination from the maker's coordination tables, and the BOM must not be changed (for example to a different contactor size or brand) without design approval, because the coordination would be lost.

## 31.9 Operator quick card

!! HINGLISH: Chhote motor ke liye DOL, 7.5 se 75 kW ke liye star-delta, smooth start ke liye soft starter, speed control ke liye VFD. Star-delta mein star aur delta contactor kabhi saath band nahi hone chahiye: electrical aur mechanical interlock zaroori. Overload relay winding circuit mein ho to 0.58 x FLC par set karo. Reversing starter mein do phase badalte hain; galat direction ho to motor terminal par do phase badlo. Emergency stop hamesha hard-wired, sirf PLC par bharosa nahi. BOM ka breaker-contactor combination design ki permission ke bina mat badlo.
