# TouchDesigner: Audio Reactivity
### Sound → Visual with CHOPs
#### IXDSN 3500 — Emerging Technologies

**Time:** ~90 minutes | **Format:** Step-by-step build + reflection

---

## What You're Building

A live audio-reactive visual — sound from your microphone (or a music file) will drive the size, brightness, and color of a visual in real time. When the music is loud, something happens. When it's quiet, something else happens. You'll wire this entirely with CHOPs.

By the end you'll have a system you can keep and adapt for your spatial project.

---

## How It Works — The Signal Chain

Every audio-reactive system in TD follows the same basic logic:

```
Audio source → Analyze → Remap → Export to visual parameter
```

1. **Get sound in** — microphone or audio file
2. **Analyze it** — extract useful numbers (volume, bass, treble)
3. **Remap the range** — audio values don't always match the range your visual needs
4. **Drive something** — send those numbers to a parameter on a visual node

That's it. Everything you build today is a variation of this chain.

---

## Before You Start — Check Your Audio

1. Open TouchDesigner
2. Press **[Tab]** → CHOP → add an **Audio Device In CHOP**
3. In its parameters, set **Device** to your microphone
4. Middle-click the node to open a floating viewer
5. Make a sound — clap, talk, play music nearby

**Do you see the waveform reacting?** Yes / No

If no — check:
- System audio input is set to the right device (check macOS Sound Settings or Windows Sound Settings)
- TouchDesigner has microphone permission (macOS: System Preferences → Security → Microphone)
- The node is not bypassed (node should not be grey — if it is, press **B** to toggle bypass off)

> **Using a file instead of mic?** Drag an `.mp3` or `.wav` into TD and it will create an **Audio File In CHOP** automatically. The rest of the steps are identical.

---

## Part 1 — Get Audio In and See It (10 min)

### Step 1 — Audio Device In CHOP

Your audio source. This node listens to your mic continuously.

1. You should already have an **Audio Device In CHOP** from the check above
2. Look at the waveform in the viewer — this is raw audio, thousands of samples per second
3. In parameters, note the **Sample Rate** — probably `44100` Hz

**What does the waveform look like when you're silent?** ________________________________

**What does it look like when you clap?** ________________________________

---

### Step 2 — Visualize the Waveform in a TOP

Raw waveforms are hard to read. Let's display yours visually.

1. Add a **CHOP to TOP** node
2. Connect **Audio Device In** → **CHOP to TOP**
3. Middle-click the CHOP to TOP to open its viewer

**What do you see?** ________________________________

> This is a literal pixel-strip of your audio. Not useful for driving visuals yet — but it shows you the raw data is flowing.

---

## Part 2 — Extract Useful Numbers (20 min)

Raw audio waveforms change thousands of times per second. You can't drive a visual with that directly — it would just flicker and be uncontrollable. You need to **analyze** the audio into slower, more usable numbers.

### Step 3 — Audio Spectrum CHOP

This breaks the audio into **frequency bands** — bass, mid, treble — so you can react to them separately.

1. Add an **Audio Spectrum CHOP**
2. Connect **Audio Device In** → **Audio Spectrum CHOP**
3. Open its viewer — you should see a spectrum graph

**What changes when you play bass-heavy music vs high-pitched sounds?**

_______________________________________________

In parameters:
- Set **Frequency Range** to `20` – `20000` Hz (full human hearing range)
- Note the **Bands** parameter — how many frequency buckets you're splitting into

---

### Step 4 — Audio Analysis CHOP

This is the workhorse. The **Analyze CHOP** takes a signal and extracts a **single number** from it — such as the current peak volume.

1. Add an **Analyze CHOP**
2. Connect **Audio Device In** → **Analyze CHOP**
3. In parameters, set **Function** to `RMS Power` (this is a smoothed volume level — better than raw peak)
4. Open the viewer — you should see a single channel, a slowly moving value

**What is the channel name?** ____________

**What is the value when you're silent?** ____________

**What is the approximate peak value when you clap?** ____________

> **RMS Power** is more useful than raw amplitude because it represents *perceived loudness* — it matches how your ears hear volume.

---

### Step 5 — Smooth It Out with a Filter CHOP

Raw RMS values jump abruptly. A **Filter CHOP** smooths the response so your visuals ease in and out rather than snapping.

1. Add a **Filter CHOP**
2. Connect **Analyze CHOP** → **Filter CHOP**
3. In parameters, set **Filter Width** to `0.05`
4. Compare the viewer of the Analyze CHOP vs the Filter CHOP side by side

**What's different about the shape of the signal?** ________________________________

Try increasing Filter Width to `0.3` — what happens to the responsiveness?

_______________________________________________

> **Design choice:** A fast filter (low width) = tight, snappy reaction. A slow filter (high width) = smooth, floaty reaction. Neither is right — it depends on the feel you want.

---

## Part 3 — Remap the Range (10 min)

Your audio signal is probably outputting values between `0.0` and `0.05` — a tiny range. Most visual parameters expect values between `0` and `1`, or between `0` and `100`. You need to stretch the signal to fill that range.

### Step 6 — Math CHOP to Remap

1. Add a **Math CHOP**
2. Connect **Filter CHOP** → **Math CHOP**
3. In parameters, find **From Range** and **To Range**:
   - Set **From Range** to `0` to `0.05` (your observed audio range)
   - Set **To Range** to `0` to `1`
4. Open the viewer — the signal should now swing between 0 and 1 as you make sound

**What happens if you make the From Range too small (e.g. 0 to 0.001)?**

_______________________________________________

**What happens if you make it too large (e.g. 0 to 1)?**

_______________________________________________

> **This step is always custom.** Every microphone, every room, every audio source has a different range. You'll tune the Math CHOP for your specific setup.

---

### Step 7 — Add a Null CHOP

Before you export values to visual parameters, always add a **Null CHOP** at the end of your signal chain. This gives you a stable reference point — if you restructure your network later, everything exported from the Null stays connected.

1. Add a **Null CHOP**
2. Connect **Math CHOP** → **Null CHOP**
3. Name it something clear — right-click → **Rename** → `audio_level`

> **Best practice:** All your exports should come from Null CHOPs, not from analysis or processing nodes directly. It makes your network easier to edit without breaking things.

---

## Part 4 — Drive Visuals (30 min)

Now the fun part. You'll export your audio signal to three different visual parameters.

---

### Step 8 — Drive Brightness (TOP)

1. Add a **Ramp TOP**
2. Add a **Level TOP**, connect Ramp → Level
3. Select the **Level TOP**
4. In the **Brightness** parameter, right-click → **Export CHOP**
5. Choose your `audio_level` Null CHOP, channel `chan1`

Make some sound — the ramp should brighten and dim with the audio.

**Does the brightness respond to your voice?** Yes / No

---

### Step 9 — Drive Scale (SOP)

1. Add a **Sphere SOP**
2. Add a **Transform SOP**, connect Sphere → Transform
3. Select the **Transform SOP**
4. Right-click the **Scale** parameter (the uniform scale field) → **Export CHOP**
5. Choose `audio_level`, channel `chan1`

Add a **Geo COMP** + **Camera COMP** + **Light COMP** + **Render TOP** to see it (you built this in the last worksheet — refer back if needed).

Make sound — the sphere should pulse in size.

**What does it look and feel like?** ________________________________

---

### Step 10 — Drive Color with Frequency Bands

Now let's use the **spectrum** data — not just overall volume, but bass vs treble — to change color.

1. Add a **Select CHOP**
2. Connect **Audio Spectrum CHOP** → **Select CHOP**
3. In parameters, set **Channel Names** to select just the low-frequency band:
   - Try `chan1` or look at the spectrum node's channel names and pick the lowest one
4. Add a **Math CHOP** after to remap this band's values to `0–1`
5. Add a **Null CHOP** — name it `bass_level`

6. Add a second **Select CHOP** + **Math CHOP** + **Null CHOP** chain for a high-frequency band
   - Name this one `treble_level`

7. Add a **Constant CHOP** with 3 channels (`r`, `g`, `b`)
   - Export `bass_level` → `r` channel
   - Export `treble_level` → `b` channel
   - Set `g` to a fixed value like `0.3`

8. Add a **CHOP to TOP** connected to your Constant CHOP — this gives you an animated color patch
9. Connect this color TOP into a **Level TOP** as the source, then into your existing network

**What colors do you see?** ________________________________

**Which part of the music triggers the red?** ________________________________

---

## Part 5 — Shape Your System (10 min)

Now that the basic chain works, make at least **two of these adjustments** and note what changed:

**A.** Slow the Filter CHOP to `0.2` — how does the visual feeling change?

_______________________________________________

**B.** Change the Analyze CHOP **Function** from `RMS Power` to `Maximum` — what's different?

_______________________________________________

**C.** Add a **Lag CHOP** after your Null CHOP — set Attack to `0.05` and Release to `0.3`. What does this add?

_______________________________________________

**D.** Multiply two channels together using a **Math CHOP** in **Combine Channels** mode — what effect does that create?

_______________________________________________

---

## Part 6 — Reflect (10 min)

**1.** Draw the full signal chain you built today, from microphone to visual. Label every node and what type of data it holds:

```
[            ] → [            ] → [            ] → [            ] → [            ]
  data type:        data type:       data type:       data type:       data type:
```

**2.** What is the job of the Math CHOP in this system?

_______________________________________________
_______________________________________________

**3.** What would happen if you skipped the Filter CHOP entirely?

_______________________________________________
_______________________________________________

**4.** What visual parameter would *you* want to drive with audio in your spatial project?

_______________________________________________
_______________________________________________

---

## Part 7 — Stretch (if you finish early)

- **Beat detection:** Add an **Audio Beat CHOP** after your Audio Device In. Export its `beat` channel to trigger a flash or jump in your visual.
- **Multi-band color:** Use 4–5 frequency bands to drive a full spectrum of colors — each band controls a different hue.
- **Threshold trigger:** Add a **Logic CHOP** set to fire when volume exceeds `0.7`. Use this to trigger a one-shot animation or color flash.
- **File playback:** Swap your microphone source for an **Audio File In CHOP** playing a track you choose. Tune your Math CHOP remapping to that specific track.
- **Oscilloscope display:** Use a **Trail CHOP** to create a scrolling history of your audio signal, then display it with a **CHOP to TOP**.

---

## Reference — Audio CHOP Quick Guide

| Node | What it does | Key parameter |
|---|---|---|
| Audio Device In | Live mic or line input | Device |
| Audio File In | Play an audio file | File, Play |
| Audio Spectrum | Frequency analysis | Bands, Frequency Range |
| Analyze | Extract one number from a signal | Function (RMS, Peak, Average...) |
| Filter | Smooth a signal over time | Filter Width |
| Math | Remap, scale, combine channels | From Range / To Range |
| Lag | Smooth with separate attack/release | Attack, Release |
| Null | Stable export point | (just a passthrough) |
| Select | Extract specific channels | Channel Names |
| Constant | Create fixed or exported values | Value |

---

## Common Problems

| Problem | Likely cause | Fix |
|---|---|---|
| Waveform is flat / no signal | Wrong input device | Check Audio Device In → Device parameter |
| Visual barely moves | From Range too large | Lower the max value in Math CHOP From Range |
| Visual is pegged at max | From Range too small | Raise the max value in Math CHOP From Range |
| Visual snaps / flickers | No Filter or Lag CHOP | Add Filter CHOP, increase width |
| Export doesn't stick | Exporting from a non-Null | Add Null CHOP and export from that |
| No sound on Mac | TD doesn't have mic permission | System Preferences → Security → Microphone |

---

## Before You Leave

In your notebook:

> **Write the four-step formula for any audio-reactive system:**
>
> 1. ________________________________
> 2. ________________________________
> 3. ________________________________
> 4. ________________________________

You should be able to rebuild this from scratch next class without the worksheet.

---

*IXDSN 3500 — CCA Interaction Design*
