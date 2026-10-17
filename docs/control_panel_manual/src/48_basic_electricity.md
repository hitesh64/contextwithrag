# 48. Basic Electricity for Operators and Trainees

This chapter explains the basic electrical ideas behind the work in a panel factory, in simple terms, for operators, helpers and trainees who have not studied electrical engineering.

## 48.1 Voltage, current and resistance

- **Voltage (V, volts)** is the electrical "pressure" that pushes current. Like water pressure in a pipe. The plant supply is 415 V between phases and 230 V between a phase and neutral.
- **Current (I, amperes)** is the flow of electricity. Like the flow of water. A 5.5 kW motor takes about 11 A.
- **Resistance (R, ohms)** opposes the flow. Thin and long wires have more resistance; thick and short wires less.
- **Ohm's law**: V = I x R. If the voltage is fixed, a lower resistance means a higher current. A short circuit is a path with almost no resistance, so the current becomes enormous until a breaker or fuse opens.

## 48.2 Power and energy

- **Power (W, watts)** is the rate of using energy. For simple loads, power = voltage x current. A 2 kW heater at 230 V takes about 8.7 A.
- **Energy (kWh, units)** is power x time. A 15 kW compressor running loaded for 8 hours uses about 120 kWh.
- The electricity bill is based on energy (kWh or kVAh) and on the maximum demand (kVA).

## 48.3 AC and DC

- **DC (direct current)** flows in one direction: batteries, 24 V DC power supplies for PLCs and sensors.
- **AC (alternating current)** changes direction 50 times per second (50 Hz) in India: the mains supply.
- Motors, heaters and lighting use AC; electronics use DC made from AC by power supplies.

## 48.4 Three-phase supply

Industrial supply has three phases (L1, L2, L3, also called R, Y, B), each an AC voltage shifted in time from the others. Three-phase power runs motors smoothly and carries more power with less copper.

| Measurement | Value in this plant |
|---|---|
| Between two phases (line voltage) | 415 V |
| Between a phase and neutral (phase voltage) | 240 V nominal (230 V commonly quoted) |
| Frequency | 50 Hz |

**Phase sequence** (the order L1-L2-L3) decides the direction of rotation of three-phase motors. Swapping any two phases reverses the motor.

## 48.5 Neutral and earth

- **Neutral (N)** is the return conductor for single-phase loads, connected to the star point of the transformer. It carries current in normal operation and can be dangerous.
- **Earth (PE)** is the protective conductor connected to the ground. It carries current only during a fault, to trip the protection.
- Never use earth as a neutral, or neutral as an earth.

## 48.6 Why electricity is dangerous

- Current through the body disturbs the heart and muscles. Even 30 mA through the chest can be fatal. Wet skin, sweat and standing on a wet floor lower body resistance and increase the current.
- An electric arc burns at thousands of degrees and can cause severe burns and blindness.
- A shock can also cause a fall from a ladder or a reflex movement into a machine.

That is why work is done dead under LOTO, and why only trained persons open panels.

## 48.7 How protection devices help

| Device | Protects against | How |
|---|---|---|
| Fuse | Overload and short circuit | Thin wire melts |
| MCB / MCCB / ACB | Overload and short circuit | Thermal and magnetic (or electronic) release opens the contacts |
| RCCB (30 mA) | Shock from earth leakage | Compares outgoing and returning current; trips on a difference |
| Overload relay | Motor overheating | Bimetals bend with long-lasting overcurrent |
| Earthing | Shock from a faulty enclosure | Gives the fault current a path to trip the breaker |

## 48.8 Simple meter use (for trained trainees under supervision)

| Measurement | Range on meter | Remember |
|---|---|---|
| Is the 24 V DC supply present? | V DC | Red on +, black on 0 V; expect 23 to 25 V |
| Is a lamp's supply present? (control circuit, supervised) | V AC | Only with a permit and supervision if live |
| Is a wire broken? (circuit dead and locked) | Continuity / ohms | Beep means continuous |
| Is a fuse good? (removed from circuit) | Ohms | Near 0 ohm good; open = blown |

Never measure on power circuits without being a skilled person with the right PPE.

## 48.9 Reading a nameplate

| Motor nameplate entry | Meaning |
|---|---|
| kW | Output power at the shaft |
| V and connection (e.g. 415 V delta / 720 V star) | Supply voltage and winding connection |
| A | Full load current at rated voltage (used to set overloads) |
| rpm | Speed at full load |
| Hz | Supply frequency |
| PF (cos phi) | Power factor at full load |
| Ins. class | Insulation class (e.g. F) |
| IP | Protection of the motor enclosure |
| Duty (S1) | Continuous duty |

!! HINGLISH: Voltage dhakka hai, current bahaav hai, resistance rukawat hai. Plant mein do phase ke beech 415 V aur phase-neutral 230-240 V. Neutral mein bhi current hota hai, wo bhi khatarnaak hai; earth sirf fault ke waqt current le jaata hai. 30 mA current bhi jaan le sakta hai, gile haath aur gile farsh par khatra badh jaata hai. Fuse, MCB, RCCB aur earthing hamari suraksha karte hain. Power circuit par naapna sirf trained aur authorised insaan ka kaam hai.
