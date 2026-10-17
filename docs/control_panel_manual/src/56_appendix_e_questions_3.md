## E.10 Drawings, design and motor control

**Q121. What does the device tag Q11 normally mean on a drawing?**
A switching device in a power circuit, such as an MCCB or MPCB (letter Q, IEC 81346-2). K is a relay or contactor in a control circuit, F a protective device, X a terminal strip (Chapter 18.3).

**Q122. In which state are contacts drawn on a control diagram?**
De-energised and unoperated: no power, breakers off, push buttons not pressed (Chapter 18.8).

**Q123. What does a cross-reference "13-14 / 12.5" under a coil mean?**
The coil's NO contact 13-14 is used on sheet 12, column 5 (Chapter 18.5.1).

**Q124. Why must the star and delta contactors never close together?**
Closing both short-circuits the supply through the windings. They are interlocked electrically and, on larger starters, mechanically (Chapter 31.3.2).

**Q125. What is the dead time in a star-delta starter?**
A pause of 50 to 100 ms between opening the star contactor and closing the delta contactor, so that the arc in the star contactor is extinguished (Chapter 31.3.1).

**Q126. What is Type 2 coordination?**
A breaker-contactor-overload combination that remains fit for further use after a short circuit (light contact welding that can be separated is allowed). The combination must not be changed without design approval (Chapter 31.8).

**Q127. How is the direction of a reversing motor corrected at site?**
Swap two phases at the motor terminals, not inside the starter (Chapter 31.4).

**Q128. Must the emergency stop work if the PLC is in STOP?**
Yes. Emergency stop circuits are hard-wired through safety relays and remove power from the contactor coils directly (Chapter 31.7).

**Q129. Estimate the short-circuit current at the LT terminals of a 500 kVA, 433 V, 5 % transformer.**
500 / (1.732 x 0.433 x 0.05) = about 13.3 kA (Chapter 32.2).

**Q130. Where is the neutral-earth link made in a TN-C-S system?**
At one point only, normally the main LT panel, as shown on the drawing. A second link causes neutral current in the earth system (Chapter 32.7).

**Q131. What should production do if a delivered device differs from the BOM?**
Raise a design query on the job card and wait for a written answer; never substitute on their own (Chapter 32.9).

## E.11 Quality and process control

**Q132. When is a first-off required?**
After any set-up: new program, new tool, new material lot, start of shift, after a repair (Chapter 21.2).

**Q133. What are the steps for non-conforming product?**
Identify (red HOLD tag), segregate, report (NCR), decide (rework, repair, concession, scrap), act, find the cause, close (Chapter 21.3).

**Q134. How often are torque wrenches calibrated?**
Every 6 months (Chapter 21.5).

**Q135. What happens if an instrument is found out of tolerance at calibration?**
The quality manager checks which products were accepted with it since the last good calibration and decides whether they must be re-checked (Chapter 21.5).

**Q136. What is a golden sample?**
A reference part or photo kept by the quality department for comparing doubtful workmanship (Chapter 41.8).

**Q137. How long are test reports kept?**
10 years (Chapter 21.8).

**Q138. What is the maximum single DFT reading allowed below specification on indoor parts?**
No single reading may be below 50 microns (Chapter 13.8.1, 41.3).

**Q139. What is the copper balance limit of a busbar job?**
Copper issued must equal bars made plus offcuts plus scrap within 1 % (Chapter 14.9).

**Q140. How are remnant sheets handled?**
Remnants larger than 300 x 300 mm are marked with thickness and grade and returned to the remnant rack (Chapter 5.5).

## E.12 Supervision, site and compliance

**Q141. When must the plant head be informed of a critical machine breakdown?**
After 4 hours of downtime; maintenance supervisor and planning after 30 minutes; managers after 2 hours (Chapter 38.3.1).

**Q142. How is a quality problem handled by the supervisor?**
Stop the process, HOLD and segregate suspect parts, inform quality and raise an NCR, check how far back the problem goes, restart after correction and a new first-off (Chapter 38.4).

**Q143. What front clearance is needed in front of a draw-out ACB panel at site?**
At least 1500 mm so that the breaker can be withdrawn; 1000 mm in front of other panels (Chapter 22.5.1).

**Q144. What is checked 24 hours after energising a new panel at site?**
Thermal imaging of all joints and terminations under load; tighten (under LOTO) any joint more than 10 degrees C above similar joints (Chapter 22.5.5, 37.3).

**Q145. What must the service engineer do before working on equipment at a customer site?**
Work under the customer's permit and LOTO, with the customer's authorised person isolating and handing over the equipment, and apply a personal lock as well (Chapter 37.2).

**Q146. What does an expired lifting equipment certificate mean?**
The equipment must be taken out of use until it is examined (Chapter 39.2).

**Q147. How often are earth pits tested?**
Every 6 months, before and after the monsoon (Chapter 39.1; Chapter 23.3.3).

**Q148. When is a hot work permit required?**
For welding, grinding or cutting outside the welding area, especially near the paint shop (Chapter 3.11, B.20).

**Q149. What must be checked after replacing a light curtain?**
Same type and resolution, same configuration, alignment, test rod at top, middle and bottom at both edges, stopping time against the safety distance, record signed by the supervisor (SOP-08).

**Q150. What must be done before replacing a servo drive?**
Save its parameters if possible, apply LOTO, wait for and measure the DC bus discharge, replace with an identical type, reload parameters and reference the axis (Chapter 36.2.1).

**Q151. Why should a machine cabinet door not be left open to cool it?**
Dust and metal particles enter, and the cooling is designed for a closed cabinet; find the real cause of overheating (Chapter 36.1).

**Q152. How is a battery of a CNC memory changed?**
Normally with the control powered on, so that data is not lost, unless the maker says otherwise (Chapter 36.4.1).

**Q153. Where do intermittent encoder faults that appear only at certain axis positions usually come from?**
A cable breaking inside the drag chain (Chapter 36.3).

**Q154. Which RCD type suits circuits feeding three-phase drives?**
Type B, which detects smooth DC residual current (Chapter 19.2, 36.6).

**Q155. How often are CNC parameters backed up?**
After any change and at least every 6 months (Chapter 36.4).

**Q156. What is the capacitance acceptance for an APFC step?**
Within -5 % / +10 % of the nameplate (as per the capacitor maker); a capacitor below 90 % of rated value is replaced in service (Chapter 34.1.3, 19.15.3).

**Q157. How are PLC panel outputs protected from field short circuits stopping the CPU?**
Separate power supplies or electronic circuit protection channels for the PLC, field inputs and field outputs (Chapter 34.2.2).

**Q158. Where is a VFD braking resistor mounted?**
On top of the panel or outside, with a guard, and wired with high-temperature cable, because it gets very hot (Chapter 34.3.2).

**Q159. What does the hose test of an outdoor feeder pillar check?**
That no water enters the enclosure when sprayed from a nozzle at the specified pressure and time (Chapter 34.4.2).

**Q160. What must be true of identical withdrawable modules?**
They must be interchangeable: tested by swapping two identical modules (Chapter 34.5.2).
