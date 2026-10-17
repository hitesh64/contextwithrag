# 26. Hydraulic Systems for Technicians

Five machines of the plant are hydraulic: SHEAR-01, PUNCH-02, BRAKE-04, PEM-07 and BUS-10. This chapter explains the common parts of their hydraulic systems, how to keep them healthy, and how to find faults.

## 26.1 Basic principles

Hydraulics transmits force through oil. A pump pushes oil into the system; the oil cannot be compressed, so the pressure acts on the piston of a cylinder and produces a force.

**Force (N) = pressure (bar) x piston area (cm2) x 10**

Example: a cylinder with a 125 mm bore (area 122.7 cm2) at 210 bar gives 210 x 122.7 x 10 = 257 700 N, about 26 tonnes. The two cylinders of a 50 t press would need about this size each.

**Speed** of a cylinder depends on the oil flow: speed (m/min) = flow (l/min) / piston area (cm2) x 10. A pump of 40 l/min moves the same 125 mm cylinder at 40 / 122.7 x 10 = 3.3 m/min (55 mm/s).

Two rules for technicians:

- **Pressure comes from resistance**: the pump makes flow; pressure rises only when the flow meets resistance (a load, a closed valve). If there is no pressure, the oil is going somewhere without resistance: a relief valve open, a valve leaking back to tank, worn pump.
- **Flow gives speed**: if a cylinder is slow, flow is missing (worn pump, internal leakage, wrong valve opening), not pressure.

## 26.2 Components

[[fig:hydraulic_circuit|Figure 26-1. Basic hydraulic circuit: tank, pump, relief valve, directional valve and cylinder|450]]

| Component | Function | Common faults |
|---|---|---|
| Tank (reservoir) | Stores oil, lets air and dirt settle, dissipates heat | Low level, water, sludge, breather blocked |
| Suction strainer | Protects pump from large particles | Blocked: pump noise (cavitation) |
| Pump (gear, vane, piston) | Creates flow | Wear (internal leakage, slow movement, heat), cavitation, shaft seal leak |
| Electric motor and coupling | Drives the pump | Coupling insert worn, misalignment |
| Pressure relief valve | Limits maximum pressure, protects the system | Set too low (weak force), stuck open (no pressure), leaking (heat) |
| Directional control valve (solenoid) | Directs oil to the cylinder ends | Coil burnt, spool stuck by dirt, internal leakage |
| Proportional / servo valve | Controls flow or pressure continuously (BRAKE-04 Y1/Y2) | Very sensitive to dirt; electronics fault |
| Check valve, pilot-operated check | Lets oil flow one way; holds load | Leak causes beam drift |
| Counterbalance valve | Holds the vertical load (press beam), prevents free fall | Wrong setting: beam drops or moves jerkily |
| Flow control valve | Sets speed | Blocked orifice |
| Cylinder | Converts pressure to force and movement | Seal wear (internal or external leak), scored rod |
| Accumulator | Stores oil under gas pressure, supplies peak flow, absorbs shocks | Loss of nitrogen pre-charge; stored energy hazard |
| Return filter | Cleans oil returning to tank | Blocked: indicator red, bypass opens (dirty oil circulates) |
| Oil cooler (air or water) | Removes heat | Dirty fins, fan failure |
| Pressure gauge, pressure switch, transducer | Measures and monitors pressure | Damaged gauge (pulsation), switch setting |
| Hoses and fittings | Carry oil | Ageing, abrasion, leaks, burst |

## 26.3 Hydraulic oil

### 26.3.1 Oil grade

The plant uses **ISO VG 46 anti-wear hydraulic oil (HLP / HM 46)** for SHEAR-01, PUNCH-02, BRAKE-04 and BUS-10, and **ISO VG 32** for PEM-07, as specified by the machine makers. The number is the viscosity at 40 degrees C in centistokes. Never mix brands or grades without checking compatibility; never top up with engine oil.

### 26.3.2 Cleanliness

Most hydraulic failures are caused by dirty oil. Particles too small to see (5 to 15 microns) wear pumps and valves and jam servo and proportional valves.

| Rule | Reason |
|---|---|
| Top up only through a filter cart (10 micron filter), never by pouring from an open drum | New oil from the drum is often dirtier than the oil in the machine |
| Keep drums closed and stored indoors, lying on the side with bungs at 3 and 9 o'clock | Prevents water entering through the bungs |
| Clean the area around any fitting before opening it | Dirt falls into the system |
| Cap open hoses and ports immediately with clean caps | - |
| Replace filters when the indicator shows red, not "when convenient" | A blocked filter opens its bypass and passes dirty oil |
| Keep the tank breather filter in good condition | Air entering the tank carries dust |

Target cleanliness (ISO 4406): **18/16/13** or better for machines with proportional or servo valves (BRAKE-04, PUNCH-02); **19/17/14** for other systems. Oil samples are taken every 6 months (Chapter 24.6) from the sampling point with the system running and warm.

### 26.3.3 Temperature

Normal working temperature is **35 to 55 degrees C**. Above 60 degrees C, oil ages quickly, seals harden and viscosity falls, so leakage increases and speed and accuracy drop. Below 20 degrees C, oil is thick, which causes slow movement and pump cavitation: warm up before precision work. High temperature is always a symptom: find the cause (cooler, relief valve leaking, worn pump, internal leakage, too high pressure setting).

## 26.4 Safety in hydraulic work

!! DANGER: Hydraulic oil at 200 bar escaping from a pin-hole can penetrate the skin and cause injury that may lead to amputation. Never feel for a leak with your hand: use a piece of cardboard. Any oil injection injury is a medical emergency, even if it looks small: go to the hospital immediately and say "high pressure injection injury".

- Before opening any fitting: stop the pump, release pressure (operate valves, lower loads, discharge accumulators), and verify with the gauge that pressure is zero.
- Support raised loads mechanically (blocks under the press beam) before working under them: a hydraulic cylinder can drop when a fitting is opened.
- Accumulators hold pressure after the pump stops. Discharge them through the discharge valve and check the gauge.
- Hoses under pressure can whip violently if they burst: never stand in line with a hose end while testing.
- Wipe up oil spills immediately: slippery floors cause falls.

## 26.5 Hoses

- Use hoses with the correct pressure rating (working pressure at least equal to the relief valve setting, with the maker's safety factor) and the correct fittings, crimped by the supplier or with the plant's hose press using the hose maker's crimp data.
- Route hoses without twisting, with bend radius above the minimum, and protected from rubbing with sleeves or clamps.
- Replace hoses that show cracks, blisters, abrasion through the outer cover, leaks at the fittings, or are older than 6 years.
- Record the hose installation date on a tag on each hose.

## 26.6 Fault finding in hydraulic systems

| Symptom | Possible causes | Checks |
|---|---|---|
| No movement | Pump not running or rotating wrong way; no electrical signal to valve; valve spool stuck; relief valve open | Pump rotation (arrow), solenoid LED / voltage at coil, manual override of valve, pressure at gauge |
| Slow movement | Low flow: worn pump, internal leakage in cylinder or valve, flow control closed, cold oil, suction restricted | Oil temperature; pressure at full load; cylinder bypass test (section 26.6.1); case drain flow of piston pump |
| Low force / pressure | Relief valve set low or leaking; pump worn; leak to tank | Pressure at dead-head (cylinder at end of stroke) compared with setting |
| Erratic or jerky movement | Air in oil; contamination in valve; low oil level; worn guides | Foam in tank, oil level, valve condition, guides |
| Noisy pump (whine, rattle, gravel sound) | Cavitation (suction blocked, oil cold, level low) or aeration (air leak on suction side) | Strainer, oil level, suction fittings tightness; foam in tank |
| Overheating | Relief valve continuously open, internal leakage, cooler fault, too high pressure setting | Temperature across components (thermal camera): the component that is hotter than others is leaking |
| Load drifts down when stopped | Leaking check valve or counterbalance valve; cylinder seal leak | Drift test; isolate components one by one |
| External leak | Seals, fittings, hoses | Clean and look; tighten fittings only after pressure release; replace seals |

### 26.6.1 Cylinder bypass (internal leakage) test

1. Move the cylinder to the end of its stroke (fully extended or retracted), with the system safe (no person at risk if the cylinder moves).
2. Stop the pump and release pressure. Apply LOTO.
3. Disconnect the line at the opposite (non-pressurised) port and cap the line; put the open port over a measuring container.
4. Remove LOTO for the test only, start the pump and apply pressure to the pressurised side (the cylinder is at the end of stroke, so it does not move).
5. Measure the oil coming out of the open port. More than a few drops per minute shows piston seal leakage.
6. Stop, release pressure, LOTO, reconnect.

!! CAUTION: This test needs a technician trained in hydraulics and the supervisor's approval, because the system runs with a port open. Keep the pressure low and stand clear.

### 26.6.2 Measuring pressure

Each hydraulic system has test points (minimess couplings) at the pump outlet, the valve block and the cylinder ports. Connect a calibrated gauge with a test hose (rated pressure above the system pressure) to compare the pressures. A large difference between the pump outlet and the cylinder port during movement shows a restriction; a pump pressure below the relief setting at dead-head shows a worn pump or a leaking relief valve.

## 26.7 Servo and proportional valves (BRAKE-04, PUNCH-02)

These valves control the press beam position and speed very precisely. They are sensitive:

- Oil cleanliness must be kept at the target (section 26.3.2); a single particle can block the pilot stage.
- Do not open the valve: it is set at the factory. Faulty valves are replaced and sent to the maker for repair.
- Electrical faults: check the connector, the cable, and the valve's electronics (LED on the valve or alarm on the CNC).
- After replacing a valve on BRAKE-04, run the maker's calibration procedure for the Y axes before production.

## 26.8 Accumulators

- Check the nitrogen pre-charge pressure every 6 months with the charging kit, with the oil side at zero pressure. The pre-charge is typically 60 to 80 % of the minimum working pressure; the value is on the accumulator label.
- Charge only with dry nitrogen, never with oxygen or compressed air (explosion risk).
- Accumulators are pressure vessels: they carry a label with the maximum pressure and must not be welded or modified.

## 26.9 Operator quick card

!! HINGLISH: Hydraulic machine mein oil se force milta hai. Oil level, temperature (35-55 degree) aur leak roz dekho. Oil hamesha filter cart se bharo, drum se seedha nahi. Filter indicator laal ho to turant badlo. Leak haath se kabhi mat dhundho, gatta (cardboard) use karo; tez dhaar wala oil chamdi mein ghus jaata hai, ye emergency hai. Koi fitting kholne se pehle pump band, pressure zero, beam ke neeche block. Pump se ghar-ghar aawaz aaye to oil level aur strainer check karo.
