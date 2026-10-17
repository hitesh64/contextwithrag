# 27. Pneumatics and Mechanical Elements

## 27.1 Pneumatic systems

Compressed air drives the clamps of PUNCH-02, the electrode cylinder of WELD-05, CRIMP-12, the feeder of PEM-07, the powder equipment of PCL-09, and many small cylinders and blow-off nozzles. Air is clean and safe, but compressible: pneumatic cylinders are used for clamping and simple movements, not for precise positioning under load.

### 27.1.1 Components

| Component | Function | Typical fault |
|---|---|---|
| Ball valve with lockable lever and exhaust | Isolation for LOTO | Not exhausting: residual pressure |
| FRL unit (filter, regulator, lubricator) | Filters water and dirt, sets pressure, adds oil mist where needed | Filter bowl full of water; regulator drifting; lubricator empty or over-oiling |
| Soft-start valve | Builds up pressure slowly at start-up so cylinders do not move violently | Stuck: no pressure downstream |
| Solenoid valves (5/2, 5/3, 3/2) | Direct air to cylinder ports | Coil burnt, spool sticking from water or dirt, exhaust silencer blocked |
| Flow control valves (meter-out) | Set cylinder speed | Wrong setting, blocked |
| Cylinders | Linear motion | Seal leak (air escaping at exhaust when cylinder at end), bent rod, worn cushion |
| Pressure switch | Confirms pressure for machine start | Setting drifted, faulty |
| Silencers | Reduce exhaust noise | Blocked: cylinder slow to exhaust |
| Tubing and push-in fittings | Carry air | Cut, kinked or pulled-out tubes; leaking fittings |

### 27.1.2 Air pressure and force

**Cylinder force (N) = pressure (bar) x piston area (cm2) x 10 x efficiency (about 0.9)**

A 63 mm bore clamp cylinder (31.2 cm2) at 6 bar gives about 6 x 31.2 x 10 x 0.9 = 1680 N. If the plant pressure falls to 4.5 bar, the force falls by a quarter: clamps may slip. That is why machines monitor air pressure with pressure switches (alarm TP-04 on PUNCH-02 at 5 bar).

### 27.1.3 Maintenance

| Interval | Task |
|---|---|
| Daily (operator) | Drain the FRL filter bowl (or check auto drain); check pressure on the regulator gauge; listen for leaks |
| Monthly | Check lubricator oil level (only on machines that need lubricated air: use ISO VG 32 pneumatic oil); check silencers; check cylinder cushioning and speed |
| Yearly | Replace filter elements; check solenoid valves for leakage at exhaust; replace worn tubing |

!! CAUTION: Once a pneumatic system has been lubricated, it must stay lubricated: the oil washes out the original grease of the seals. Do not stop lubricating a system that was lubricated, and do not start lubricating a system designed for dry air (such as powder coating air, which must be oil-free).

### 27.1.4 Pneumatic fault finding

| Symptom | Check |
|---|---|
| Cylinder does not move | Air pressure at the valve; solenoid energised (LED, manual override button on the valve); tubing to correct port; cylinder mechanically blocked |
| Cylinder moves slowly | Flow control setting, blocked silencer, low pressure, leaking seals, undersized tubing |
| Cylinder moves without command | Valve spool stuck or leaking; wrong valve type (5/3 centre position) |
| Constant air blowing at valve exhaust | Valve seal leak or cylinder piston seal leak: disconnect cylinder line at the valve to find which |
| Water in the cylinders and valves | Dryer not working, drains blocked |

## 27.2 Bearings

### 27.2.1 Types

| Type | Load | Typical use in the plant |
|---|---|---|
| Deep groove ball bearing | Radial and moderate axial | Motors, fans, small pumps |
| Angular contact ball bearing | Combined radial and axial, often in pairs | Ball screw supports of CNC axes |
| Cylindrical roller bearing | Heavy radial | Large motors (drive end), gearboxes |
| Tapered roller bearing | Heavy radial and axial | Crane wheels, gearboxes |
| Spherical roller bearing | Heavy loads with misalignment | Large fans, conveyor drives |
| Linear guides (recirculating ball carriages) | Linear motion with precision | Back gauges, laser gantry, turret carriage |

### 27.2.2 Mounting and removal

- Use a bearing puller to remove bearings; never hammer on the rings or the cage.
- Mount by heating with an induction heater to 80 to 100 degrees C above ambient (never above 120 degrees C) or with a mounting sleeve pressing on the ring that is the interference fit. Never press through the balls.
- Keep new bearings in their package until mounting; work with clean hands and tools.
- Fill a grease-lubricated bearing to about 30 to 50 % of the free space; too much grease causes overheating.

### 27.2.3 Signs of bearing trouble

| Sign | Possible cause |
|---|---|
| Rumbling noise, rising vibration | Wear, fatigue (spalling) of the rings |
| Squealing | Lack of lubrication, too tight fit |
| High temperature | Over-greasing, wrong grease, misalignment, overload |
| Rust or discolouration | Water ingress, corrosion |
| Fluting (washboard marks) on motor bearings fed by VFD | Electrical discharge currents through the bearing; use insulated bearings or shaft grounding |

## 27.3 Belts, chains and couplings

### 27.3.1 V-belts and timing belts

- Check tension: deflection of about 16 mm per metre of span under a moderate thumb force for V-belts, or use a belt tension meter with the maker's value.
- Check alignment of pulleys with a straight edge or laser alignment tool: misalignment wears belts on one side.
- Replace V-belts in matched sets; never mix old and new belts on one drive.
- Timing belts (on some CNC axes): check for cracked teeth and correct tension; replace after any tooth damage.

### 27.3.2 Chains

- Lubricate chains regularly (conveyor chain of the paint line: high-temperature chain oil for the oven section).
- Measure elongation: replace a chain when elongation exceeds 2 to 3 % (measured over a length of several links).
- Check sprocket teeth: hooked teeth mean the sprocket must be replaced with the chain.

### 27.3.3 Couplings and alignment

Flexible couplings between motors and pumps (jaw couplings with elastomer spiders, tyre couplings) tolerate small misalignment but wear fast if misalignment is large. Align with a dial gauge or laser alignment tool to within 0.05 mm offset and 0.05 mm per 100 mm angularity for pumps running at 1500 rpm. Replace worn spiders (cracked or with play).

## 27.4 Ball screws and linear guides

CNC axes (back gauges of SHEAR-01, BRAKE-04, carriage of PUNCH-02 and BUS-10) use ball screws and linear guides. Their accuracy decides the accuracy of the parts.

- Keep them clean: wipers and bellows covers must be intact. A torn bellows lets chips in that destroy the balls.
- Lubricate as per the lubrication chart; use only the specified grease or oil (wrong grease can harden).
- Check backlash monthly on critical axes: move the axis back and forth by a small distance with a dial gauge on the moving part; backlash above 0.03 mm on a back gauge is investigated (support bearing preload, nut wear, coupling looseness).
- After a crash (collision), check the axis for bent screws, displaced bearings and lost reference before production.

## 27.5 Gearboxes

- Check oil level monthly at the level plug or sight glass, with the gearbox stopped.
- Change oil after the first 500 running hours of a new gearbox, then as per maker (typically every 5000 to 10 000 hours or 2 years).
- Use the specified gear oil (for example ISO VG 220 EP for crane gearboxes).
- Signs of trouble: rising temperature (above 80 degrees C on the housing), noise, leaks at the shaft seals, metal particles on the magnetic drain plug.

## 27.6 Bolted joints in machines

- Use the property class and torque specified by the machine maker for machine bolts.
- Loose bolts on moving parts (back gauge fingers, die clamps, guard brackets) are found during cleaning and inspection. Match marks (paint lines across bolt and part) make loosening visible.
- Thread-locking adhesive (medium strength) is used on screws subject to vibration where the maker specifies; clean threads before applying.
- Never replace a high-tensile bolt (8.8, 10.9 or 12.9) with an ordinary bolt of unknown grade.

## 27.7 Operator quick card

!! HINGLISH: Har din FRL ke filter ka paani nikalo aur pressure 6 bar dekho. Air kam ho to clamp ki pakad kam ho jaati hai. Bearing ko hathode se mat thoko, puller aur heater use karo, grease zyada mat bharo. Belt ka tension aur pulley alignment check karo, belt set mein badlo. Ball screw ke bellows phate ho to turant batao. Machine ke bolt ki jagah koi bhi saadhaaran bolt mat lagao.
