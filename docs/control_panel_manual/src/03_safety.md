# 3. Safety in the Plant

## 3.1 Safety rules that apply to everyone

The following rules apply to every person in the plant, including visitors, contractors and managers. Breaking a rule in this list is a serious offence.

1. Wear the PPE required for the area at all times (section 3.2).
2. Never remove, bypass, bridge or mute a guard, interlock, light curtain or emergency stop.
3. Never work on a machine or a panel that has not been isolated, locked and proved dead (section 3.4).
4. Operate only the machines for which you have been trained and authorised. Your name must be on the authorisation list posted on the machine.
5. Report every injury, near miss and unsafe condition to your supervisor in the same shift.
6. No mobile phone use while operating a machine or while walking in a crane zone.
7. No smoking anywhere inside the building. No open flame in the paint shop.
8. Keep walkways, fire extinguishers, emergency exits and electrical panels clear.
9. Do not come to work under the influence of alcohol or drugs, or with medicine that makes you sleepy, without telling your supervisor.
10. Stop work when you are unsure. Every worker has the right and the duty to stop a job that looks unsafe.

!! WARNING: Most serious accidents in sheet metal and panel shops happen when an operator reaches into a machine "just for a second" to clear a part, or when a technician works on a circuit believed to be dead without testing it. Both are covered in this chapter. Read them twice.

## 3.2 Personal protective equipment

| Area or task | Required PPE |
|---|---|
| All production areas | Safety shoes (steel toe), cotton uniform with full sleeves, safety glasses |
| Sheet handling, shearing, punching, bending | Cut-resistant gloves (level 3 or higher), safety shoes, safety glasses |
| Laser cutting area | Safety glasses; laser-rated glasses only when the maker's manual requires them for open service work |
| Grinding and deburring | Face shield over safety glasses, leather gloves, ear plugs |
| Spot and MIG welding | Welding helmet with correct shade (shade 10 to 12 for MIG), leather gloves, leather apron, closed collar |
| Pre-treatment chemicals | Chemical goggles, PVC or nitrile gauntlets, PVC apron, gumboots |
| Powder coating booth | Dust mask (FFP2 or better), antistatic shoes, cotton overalls, no rings or watches |
| Busbar machine | Safety glasses, cut-resistant gloves, ear plugs while punching |
| Electrical testing (HV and live work) | Arc-rated clothing, insulated gloves rated for the voltage, face shield, insulated mat |
| Crane operation and slinging | Safety helmet, safety shoes, gloves |
| Noise above 85 dB(A) (punching, compressor room) | Ear plugs or ear muffs |

PPE is issued by the store against the worker's PPE card. Damaged PPE must be returned and replaced the same day. Insulated gloves for electrical work are tested by air inflation before each use and dielectric tested every six months; a glove with a pin-hole, crack or swelling must be destroyed.

## 3.3 Hazards of the plant

| Hazard | Where | Main control |
|---|---|---|
| Crushing and amputation | Shear, turret punch, press brake, PEM press, busbar machine | Fixed guards, light curtains, two-hand controls, LOTO |
| Cuts | Sheet handling, sharp burrs | Cut-resistant gloves, deburring, edge protection |
| Laser radiation and fire | LASER-03 | Closed cabin, interlocked doors, fire extinguisher, no unattended cutting |
| Electric shock and arc flash | Panels, test bench, machine control cabinets | LOTO, testing before touch, test bay barriers, trained persons only |
| Burns and UV light | Welding | Screens, helmets, gloves |
| Chemical burns | Pre-treatment tanks | Goggles, gauntlets, eye wash, chemical handling procedure |
| Dust explosion and fire | Powder booth and recovery | Earthing, ventilation, no ignition sources, cleaning |
| Hot surfaces | Curing oven, dry-off oven, parts leaving the oven | Gloves, warning signs, cooling zone |
| Falling loads | Crane, stacked material | Certified slings, trained slinger, no one under load |
| Noise | Punching, grinding, compressor | Ear protection, enclosures |
| Stored energy | Hydraulic accumulators, compressed air, springs, capacitors | Release and verify during LOTO |
| Manual handling | Sheets, doors, devices | Lifting aids, two-person lifts, correct posture |

## 3.4 Lockout and tagout (LOTO)

Lockout means putting a personal lock on every energy isolation point of a machine or panel, so that nobody can switch it on while you work. Tagout means hanging a tag on the lock that says who you are and why the equipment is locked. LOTO is required for every job that puts any part of your body into a danger zone, or brings you close to parts that could be live: clearing a jam inside a guard, changing tools, adjusting, cleaning inside, repairing and inspecting.

### 3.4.1 Energy sources to be isolated

| Energy | Examples in this plant | Isolation point |
|---|---|---|
| Electrical | All machines, panels under test, conveyors | Main isolator of the machine, upstream breaker of the panel |
| Hydraulic | SHEAR-01, BRAKE-04, BUS-10, PEM-07 | Pump stopped, pressure released through the release valve, gauge reads zero |
| Pneumatic | PUNCH-02 clamps, CRIMP-12, WIRE-11, LASER-03 | Lockable air valve closed, residual air exhausted |
| Gravity | Press brake beam, shear blade holder, raised conveyor hooks | Mechanical blocks or beam rested on the die |
| Thermal | Ovens, heated tanks | Burners off, allowed to cool, gas valve locked |
| Stored electrical | VFD DC bus, APFC capacitors, test bench | Discharge time observed, voltage measured |
| Chemical | Pre-treatment pumps and dosing | Pump isolated, valves closed and locked |
| Gas | Laser assist gas (oxygen, nitrogen), oven LPG/PNG | Cylinder or line valve closed and locked |

### 3.4.2 The LOTO procedure

[[fig:loto_steps|Figure 3-1. The eight steps of lockout and tagout|470]]

1. **Prepare.** Know which energies the equipment uses and where every isolation point is. The LOTO point list is posted on every machine and is included in each machine chapter.
2. **Inform.** Tell the operator and the supervisor of the area that the equipment will be shut down and locked.
3. **Shut down.** Stop the equipment by its normal stop sequence (cycle stop, then stop), so that nothing stops in the middle of a dangerous movement.
4. **Isolate.** Switch off and open every isolation point: main switch, air valve, hydraulic pump, gas valve.
5. **Lock and tag.** Put your own personal lock and your tag on every isolation point. If several people work on the equipment, use a multi-lock hasp: each person puts on his or her own lock. Nobody ever uses somebody else's lock or key.
6. **Release stored energy.** Lower the press beam onto blocks, release hydraulic pressure, exhaust air, wait for capacitors to discharge for the time printed on the device, let hot parts cool.
7. **Verify zero energy.** Try to start the equipment with the normal start button (with all controls then returned to off). For electrical work, test with an approved voltage tester: test the tester on a known live source, test the circuit phase to phase and phase to earth, then test the tester again on the known live source.
8. **Do the work, then remove LOTO safely.** When the work is complete, remove tools, refit all guards, count people out of the danger zone, inform the area, and remove locks in the reverse order. Each person removes only his or her own lock.

!! DANGER: "Switched off" is not "dead". A breaker can be mislabelled, a circuit can be fed from a second source, and capacitors keep their charge. Before you touch any conductor, prove it dead with a tested voltage tester. Test - test - test: the tester on a live source, the circuit, the tester again.

### 3.4.3 Locks, tags and keys

- Personal locks are red, keyed differently, and each carries the name and photo of its owner. They are issued only to trained people.
- Department locks (blue) are used by the maintenance department for long jobs at shift change, under the control of the maintenance supervisor.
- A tag must show the name, department, date, time, reason, and expected completion.
- A lock left on after the owner has gone home may only be removed by the maintenance manager, after trying to contact the owner, checking the equipment personally, and recording the removal in the LOTO register. The owner must be told before starting work the next day.

### 3.4.4 Shift change during locked-out work

When work under LOTO continues into the next shift, the outgoing person and the incoming person meet at the isolation point. The incoming person puts on his or her lock first, then the outgoing person removes his or hers. At no moment is the isolation point without a lock.

## 3.5 Electrical safety

### 3.5.1 Who may do electrical work

| Category | Who | Allowed work |
|---|---|---|
| Ordinary person | Operators, helpers | Operate switches and push buttons on closed panels; no opening of panels |
| Instructed person | Wiremen and fitters trained in this plant | Work on de-energised and locked panels under supervision; assist in testing |
| Skilled person | Licensed electricians, testing engineers, maintenance technicians with supervisor licence | Testing, fault finding, live measurements with a permit, HV testing |

### 3.5.2 Rules for working near live parts

- Work dead whenever possible. Live work is allowed only for measurement and fault finding where the circuit cannot be tested dead, under a permit signed by the maintenance manager.
- Use only insulated tools rated 1000 V and test instruments of measurement category CAT III 600 V or better.
- Wear arc-rated clothing, insulated gloves and a face shield when measuring at the incomer or busbars of a live panel.
- Remove rings, watches, metal chains and identity cards with metal clips.
- Stand on an insulating mat. Keep one hand away from the panel whenever possible.
- Never work alone on live equipment: a second trained person must be present who knows where the isolation is and how to give first aid.

### 3.5.3 Earthing

Every machine and every panel must be earthed through two separate earth conductors to the plant earth grid. The plant earth pits are tested once a year before the monsoon, and the value of each pit is recorded. A machine whose body shows any voltage to earth must be stopped and reported immediately.

## 3.6 Machine guarding

Each machine has fixed guards, interlocked guards and presence-sensing devices. The machine chapters describe them in detail. General rules:

- A fixed guard is fastened with screws that need a tool. It is removed only under LOTO by maintenance.
- An interlocked guard stops the machine when it is opened. Daily, the operator checks that opening the guard stops the machine.
- A light curtain stops a dangerous movement when the light beams are interrupted. Daily, the operator checks it with the test rod at three heights.
- The emergency stop is a red mushroom button on a yellow background. Daily, each emergency stop is pressed once and must stop the machine. It must be reset by turning or pulling before the machine can be restarted.

!! WARNING: A safety device that fails its daily test must be reported at once. The machine must not be used until maintenance has repaired and re-tested the device and the supervisor has signed the check sheet.

## 3.7 Cranes and lifting

CRANE-16 and the jib cranes may be operated only by trained and authorised operators. The lifting tackle (slings, shackles, eye bolts, spreader beam) is inspected and certified every six months by a competent person and carries a colour tag of the current period.

1. Check the load weight on the drawing or job card. Never lift a load heavier than the safe working load of the crane or of the tackle.
2. Inspect the slings before use: no cuts, kinks, broken wires, damaged stitching or missing tags.
3. Use the lifting eyes of the panel, a spreader beam for long shipping sections, and keep the sling angle within 60 degrees from vertical.
4. Lift a few centimetres, stop and check balance, then lift fully.
5. Never walk under a suspended load and never leave a load hanging unattended.
6. Use a tag line to guide long loads.

## 3.8 Chemicals

The pre-treatment line uses alkaline degreaser, acid derusting chemical, zinc phosphate and passivation chemicals. The material safety data sheet (MSDS) of every chemical is kept at the paint shop entrance.

- Always add acid to water, never water to acid.
- Wear goggles, gauntlets, apron and gumboots for any work at the tanks.
- Keep the emergency shower and eye wash station clear and test it weekly.
- In case of contact with eyes, wash with running water for at least 15 minutes and go to the first aid room.
- Keep chemicals in their labelled containers in the bunded chemical store. Never put a chemical in a drinking water bottle.

## 3.9 Fire safety

| Fire class | Material | Extinguisher |
|---|---|---|
| A | Wood, paper, cardboard, cloth | Water, foam, ABC dry powder |
| B | Oil, thinner, flammable liquids | Foam, CO2, ABC dry powder |
| C | Gas (LPG, PNG) | Shut off the gas first, then dry powder |
| Electrical | Live panels, machines | CO2 or clean agent; never water or foam on live equipment |
| Metal | Fine metal dust | Special dry powder or dry sand |

The powder coating booth has an automatic flame detector that stops the guns and the recovery fan. The laser cutting cabin has a CO2 extinguisher at the door. Every worker must know how to use an extinguisher by the PASS method: Pull the pin, Aim at the base of the fire, Squeeze the handle, Sweep from side to side.

### 3.9.1 Emergency procedure

1. Shout "Fire" and press the nearest fire alarm call point.
2. If the fire is small and you are trained, use the correct extinguisher. Keep your back to an exit.
3. If the fire cannot be controlled within 30 seconds, leave the area.
4. Leave by the nearest marked exit; do not use the goods lift.
5. Go to the assembly point in front of the main gate and report to your supervisor for the head count.
6. Do not go back into the building until the fire warden says it is safe.

## 3.10 First aid

First aid boxes are placed in every bay. Trained first aiders are named on the board at each bay and wear a green badge.

| Injury | First action |
|---|---|
| Electric shock | Do not touch the person until the supply is switched off, or move him away with dry wood; check breathing; start CPR if needed; call the first aider and doctor |
| Cut with bleeding | Press a clean pad on the wound, raise the limb, call the first aider |
| Crushed finger or hand | Do not reverse the machine without a technician; switch off, call the first aider and supervisor |
| Burn | Cool under running water for 20 minutes; do not apply oil or toothpaste; cover loosely |
| Chemical in eyes | Eye wash for 15 minutes, holding the eyelids open; go to the doctor |
| Foreign body in eye | Do not rub; eye wash; go to the first aider |
| Arc eye from welding | Cold compress, rest in a dark place, report to the first aider |

## 3.11 Permit to work

A written permit is required for the following jobs, in addition to LOTO:

- Hot work (welding, grinding, gas cutting) outside the welding area, especially near the paint shop.
- Work at height above 1.8 metres (crane maintenance, roof work, lighting).
- Entry into tanks, pits and the oven (confined space).
- Live electrical measurement and HV testing outside the test bay.
- Excavation for earth pits.

The permit is issued by the area in-charge, countersigned by the safety officer, displayed at the work site and closed at the end of the work.

## 3.12 Near miss and incident reporting

A near miss is an event that could have caused injury or damage but did not. Every near miss is a free lesson. Write it on the near miss card at the bay notice board or tell your supervisor. The safety committee reviews all near misses every week, and the corrective actions are displayed on the board.

!! HINGLISH: Har kaam se pehle PPE pehno. Machine ke andar haath daalne se pehle LOTO karo: band karo, apna lock aur tag lagao, pressure aur air nikalo, tester se check karo ki current nahi hai. Kisi aur ka lock kabhi mat kholo. Guard, light curtain ya emergency stop ko kabhi bypass mat karo. Aag lage to alarm dabao aur assembly point par jao.
