# 16. Mechanical Assembly of Panels

## 16.1 Purpose

Assembly turns painted sheet metal parts, busbars and bought-out devices into a complete panel ready for wiring. The assembly team builds the structure, fits doors and covers, erects the busbar system and mounts the devices. Mistakes made in assembly are expensive to correct later: a frame out of square makes doors that do not close; a loose busbar joint overheats years later; a breaker mounted without the clearance its maker requires trips on heat or fails in a short circuit.

## 16.2 Assembly bay, tools and preparation

### 16.2.1 Assembly stations

Each assembly station in Bay 5 has a levelled steel floor plate (checked every 6 months with a level), a tool board, a parts trolley, a drawing stand, and access to CRANE-16.

### 16.2.2 Tools

| Tool | Purpose | Control |
|---|---|---|
| Torque wrenches 2-25 Nm, 20-100 Nm, 60-200 Nm | Busbar joints, device terminals, structure | Calibrated every 6 months; sticker with due date |
| Torque screwdrivers 0.5-6 Nm | Device terminals and terminal blocks | Calibrated every 6 months |
| Socket sets, ring spanners, Allen keys | General | Personal kit |
| Spirit level 600 mm and 1500 mm, steel square, tape | Levelling and squareness | Checked monthly |
| Electric screwdriver with clutch | Sheet metal screws, DIN rails | Clutch set for each screw type |
| Rivet gun, rivet nut tool | Rivet nuts where PEM fasteners are not fitted | - |
| Hole saw set, knock-out punch set | Late changes, gland plate holes | Only with supervisor approval |
| Paint marker (yellow), torque seal | Marking torqued joints | - |
| Insulation shrouds, edge protector | Protection | - |

### 16.2.3 Before starting

1. Check the drawings: GA, busbar drawing, mounting plate layout, BOM. All must carry "released for manufacturing" and the same revision as the job card.
2. Check the painted parts: count against the parts list, check for paint damage. Report any damage before assembly (touch-up after assembly is harder and visible).
3. Check the bought-out devices against the BOM: make, type, rating, coil voltage of contactors, auxiliary contacts, release settings of breakers. A wrong coil voltage is a common error that is found only at testing.
4. Collect busbars: check job number and bar numbers on each bar.

## 16.3 Structure assembly

### 16.3.1 Sequence for a multi-section panel

1. Place the base frame on the assembly floor. Check that it is level in both directions (bubble centred) and shim if needed.
2. Erect the vertical frame members on the base frame; fix with the bolts in the drawing (generally M8, property class 8.8, with plain and spring washers).
3. Fit the top frame members.
4. Before tightening, check squareness: measure both diagonals of each face. The difference must be below 2 mm. Correct by loosening and pushing the frame; then tighten.
5. Fit internal members: horizontal partitions supports, cable alley supports, busbar chamber supports.
6. Join sections: place the next section against the first, align the faces and the tops, and bolt through the joining holes (M8 with washers). Place the inter-section gasket between sections if the panel is IP54 or above.
7. Check the overall length, height and alignment along the whole line with a string or laser line: the front face must be straight within 3 mm over the whole length.

**Table 16-1. Torque for structure bolts (steel, property class 8.8)**

| Bolt | Torque |
|---|---|
| M5 | 5 Nm |
| M6 | 8 Nm |
| M8 | 20 Nm |
| M10 | 40 Nm |
| M12 | 70 Nm |

### 16.3.2 Doors and covers

1. Fit hinges to the frame; fit the door. Check that the door hangs square to the frame with an even gap of 2 to 3 mm all around.
2. Adjust with the hinge slots so that the door does not drop when opened (sag) and closes without force.
3. Fit the gasket: self-adhesive neoprene or EPDM profile on the door return, starting and ending at the bottom centre with a butt joint (no gap, no overlap). Clean the surface with isopropyl alcohol first.
4. Fit locks: quarter-turn or handle locks as per drawing. Adjust the lock cam so that the gasket is compressed by 25 to 35 % (a 6 mm gasket to about 4 mm). Test: a sheet of paper closed in the door at the gasket should be held firmly.
5. Fit door stoppers / stays so that the door does not swing back against the next door.
6. Fit covers with their screws; check the gaskets for IP54 panels.

### 16.3.3 Earthing of the structure

Every metallic part that can be touched must be connected to the protective earth so that a fault on any device trips the protection instead of making the body live. Painted joints do not conduct, so earth continuity is provided deliberately:

| Part | Earth connection |
|---|---|
| Frame sections | Bolted to the PE busbar at every section with earth studs (masked during painting) |
| Doors carrying electrical devices | Flexible earth braid or green-yellow wire, minimum 6 mm2, from door stud to frame stud |
| Doors without devices | Earth braid or wire, minimum 4 mm2 (plant standard: 6 mm2 for all doors) |
| Mounting plates | Earth stud on plate to frame or PE bar, 6 mm2 minimum, or bolted contact on bare masked areas |
| Gland plates | Earth stud to PE bar, 6 mm2; for single-core cable gland plates (aluminium): earth stud as per drawing |
| Covers with no devices | Contact through serrated (toothed) washers on masked areas, or earth wire |
| Section to section | Through bolted PE busbar joints |

!! WARNING: Earth wires and braids must use ring lugs on studs with a nut and a serrated lock washer. Never earth through a hinge or through a painted screw. The testing engineer measures the resistance from every door and mounting plate to the main PE terminal (Chapter 20); a single missing earth strap fails the panel.

### 16.3.4 Lifting arrangements

Fit the lifting eye bolts (or lifting angles) on each shipping section as per the drawing. Screw eye bolts fully down so that the collar sits on the frame; never use an eye bolt that cannot be fully tightened. Lifting angles carry a label with the maximum load.

## 16.4 Busbar system erection

### 16.4.1 Busbar arrangement

[[fig:busbar_layout|Figure 16-1. Typical busbar arrangement in a PCC/MCC section (side view)|430]]

The main horizontal busbars run in the busbar chamber at the top (or bottom) of the panel, supported on insulators fixed to support channels. In each section, vertical droppers are connected to the main busbars and feed the functional units. The neutral bar runs parallel to the phase bars; the PE bar runs along the bottom of the panel. Phase order from front to back, top to bottom, or left to right (as viewed from the front) is **L1 (R), L2 (Y), L3 (B), N**, unless the drawing states otherwise. The same order must be kept throughout the panel and in every section.

### 16.4.2 Clearances

**Table 16-2. Minimum clearances inside panels (plant standard for 415 V systems, Uimp 8 kV)**

| Between | Minimum air clearance |
|---|---|
| Phase to phase (live bare parts) | 25 mm |
| Phase to neutral | 25 mm |
| Phase or neutral to earth (including frame, barriers, door) | 20 mm |
| Bare live parts to a door or cover that can be opened | 25 mm |
| Busbar to an insulated (sleeved) wire passing nearby | 20 mm, and the wire is fixed so that it cannot move closer |

These plant values are larger than the minimum clearances of IEC 61439-1 for 8 kV impulse withstand voltage; they include a margin for assembly tolerances and for fingers and tools during maintenance. Creepage distances along insulating surfaces (insulators, terminal supports) follow the drawing and the insulator rating.

!! CAUTION: Clearances are checked at the closest point: bolt heads and nuts, the ends of bolts that stick out, the edges of washers and the corners of bars. A bolt that is 10 mm too long can reduce a 25 mm clearance to 15 mm. Use the bolt length on the drawing.

### 16.4.3 Busbar supports

- Use only the insulators specified for the panel's short-circuit rating; the drawing gives the type and the maximum spacing between supports (for example 50 kA for 1 s, maximum 400 mm spacing for 10 x 100 mm copper).
- Fix insulators to the support channel with the bolts specified; do not over-tighten into insulator inserts (use the insulator maker's torque, typically 20 Nm for M8 inserts and 30 Nm for M10).
- Bars must rest freely in the support slots; supports must not be forced. If a bar has to be pulled to reach a support, the bar or support position is wrong: correct it, do not force it.

### 16.4.4 Making a bolted busbar joint

A bolted joint carries the full current through the contact area between the bars. Its resistance must be as low as the bar itself and must stay low for 20 years under heating and cooling cycles. Most panel failures in service start at a busbar joint that was dirty, poorly tightened or loosened.

1. **Clean** the contact faces just before assembly: non-woven abrasive pad on bare copper (light, until the surface is bright), lint-free cloth with isopropyl alcohol. On tin-plated bars, only wipe with alcohol: abrasives remove the tin.
2. For aluminium bars: brush the contact faces with a stainless steel wire brush and immediately apply a thin layer of jointing compound (contact grease with zinc particles) to break the oxide layer and keep air out. For aluminium-to-copper joints, use a bimetallic plate (Cu-Al) or tinned copper, never bare copper directly on aluminium.
3. **Assemble** with the specified bolts: property class 8.8, zinc-plated or hot-dip galvanised, with a large flat washer under the bolt head and under the nut, and a spring washer or disc spring (Belleville) washer under the nut. Aluminium joints always use disc spring washers.
4. Insert all bolts finger-tight first; check alignment of bars and clearances.
5. **Torque** with a calibrated torque wrench to the value in Table 16-3, tightening in a cross pattern for multi-bolt joints, in two stages (first 50 %, then 100 %).
6. **Mark** each tightened bolt with a yellow paint marker line across the nut, washer and bar (torque seal). The mark shows that the bolt was torqued and shows later if it has turned.
7. Record the joint numbers and torque in the busbar torque record of the job, signed by the fitter.

**Table 16-3. Tightening torque for busbar joints (steel bolts property class 8.8, lightly oiled, with flat and spring or disc spring washers)**

| Bolt size | Torque | Used for |
|---|---|---|
| M6 | 10 Nm | Small links, CT secondary links, neutral links of small DBs |
| M8 | 22 Nm | Bars up to 25 mm wide, device terminals where the device maker gives no value |
| M10 | 44 Nm | Bars 20 to 30 mm wide, M10 device terminals |
| M12 | 75 Nm | Bars 40 mm wide and above, main busbar joints |
| M16 | 160 Nm | Heavy main bus joints of 4000 A panels, as per drawing |

!! NOTE: Device terminals (ACB, MCCB, contactors) are tightened to the torque given by the device manufacturer, which can be different from Table 16-3. The device value always applies to the device terminal. Table 16-3 applies to bar-to-bar joints and to bar-to-device connections only where the device maker gives no value.

### 16.4.5 Shrouds and joint covers

After testing the joints, fit the joint covers and phase barriers shown on the drawing. Bare joints in Form 2 and higher panels are covered so that a dropped tool cannot bridge phases. Shrouds must not touch hot joints in a way that traps heat, and must not reduce clearances.

## 16.5 Mounting plates and devices

### 16.5.1 Mounting plate layout

Mounting plates are usually laid out and partly assembled on the bench, then fitted into the panel. Check the plate layout drawing: device positions, DIN rail and wire duct positions, and the free spaces required by devices.

### 16.5.2 DIN rails and ducts

1. Cut DIN rails (35 mm top hat rail) to length with the rail cutter; deburr ends.
2. Fix rails with M5 screws into PEM nuts or rivet nuts, at most 250 mm apart and within 30 mm of each end.
3. Fit wire ducts (slotted PVC trunking) with screws or rivets, at most 400 mm apart. Duct size is chosen so that it is filled to at most 70 % after wiring (to allow later changes and heat dissipation).
4. Keep a gap of at least 30 mm between a duct and the terminals of a device for wire bending, or as the device maker requires.

### 16.5.3 Mounting devices

- Mount breakers and contactors in the orientation allowed by the maker (usually vertical, supply at the top). An MCCB mounted horizontally may need derating; check the data sheet.
- Respect the **minimum clearances** around breakers given by the maker: for MCCBs typically 50 to 100 mm above the arc chute side to an earthed metal part, because hot ionised gas is expelled during a short-circuit break.
- Do not drill holes above a mounted device: metal swarf falling into a breaker, contactor or drive can cause failure. Cover devices with a cloth or plastic sheet when any drilling or cutting is unavoidable.
- Fit PLCs, drives and electronic devices last, and handle them by the case with ESD precautions: touch the earthed frame before handling, keep them in their antistatic bags until fitting.
- Drives (VFDs) need free space above and below for cooling as per the maker (often 100 mm or more). Do not place them directly above another heat source.
- Mount door devices (meters, push buttons, lamps, selector switches, HMIs) with their gaskets so that the door IP rating is kept.

### 16.5.4 Heavy devices

ACBs (50 to 120 kg) are lifted into the panel with CRANE-16 and a lifting beam or with the ACB lifting trolley, using only the lifting points of the ACB. Draw-out ACBs: fix the cradle first, check its alignment, then rack in the breaker body and check that it moves smoothly between the disconnected, test and connected positions before connecting the busbars.

### 16.5.5 Interlocks

| Interlock | Purpose | Check during assembly |
|---|---|---|
| Door interlock with breaker handle | Door cannot be opened with the breaker ON (unless defeated by an authorised tool) | Operate handle ON: door must not open; OFF: door opens |
| Mechanical interlock between two ACBs (incomer / DG or bus coupler) | Prevents parallel connection of two sources | Close one: the other cannot be closed |
| Castell / key interlock | Sequence of operations with transferable keys | Keys only free in the correct position |
| Padlocking facility | LOTO of breakers | Handle can be locked in OFF position only |
| Shutters in withdrawable units | Cover busbar stabs when unit is withdrawn | Shutters close automatically |

### 16.5.6 Labels

| Label | Where | Content |
|---|---|---|
| Feeder name plate | On each door / module front | Feeder name and number as per SLD (e.g. "F-12 COOLING TOWER FAN 2, 15 kW") |
| Device labels | Next to each device inside | Device tag from drawing (Q1, K1, F3, X1) |
| Danger plate | On every incomer and on covers of live compartments | "Danger 415 V" with symbol, in English and the local language |
| Rating plate | On the main incomer door | Ratings of section 1.4 |
| Phase identification | On busbars and cable terminals | L1, L2, L3, N, PE |
| Terminal strip labels | On terminal blocks | Strip number and terminal numbers |

## 16.6 Assembly inspection

Before the panel goes to wiring, the assembly inspector checks:

| Item | Requirement |
|---|---|
| Dimensions and alignment | As per GA; front face straight within 3 mm |
| Squareness | Diagonals within 2 mm |
| Doors | Even gaps, no sag, locks working, gasket complete |
| Earth continuity of structure | All earth braids and studs fitted (count) |
| Busbars | Correct size and phase order, supports at drawing spacing, clearances (Table 16-2) |
| Busbar joints | Every bolt torqued and marked (100 % visual check of marks), torque record signed |
| Devices | Correct type, rating, coil voltage, as per BOM; clearances respected |
| Interlocks | All operate correctly |
| Paint damage | Touched up with the correct paint |
| Cleanliness | No swarf, no loose parts, no tools inside |

Defects are written on the punch list and corrected before wiring starts.

## 16.7 Operator quick card

!! HINGLISH: Assembly se pehle drawing ka revision aur BOM ke saath devices (rating, coil voltage) milao. Frame ke diagonal ka farak 2 mm se kam ho. Har door aur mounting plate ka earth strap 6 mm2 lagao, kabhi hinge se earth mat maano. Busbar joint: pehle saaf karo, sahi bolt aur washer lagao, torque wrench se Table 16-3 ke hisaab se kaso (M10 44 Nm, M12 75 Nm), phir peela paint marker lagao aur record par sign karo. Phase se phase 25 mm aur phase se earth 20 mm doori zaroori. Device ke upar drilling mat karo. PLC aur drive ko antistatic dhyan se pakdo.
