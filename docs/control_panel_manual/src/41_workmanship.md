# 41. Workmanship Standards and Acceptance Criteria

This chapter collects in one place the acceptance criteria that inspectors use to decide whether work is good. Where a criterion is also stated in a process chapter, the value is the same. A customer specification may set stricter criteria; they are written on the job card.

## 41.1 Sheet metal parts

| Feature | Acceptable | Not acceptable |
|---|---|---|
| Linear dimensions up to 1000 mm | +/- 1 mm | Outside tolerance |
| Linear dimensions above 1000 mm | +/- 2 mm | Outside tolerance |
| Hole positions on mounting plates | +/- 0.5 mm | Outside tolerance; device does not fit |
| Bend angles | +/- 0.5 degrees (process) / +/- 1 degree (assembly function) | Larger deviation |
| Diagonals of doors | Difference up to 1 mm | Above 1 mm |
| Diagonals of frames | Difference up to 1.5 mm (welded part), 2 mm (assembled structure) | Above |
| Flatness of doors and covers | Up to 2 mm over the length | Above 2 mm or visible waviness |
| Burrs | None that can be felt with a gloved hand; below 10 % of thickness at process | Sharp edges |
| Tool marks | Light marks not visible after painting | Marks that show through paint on visible faces |
| Scratches before painting | Light, not felt by fingernail | Deep scratches on visible faces |
| Laser cut edges | Light dross removable by hand scraper; pierce marks outside parts | Heavy dross; burnt corners on visible parts |

## 41.2 Welds

| Feature | Acceptable | Not acceptable |
|---|---|---|
| Spot welds | Round marks, regular pitch per drawing, indentation below 20 % of thickness | Cracks, burn-through, expulsion craters on visible faces, missing spots |
| Spot weld strength | Peel test button at least the minimum nugget diameter | Interface failure, small nugget |
| MIG fillet welds | Full length, leg size per drawing (fillet gauge), smooth transition | Cracks, porosity visible, undercut deeper than 0.5 mm, lack of fusion, missing length |
| Lifting brackets | 100 % inspected, full length, correct leg size | Any defect: repair and re-inspect |
| Spatter | None on visible faces and on threads | Spatter remaining |
| Ground welds on visible faces | Flush, blended, no dip | Dip or thinning of sheet |

## 41.3 Paint

| Feature | Acceptable | Not acceptable |
|---|---|---|
| DFT indoor | 60 to 80 microns average; no reading below 50 | Below 50 microns anywhere |
| DFT outdoor | 80 to 100 microns average; no reading below 65 | Below 65 microns |
| Colour | Matches master plate in daylight | Visible difference between parts of the same panel |
| Texture | Uniform | Patches of different texture |
| Defects on visible faces (doors, front frames, side covers) viewed at 1 m | None | Runs, sags, pinholes, craters, inclusions, bare spots |
| Defects on non-visible faces (inside, back of mounting plates) | Small isolated inclusions or texture variation | Bare spots, rust, poor adhesion |
| Adhesion | Cross-cut class 0 or 1 | Class 2 or worse |
| Cure | Solvent rub: slight dulling only | Softening or removal |
| Earth points | Bare metal | Paint on earth contact areas |
| Touch-up | Same colour, small area, blended | Visible patches on front faces (recoat the part instead) |

## 41.4 Busbars

| Feature | Acceptable | Not acceptable |
|---|---|---|
| Length | +/- 1 mm | Outside |
| Hole positions | +/- 0.5 mm | Outside; bolts must be forced |
| Bend angle | +/- 1 degree | Outside; bar must be forced into supports |
| Bends | Smooth, no cracks, radius at least minimum | Any crack or crease |
| Surface | Clean, bright; light handling marks | Deep scratches, dents, oxidised patches, oil |
| Burrs and corners | Removed; corners rounded 2 to 3 mm | Sharp burrs |
| Sleeve | Tight, correct colour, no air, clean cut | Splits, burns, loose, wrong colour |
| Joint | Torqued, marked, clean faces | Any unmarked bolt; dirty faces |

## 41.5 Wiring

| Feature | Acceptable | Not acceptable |
|---|---|---|
| Routing | In ducts, bundles neatly tied, no crossing over devices | Wires across devices, loose loops |
| Duct fill | Up to 70 % | Cover cannot close without force |
| Ferrules | Correct size and colour, fully inserted | Wrong size, strands outside, bare copper visible |
| Wire numbers | Both ends, readable from the front | Missing, wrong or unreadable |
| Crimps | Strands visible at barrel end, insulation 0.5 to 1 mm away, pull test met | Strands outside barrel, insulation in crimp, cracked terminal |
| Terminations | One wire per clamp (or twin ferrule), torque per maker, tug test passed | Two wires in one ferrule, loose wire |
| Bend radius | At least 4 x outside diameter (small wires), 6 x for large cables | Kinks |
| Door loops | Protected, fixed both ends, free movement | Pinched or stretched when door opens |
| Insulation | Undamaged | Cuts, nicks, heat damage |
| Cleanliness | No offcuts, slugs or cable tie ends | Debris inside the panel |

## 41.6 Assembly

| Feature | Acceptable | Not acceptable |
|---|---|---|
| Door gaps | Even, 2 to 3 mm | Uneven gaps causing visible misalignment or poor sealing |
| Door closing | Closes and locks without force; gasket compressed 25 to 35 % | Needs force; gasket not touching |
| Earth straps | All present, on studs with serrated washers | Missing or on paint |
| Clearances | Table 16-2 values or more | Less, at any point including bolt ends |
| Devices | As per BOM, mounted per maker | Different type, wrong coil voltage, missing clearances |
| Labels | Correct text, straight, fixed | Wrong text, missing, crooked |
| Interlocks | All work as designed | Any not working |

## 41.7 Electrical test acceptance (summary)

| Test | Acceptance |
|---|---|
| Earth continuity | 0.1 ohm or less per point |
| IR main circuits (1000 V DC) | 100 megohm or more |
| IR control circuits (500 V DC) | 50 megohm or more |
| IR 24 V DC circuits (250 V DC) | 10 megohm or more |
| Dielectric test | No breakdown at Table 8 voltage (e.g. 1890 V for Ui 690 V) |
| Wiring | 100 % as per drawing |
| Functions | All as per drawing |
| Protection | Settings as per chart; trip tests within curves |

## 41.8 When in doubt

If a feature is not covered by this chapter or the drawing, the inspector compares it with the "golden sample" (reference part or reference photo kept by the quality department) and, if still in doubt, asks the quality manager. Doubtful parts are never passed "to save time".

!! HINGLISH: Ye chapter batata hai kaunsa kaam "OK" hai aur kaunsa "Not OK": sheet ke naap, weld, paint (DFT 60-80 micron), busbar, wiring (ferrule, number, crimp), assembly aur testing. Shak ho to golden sample se milao ya quality manager se poocho. Jaldi ke chakkar mein shak wala part pass mat karo.
