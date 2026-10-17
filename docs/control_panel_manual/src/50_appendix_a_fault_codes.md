# Appendix A. Alarm and Fault Code Master List

This appendix collects every alarm code used in the machine chapters, sorted by machine. The machine chapter gives the full troubleshooting table; this list is for quick look-up when an alarm appears on a screen. The codes are the plant's own codes for the demonstration factory (see the note at the start of the manual).


## Codes SH-xx: SHEAR-01

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| SH-01 | SHEAR-01 | Emergency stop pressed | One of the three emergency stops is pressed | Find and reset the button, press Control ON |
| SH-02 | SHEAR-01 | Rear light curtain interrupted | Person or object behind the machine; curtain misaligned | Clear the area; check alignment of transmitter and receiver |
| SH-03 | SHEAR-01 | Pump motor overload | Motor overload relay tripped | Check oil temperature and pressure; reset overload; if it trips again call electrical technician |
| SH-04 | SHEAR-01 | Oil temperature high | Oil above 65 degrees C | Stop work, let it cool, clean cooler, check cooler fan |
| SH-05 | SHEAR-01 | Oil level low | Float switch in tank | Find and repair the leak, top up with ISO VG 46 |
| SH-06 | SHEAR-01 | Return filter clogged | Clogging indicator | Replace filter element |
| SH-07 | SHEAR-01 | Back gauge not referenced | Power was switched off or encoder lost position | Run the reference (home) cycle |
| SH-08 | SHEAR-01 | Back gauge following error | Mechanical obstruction, ball screw dry, drive fault | Check for obstruction, lubricate, check servo drive alarm |
| SH-09 | SHEAR-01 | Back gauge limit switch | Gauge reached end of travel | Check program dimension; move gauge in manual mode |
| SH-10 | SHEAR-01 | Blade gap motor fault | Gap adjusting motor overload or encoder error | Check motor, limit switches, reference gap |
| SH-11 | SHEAR-01 | Rake angle not reached | Valve or sensor fault | Check rake angle sensor; check proportional valve |
| SH-12 | SHEAR-01 | Hold-down pressure not reached | Low pressure, hold-down leak | Check pressure switch, hold-down seals |
| SH-13 | SHEAR-01 | Beam not at top dead centre | Beam stopped in middle of stroke | Return beam in adjust mode, check TDC sensor |
| SH-14 | SHEAR-01 | Cylinder synchronisation error | Two cylinders not moving together | Stop; call maintenance; check synchronisation valve and cylinder seals |
| SH-15 | SHEAR-01 | CNC communication error | Cable, connector or controller fault | Switch off and on; check cables; call electrical technician |

## Codes TP-xx: PUNCH-02

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| TP-01 | PUNCH-02 | Emergency stop | Button pressed | Reset, restart hydraulics |
| TP-02 | PUNCH-02 | Light curtain interrupted | Person in machine zone | Leave the zone, reset |
| TP-03 | PUNCH-02 | Turret door open | Door not closed or switch fault | Close door; check switch |
| TP-04 | PUNCH-02 | Air pressure low | Below 5 bar | Check compressor, valve, leaks |
| TP-05 | PUNCH-02 | Clamp not closed | Clamp sensor | Check sheet position, clamp air |
| TP-06 | PUNCH-02 | Clamp dead zone violation | Hit inside clamp zone | Edit program; reposition |
| TP-07 | PUNCH-02 | X axis following error | Obstruction, heavy sheet, drive | Remove obstruction, check sheet weight, check drive |
| TP-08 | PUNCH-02 | Y axis following error | As TP-07 | As TP-07 |
| TP-09 | PUNCH-02 | Turret index error | Pin not engaged, sensor | Jog turret to reference, check pin and sensor |
| TP-10 | PUNCH-02 | Auto-index position error | Index motor or encoder | Reference C-axis; check drive |
| TP-11 | PUNCH-02 | Ram overload | Force above limit | Check tool, thickness, material in program |
| TP-12 | PUNCH-02 | Ram not at top | Ram stopped mid-stroke (punch stuck) | Lift ram in manual; free the punch under LOTO |
| TP-13 | PUNCH-02 | Hydraulic oil temperature high | Cooler, heavy nibbling | Allow cooling, clean cooler |
| TP-14 | PUNCH-02 | Hydraulic filter clogged | Filter dirty | Replace element |
| TP-15 | PUNCH-02 | Lubrication level low | Lube tank empty | Fill with recommended oil |
| TP-16 | PUNCH-02 | Software limit X / Y | Program outside travel | Check program origin and sheet size |
| TP-17 | PUNCH-02 | Tool not in tool table | Program calls missing tool | Load tool and update table |
| TP-18 | PUNCH-02 | Slug detected / slug sensor | Slug lying on die | Stop; clean die and check slug chute |

## Codes LS-xx: LASER-03

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| LS-01 | LASER-03 | Emergency stop | Button pressed | Reset |
| LS-02 | LASER-03 | Cabin door open | Door interlock | Close door; check switch |
| LS-03 | LASER-03 | Chiller not ready | Water temperature out of range or flow low | Wait for temperature; check water level, filter, pump |
| LS-04 | LASER-03 | Chiller flow alarm | Blocked filter, low level | Clean filter, top up |
| LS-05 | LASER-03 | Laser source fault | Internal source alarm | Note the source code, switch off and on once; call service if repeated |
| LS-06 | LASER-03 | Back-reflection warning | Reflective material, wrong parameters | Check material (brass, copper need special parameters), check focus |
| LS-07 | LASER-03 | Protective window temperature high | Dirty or damaged window | Clean or replace window |
| LS-08 | LASER-03 | Height sensor collision | Nozzle touched sheet | Check nozzle and ceramic; recalibrate |
| LS-09 | LASER-03 | Height sensor calibration failed | Dirty nozzle, loose ceramic, earthing | Clean, tighten, check slats earthing |
| LS-10 | LASER-03 | Gas pressure low | Cylinder empty, regulator, leak | Change cylinder bank; check regulator |
| LS-11 | LASER-03 | Fume extractor not running | Extractor off or overload | Switch on extractor; check overload and filter |
| LS-12 | LASER-03 | Pallet exchange error | Pallet not in position, sensor, chain | Check sensors, obstruction |
| LS-13 | LASER-03 | X / Y / Z following error | Obstruction, drive fault | Remove obstruction; check drive alarms |
| LS-14 | LASER-03 | Focus motor error | Auto-focus drive | Reference focus; call service |
| LS-15 | LASER-03 | Cabinet temperature high | Cabinet AC or fan failed | Check cabinet cooling; clean filters |

## Codes PB-xx: BRAKE-04

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| PB-01 | BRAKE-04 | Emergency stop | Button pressed | Reset |
| PB-02 | BRAKE-04 | Laser guard interrupted | Object in beam during fast approach | Remove obstruction; check guard alignment |
| PB-03 | BRAKE-04 | Laser guard test not done | Daily test not performed after power on | Perform test |
| PB-04 | BRAKE-04 | Rear light curtain interrupted | Person behind machine | Clear area, reset |
| PB-05 | BRAKE-04 | Side guard open | Guard door open | Close; check switch |
| PB-06 | BRAKE-04 | Y1 / Y2 synchronisation error | Difference between cylinders above limit | Stop; check scale, servo valve; call maintenance |
| PB-07 | BRAKE-04 | Y axis linear scale error | Dirty or damaged scale, cable | Clean scale, check cable |
| PB-08 | BRAKE-04 | Hydraulic oil temperature high | Cooler, heavy use | Cool down; clean cooler |
| PB-09 | BRAKE-04 | Hydraulic pressure too low | Pump, relief valve, leak | Check pressure; call maintenance |
| PB-10 | BRAKE-04 | Hydraulic filter clogged | Filter dirty | Replace element |
| PB-11 | BRAKE-04 | Tool clamp not closed | Clamp pressure, sensor | Clamp tools; check pressure |
| PB-12 | BRAKE-04 | Back gauge X axis fault | Drive, encoder, obstruction | Remove obstruction; reset drive; check encoder |
| PB-13 | BRAKE-04 | Back gauge R axis fault | As PB-12 | As PB-12 |
| PB-14 | BRAKE-04 | Crowning axis fault | Motor, sensor | Reference crowning; check motor |
| PB-15 | BRAKE-04 | Force limit exceeded | Bending force above programmed limit | Check material, V-die, program |
| PB-16 | BRAKE-04 | Collision warning | Sequence collides with tool or machine | Change sequence or tools |

## Codes SW-xx: WELD-05

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| SW-01 | WELD-05 | Cooling water flow low | - | Open water, clean strainer, check drain |
| SW-02 | WELD-05 | Transformer over-temperature | - | Wait; check water flow; reduce duty cycle |
| SW-03 | WELD-05 | Air pressure low | - | Check air supply and regulator |
| SW-04 | WELD-05 | No current detected | - | Check secondary connections, electrodes, part contact |
| SW-05 | WELD-05 | Current outside limit | - | Check programme, tips, part; dress tips |
| SW-06 | WELD-05 | Thyristor fault | - | Call electrical technician |
| SW-07 | WELD-05 | Tip dressing counter reached | - | Dress tips, reset counter |

## Codes MG-xx: WELD-06

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| MG-01 | WELD-06 | Over-temperature | - | Allow cooling; check fan and inlet |
| MG-02 | WELD-06 | Supply phase missing | - | Check supply fuses and isolator |
| MG-03 | WELD-06 | Wire feed motor overload | - | Check liner and drive rolls |
| MG-04 | WELD-06 | Gas flow low (with sensor) | - | Check cylinder and hose |
| MG-05 | WELD-06 | Output short circuit at start | - | Check torch for spatter bridge between tip and nozzle |

## Codes PM-xx: PEM-07

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| PM-01 | PEM-07 | Emergency stop | - | Reset |
| PM-02 | PEM-07 | No contact (safety) | - | Check placement and tooling; remove non-conductive objects |
| PM-03 | PEM-07 | Force not reached | - | Check oil level, pump, pressure transducer |
| PM-04 | PEM-07 | Oil temperature high | - | Allow cooling, check cooler fan |
| PM-05 | PEM-07 | Feeder jam | - | Clear feeder track under LOTO of the feeder air |

## Codes PT-xx: PTL-08

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| PT-01 | PTL-08 | Emergency stop | - | Find and reset |
| PT-02 | PTL-08 | Tank level low (stage number shown) | - | Top up; check for leak; pump stops to protect itself |
| PT-03 | PTL-08 | Tank temperature low | - | Check heater, valve, heat exchanger |
| PT-04 | PTL-08 | Tank temperature high | - | Check control valve; stop heating |
| PT-05 | PTL-08 | Pump motor overload | - | Check pump for blockage; reset; call electrician if repeated |
| PT-06 | PTL-08 | Spray pressure low | - | Clean strainer and nozzles; check pump |
| PT-07 | PTL-08 | Burner lockout (hot water generator) | - | Trained person only: check gas pressure, reset once; call burner service if repeated |
| PT-08 | PTL-08 | Oven burner lockout | - | As PT-07 |
| PT-09 | PTL-08 | Oven temperature out of range | - | Check burner, fan, thermocouple |
| PT-10 | PTL-08 | DM water conductivity high | - | Regenerate or replace resin |
| PT-11 | PTL-08 | Exhaust fan failure | - | Stop line; check fan |
| PT-12 | PTL-08 | Conveyor stopped | - | Check conveyor drive and pull cords (common alarm with PCL-09) |

## Codes PC-xx: PCL-09

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| PC-01 | PCL-09 | Emergency stop | - | Reset |
| PC-02 | PCL-09 | Flame detected | - | All guns and fan stopped automatically; check booth; follow fire procedure; investigate cause before restart |
| PC-03 | PCL-09 | Recovery fan off / airflow low | - | Guns blocked; check fan and filters |
| PC-04 | PCL-09 | Filter differential pressure high | - | Pulse clean; replace cartridges if pressure stays high |
| PC-05 | PCL-09 | Gun high voltage fault | - | Check gun cable and electrode; replace cascade if faulty |
| PC-06 | PCL-09 | Hopper level low | - | Fill powder |
| PC-07 | PCL-09 | Fluidising air pressure low | - | Check air supply and regulator |
| PC-08 | PCL-09 | Reciprocator fault | - | Check drive, belt, limit switches |
| PC-09 | PCL-09 | Oven burner lockout | - | Trained person only; check gas; reset once; call burner service if repeated |
| PC-10 | PCL-09 | Oven temperature out of range | - | Check burner, circulation fan, thermocouple; hold parts until temperature is in range |
| PC-11 | PCL-09 | Oven circulation fan failure | - | Burner stops automatically; check fan motor and belt |
| PC-12 | PCL-09 | Conveyor stopped | - | Check drive and pull cords; remove parts from the oven if the stop is longer than 10 minutes |

## Codes BB-xx: BUS-10

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| BB-01 | BUS-10 | Emergency stop | Button pressed | Reset |
| BB-02 | BUS-10 | Two-hand control fault | One button pressed alone or held longer than 0.5 s before the other | Release both, press together |
| BB-03 | BUS-10 | Hydraulic pressure low | Pump, relief valve, oil level | Check level, pressure; call maintenance |
| BB-04 | BUS-10 | Oil temperature high | Cooler, continuous heavy punching | Allow cooling; clean cooler |
| BB-05 | BUS-10 | Filter clogged | Return filter | Replace element |
| BB-06 | BUS-10 | Gripper not closed | Bar missing or gripper pressure low | Check bar and gripper air / hydraulic pressure |
| BB-07 | BUS-10 | Tool magazine index error | Magazine not at commanded tool, sensor dirty, index pin | Re-reference magazine; clean sensor; check index pin; check tool number in program |
| BB-08 | BUS-10 | Punch not at top | Punch stuck in bar | Lift in manual mode; under LOTO free the bar and check the punch |
| BB-09 | BUS-10 | X axis following error | Obstruction, heavy bar, drive fault | Support bar on rollers; check drive |
| BB-10 | BUS-10 | X axis limit | Bar too long for program without repositioning | Check program; use repositioning |
| BB-11 | BUS-10 | Bending angle not reached | Pressure, encoder, bar harder than expected | Check pressure; check encoder; increase angle correction |
| BB-12 | BUS-10 | Bending back gauge error | Drive or encoder | Re-reference; check drive |
| BB-13 | BUS-10 | Shear not at top | Shear blade stuck | Retract in manual; check blade |
| BB-14 | BUS-10 | Program collision warning | Bent bar collides with machine | Change bend sequence or use manual bending |

## Codes WR-xx: WIRE-11

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| WR-01 | WIRE-11 | Wire end / reel empty | - | Load new reel |
| WR-02 | WIRE-11 | Wire slip at feeder | - | Clean belts; increase belt pressure; check wire size setting |
| WR-03 | WIRE-11 | Blade motor error | - | Check for jammed slug; reference blades |
| WR-04 | WIRE-11 | Cover open | - | Close cover |
| WR-05 | WIRE-11 | Strip not complete (sensor) | - | Check blade depth and strip length |

## Codes CR-xx: CRIMP-12

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| CR-01 | CRIMP-12 | Crimp force outside window | - | Check terminal, wire size, strip length, die; re-teach reference curve after die change |
| CR-02 | CRIMP-12 | Air pressure low | - | Check supply |
| CR-03 | CRIMP-12 | Stroke incomplete | - | Check for obstruction; check pedal |
| CR-04 | CRIMP-12 | Die not identified | - | Fit the correct die with its coding pin |

## Codes MK-xx: MARK-13

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| MK-01 | MARK-13 | Ribbon end | - | Replace ribbon |
| MK-02 | MARK-13 | Sleeve end or jam | - | Reload; clear jam |
| MK-03 | MARK-13 | Print head temperature | - | Wait; check fan |

## Codes CP-xx: COMP-15

| Code | Machine | Message | Cause | Action |
|---|---|---|---|---|
| CP-01 | COMP-15 | High discharge temperature (trip at 110 degrees C) | Dirty cooler, low oil, high room temperature, thermostatic valve stuck, blocked oil filter | Clean cooler, check oil level, ventilate room, check valve, replace filter |
| CP-02 | COMP-15 | Motor overload | Low voltage, high pressure, bearing problem | Check supply voltage, pressure settings, bearings |
| CP-03 | COMP-15 | Phase failure / reversal | Supply fault | Check incoming supply; never run reversed (rotor damage) |
| CP-04 | COMP-15 | Separator differential pressure high | Separator element blocked | Replace separator |
| CP-05 | COMP-15 | Pressure sensor fault | Sensor or cable | Check sensor |

!! NOTE: An alarm that comes back after reset is a symptom, not the fault. Record every repeated alarm in the breakdown record with the asset code and the code shown (for example "BRAKE-04, PB-12"), so that repeated causes can be found in the history.
