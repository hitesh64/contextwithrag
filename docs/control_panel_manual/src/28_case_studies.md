# 28. Breakdown Case Studies

The cases below are written as training examples for the demonstration factory. They are invented, but each one is typical of what happens in a panel factory. Each case shows the symptom as the operator described it, how the technician found the cause, and what was changed so that it does not happen again. Read them as examples of the method in Chapter 25.

## 28.1 Case 1: BRAKE-04 angles open in the middle of long parts

**Symptom**: side covers of 1.6 mm CRCA, 2000 mm long, were bent at 90 degrees at the ends but 92 degrees in the middle. The problem started after a new lot of sheet.

**Investigation**: the operator had corrected the angle at the ends with the CNC angle correction, which made the ends right but left the middle open. The technician checked the crowning value in the program: it had been set for 1.2 mm material in an old program copied for the new job. Material thickness of the new lot measured 1.62 mm, within tolerance.

**Root cause**: wrong crowning value in a copied program; the beam deflection at the higher force was not compensated.

**Action**: the crowning was recalculated by the CNC for the correct material and thickness; the test bend gave 90 +/- 0.3 degrees along the full length.

**Prevention**: programs are no longer copied between materials; the CNC material and thickness field is checked at first-off. Added to the BRAKE-04 first-off check: "measure angle at both ends and in the middle of parts longer than 1000 mm".

## 28.2 Case 2: LASER-03 dross on stainless steel after nitrogen tank refill

**Symptom**: heavy dross under the cut on 1.5 mm stainless steel and a yellow edge, from the morning after the nitrogen tank was refilled.

**Investigation**: parameters and nozzle were checked and correct; protective window clean. The cut was good when the gas was switched to the cylinder bank. The supplier's delivery note showed nitrogen of 99.5 % purity instead of 99.99 %.

**Root cause**: wrong nitrogen purity delivered; oxygen content in the assist gas oxidised the cut.

**Action**: the supplier replaced the gas. Parts cut during the morning were inspected; 12 parts with discoloured edges on visible faces were re-cut.

**Prevention**: the store checks purity on the delivery note before the tank is filled; the specification "99.99 % minimum" was added to the purchase order.

## 28.3 Case 3: SHEAR-01 stops in the middle of the cut, alarm SH-12

**Symptom**: on 3 mm sheet, the blade sometimes did not start and alarm SH-12 (hold-down pressure not reached) appeared. Resetting and retrying worked.

**Investigation**: the pressure gauge showed that the hold-down pressure built up slowly. Oil level and temperature were normal. With a test gauge on the hold-down circuit, one hold-down was found leaking oil past its seal (oil wetness under the pad).

**Root cause**: worn seal in one of the 14 hold-down cylinders.

**Action**: seal kit replaced (from stock), pressure built up normally, alarm stopped.

**Prevention**: "check hold-down pads for wear and oil leaks" was already a weekly task but had been ticked without looking. The supervisor re-trained the operators on the weekly checks, and photos of a good and a leaking hold-down were added to the check sheet.

## 28.4 Case 4: Earth continuity failure on doors of three panels

**Symptom**: at testing, the earth continuity of several doors of three different panels read 1.5 to 4 ohm instead of below 0.1 ohm.

**Investigation**: all failed doors had their earth braid correctly fitted, but the earth studs were coated with powder. The masking caps were missing on all of them. Doors from the same paint batch had the same problem.

**Root cause**: a new lot of silicone masking caps was slightly oversized and fell off the studs in the pre-treatment spray.

**Action**: the studs of the affected doors were cleaned to bare metal under the nut area, and the earth braids refitted with serrated washers; all doors retested.

**Prevention**: masking cap fit is now checked at goods receipt; the paint unloading operator checks every earth stud for bare metal before unloading (see also the five whys example in Chapter 21.4.1).

## 28.5 Case 5: Hot busbar joint found at site

**Symptom**: the customer's thermal survey, two months after commissioning, showed one busbar joint of a 1600 A PCC at 92 degrees C, while other joints were at 55 degrees C.

**Investigation**: the factory's torque record of the job showed all joints signed. During the shutdown visit the joint was opened: the bolts were tight, but the contact faces of one link were dull and partly painted with overspray from site touch-up painting.

**Root cause**: the link had been removed for transport and refitted at site by the customer's contractor, who did not clean the faces and had touched up paint nearby without masking.

**Action**: faces cleaned, link refitted with new washers, torqued to 75 Nm (M12) per Table 16-3 and marked. Re-check under load: 57 degrees C.

**Prevention**: the shipping section links are now delivered in a bag with a printed instruction card "clean faces, torque to Table 16-3, mark"; the installation instructions were updated (Chapter 22.5.2).

## 28.6 Case 6: Contactor coils burning in a new MCC at testing

**Symptom**: on the functional test of a new MCC, three contactors buzzed loudly and their coils burned within a minute.

**Investigation**: the control supply was 110 V AC from the control transformer. The three contactors had 24 V AC coils. The BOM specified 110 V AC coils; the store had issued contactors of the same type with the wrong coil voltage.

**Root cause**: issue of wrong coil voltage variant; the coil voltage was not checked at assembly.

**Action**: contactors replaced; all other contactors of the panel checked.

**Prevention**: the assembly inspection checklist now has a separate line "coil voltage of each contactor and relay as per BOM"; the store keeps coil voltage variants in separately labelled bins.

## 28.7 Case 7: PUNCH-02 holes out of position by 0.5 mm on some sheets

**Symptom**: some mounting plates had a row of holes shifted by about 0.5 mm in Y; other sheets from the same program were good.

**Investigation**: the shift happened only on heavy 2.5 mm GI sheets after the sheet was repositioned. The clamp jaws were worn and smooth; the clamp pressure was correct.

**Root cause**: worn clamp jaws let the heavy sheet slip during fast Y movements.

**Action**: clamp jaws replaced; axis acceleration for sheets above 100 kg reduced in the machine parameter (by the service engineer).

**Prevention**: clamp jaw teeth inspection added to the weekly check with a reference photo.

## 28.8 Case 8: Powder coating peeling on base frames

**Symptom**: powder on base frames (5 mm) chipped off easily when the panels were lifted with slings; cross-cut test on frames failed (class 4).

**Investigation**: the solvent rub test failed (film softened). The oven profile with a thermocouple on a base frame showed that the metal reached 180 degrees C for only 4 minutes at the normal conveyor speed.

**Root cause**: under-cure of thick parts run with thin parts at 1.5 m/min.

**Action**: affected frames re-baked in batch mode (passed the rub test). Base frames are now run in a separate batch at 1.0 m/min (Chapter 13.7.4).

**Prevention**: monthly oven profile includes a 5 mm part; planning schedules heavy parts as a separate batch.

## 28.9 Case 9: COMP-15 trips on high temperature every afternoon

**Symptom**: the compressor tripped with CP-01 (high discharge temperature) between 14:00 and 16:00 on hot days.

**Investigation**: discharge temperature in the morning 88 degrees C, rising to 108 degrees C in the afternoon. The cooler fins were clean. The compressor room temperature was 46 degrees C: the hot cooling air from the compressor was being drawn back into the room because the exhaust duct had been disconnected during roof work.

**Root cause**: hot air recirculation in the compressor room.

**Action**: exhaust duct reconnected; room temperature 36 degrees C; discharge temperature 86 degrees C in the afternoon.

**Prevention**: "compressor room temperature below 40 degrees C" added to the daily check; roof work permits now include a check of the ventilation ducts.

## 28.10 Case 10: WELD-05 weak spot welds after electrode change

**Symptom**: door corners cracked at the spot welds during bending checks; the peel test showed small nuggets (3 mm instead of at least 5.1 mm for 1.6 mm sheet).

**Investigation**: the electrodes had been changed the previous day. The new caps had a face diameter of 8 mm instead of 6.3 mm (wrong cap type for this sheet), reducing current density.

**Root cause**: wrong electrode cap type fitted.

**Action**: caps replaced with the correct type (dressed to 6.3 mm face); peel test passed. Doors welded since the change were tested by sample peel tests on scrap and the doors were re-welded with additional spots where required.

**Prevention**: cap types are now stored with labels showing the sheet thickness range; a peel test after every cap change is mandatory (Chapter 10.2.7).

## 28.11 Case 11: VFD feeder trips with overvoltage during stopping

**Symptom**: during the functional test of a conveyor VFD panel with a test motor and flywheel, the drive tripped with "DC bus overvoltage" every time the stop button was pressed.

**Investigation**: deceleration time was set to 2 seconds, while the load had high inertia. During braking the motor acted as a generator and raised the DC bus voltage.

**Root cause**: deceleration time too short for the load; no braking resistor in this design.

**Action**: deceleration time set to 10 seconds as per the customer's process requirement; no more trips. The design engineer confirmed that a braking resistor is not needed for the actual conveyor.

**Prevention**: VFD parameter sheets of each job now include accel / decel times agreed with the customer.

## 28.12 Case 12: BUS-10 bars cracked at bends

**Symptom**: three 10 x 80 mm copper bars cracked on the outside of the 90 degree flat bends.

**Investigation**: the bend radius in the program was 6 mm, below the minimum of 1 x thickness (10 mm). The design drawing showed 10 mm; the radius had been changed in the CNC program by mistake while editing a different bar.

**Root cause**: program editing error; no check of bend radius at first-off.

**Action**: bars scrapped (copper recovered in the locked scrap bin); program corrected; new bars made and checked.

**Prevention**: inspection of the outside of every bend before sleeving was made explicit in the busbar checklist (Chapter 14.7.2); CNC program changes require supervisor approval.

## 28.13 Case 13: PCL-09 flame detector shut down the booth

**Symptom**: the booth stopped suddenly with alarm PC-02 (flame detected). No fire was visible.

**Investigation**: the event log showed a spark detection, not a flame, from a manual gun station. The manual operator had changed into new shoes that were not antistatic; the operator's body charged up and sparked to an earthed part.

**Root cause**: operator not earthed (non-antistatic footwear).

**Action**: operator issued antistatic shoes; booth cleaned and restarted.

**Prevention**: daily check of footwear for booth operators; antistatic footwear tester installed at the booth entrance.

## 28.14 Case 14: Motor feeder overload trips at 50 % load

**Symptom**: at site, a 30 kW pump on a star-delta starter tripped on overload after 20 minutes, while the pump current measured by a clamp meter on the incoming cable was only 30 A (motor FLC 55 A).

**Investigation**: the overload relay was in the winding (delta) circuit, where the current is 0.58 x line current. It had been set at 18 A (instead of 0.58 x 55 = 32 A), because the setting sheet had been read for a different motor.

**Root cause**: wrong overload setting.

**Action**: relay set to 32 A; no more trips.

**Prevention**: the testing engineer checks overload settings against the motor list during functional tests and writes the setting in the test report.

## 28.15 Case 15: TEST-14 HV tester trips at 1200 V on a new MCC

**Symptom**: during the dielectric test of a new MCC, the HV tester tripped at about 1200 V on the "L1 to rest" combination. IR before HV had been 650 megohm on all combinations.

**Investigation**: the panel was divided into sections and tested section by section; the trip occurred in section 3. Visual inspection with a torch found a bolt of a dropper support whose end was 9 mm from the L1 dropper (requirement 20 mm to earth). A longer bolt had been used because the correct length was out of stock.

**Root cause**: wrong bolt length reduced clearance; insulation by air was not enough at the test voltage.

**Action**: bolt replaced with the correct length; clearance 24 mm; HV test passed at 1890 V; IR after HV 640 megohm.

**Prevention**: bolt lengths are listed on the busbar drawing; a stock-out of a bolt is reported to the supervisor, not solved by substitution. Clearance check at bolt ends was added to assembly inspection.

## 28.16 Lessons from the cases

| Lesson | Cases |
|---|---|
| Check the first part properly, including all critical points | 1, 7, 12 |
| Do the daily and weekly checks honestly | 3, 9 |
| Material and consumables can be wrong even from a regular supplier: check at receipt | 2, 4, 6, 10 |
| Follow the documented values: torque, clearance, bolt length, settings | 5, 14, 15 |
| Thick and thin parts behave differently in heat processes | 8 |
| Safety devices stop machines for a reason: find the cause | 13 |
| Agree process parameters with the customer and record them | 11 |

!! HINGLISH: In case studies se seekho: pehla piece har jagah naapo, roz aur hafte ki check sheet imaandari se bharo, naya material aur consumable aate hi check karo, aur drawing ki value (torque, doori, bolt length, setting) kabhi apne man se mat badlo. Har breakdown ka asli kaaran dhundh ke likho.
