# TouchDesigner: External Hardware
### OSC, MIDI & Serial Connections
#### IXDSN 3500 — Emerging Technologies

**Time:** ~90 minutes | **Work in pairs — you will need to share devices**

---

## What This Worksheet Is About

TouchDesigner becomes most powerful when it talks to the physical world — a MIDI controller, a phone sending sensor data, an Arduino reading a pressure pad. This worksheet covers the three most common protocols for connecting external hardware to TD:

| Protocol | Best for | Example devices |
|---|---|---|
| **OSC** (Open Sound Control) | Networked devices, phones, other software | TouchOSC, smartphones, Ableton, Max/MSP |
| **MIDI** | Musical controllers, keyboards, pads | MIDI keyboards, Ableton Push, drum pads |
| **Serial** | Microcontrollers, custom sensors | Arduino, Teensy, custom hardware |

You don't need to master all three today. **Work through Part 1 (OSC) fully, then choose one of Part 2 (MIDI) or Part 3 (Serial) depending on what hardware you have access to.**

---

## Before You Start — What Hardware Do You Have?

Check the equipment available at your station:

- [ ] A smartphone (iOS or Android) — needed for OSC via TouchOSC
- [ ] A MIDI controller (keyboard, pad controller, knob box)
- [ ] An Arduino + USB cable
- [ ] A USB MIDI adapter

**What you have available:** ________________________________

---

## The Big Idea — TD Is Always Listening

When you connect external hardware to TD, TD doesn't go looking for data — it **listens** on a specific port or channel and waits for data to arrive. Your job is:

1. Tell TD where to listen (which port, which channel)
2. Tell your device where to send (same port, same channel)
3. Route the incoming data through CHOPs to where you need it

The data, once it arrives in TD, is just a CHOP signal — the same as anything you've worked with before.

---

## Part 1 — OSC: Open Sound Control (30 min)

OSC sends data over a network — your local Wi-Fi. A device (phone, another computer, another app) sends messages to TD's IP address on a specific port. TD receives them and converts to CHOP channels.

**OSC is the most flexible protocol.** Any device that can connect to Wi-Fi and run an OSC app can talk to TD.

---

### Step 1 — Find Your Computer's IP Address

TD and your device need to be on the same network. First, find your machine's local IP.

**On Mac:**
- System Preferences → Network → Wi-Fi → your IP is listed (e.g. `192.168.1.42`)

**On Windows:**
- Start → cmd → type `ipconfig` → look for IPv4 Address

**Your IP address:** ________________________________

> This address will change if you connect to a different network. Always check before a performance or installation.

---

### Step 2 — Set Up the OSC In CHOP

1. In TD, press **[Tab]** → CHOP → **OSC In CHOP**
2. In parameters:
   - Set **Port** to `7000` (you can use any unused port — 7000 and 8000 are common conventions)
   - Set **Active** to `On`
3. Middle-click the node — viewer is probably empty right now

**What is a "port"?**

_______________________________________________

> **Analogy:** Your IP address is like a building's street address. A port is like the apartment number inside — many apps can share the same IP address but each listens on a different port number.

---

### Step 3 — Set Up TouchOSC on Your Phone

**TouchOSC** is a free app (iOS and Android) that turns your phone into a custom OSC controller with sliders, buttons, and XY pads.

1. Download **TouchOSC** from the App Store or Google Play
2. Open it and create a new layout (or use a default template)
3. Go to **Connections** → **OSC**:
   - Set **Host** to your computer's IP address from Step 1
   - Set **Port (send)** to `7000`
   - Set **Port (receive)** to `7001` (TD sending back to phone — we won't use this today but set it anyway)
4. Enable the connection

5. Go back to TD and middle-click your **OSC In CHOP** — you should see channels appearing as you move controls on your phone

**What channel names appear?** ________________________________

**What happens to the values when you move a slider?** ________________________________

---

### Step 4 — Select and Name Your Channels

OSC messages arrive with path-based names like `/1/fader1` or `/accelerometer/x`. These become CHOP channel names.

1. Add a **Select CHOP** after the OSC In CHOP
2. In parameters, type the channel name of one slider (e.g. `/1/fader1`)
3. You should now see just that one channel

**What is the value range of your slider?** ____________ to ____________

4. Add a **Rename CHOP** after the Select CHOP
5. In parameters, set **From** to the OSC path name and **To** to something readable like `slider1`

> **Good practice:** Always rename OSC channels to meaningful names early in your network. `/1/fader3` is hard to read; `room_brightness` is not.

---

### Step 5 — Use OSC to Drive a Visual

1. Add a **Math CHOP** after Rename — remap the value range if needed
2. Add a **Null CHOP** — name it `osc_slider1`
3. Build a simple visual (Ramp TOP → Level TOP, or use your network from a previous worksheet)
4. Export `osc_slider1` to the **Brightness** parameter of your Level TOP

Move the slider on your phone — the visual should respond.

**Does it work?** Yes / No

**Latency — does it feel instant, or is there a delay?** ________________________________

---

### Step 6 — Use Phone Accelerometer (Bonus)

Many OSC apps can send your phone's accelerometer data — tilt and rotation.

In TouchOSC, add an **Accelerometer** sensor to your layout. It sends three channels: `x`, `y`, `z` — one per axis of movement.

1. Look at the OSC In CHOP — find the accelerometer channels
2. Use a **Select CHOP** to pull out just the `x` axis
3. Add a **Math CHOP** to remap — accelerometer values are typically `-1` to `1`
4. Export to a rotation parameter on a **Transform SOP** or **Camera COMP**

**What does tilting your phone left/right do to the visual?** ________________________________

---

## Part 2 — MIDI (30 min)

*Complete this section if you have a MIDI controller available.*

MIDI (Musical Instrument Digital Interface) is a 40-year-old protocol that is still everywhere. Keyboards, drum pads, knob controllers — they all speak MIDI. TD receives MIDI directly, no network required.

---

### Step 7 — Connect Your MIDI Device

1. Plug your MIDI controller into your computer via USB
2. If it's an older device with 5-pin DIN MIDI connectors, use a USB-MIDI adapter
3. Your OS should recognise it automatically — no drivers needed for most modern controllers

**Mac:** Open **Audio MIDI Setup** (in Applications/Utilities) — your device should appear in the MIDI Studio window

**Windows:** Check **Device Manager** — it should appear under Sound, video and game controllers

**Device name as shown in your OS:** ________________________________

---

### Step 8 — Set Up the MIDI In CHOP

1. In TD, press **[Tab]** → CHOP → **MIDI In CHOP**
2. In parameters:
   - Set **Device** to your controller name from the dropdown
   - Set **Active** to `On`
3. Move a knob or press a key — you should see channels appear in the node viewer

**What channel names appear when you turn a knob?** ________________________________

**What channel names appear when you press a key?** ________________________________

> **MIDI channels and CC numbers:** MIDI data has two addressing layers — a **channel** (1–16, for separating instruments) and a **CC number** (0–127, for identifying which knob/slider). TD names channels like `tx/1` for channel 1.

---

### Step 9 — Read MIDI Data Types

MIDI carries several types of messages. The three most useful in TD:

| Message type | What it is | Value range | TD channel prefix |
|---|---|---|---|
| **Note On/Off** | Key press and release | 0–127 (velocity) | `tx/` |
| **Control Change (CC)** | Knob or slider movement | 0–127 | `tx/` |
| **Pitch Bend** | Pitch wheel | -8192 to 8191 | `pitchbend/` |

1. Turn several knobs and press several keys on your controller
2. In the MIDI In CHOP viewer, identify at least one of each type you can generate

**CC message observed:** channel name ____________, value range ____________

**Note On observed:** channel name ____________, velocity range ____________

---

### Step 10 — Remap and Drive a Visual

MIDI values arrive as integers from `0–127`. Most TD parameters expect `0.0–1.0`.

1. Add a **Math CHOP** after MIDI In
   - Set **From Range** to `0` to `127`
   - Set **To Range** to `0` to `1`
2. Add a **Select CHOP** to isolate one knob's channel
3. Add a **Null CHOP** — name it `midi_knob1`
4. Export to a visual parameter of your choice

**What parameter did you drive?** ________________________________

**Does the knob feel responsive?** ________________________________

---

### Step 11 — Map Multiple Controls

1. Use a **Merge CHOP** to combine multiple Select CHOPs into one signal stream
2. Rename channels to meaningful names: `brightness`, `scale`, `hue`
3. Export each channel to a different visual parameter

**How many controls did you map?** ________________________________

**What interaction did you create?** ________________________________

---

## Part 3 — Serial: Arduino (30 min)

*Complete this section if you have an Arduino available.*

Serial communication sends raw text or bytes over USB between TD and a microcontroller like an Arduino. This is how you connect custom sensors — pressure pads, distance sensors, flex sensors, buttons — to TD.

---

### Step 12 — Upload a Simple Sketch to Arduino

Before TD can receive anything, the Arduino needs to be sending data.

1. Open the **Arduino IDE** on your computer
2. Upload this sketch — it sends a potentiometer reading over serial every 50ms:

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A0);  // Read analog pin A0 (0–1023)
  Serial.println(sensorValue);       // Send as text with newline
  delay(50);
}
```

3. Open the **Serial Monitor** (Tools → Serial Monitor) — you should see numbers scrolling

**What numbers do you see?** ________________________________

**What changes them?** ________________________________

> **No potentiometer?** Connect a wire from pin A0 to 3.3V — you'll get a fixed high value. Connect to GND for a low value. This is enough to verify the connection.

---

### Step 13 — Connect Serial to TD

1. Close the Arduino Serial Monitor — only one app can use the serial port at a time
2. In TD, press **[Tab]** → DAT → **Serial DAT**
3. In parameters:
   - Set **Port** to your Arduino's port (e.g. `COM3` on Windows, `/dev/cu.usbmodem...` on Mac)
   - Set **Baud Rate** to `9600` (must match your Arduino sketch)
   - Set **Active** to `On`
4. Middle-click the Serial DAT — you should see numbers arriving as text rows

**What do you see in the DAT viewer?** ________________________________

**What is the value range?** ____________ to ____________

---

### Step 14 — Convert Serial Text to a CHOP Signal

Data arrives in a DAT as text. You need to convert it to a CHOP number.

1. Add a **DAT to CHOP** node
2. Connect **Serial DAT** → **DAT to CHOP**
3. In parameters, set **Select Rows** to `By Index`, **Start Row Index** to `0`
4. Set **Select Cols** to `By Index`, **Start Col Index** to `0`

You should now have a single-channel CHOP with your sensor value.

**What is the channel name?** ________________________________

---

### Step 15 — Clean and Remap

Arduino analog values arrive as integers from `0–1023`. Remap to `0–1`:

1. Add a **Math CHOP**
   - **From Range:** `0` to `1023`
   - **To Range:** `0` to `1`
2. Add a **Filter CHOP** — set Filter Width to `0.03` to smooth out noise
3. Add a **Null CHOP** — name it `sensor_value`

**Does the signal look clean?** ________________________________

**Is there noise when the sensor is held still?** ________________________________

---

### Step 16 — Drive a Visual with Your Sensor

Export `sensor_value` to a visual parameter of your choice.

**What sensor input are you using?** ________________________________

**What visual parameter did you connect it to?** ________________________________

**Describe the interaction in one sentence:**

_______________________________________________
_______________________________________________

---

## Part 4 — Troubleshooting & Diagnostics (10 min)

Hardware connections fail in predictable ways. Work through this diagnostic checklist whenever something isn't working.

### OSC not receiving?

- [ ] Are both devices on the **same Wi-Fi network**?
- [ ] Does the phone's Host IP match your computer's current IP exactly?
- [ ] Do the port numbers match on both ends?
- [ ] Is the OSC In CHOP **Active**?
- [ ] Is a firewall blocking the port? (Try turning off firewall temporarily to test)
- [ ] Try pressing **Ctrl+Alt+Delete** to restart TD's network listener

### MIDI not receiving?

- [ ] Is the device plugged in and powered?
- [ ] Does it appear in **Audio MIDI Setup** (Mac) or **Device Manager** (Windows)?
- [ ] Is the correct device selected in the MIDI In CHOP **Device** parameter?
- [ ] Does the device require its own driver? (Check manufacturer's website)
- [ ] Is the MIDI channel set to **All** in the CHOP parameters?

### Serial not receiving?

- [ ] Is the **Serial Monitor closed** in Arduino IDE?
- [ ] Do the **baud rates match** in the sketch and the Serial DAT?
- [ ] Is the correct **port name** selected? (On Mac it starts with `/dev/cu.`)
- [ ] Try unplugging and replugging the USB cable
- [ ] Reupload the sketch — sometimes the Arduino resets to a bad state

---

## Part 5 — Build a Multi-Input Network (10 min)

Combine at least **two** of the protocols you've worked with today into a single network.

For example:
- A MIDI knob controls brightness, a phone accelerometer controls rotation
- An Arduino sensor controls scale, an OSC slider controls color
- Two OSC sliders control X and Y position of a shape

**What inputs are you combining?** ________________________________

**What do they each control?** ________________________________

**Sketch your combined network here:**

```
 ┌──────────┐                         ┌──────────┐
 │          │──────►                  │          │
 │ Input 1  │          ┌──────────┐   │  Output  │
 └──────────┘    ─────►│  Merge   │──►│          │
                        │  CHOP    │   └──────────┘
 ┌──────────┐    ─────►│          │
 │          │──────►   └──────────┘
 │ Input 2  │
 └──────────┘
```

---

## Part 6 — Reflect (10 min)

**1.** What is the fundamental difference between OSC and MIDI in terms of how data is transmitted?

_______________________________________________
_______________________________________________

**2.** In all three protocols, once the data arrives in TD, what data type does it become?

_______________________________________________

**3.** What was the most confusing part of setting up your connection? What did you do to debug it?

_______________________________________________
_______________________________________________

**4.** For your spatial project — what physical interaction or sensor input would make your concept stronger? What protocol would you use to connect it?

_______________________________________________
_______________________________________________

---

## Part 7 — Stretch (if you finish early)

- **OSC feedback:** Configure TD to *send* OSC back to your phone using an **OSC Out CHOP** — make a light on the phone illuminate when a visual threshold is crossed.
- **MIDI learn:** Build a simple MIDI learn system using a **Table DAT** to store which CC number maps to which TD parameter — so you can remap without rewiring.
- **Arduino multi-sensor:** Modify the Arduino sketch to send multiple sensor values separated by commas (`Serial.println(String(val1) + "," + String(val2))`), then parse the comma-separated data in TD using a **DAT** and **Convert DAT**.
- **OSC from Ableton:** If Ableton Live is available, configure it to send OSC via the Max for Live OSC Send device — use a track's volume or a clip trigger to drive a TD visual.

---

## Protocol Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  OSC                                                        │
│  Transport: Wi-Fi / UDP network                             │
│  Addressing: IP address + port number + message path        │
│  TD node: OSC In CHOP (port 7000 convention)                │
│  Data type on arrival: CHOP (named channels)                │
│  Best for: phones, networked devices, other software        │
├─────────────────────────────────────────────────────────────┤
│  MIDI                                                       │
│  Transport: USB (or 5-pin DIN cable)                        │
│  Addressing: MIDI channel (1–16) + CC number (0–127)        │
│  TD node: MIDI In CHOP                                      │
│  Data type on arrival: CHOP (0–127 integer values)          │
│  Best for: music controllers, knobs, pads, keyboards        │
├─────────────────────────────────────────────────────────────┤
│  Serial                                                     │
│  Transport: USB cable                                       │
│  Addressing: port name + baud rate                          │
│  TD node: Serial DAT → DAT to CHOP                          │
│  Data type on arrival: DAT text → then CHOP after convert   │
│  Best for: Arduino, custom sensors, physical computing      │
└─────────────────────────────────────────────────────────────┘
```

---

## Vocabulary

| Term | Definition |
|---|---|
| OSC | Open Sound Control — a network protocol for sending control data over Wi-Fi |
| MIDI | Musical Instrument Digital Interface — a hardware/software protocol for musical controllers |
| Serial | A simple text-based protocol for USB communication between computer and microcontroller |
| Port | A numbered address on a computer that a specific app listens on (OSC/network) |
| Baud rate | The speed of serial communication — must match on both ends |
| CC (Control Change) | A MIDI message type from knobs and sliders, numbered 0–127 |
| Protocol | An agreed-upon language and format that two devices use to communicate |
| Latency | The delay between an action and its result — important for live performance |

---

## Before You Leave

On a sticky note:

> **Name the protocol you'd use for your spatial project input, and explain why in one sentence.**

---

*IXDSN 3500 — CCA Interaction Design*
