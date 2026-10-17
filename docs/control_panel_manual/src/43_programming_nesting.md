# 43. CNC Programming, Nesting and Program Management

CNC programs for LASER-03, PUNCH-02, BRAKE-04 and BUS-10 are prepared by the programming office from the released drawings. This chapter explains the rules for programmers and what operators need to know about programs.

## 43.1 From drawing to program

1. **Flat pattern**: the design team's 3D model is unfolded into a flat pattern using the plant's bend deduction values (Chapter 9.7.2). The flat pattern is checked against the drawing.
2. **Part program**: tooling (punch) or cutting technology (laser) is assigned to each contour.
3. **Nesting**: parts of the same material and thickness are arranged on sheets.
4. **Simulation**: the program is simulated in the CAM software for collisions, clamp zones, tool changes and time.
5. **Release**: the program is checked by a second programmer for new parts and released to the machine with the nest report.

## 43.2 Program naming

| Element | Format | Example |
|---|---|---|
| Job programs | Job number - machine letter and number | J2617-L01 (laser), J2617-P03 (punch), J2617-B05 (press brake) |
| Standard parts (repeat) | STD - part number - revision | STD-GLP-3060-B (gland plate 300 x 600, revision B) |
| Busbar programs | Job - BB - vertical | J2617-BB-V3 |

The program header contains the job number, part numbers, material, thickness, sheet size, programmer and date. The operator checks the header against the job card before running.

## 43.3 Laser programming rules

| Rule | Reason |
|---|---|
| Lead-in outside the part contour (inside for holes, in the scrap area) | Pierce marks and start defects stay off the part |
| Lead-in length about 3 to 5 mm (longer for thick sheet) | Stable cut before reaching the contour |
| Small holes (diameter below the thickness): use special small-hole technology or punch | Burning and poor roundness |
| Micro-joints: 0.2 to 0.5 mm on small parts that could tip up, placed on straight edges | Prevent tip-up and head collision; easy to break out |
| Cut inner contours before outer contours | Part stays fixed while holes are cut |
| Avoid-cut-parts path (head lifts over cut areas) | Prevents collisions with tipped parts |
| Common-line cutting for rectangular parts where edge quality allows | Saves time and material |
| Corner treatments for thick mild steel (loops or power ramping) | Avoids burn-out |
| Heat distribution: sequence that jumps across the sheet for many small holes in thin sheet | Avoids warping |

## 43.4 Turret programming rules

| Rule | Reason |
|---|---|
| Use the largest suitable tool for nibbling and fewer hits | Faster, less tool wear |
| Nibbling pitch: scallop height below 0.05 mm on visible edges | Smooth edges |
| Forming tools (louvres, extrusions) last, and in a separate area of the sheet where possible | Formed features can catch on the die and table |
| Keep holes and forming outside the clamp dead zone | Avoid TP-06 and clamp damage |
| Respect minimum web between holes (at least the sheet thickness, 1.5 x for stainless) | Prevents distortion and tearing |
| Respect punch force limit of 80 % of machine capacity (24 t) | Machine and tool protection |
| Plan repositioning for parts longer than X travel | Accuracy |
| Slug-free dies or vacuum for small holes | Prevent slug pulling |

## 43.5 Press brake programming

- The graphic CNC proposes a bending sequence; the programmer checks it for collisions, handling and back gauge positions (Chapter 9.7.3).
- The tool setup (stations of punches and dies along the beam) is optimised so that a part with several flange types can be bent without tool changes.
- Programs for new parts are marked "NEW - first-off by setter" so that the most experienced operator does the first part.
- Angle corrections found at first-off are saved in the program so that the next batch starts with them.

## 43.6 Busbar programming

- Busbar programs are generated from the busbar drawing (bar list with lengths, holes, bends).
- The software checks bending rules (minimum radius, distance between bends, hole to bend distance; Chapter 14.7.2). Warnings must not be overridden without design approval.
- Bar marking text is included in the program printout.

## 43.7 Nesting

| Guideline | Value |
|---|---|
| Target utilisation | Above 80 % |
| Minimum part spacing (laser) | 1 x thickness, minimum 3 mm (more for thick sheet) |
| Edge margin (laser) | 5 to 10 mm |
| Sheet sizes in stock | 1250 x 2500 and 1500 x 3000 mm (Chapter 5) |
| Grain direction | Respected for parts with visible structure or brushed finish |
| Mixing jobs | Allowed for same material and thickness; each part labelled with its job number by the marking function or tag |

## 43.8 Program management

- Released programs are stored on the programming server in folders by machine; only the programming office can write to them.
- Machines load programs from the server (DNC) or by approved USB stick from the programming office.
- An operator may change a program at the machine only for set-up corrections (angle corrections, offsets) and must inform the programming office, which updates the master program. Any change to geometry, tooling or sequence is made by the programming office only.
- When a drawing revision changes, the programming office withdraws the old program (renamed with "OLD") and releases a new one; the operator checks the revision on the program header against the job card.

!! CAUTION: A program copied from a similar part or another material is a common source of errors (wrong crowning, wrong bend radius, wrong parameters; see case studies 28.1 and 28.12). Programs are created for the actual material and thickness, never copied between materials.

!! HINGLISH: Program ka naam job number se: J2617-L01 laser, P03 punch, B05 press brake. Chalane se pehle program header ka job, material, thickness aur revision job card se milao. Laser mein lead-in part ke bahar, chhote part ke liye micro-joint. Punch mein forming tool aakhir mein aur clamp zone se door. Operator sirf angle ya offset correction kar sakta hai aur programming office ko batayega; shape ya tool ka badlav sirf programming office karega. Program ek material se doosre material ke liye copy mat karo.
