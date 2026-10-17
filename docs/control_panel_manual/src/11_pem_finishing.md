# 11. Hardware Insertion (PEM-07), Deburring and Fabrication Inspection

## 11.1 Purpose

Thin sheet cannot hold a tapped thread strongly enough for repeated assembly: a 2 mm sheet gives only about two threads of engagement. Panels therefore use **self-clinching fasteners**: nuts, studs and standoffs pressed permanently into the sheet. They give strong, reusable threads for mounting plates, doors, earth studs, DIN rail supports, busbar insulator brackets and hinges. PEM-07 presses them in with controlled force.

Hardware is inserted after bending and welding and **before painting**, so that the paint is not cracked by pressing and the threads can be protected with masking plugs before coating.

## 11.2 How self-clinching works

[[fig:clinch|Figure 11-1. Self-clinching nut: before and after pressing|380]]

A self-clinching fastener has a knurled or splined collar and an undercut groove, and it is harder than the sheet. It is placed in a punched or laser-cut hole of exact size and pressed with a flat anvil and punch. The force pushes the collar into the sheet; the displaced sheet metal flows into the undercut and locks the fastener. The knurl stops it from turning (torque-out resistance) and the undercut stops it from being pushed out (push-out resistance).

Three conditions must be met for a good clinch:

1. The hole must be the exact size given by the fastener maker, punched or laser cut, not drilled oversized, and not chamfered or deburred on the insertion side.
2. The sheet must be at least the minimum thickness for the fastener, and softer than the fastener (standard steel fasteners are for CRCA and GI sheet; stainless steel sheet needs special hardened stainless fasteners).
3. The fastener must be pressed squarely with the right force, until the head is flush with the sheet. Never hammer a self-clinching fastener.

## 11.3 PEM-07 machine

### 11.3.1 Main parts and data

| Part / item | Description |
|---|---|
| Type | C-frame hydraulic insertion press with safety tooling system |
| Force | Adjustable, 6 to 60 kN (maximum 6 tonnes) |
| Throat depth | 460 mm |
| Safety system | Punch-to-anvil contact sensing: the press develops full force only when the punch touches a conductive fastener on the work, not a finger |
| Tooling | Anvils and punches for each fastener type and size, colour coded |
| Feeding | Manual placement; automatic bowl feeder for nuts M4, M5, M6 |
| Hydraulic oil | ISO VG 32, 40 litres |
| Air (feeder) | 6 bar |

### 11.3.2 Fastener table (steel fasteners in CRCA and GI sheet)

| Fastener | Size | Hole diameter (mm) | Minimum sheet (mm) | Minimum centre-to-edge (mm) | Typical press force (kN) |
|---|---|---|---|---|---|
| Self-clinching nut | M4 | 5.41 | 1.0 | 6.9 | 13 to 18 |
| Self-clinching nut | M5 | 6.35 | 1.0 | 7.1 | 18 to 27 |
| Self-clinching nut | M6 | 8.75 | 1.4 | 8.6 | 27 to 36 |
| Self-clinching nut | M8 | 10.50 | 1.4 | 9.7 | 36 to 45 |
| Self-clinching stud | M5 | 5.00 | 1.0 | 6.4 | 18 to 22 |
| Self-clinching stud | M6 | 6.00 | 1.2 | 7.1 | 22 to 27 |
| Self-clinching stud | M8 | 8.00 | 1.6 | 7.9 | 31 to 36 |
| Threaded standoff | M4 | 5.41 | 1.0 | 6.9 | 13 to 18 |
| Threaded standoff | M5 | 7.14 | 1.0 | 7.1 | 18 to 27 |

!! NOTE: The values are the plant's working data for the fasteners stocked. Always check the fastener maker's data sheet for a new fastener type, and run a push-out test on the first part.

### 11.3.3 Operation

1. Switch on the press and the hydraulic pump; select the force programme for the fastener (the programme number is written on the tool rack next to each tooling set).
2. Fit the anvil and punch of the matching colour code.
3. Do the safety test: place the test plastic piece (non-conductive) on the anvil and operate: the press must stop with low force and show "no contact".
4. Place the part with the hole over the anvil; place the fastener in the hole from the correct side (the side shown on the drawing; nuts from the opposite side of the mating part).
5. Press the pedal. The punch descends, detects the fastener, applies the programmed force, and returns.
6. Check: head flush with the sheet (within 0.1 mm), fastener square, no sheet bulging on the reverse side.
7. Fit masking plugs or caps to threads that must stay paint-free (earth studs, earth nuts).

!! WARNING: Keep fingers out from under the punch. The contact sensing system reduces the risk but does not remove it: a conductive glove, a ring or a metal object under the punch can be detected as a fastener. Do not wear rings or metal watches at PEM-07.

### 11.3.4 Quality tests

| Test | How | Frequency | Accept if |
|---|---|---|---|
| Flushness | Straight edge, feeler gauge | Every part | Head flush within 0.1 mm |
| Push-out | Press the fastener out on a test sample with a push-out tool on the force gauge | First-off of each lot and size | Above the minimum value of the data sheet (for M5 nut in 2.0 mm CRCA: 1300 N) |
| Torque-out | Torque wrench with a mating screw on a test sample | First-off of each lot and size | Above the minimum value (M5 nut in 2.0 mm CRCA: 6 Nm) |
| Thread | Thread gauge or screw | First-off, after painting | Screw goes in by hand |
| Earth stud continuity | After painting, ohmmeter between stud and bare sheet | Every earth stud | Below 0.1 ohm (masking was effective) |

### 11.3.5 Troubleshooting PEM-07

| Problem | Cause | Remedy |
|---|---|---|
| Fastener spins in hole | Hole too large; force too low; sheet too thin | Check hole size and sheet thickness; check programme |
| Fastener pushes out | Force too low; hole deburred or chamfered; sheet too hard (stainless) | Increase force within limits; no deburr on insertion side; use correct fastener |
| Sheet bulges or distorts | Force too high; centre-to-edge too small | Reduce force; check drawing; relocate fastener |
| Fastener not flush | Force too low; anvil not flat; burr on hole | Check force; check anvil; remove slug or burr |
| Press does not reach force | "No contact" detected; punch not touching fastener | Check fastener placed, punch type, contact sensor cable |
| Thread damaged | Fastener pressed upside down; wrong punch | Check orientation; use correct punch |

| Code | Message | Action |
|---|---|---|
| PM-01 | Emergency stop | Reset |
| PM-02 | No contact (safety) | Check placement and tooling; remove non-conductive objects |
| PM-03 | Force not reached | Check oil level, pump, pressure transducer |
| PM-04 | Oil temperature high | Allow cooling, check cooler fan |
| PM-05 | Feeder jam | Clear feeder track under LOTO of the feeder air |

### 11.3.6 Maintenance

| Frequency | Task |
|---|---|
| Daily | Safety test (non-conductive piece); clean anvils and punches; check oil level |
| Weekly | Clean feeder bowl and tracks; check punch faces for wear |
| Monthly | Verify force with the load cell test kit at 20 kN and 40 kN (within +/- 5 %) |
| Yearly | Change hydraulic oil and filter; check contact sensing circuit |

## 11.4 Deburring and grinding

Every cut edge has a burr: a small sharp ridge of metal pushed out by the cutting process. Burrs cut hands, damage wire insulation inside the panel, prevent parts from fitting flat, and cause paint to be thin on the sharp edge so that rust starts there. All cut parts are therefore deburred before bending.

### 11.4.1 Methods

| Method | Tool | Use |
|---|---|---|
| Hand deburring | Swivel blade deburring tool, file | Holes and small parts |
| Orbital sander | 120 grit disc | Flat edges of large parts |
| Angle grinder with flap disc | 60 to 80 grit flap disc | Weld seams, heavy burrs, laser dross |
| Belt grinder | 80 grit belt | Small brackets, busbar supports |
| Countersink tool | 90 degree countersink | Light chamfer of holes where wires pass |

!! CAUTION: Holes through which wires or cables will pass (cable entries, wire passages in partitions) must be deburred and fitted with a rubber grommet or edge protector. A sharp edge can cut through insulation by vibration over months and cause an earth fault.

### 11.4.2 Grinding safety

- Use the correct disc for the grinder speed: the disc rated speed (rpm) must be equal or higher than the grinder speed.
- Fit the guard; never remove it.
- Wear face shield over safety glasses, leather gloves, ear plugs; no loose clothing.
- Hold the grinder with both hands; let it reach full speed before touching the work.
- Never grind with the side of a cutting disc.
- Direct sparks away from people, gas cylinders and the paint shop.
- Unplug the grinder before changing discs.

### 11.4.3 Grinding welds

Weld seams on visible faces (door fronts, top covers) are ground flush with a flap disc, then blended with 120 grit. Do not grind deeper than the sheet surface: thinning the sheet weakens the joint and shows as a dip under the paint. Weld seams on hidden faces are only cleaned of spatter.

## 11.5 Fabrication inspection before painting

Before parts go to the paint shop, the sheet metal inspector checks each sub-assembly. A defect found now costs minutes; the same defect found after painting costs hours (paint strip, rework, recoat), and after assembly it can cost days.

| Item | Check | Tolerance / requirement |
|---|---|---|
| Overall dimensions | Tape, against drawing | +/- 1 mm up to 1000 mm, +/- 2 mm above |
| Diagonals of frames and doors | Tape | Difference below 1.5 mm for frames, 1 mm for doors |
| Flatness of doors and covers | Straight edge | Below 2 mm over the length |
| Hole positions (mounting plates) | Tape, vernier, template | +/- 0.5 mm |
| Cut-outs for meters and devices | Vernier, sample device | Device fits without force |
| Weld quality | Visual | No cracks, porosity, spatter on visible faces |
| Burrs and sharp edges | Gloved hand, visual | None |
| Hardware | Count, type, flushness | As per drawing |
| Earth points | Marking, masking plugs | Every earth stud masked |
| Job and part tags | Tag present | Job number, part number |

Parts that pass get a green "OK for paint" tag stamped by the inspector. Rejected parts get a red tag with the defect written on it and go back to the responsible operation.

## 11.6 Operator quick card

!! HINGLISH: PEM-07 se nut, stud aur standoff sheet mein dabaye jaate hain, painting se pehle. Hole ka size bilkul sahi hona chahiye, aur insertion wali side par hole ka burr ya chamfer mat karo. Shift start par plastic test piece se safety test karo. Nut ka head sheet ke barabar (flush) hona chahiye. Earth stud par masking cap lagao. Grinding karte waqt face shield, gloves, ear plug pehno aur guard kabhi mat hatao. Paint mein bhejne se pehle har part par inspector ka green tag zaroori hai.
