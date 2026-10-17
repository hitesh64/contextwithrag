# 42. Electrical Safety for Testing and Live Work

Chapter 3 gives the general electrical rules. This chapter goes deeper for testing engineers, electrical technicians and service engineers, who sometimes must work near live parts.

## 42.1 The two electrical hazards

| Hazard | What happens | Main protection |
|---|---|---|
| Electric shock | Current through the body; above about 30 mA through the chest can cause heart fibrillation | Dead working; insulation; barriers; RCDs; insulated tools and gloves |
| Arc flash | A fault through air releases enormous energy within milliseconds: heat (thousands of degrees), light, pressure wave, molten metal, toxic gases | Dead working; arc-rated PPE; remote operation; fast protection; distance |

Arc flash can occur when a tool slips between phases, a test lead touches the wrong point, a breaker is racked in on a fault, dust or moisture tracks across insulation, or a CT secondary is opened. The arc energy depends on the fault current and on how long the protection takes to clear it: the same panel can be much more dangerous at its incomer (cleared slowly by the upstream breaker) than at an outgoing feeder (cleared quickly by the feeder breaker).

## 42.2 Hierarchy of control

1. **Eliminate**: work dead. Plan the work so that the circuit is isolated, locked and proved dead.
2. **Substitute / engineer**: use remote racking devices, viewing windows for thermography, finger-safe test points, CT test terminal blocks, test plugs.
3. **Administrative**: permits, two-person rule, approach boundaries, barriers and signs.
4. **PPE**: the last line of defence, chosen for the task.

## 42.3 When live work is allowed

Live work in this plant is limited to:

- Measurements and fault finding that cannot be done dead (for example voltage measurement to find which contact is open, current measurement with a clamp meter).
- Thermographic inspection through opened doors where designed for it.
- Racking breakers in and out of live cradles (with arc-rated PPE and preferably remote racking).
- Testing in the test bay under the test bay rules (Chapter 20.3.1).

Repairs, re-termination, tightening of busbar joints and replacement of devices are **never** done live.

## 42.4 Live work permit

| Field | Content |
|---|---|
| Task and reason why it cannot be done dead | Written explanation |
| Equipment and voltage | Panel, feeder, voltage |
| Hazards | Shock, arc flash, others |
| Approach boundaries | Marked with barriers and signs |
| PPE required | Gloves class and voltage, arc-rated clothing, face shield / hood, insulated tools |
| Instruments | CAT rating, condition checked |
| Persons | Skilled person doing the work; second trained person as standby who knows isolation and first aid |
| Emergency | Location of isolation, phone number, first aider |
| Approval | Maintenance manager |

## 42.5 PPE for electrical work

| Task | PPE |
|---|---|
| Voltage measurement on control circuits (110 / 230 V) inside a machine cabinet | Safety glasses, insulated gloves class 00 (500 V), cotton clothing, CAT III meter |
| Voltage measurement on 415 V power circuits of feeders | Insulated gloves class 0 (1000 V) with leather protectors, arc-rated shirt and trousers, arc-rated face shield, safety glasses |
| Work at the main incomer of a PCC (live measurement, racking) | As above plus arc-rated hood or flash suit as specified by the arc flash study, remote racking where available |
| HV testing in the test bay | Outside the fence: no special PPE beyond the bay rules; inside only when de-energised and earthed |

- Insulating gloves are inspected and air-tested before each use and dielectric tested every 6 months (Chapter 3.2).
- Arc-rated clothing is worn as the outer layer; synthetic underwear (nylon, polyester) melts and must not be worn under it.
- Remove metal: rings, watches, chains, metal-framed spectacles where possible.

## 42.6 Approach boundaries

Around exposed live parts, two boundaries are marked for live work:

| Boundary | Who may cross | Typical distance at 415 V (guide) |
|---|---|---|
| Limited approach boundary | Only skilled persons, or others escorted by a skilled person | About 1 m |
| Restricted approach boundary | Only skilled persons with shock PPE and insulated tools, for the task in the permit | About 0.3 m |
| Arc flash boundary | Anyone crossing must wear arc-rated PPE | From the arc flash study; often 1 to 2 m at large incomers |

Place barriers (barrier tape and stands) at the limited approach boundary and a "Danger - live work" sign.

## 42.7 Proving dead and earthing

1. Isolate at the correct point (check the drawing, labels can be wrong); lock and tag.
2. Test the tester on a known live source or proving unit.
3. Test all combinations: L1-L2, L2-L3, L3-L1, each phase to N and to PE, N to PE.
4. Test the tester again.
5. For busbar and cable work at 415 V in large installations, or where there is any risk of back-feed (DG, UPS, capacitors, parallel feeds), apply **portable earths**: connect the earth clamp to the earth bar first, then clamp each phase with the insulated stick. Remove in the reverse order (phases first, earth last).
6. Discharge capacitors (APFC, VFD, long cables) and wait for the labelled discharge times.

## 42.8 Back-feed sources

| Source | Precaution |
|---|---|
| DG set connected through changeover | Lock the DG breaker and the changeover in the safe position; stop the DG |
| UPS and inverters | Isolate the UPS output and battery |
| Capacitors (APFC, motor PF capacitors) | Isolate, discharge, wait, measure |
| VFD DC bus | Wait for discharge time, measure DC bus |
| Interlocking wires from other panels (orange) | Isolate at the source panel |
| PT secondary back-energising primary | Remove PT secondary fuses before working on PT primary side |
| Motors being driven by the load (fans windmilling, pumps back-flowing) | Mechanically stop the load or close valves; a rotating motor can generate voltage (especially permanent magnet motors) |

## 42.9 Using test instruments safely

- Use leads with finger guards and short exposed tips (4 mm or less) and fused leads for multimeters.
- Select the function before connecting; never switch ranges with the leads connected to a live circuit.
- Never measure voltage with the meter on the current or resistance range.
- Connect the black (common) lead first and remove it last.
- Keep the meter in a position where you do not have to lean into the panel.
- Do not use instruments with cracked cases, damaged leads or expired calibration.

!! DANGER: Most fatal electrical accidents happen on circuits that people believed were dead. Never trust a label, a breaker position or another person's word. Prove it dead yourself, every time.

!! HINGLISH: Bijli ke do khatre: current lagna (shock) aur arc flash (dhamaka aur aag). Sabse achha tareeka: band karke kaam. Live kaam sirf naapne aur fault dhundhne ke liye, permit ke saath, do log, insulated gloves, arc-rated kapde aur face shield. Repair, torque ya device badalna kabhi live nahi. Dead prove karne se pehle aur baad tester check karo. DG, UPS, capacitor, VFD aur orange wire se back-feed ho sakta hai, unhe bhi alag karo.
