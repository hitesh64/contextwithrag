# 47. Troubleshooting Panels in Service

This chapter is a symptom-based guide for technicians and service engineers who maintain panels in operation, both the plant's own distribution panels and the panels supplied to customers. Always apply the safety rules of Chapters 3 and 42: diagnose with measurements, repair dead.

## 47.1 ACB will not close

| Check | Normal | If not |
|---|---|---|
| Position indicator | "Connected" (or "test" for testing) | Rack fully in; between positions the ACB is blocked |
| Spring status | "Charged" | Charge manually; if the motor does not charge: check motor supply, motor fuse / MCB, limit switch |
| Under-voltage release (UVR) | Energised (voltage present on UVR terminals) | Without UVR voltage the ACB cannot close: check UVR supply |
| Trip indicator / reset button | Reset | After a protection trip the release must be reset (mechanical reset button) and the cause investigated first |
| Mechanical interlock | Other breaker (e.g. DG incomer) open | Close is blocked by design |
| Electrical closing circuit | Closing coil receives voltage when close is commanded | Check close push button, permissive contacts, closing coil |
| Padlock / key interlock | Released | Remove only with authorisation |

!! WARNING: An ACB that tripped on a short circuit must not be closed again until the cause has been found and the breaker inspected. Read the trip history from the release (which protection, which phase, what current).

## 47.2 MCCB trips repeatedly

| Indication / pattern | Likely cause | Action |
|---|---|---|
| Trips after minutes or hours of load | Overload (L protection): load current above Ir; high ambient in panel; loose terminal heating the breaker | Measure current; check Ir setting against load and cable; thermal image of terminals |
| Trips instantly when the load starts | Instantaneous setting too low for inrush (transformer, motor, capacitor), or real short circuit | Measure starting current; check setting and curve; IR test of load cable and equipment |
| Trips with "G" (ground fault) indication | Earth fault in cable or equipment; neutral wrongly connected (N-PE link downstream) | IR test; check neutral arrangement |
| Trips at random, no load change | Faulty release, loose connection, vibration, shunt trip / UVR operated by control circuit | Check accessory circuits; release test with test kit |
| Does not reset | Mechanism not reset (handle to OFF / RESET first), UVR without voltage | Move handle fully to reset; check UVR |

## 47.3 Motor feeder does not start

1. Check the indications: "trip" lamp? Overload tripped? MPCB tripped?
2. Check the selector: in LOCAL or REMOTE as required? The remote permissive from the process present?
3. Check the emergency stop chain: any emergency stop pressed or faulty?
4. Check the control supply: control MCB on? Control transformer output voltage?
5. Command start and measure along the control rung (voltage method, Chapter 25.3.1).
6. If the contactor pulls in but the motor does not run: measure the three output voltages at the contactor output; check the overload relay, the cable and the motor (Chapter 25.5).
7. For PLC-controlled feeders: check the PLC output LED and the interface relay (Chapter 25.8).

## 47.4 Motor trips or runs hot

See Chapter 25.5.2. In addition, for panel causes:

- Overload relay set wrong (star-delta 0.58 x FLC; Chapter 28.14).
- One contactor main contact pitted (voltage drop across contact under load above 0.5 V): single phasing effect.
- Loose terminal in the starter (thermal image).
- Supply voltage unbalance from the panel busbar (check other feeders, upstream supply).

## 47.5 Meter readings wrong or blank

| Symptom | Cause |
|---|---|
| Meter blank | Auxiliary supply fuse blown; supply wiring loose; meter failure |
| Voltage on one phase missing | Voltage sensing fuse blown; loose wire |
| Current reading too high or low by a fixed ratio | CT ratio setting in meter wrong |
| Negative kW on one phase | CT polarity reversed on that phase, or CT and voltage of different phases |
| kW total low, PF strange | CTs and voltages not matched phase by phase |
| Energy not counting | Meter in wrong wiring mode; communication only |

Before disconnecting any CT wire, short the CT at the CT test terminal block (Chapter 17.5.3).

## 47.6 Control circuit faults

| Symptom | Likely cause |
|---|---|
| Control MCB trips when closed | Short circuit or earth fault in control wiring or a coil; disconnect circuits one by one (half-split) to find it |
| Contactors chatter | Low control voltage (long remote cables, overloaded control transformer), loose wire in holding circuit |
| Lamps glow faintly when off | Induced voltage on long control cables (capacitive coupling); use relays or lamp with lower impedance as per design |
| Device operates by itself | Earth fault on a control circuit that is not earthed (both sides floating), or induced voltage on long cables |

## 47.7 PLC panel faults

| Symptom | Check |
|---|---|
| PLC in STOP / ERROR | Diagnostic buffer (with authorised person); module missing or failed; power supply |
| Communication lost to HMI or SCADA | Cable, connector, switch port LEDs, IP address conflicts, network switch power |
| All inputs of a module off | 24 V supply to the input common; module fuse |
| One input does not change | Field device, wiring, input channel (swap wire to a spare channel to test, with authorisation) |
| Analogue value wrong | Loop wiring, 4-20 mA measured with loop calibrator, scaling in PLC, shield |
| Random resets | 24 V supply dips; earth / shield problems; overheating |

## 47.8 Panel heating and environmental problems

| Symptom | Check |
|---|---|
| Panel interior hot | Fans running? Filters clean? Louvres blocked? Heat load increased (devices added)? Ambient higher? |
| Condensation, rust inside | Heater and hygrostat working? Gland plate sealed? Cable trench damp (seal trench entry)? |
| Dust inside | Door gaskets, filter mats, unused openings |
| Rodent damage | Unsealed cable entries; seal with compound and mesh |
| Insects nests (outdoor) | Seal openings; fine mesh on louvres |

## 47.9 Busbar and connection problems

| Symptom | Check |
|---|---|
| Discoloured busbar or sleeve near a joint | Overheating joint: plan shutdown, clean and re-torque (Chapter 16.4.4) |
| Burning smell | Overheated insulation; locate with thermal camera; reduce load or shut down |
| Tracking marks on insulators | Dirt and moisture; clean, dry, check heater; replace damaged insulators |
| Buzzing from busbars | Loose supports or covers vibrating with current; check bolts (dead) |

## 47.10 Fault record

Record every fault on a panel in the breakdown record with the panel name and feeder number as "asset" (for example "MCC-2 / F14"), so that repeated faults of a feeder can be found. For customer panels, the service report (Chapter 37.6) is the record.

!! HINGLISH: ACB band na ho to dekho: position "connected", spring "charged", UVR par voltage, trip reset, interlock. Short circuit se trip hua ACB bina kaaran dhundhe dobara band mat karo. MCCB baar-baar trip: current naapo, setting dekho, terminal ka thermal image lo. Meter galat: CT ratio setting aur polarity check karo, CT wire kholne se pehle shorting link. Joint ke paas busbar ka rang badla dikhe to shutdown lekar saaf karke torque karo.
