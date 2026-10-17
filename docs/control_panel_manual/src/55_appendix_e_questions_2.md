## E.5 Busbars and wiring preparation

**Q56. What is the minimum inside bend radius for a copper busbar?**
1 x thickness for a flat bend and 1 x width for an edgewise bend. Aluminium needs 1.5 times these values (Chapter 14.7.2).

**Q57. How many holes and what size are used in a joint of a 100 mm wide busbar?**
Four holes of 14 mm in a square pattern, for M12 bolts. The overlap equals the bar width (Chapter 14.7.1).

**Q58. What is the flat length of a 10 x 60 mm copper L-bar with outside dimensions 300 and 200 mm?**
500 - 1.8 x 10 = 482 mm (Chapter 14.7.3).

**Q59. What colours are used for busbar sleeves?**
L1 red, L2 yellow, L3 blue, neutral black, PE green or green-yellow (Chapter 14.8.3).

**Q60. How are copper joint faces cleaned?**
Just before assembly, with a non-woven abrasive pad until bright, then wiped with isopropyl alcohol. Tin-plated bars are only wiped, never abraded (Chapter 14.8.1, 16.4.4).

**Q61. What does alarm BB-07 mean on BUS-10?**
Tool magazine index error: the magazine is not at the commanded tool, the sensor is dirty or the index pin is faulty. Re-reference the magazine, clean the sensor, check the pin and the tool number in the program (Chapter 14.11.1).

**Q62. What colour is a 1.5 mm2 bootlace ferrule in this plant?**
Black (0.5 white, 0.75 grey, 1.0 red, 1.5 black, 2.5 blue) (Chapter 15.2.3).

**Q63. What is the minimum pull-out force for a 2.5 mm2 crimp?**
230 N (Chapter 15.4.4).

**Q64. Why must the marker sleeve be fitted before crimping?**
After crimping, the sleeve cannot pass over the ferrule or lug (Chapter 15.6).

**Q65. What does a red crimp force monitor signal mean?**
The crimp is outside the force window: cut off the terminal and crimp again; check terminal, wire size, strip length and die (Chapter 15.4.3).

## E.6 Assembly and wiring

**Q66. What is the torque for an M12 busbar joint?**
75 Nm (Table 16-3). M10 is 44 Nm, M8 22 Nm, M16 160 Nm.

**Q67. Does Table 16-3 apply to breaker terminals?**
No. Device terminals are tightened to the device maker's torque, which always applies to the device (Chapter 16.4.4 note).

**Q68. What are the minimum clearances inside panels?**
Phase to phase 25 mm, phase to neutral 25 mm, phase or neutral to earth 20 mm, bare live parts to an opening door or cover 25 mm (Table 16-2).

**Q69. Why is a yellow paint mark put on busbar bolts?**
It shows the bolt was torqued and shows later if it has turned (torque seal) (Chapter 16.4.4).

**Q70. What size is the door earth connection?**
6 mm2 green-yellow wire or flexible braid, with ring lugs on studs (Chapter 16.3.3).

**Q71. What is the maximum diagonal difference allowed for a frame?**
2 mm (Chapter 16.3.1).

**Q72. What is the minimum wire size for CT secondary circuits?**
2.5 mm2 with ring lugs (Chapter 17.2.1, 17.5.3).

**Q73. What is the minimum control wire size for 230 V AC control circuits?**
1.5 mm2; 24 V DC PLC wiring 0.75 mm2 (Chapter 17.2.1).

**Q74. What cable size is used inside the panel after a 63 A breaker?**
16 mm2 copper minimum (Chapter 17.2.2).

**Q75. How full may a wire duct be?**
At most 70 % of its cross-section (Chapter 17.4).

**Q76. How many wires may go into one terminal clamp?**
One, unless the terminal is approved for two wires of the same size; then use a twin ferrule (Chapter 17.5.1).

**Q77. Where is the CT star point earthed?**
At one point only, at the CT test terminal block, with 2.5 mm2 green-yellow wire (Chapter 17.5.3).

**Q78. How is the shield of an analogue cable terminated?**
At one end only (normally the panel end) on the shield earth bar, unless the drawing says both ends (Chapter 17.5.5).

**Q79. What is "yellowing" the drawing?**
Marking each wire on the drawing with a highlighter as it is installed, so that missing wires are easy to see (Chapter 17.7).

## E.7 Components

**Q80. Which MCB curve is used for a control transformer?**
Curve D (10 to 20 x In), because of the transformer inrush current (Chapter 19.1.1, 19.11).

**Q81. What is the difference between Icu and Ics?**
Icu is the ultimate breaking capacity (the breaker may need replacement after breaking it); Ics is the service breaking capacity (the breaker remains in service) (Chapter 19.3.2).

**Q82. What do contact numbers 13-14 and 21-22 mean?**
13-14 is a normally open auxiliary contact; 21-22 is a normally closed auxiliary contact (Chapter 18.5.2).

**Q83. What do 95-96 and 97-98 on an overload relay mean?**
95-96 is the NC trip contact in the contactor coil circuit; 97-98 is the NO alarm contact (Chapter 18.5.2, 19.6).

**Q84. How is an overload relay set in a star-delta starter?**
At 0.58 x motor full load current, when the relay is in the winding (delta) circuit (Chapter 19.6.1; case study 28.14).

**Q85. What happens if a 24 V DC contactor coil is connected to 230 V AC?**
It burns at once. Always check the coil voltage against the BOM (Chapter 19.5; case study 28.6).

**Q86. Why must a CT secondary never be opened under load?**
A very high voltage appears across the open terminals, which can kill and destroys the CT. Short the secondary with the shorting link first (Chapter 17.5.3).

**Q87. How long must you wait after switching off a VFD before touching it?**
At least the time on the drive's warning label, then measure the DC bus: it must be below 50 V DC (Chapter 19.13.1).

**Q88. What causes a VFD overvoltage trip during stopping?**
Deceleration time too short for a high inertia load; the motor regenerates into the DC bus. Increase decel time or add a braking resistor (Chapter 19.13.4; case study 28.11).

**Q89. How long do APFC capacitors take to discharge?**
Discharge resistors bring them below 50 V within 1 to 3 minutes. Wait at least 5 minutes, check the voltage and short the terminals before touching (Chapter 19.15.3).

**Q90. Why does an APFC relay hunt or fail to switch?**
Most often because the CT is on the wrong phase or has the wrong polarity (Chapter 19.15.3).

**Q91. In which position can an ACB be closed and opened without connecting the main circuit?**
The test position: main circuit disconnected, control circuit connected (Chapter 19.4.1).

**Q92. When may an ACB be racked out?**
Only when it is open. Wear arc-rated face protection when racking in or out of a live cradle (Chapter 19.4.3).

**Q93. What does a PLC input LED that does not light when the push button is pressed tell you?**
The fault is in the field: device, wiring or 24 V supply, not in the PLC program (Chapter 19.12.3, 25.8).

**Q94. What airflow is needed to remove 600 W of losses with a 10 K rise?**
3.1 x 600 / 10 = 186 m3/h, at the actual filter pressure drop (Chapter 19.17).

## E.8 Testing

**Q95. In what order are routine tests done?**
Visual and mechanical inspection, earth continuity, IR before HV, dielectric test, IR after HV, wiring check, functional tests, protection tests, final inspection (Chapter 20.4).

**Q96. What is the acceptance value for earth continuity?**
0.1 ohm or less from each exposed conductive part to the main PE terminal, measured with 10 A DC (Chapter 20.6).

**Q97. What IR value is required on main circuits of a new panel?**
100 megohm or more at 1000 V DC, for 60 seconds (Chapter 20.7.2).

**Q98. What is the dielectric test voltage for a panel with Ui = 690 V?**
1890 V AC. Applied for at least 1 second by the standard; the plant applies 5 seconds, or 60 seconds if the customer requires (Chapter 20.8.1).

**Q99. Which devices are disconnected before IR and HV tests?**
Electronic meters, PLCs and I/O, drives, soft starters, SPDs, power supplies, protection relays (unless allowed), capacitors and electronic voltage indicators (Chapter 20.7.1).

**Q100. What is the most common reason for an HV flashover in a new panel?**
A clearance too small at a bolt end, a forgotten SPD or meter, or swarf (Chapter 20.14; case study 28.15).

**Q101. How is the RCCB trip tested?**
With an RCD tester: a 30 mA device must trip between 15 and 30 mA, within 300 ms at rated residual current (Chapter 19.2).

## E.9 Utilities and maintenance

**Q102. What are the load and unload pressures of COMP-15?**
Load at 7.0 bar, unload at 8.0 bar (Chapter 23.2.1).

**Q103. What does CP-01 mean on the compressor?**
High discharge temperature (trip at 110 degrees C): dirty cooler, low oil, high room temperature, stuck thermostatic valve, blocked oil filter (Chapter 23.2.5).

**Q104. How much air does a 3 mm leak waste?**
About 0.6 m3/min at 7 bar, roughly a quarter of the compressor's output (Chapter 23.2.6).

**Q105. What must be done after a power dip on a CNC machine?**
Re-reference the machine before restarting (Chapter 23.3.2).

**Q106. What are the daily checks of CRANE-16?**
Pendant and emergency stop, hook and latch, visible wire rope, upper limit switch, hoist brake, horn; recorded in the crane log book (Chapter 23.4.3).

**Q107. Who approves a work order?**
The maintenance manager. A work order is not started before approval; safety-related tasks are approved only by the maintenance manager (Chapter 24.4).

**Q108. What are the states of a work order?**
Draft, pending approval, approved, in progress, completed; it may also be rejected or cancelled (Chapter 24.4).

**Q109. What should be written when a PM step could not be done?**
Record it as "not done" with the reason, and raise a follow-up work order. Never tick it as done (Chapter 24.4).

**Q110. What fields does a breakdown record need?**
Asset code, date and time, reporter, symptom with alarm codes, repair times, downtime, cause, whether the root cause is known, action, parts used, technician (Chapter 24.5).

**Q111. What vibration level means "plan repair"?**
2.8 to 4.5 mm/s RMS (zone C) for small machines; above 4.5 mm/s damage is likely (Chapter 24.6.1).

**Q112. A connection is 25 degrees C hotter than similar connections. What action?**
Repair as soon as possible, within one week (Chapter 24.6.2).

**Q113. What is the normal hydraulic oil temperature?**
35 to 55 degrees C. Above 60 degrees C oil ages quickly and accuracy drops (Chapter 26.3.3).

**Q114. How should hydraulic oil be topped up?**
Through a filter cart with a 10 micron filter, never by pouring from an open drum (Chapter 26.3.2).

**Q115. What oil grade is used in the press brake?**
ISO VG 46 anti-wear hydraulic oil (HLP / HM 46); PEM-07 uses ISO VG 32 (Chapter 26.3.1).

**Q116. A pump makes a gravel-like noise. What should be checked?**
Cavitation or aeration: suction strainer, oil level, cold oil, air leaks on the suction side, foam in the tank (Chapter 26.6).

**Q117. What is the half-split method?**
Test in the middle of a chain of elements; the result tells which half has the fault. Repeat on the faulty half (Chapter 25.2).

**Q118. What is the minimum insulation resistance of a 415 V motor in service?**
10 megohm at 500 V DC (above 100 megohm for new motors) (Chapter 25.4.4).

**Q119. Three motor phase currents differ by 15 %. What does it mean?**
More than 10 % difference indicates supply unbalance, a high-resistance connection or a winding fault (Chapter 25.4.3).

**Q120. What lubricant code is used on machine guides with grease nipples?**
G2: lithium complex EP grease NLGI 2, green triangle mark (Chapter 29.2.1).

!! HINGLISH: Ye sawaal-jawaab training aur assessment ke liye hain. Har jawaab ke saath chapter number diya hai, poori jaankari wahan padho. Kisi jawaab mein shak ho to supervisor se poocho, andaaze se kaam mat karo.
