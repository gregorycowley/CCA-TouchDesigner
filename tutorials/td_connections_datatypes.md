# TouchDesigner: Connections & Data Types
### IXDSN 3500 — Emerging Technologies

**Time:** ~90 minutes | **Work individually, compare with your partner**

---

## What You're Building

A network where **three different data types talk to each other** — a CHOP signal drives a TOP effect, which textures a SOP shape, and a DAT logs what's happening in real time. By the end you'll understand not just *how* to connect nodes, but *why* some connections work and others don't.

---

## The Core Idea

In TouchDesigner, **connections are not all the same**. A wire between two TOPs carries pixels. A wire between two CHOPs carries numbers over time. You can't mix them — a TOP output cannot plug directly into a CHOP input. But you *can* convert between families using bridge nodes.

Think of it like adapters: a USB-C cable won't fit a headphone jack, but an adapter makes it possible. TD has adapters for every family pair.

---

## Part 1 — What Can Connect to What? (10 min)

Before building anything, map out the rules.

In the Network Editor, press **[Tab]** and browse each family. Look at node inputs and outputs (the small triangles on the left and right edges of nodes). Inputs and outputs are **color-coded by family**.

**Fill in the connection rules:**

| I want to connect... | ...to a | Can I do it directly? | What node converts between them? |
|---|---|---|---|
| TOP output | CHOP input | No | **TOP to CHOP** |
| CHOP output | TOP input | No | **CHOP to TOP** |
| SOP output | TOP input | No | **Render TOP** |
| DAT output | CHOP input | No | **DAT to CHOP** |
| TOP output | TOP input | | |
| CHOP output | CHOP input | | |
| SOP output | SOP input | | |

> **Key rule to write down in your own words:** 
>
> _____________________________________________
> _____________________________________________

---

## Part 2 — Reading a Wire (10 min)

Every connection carries a specific data type. You can inspect what's flowing through any wire by hovering over it or viewing the node's output.

### What CHOPs carry

A CHOP carries **channels** — named streams of numbers sampled over time. Think of each channel like a single instrument track in a recording.

1. Press **[Tab]** → CHOP → add a **LFO CHOP** (Low Frequency Oscillator)
2. Click on it and look at the viewer at the bottom of the node
3. You should see a waveform — a sine wave going up and down

**What is the LFO's default:**
- Channel name: ____________
- Frequency: ____________ Hz
- Range (min to max): ____________ to ____________

---

### What TOPs carry

A TOP carries **pixels** — a 2D grid of color values (RGBA).

1. Press **[Tab]** → TOP → add a **Ramp TOP**
2. Click it and observe the viewer

**What does the Ramp TOP output?** ________________________________

**What is the default resolution?** ____________ × ____________ pixels

---

### What SOPs carry

A SOP carries **3D geometry** — points, edges, polygons, and their attributes.

1. Press **[Tab]** → SOP → add a **Box SOP**
2. Middle-click on it to open a floating viewer
3. Press **W** to switch to wireframe mode

**How many points does a default Box SOP have?** ____________

> **Tip:** You can find this in the node's Info popup — right-click → **Info DAT**

---

### What DATs carry

A DAT carries **text or tables** — rows and columns of strings or numbers.

1. Press **[Tab]** → DAT → add a **Table DAT**
2. Double-click to open the editor
3. Type some values into the cells — anything

**What data type does a DAT cell hold?** ________________________________

---

## Part 3 — Build the Network (40 min)

You'll build this network step by step. Each section introduces one new connection type.

```
[LFO CHOP] ──► [Math CHOP] ──► [CHOP to TOP] ──► [Level TOP] ──► [Render TOP] ──►[Out TOP]
                                                                         ▲
                                                              [Sphere SOP]──►[Geo COMP]
                                                                         
[LFO CHOP] ──► [CHOP to DAT] ──► [Table DAT] (live log)
```

---

### Step 1 — Build the CHOP signal chain

**Goal:** Create a smooth oscillating signal that we'll use to drive visual parameters.

1. Add an **LFO CHOP**
   - Set **Frequency** to `0.25` (one full cycle every 4 seconds)
   - Set **Type** to `Sine`

2. Add a **Math CHOP** to the right, connect LFO → Math
   - In parameters, set **From Range** to `-1` to `1`
   - Set **To Range** to `0` to `1`
   - This remaps the sine wave so it oscillates between 0 and 1 instead of -1 to 1

**Why do we remap it?** ________________________________

> **Hint:** Think about what range makes sense for things like brightness or scale.

---

### Step 2 — Convert CHOP to TOP

A **CHOP to TOP** node converts a stream of numbers into a strip of pixels — one pixel per sample.

1. Add a **CHOP to TOP**
2. Connect **Math CHOP** → **CHOP to TOP**
3. Look at the node's viewer

**What does the output look like?** ________________________________

**What color does a value of 1.0 become?** ____________  
**What color does a value of 0.0 become?** ____________

---

### Step 3 — Use the signal to drive a Level TOP

1. Add a **Ramp TOP**
2. Add a **Level TOP**, connect Ramp → Level
3. Now wire your **Math CHOP** output into the **Brightness** parameter of the Level TOP

   To do this:
   - Select the **Level TOP**
   - In the **Brightness** parameter field, right-click → **Export CHOP**
   - Select your Math CHOP from the list, choose the channel `chan1`

4. Watch the brightness of your ramp pulse up and down

**What is "exporting" a CHOP doing, in your own words?**

_______________________________________________
_______________________________________________

---

### Step 4 — Add 3D geometry and render it

1. Add a **Sphere SOP** — set Rows and Cols to `50`
2. Add a **Geo COMP** — connect Sphere → Geo
3. Add a **Camera COMP** — leave default settings
4. Add a **Light COMP** — leave default settings
5. Add a **Render TOP**
   - In parameters, set **Camera** to `/project1/camera1`
   - Set **Geometry** to `/project1/geo1`

6. You should now see your sphere rendered in the Render TOP viewer

> **Important:** The Render TOP doesn't use a wire connection to the Camera and Geo — it references them by **path**. This is a different kind of connection: a **reference** rather than a **wire**.

**What is the difference between a wire connection and a path reference?**

_______________________________________________
_______________________________________________

---

### Step 5 — Texture the sphere with your animated TOP

1. Select the **Geo COMP**
2. Go to the **Render** parameter page
3. In the **Material** field — add a **Phong MAT** first:
   - Press **[Tab]** → MAT → **Phong**
   - In the Geo COMP's Render page, set Material to `/project1/phong1`
4. Select the **Phong MAT**
5. In the **Color Map** parameter, set it to your **Level TOP** path

Your LFO-driven animated ramp should now appear as a texture on the sphere.

**Does the texture animate?** Yes / No

**If not, what did you check?** ________________________________

---

### Step 6 — Log data in real time with a DAT

DATs can be used to inspect live values from your network.

1. Add a **CHOP to DAT** node
2. Connect your **Math CHOP** → **CHOP to DAT**
3. Add a **Table DAT** to the right — connect CHOP to DAT → Table DAT
4. Middle-click the Table DAT to open a floating viewer

**What do you see in the table?** ________________________________

**What updates as your LFO runs?** ________________________________

> **DATs as debugging tools:** Any time you're not sure what value is flowing through your network, pipe it through a CHOP to DAT → Table DAT to inspect it. This is your console.

---

## Part 4 — Break It On Purpose (10 min)

Understanding errors is part of understanding connections.

Try each of these and note what happens:

**1.** Disconnect the Math CHOP from the CHOP to TOP. What happens to the downstream nodes?

_______________________________________________

**2.** Try to connect a TOP output directly into a CHOP input (drag the wire — TD won't let you). What does the cursor show?

_______________________________________________

**3.** Delete the Camera COMP while the Render TOP is referencing it. What does the Render TOP show?

_______________________________________________

**4.** Reconnect everything. Did your network restore itself?

_______________________________________________

> **What error handling did you notice?** TD shows errors in __________ color on the node.

---

## Part 5 — Reflect (10 min)

**1.** In the network you built, trace the full path data takes from the LFO CHOP to the final texture on the sphere. List every node it passes through and what data type it carries at each step:

| Node | Data type going IN | Data type going OUT |
|---|---|---|
| LFO CHOP | (none) | CHOP signal |
| Math CHOP | | |
| CHOP to TOP | | |
| Level TOP | | |
| Phong MAT | | |
| Geo COMP / Sphere | | |
| Render TOP | | |

**2.** What is the most useful conversion node you used today, and why?

_______________________________________________
_______________________________________________

**3.** What question do you still have about connections or data types?

_______________________________________________
_______________________________________________

---

## Part 6 — Stretch (if you finish early)

- **Add a second LFO CHOP** at a different frequency and use a **Merge CHOP** to combine two channels. Use one channel for brightness and one for the sphere's X rotation.
- **Add a Text DAT**, type a Python expression, and use a **DAT Execute DAT** to run it when a value crosses a threshold.
- **Replace the Ramp TOP** with a movie file (drag a video into TD) and use your LFO to scrub through the timeline using the **playback** parameter.
- **Try a Null CHOP** between your Math CHOP and your exports — this is a best practice for building stable networks. Why might that be useful?

---

## Connection Cheat Sheet

Keep this for reference:

| Convert FROM | Convert TO | Node to use |
|---|---|---|
| CHOP | TOP | CHOP to TOP |
| CHOP | DAT | CHOP to DAT |
| TOP | CHOP | TOP to CHOP |
| DAT | CHOP | DAT to CHOP |
| SOP | TOP | Render TOP |
| SOP | CHOP | SOP to CHOP |

**Two ways to connect nodes:**
- **Wire** — drag from output to input (real-time data flow)
- **Path reference** — type a node's address into a parameter field (lookup, not stream)

---

## Vocabulary

| Term | Definition |
|---|---|
| Channel | A single named stream of values inside a CHOP |
| Sample | One value at one point in time in a CHOP channel |
| Resolution | Width × height in pixels (TOPs) |
| Export | Locking a parameter to follow a CHOP channel's live value |
| Path reference | Pointing to a node by its address instead of wiring to it |
| Cook | Processing — a node recalculates its output when upstream data changes |
| Null | A pass-through node used as a stable reference point |

---

## Before You Leave

Write in your notebook:

> **Draw a rough diagram of the data flow you built today — just boxes and arrows, with the data type labeled on each arrow.**

You'll use this as a reference for every network you build this semester.

---

*IXDSN 3500 — CCA Interaction Design*
