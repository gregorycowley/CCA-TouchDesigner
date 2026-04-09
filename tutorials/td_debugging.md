# TouchDesigner: Debugging & Reading Error States
### When Things Break — and How to Fix Them
#### IXDSN 3500 — Emerging Technologies

**Time:** ~75 minutes | **Work individually**

---

## What This Guide Is About

Things will break. Networks go dark, values disappear, operators turn red, and nothing happens when you expect something to. This is not a sign that you're doing it wrong — it's a normal part of working in TD.

The difference between someone who gets stuck for two hours and someone who fixes it in five minutes is not talent. It's having a systematic way of reading what TD is already telling you.

TD is unusually communicative about its own errors. Almost every failure leaves a visible trace. This guide teaches you how to read those traces.

---

## The Debugging Mindset

Before touching anything when something breaks, ask three questions — in this order:

```
1. WHAT is broken?       Describe the symptom precisely.
2. WHERE did it break?   Find the first node upstream that looks wrong.
3. WHY did it break?     Read the error. Don't guess — read first.
```

The most common debugging mistake is skipping straight to fixing before understanding. You end up changing things at random, making the problem harder to trace.

---

## Part 1 — How TD Communicates Errors (15 min)

TD shows you errors in several ways simultaneously. Learn to read all of them.

---

### 1.1 — Node Colors and States

Every node in the network has a visual state. Look at your network now and identify any of these:

| Node appearance | What it means |
|---|---|
| **Normal** (slightly lit) | Cooking correctly |
| **Dark / dim** | Bypassed — press **B** to toggle, or check the Bypass flag |
| **Red border or red background** | Error — hover to see the message |
| **Yellow / orange border** | Warning — something is off but not fatal |
| **Blue tint** | Viewer is active on this node |
| **Lock icon** | A parameter is exported from a CHOP |
| **Purple tint on parameter** | Parameter has a Python expression |
| **Grey with diagonal lines** | Node is set to Unload — it's not cooking at all |

**Create a node right now that produces an error. How?**

Press **[Tab]** → TOP → add a **Movie File In TOP**. Leave the File parameter empty.

**What color does it turn?** ____________

**What does the node thumbnail show?** ________________________________

---

### 1.2 — The Info Pop-up

Hover your mouse over any node for about half a second. A pop-up appears with:
- Node type and name
- Current resolution or channel count
- **Error or warning message** (if any)
- Cook time in milliseconds

**Hover over your broken Movie File In TOP. What does the info pop-up say?**

_______________________________________________

> This is your first stop for any broken node. Before anything else — hover and read.

---

### 1.3 — The Info DAT

For more detail, right-click any node → **Info DAT**. This creates a connected DAT that continuously updates with full diagnostic information about that node.

1. Right-click your Movie File In TOP → **Info DAT**
2. Read the contents

**What fields appear in the Info DAT?** ________________________________

**What does the `errors` field say?** ________________________________

> The Info DAT is especially useful for nodes that have intermittent errors — you can watch it update in real time as conditions change.

---

### 1.4 — The Textport

TD has a console — the **Textport**. It logs Python errors, print statements, and system messages.

Open it: **Dialogs** menu → **Textport and DATs** (or press **Alt+T**)

**When does the Textport matter?**
- Any time you're writing Python expressions or scripts
- When a DAT Execute or CHOP Execute fires unexpectedly
- When a node reports a Python error

Type this in the Textport right now to confirm it works:
```python
print("hello from textport")
```

**What appears?** ________________________________

---

### 1.5 — The Error DAT

**Dialogs** → **Error DAT** shows a running log of all errors across your entire project, not just one node.

Open it now. Leave it open in a corner of your workspace whenever you're debugging.

**What is currently listed?** ________________________________

> Get into the habit of having the Error DAT open during sessions. Many errors are silent — the node looks normal from the outside but is producing garbage values. The Error DAT catches them.

---

## Part 2 — The Six Most Common Error Types (20 min)

Each section below describes a common error, how to reproduce it, how to recognise it, and how to fix it. Work through each one.

---

### Error Type 1 — Missing File

**What it looks like:** Movie File In, Audio File In, or GLSL nodes go red. Thumbnail shows a grey or black frame.

**Reproduce it:**
1. Add a **Movie File In TOP**
2. In parameters, type a fake file path: `/fake/path/video.mp4`

**What does the node show?** ________________________________

**How to fix it:**
- Check the **File** parameter — is the path correct?
- Is the file where you think it is? (Use Finder/Explorer to verify)
- Did the file move? TD stores absolute paths — if you reorganise your folders, all file references break
- **Best practice:** Keep all media files in a folder inside your TD project folder, and use **relative paths**: `./media/video.mp4` instead of `/Users/name/Desktop/video.mp4`

**Fix your node.** Point it to a real video file from the class materials.

---

### Error Type 2 — Wrong Input Type

**What it looks like:** A node turns red or shows no output. The info pop-up says something like *"input must be a..."*

**Reproduce it:**
1. Add a **Blur TOP**
2. Try to connect a **Constant CHOP** into it (drag the CHOP output toward the TOP input)

**What happens?** ________________________________

**Why?** The Blur TOP expects a TOP (pixel data) as input. CHOPs carry signal data — a completely different type.

**How to fix it:**
- Check what data type the node expects — look at the input triangle color
- Use a conversion node (**CHOP to TOP**, **Render TOP**, **DAT to CHOP**, etc.) to bridge the gap
- Refer to the Connection Cheat Sheet from Worksheet 2

---

### Error Type 3 — Broken Path Reference

**What it looks like:** A node that uses a path reference (Render TOP, Geometry COMP, MAT) shows a black output or red warning. The parameter field shows a red background.

**Reproduce it:**
1. Add a **Render TOP**
2. In the **Camera** parameter, type `/project1/camera_fake`
3. Look at the parameter field color

**What color does the parameter field turn?** ____________

**How to fix it:**
- The node at that path doesn't exist, or the path is spelled wrong
- Right-click the broken parameter → **Open Viewer** — TD will tell you what it can't find
- Use the **OP Find DAT** (press **[Tab]** → DAT → **OP Find**) to search for nodes by name across your whole project
- Make sure the node you're referencing hasn't been renamed or moved to a different container

**Fix it:** Change the path to a real Camera COMP in your network.

---

### Error Type 4 — Python Expression Error

**What it looks like:** A parameter shows a red or orange background. The Textport shows a traceback. The value the parameter produces may be `0` or the last valid value.

**Reproduce it:**
1. Add a **Constant CHOP**
2. Click the **Value** parameter field
3. Press the **`=`** key to enable expression mode (the field turns green)
4. Type: `me.badattribute * 2`
5. Press Enter

**What does the parameter field show?** ________________________________

**What appears in the Textport?** ________________________________

**How to fix it:**
- Read the traceback — it tells you the exact line and type of error
- Common Python errors in TD:

| Python error | What it usually means |
|---|---|
| `AttributeError` | You referenced something that doesn't exist on that object |
| `TypeError` | You tried to do math on the wrong type (e.g. string × int) |
| `NameError` | You used a variable name that TD doesn't know |
| `ZeroDivisionError` | Something in your expression divided by zero |

- Press the `=` key again to toggle expression mode off and return to a safe value while you debug

**Fix it:** Change the expression to `me.numChans * 2` and confirm it works.

---

### Error Type 5 — Export Lock Mismatch

**What it looks like:** A parameter has a green lock icon but isn't behaving as expected. The value appears frozen or wrong even though the source CHOP is changing.

**Reproduce it:**
1. Add an **LFO CHOP** and a **Null CHOP**, connect them
2. Add a **Constant CHOP** — export the Null to its **Value** parameter
3. Now delete the Null CHOP

**What happens to the Constant CHOP's Value parameter?** ________________________________

**How to fix it:**
- Right-click the parameter with the broken lock → **Remove Export**
- Then re-export from a valid CHOP
- Check that the CHOP you're exporting from is named what you think it is — if you renamed a Null, the export may have silently broken

**Fix it:** Re-add the Null CHOP and re-export.

---

### Error Type 6 — Node Not Cooking

**What it looks like:** A node looks fine — no red, no error — but its output never changes. It's stuck on a single frame or value.

**Common causes:**

1. **Bypass is on** — the node is skipped entirely
   - Check: Is the node visually dimmed?
   - Fix: Press **B** to toggle bypass, or click the Bypass flag in parameters

2. **Cook type is set to "Off"**
   - Check: Select the node → right-click → **Cook Type**
   - Fix: Set to **Always** or **Every Frame**

3. **The Timeline isn't playing**
   - Check: Is the play button pressed at the bottom of TD?
   - Fix: Press **Space** or click the play button

4. **The node is inside a paused container**
   - Check: Navigate up with **U** and look for a container with bypass or cook set to off
   - Fix: Fix the container's cook settings

**Find a node in your network that isn't cooking.** Describe what you found:

_______________________________________________
_______________________________________________

---

## Part 3 — The Upstream Rule (10 min)

This is the single most important debugging principle in TD:

> **Errors travel downstream. Fix them upstream.**

If node F is producing garbage, the problem is rarely in F itself. It started somewhere in A, B, C, D, or E — and propagated forward through every connection.

```
[A] → [B] → [C] → [D] → [E] → [F] ← you're looking here
 ↑
 start here instead
```

### How to trace upstream

1. Look at the broken node (F)
2. Note its inputs — follow the wires backward
3. Middle-click each upstream node to open its viewer
4. Find the **first node where the output looks wrong**
5. That's where the error actually is — fix it there

**Practice:**

Build this broken network on purpose:

1. Add a **Movie File In TOP** — leave file empty (broken)
2. Connect → **Blur TOP**
3. Connect → **Level TOP**
4. Connect → **Out TOP**

**Which nodes look broken?** ________________________________

**Which is the first broken node upstream?** ________________________________

**Fix only the first broken node. What happens to the rest of the network?**

_______________________________________________

---

## Part 4 — Systematic Debugging Procedure (10 min)

When you're stuck, follow this sequence. Don't skip steps.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  STEP 1   Describe the symptom precisely                    │
│           "The sphere is black" not "it's broken"           │
│                                                             │
│  STEP 2   Open the Error DAT                                │
│           Read every entry. Don't dismiss anything.         │
│                                                             │
│  STEP 3   Find the first broken node upstream               │
│           Middle-click each node back through the chain     │
│                                                             │
│  STEP 4   Hover for the info pop-up                         │
│           Read the exact error message on that node         │
│                                                             │
│  STEP 5   Right-click → Info DAT                            │
│           Get the full diagnostic on that node              │
│                                                             │
│  STEP 6   Check the Textport                                │
│           Look for Python tracebacks or print output        │
│                                                             │
│  STEP 7   Isolate — bypass or disconnect nodes              │
│           Find the smallest version of the network          │
│           that still shows the problem                      │
│                                                             │
│  STEP 8   Check the obvious                                 │
│           Is the node bypassed? Is timeline playing?        │
│           Is the file path correct? Is it the right type?   │
│                                                             │
│  STEP 9   Search the TD wiki or forum                       │
│           derivative.ca/wiki — search the exact error text  │
│                                                             │
│  STEP 10  Ask for help — but describe steps 1–8 first       │
│           "I tried X, Y, Z and I see this exact message"    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Why does Step 10 say to describe what you've already tried?**

_______________________________________________
_______________________________________________

---

## Part 5 — Debugging Scenarios (15 min)

Work through each scenario. For each one: describe the symptom, trace upstream, identify the cause, and fix it.

---

### Scenario 1

**Setup:**
1. Add a **Noise TOP**
2. Add a **CHOP to TOP** — connect Noise → CHOP to TOP
3. Add a **Level TOP** — connect CHOP to TOP → Level

**Symptom:** The Level TOP output looks wrong — it's a single color strip, not a noise pattern.

**Why is this happening?**

_______________________________________________

**What is the correct connection?**

_______________________________________________

---

### Scenario 2

**Setup:**
1. Add an **LFO CHOP** with Frequency `0.5`
2. Add a **Math CHOP** — connect LFO → Math
3. In Math, set From Range `-1` to `1`, To Range `0` to `1`
4. Add a **Sphere SOP**
5. Export the Math CHOP to the Sphere's **Radius** parameter

**Symptom:** The sphere is scaling, but it collapses to nothing and then jumps back — it never smoothly grows and shrinks.

**Why is this happening?**

_______________________________________________

**How do you fix it?**

_______________________________________________

---

### Scenario 3

**Setup:**
1. Create a container (press **[Tab]** → COMP → **Base**)
2. Double-click to go inside it
3. Add a **Constant TOP** inside the container
4. Press **U** to go back up to the root level
5. Add a **Null TOP** at the root level
6. Try to connect the Constant TOP to the Null TOP

**Symptom:** You can't make the connection — or the Null TOP stays empty.

**Why?**

_______________________________________________

**How do you get data out of a container to use at the root level?**

_______________________________________________

> **Hint:** Look for an **Out TOP** inside the container.

---

### Scenario 4

**Setup:**
1. Add an **Audio Device In CHOP**
2. Add an **Analyze CHOP** — connect Audio → Analyze, set Function to RMS
3. Add a **Math CHOP** — From Range `0` to `1`, To Range `0` to `100`
4. Export Math CHOP to a **Noise TOP**'s **Period** parameter

**Symptom:** The Period parameter has a green lock icon but the noise pattern never changes, even though you're making sound.

**Step through the debugging procedure. What do you check first?**

_______________________________________________

**What are three possible causes?**

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## Part 6 — Build Your Own Debugging Reference (10 min)

You will encounter errors we haven't covered here. The skill is knowing how to figure out new ones.

Fill this in based on errors you've personally hit today or in previous worksheets:

| Error I hit | What it looked like | What caused it | How I fixed it |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

This becomes your personal error log. Keep adding to it throughout the semester.

---

## Reflect

**1.** In your own words, why do errors travel downstream in TD?

_______________________________________________
_______________________________________________

**2.** What is the difference between the Info pop-up, the Info DAT, and the Error DAT? When do you use each?

_______________________________________________
_______________________________________________
_______________________________________________

**3.** What debugging habit do you most need to build? (Be honest.)

_______________________________________________
_______________________________________________

---

## Quick Reference Card

Cut this out and keep it at your station.

```
┌─────────────────────────────────────────────────────────────┐
│  TD DEBUGGING — QUICK REFERENCE                             │
├─────────────────────────────────────────────────────────────┤
│  NODE STATES                                                │
│  Red border      → Error — hover to read it                 │
│  Yellow border   → Warning — check parameters               │
│  Dimmed          → Bypassed — press B to toggle             │
│  Diagonal lines  → Unloaded — check Cook Type               │
│  Red parameter   → Bad path or broken expression            │
├─────────────────────────────────────────────────────────────┤
│  WHERE TO LOOK                                              │
│  Hover           → Info pop-up (fastest)                    │
│  Right-click     → Info DAT (full detail)                   │
│  Alt+T           → Textport (Python errors)                 │
│  Dialogs menu    → Error DAT (whole project log)            │
├─────────────────────────────────────────────────────────────┤
│  THE UPSTREAM RULE                                          │
│  Errors flow downstream. Always trace back to the           │
│  first broken node. Fix there, not at the symptom.          │
├─────────────────────────────────────────────────────────────┤
│  CHECK THE OBVIOUS FIRST                                    │
│  □ Is the node bypassed?                                    │
│  □ Is the timeline playing?                                 │
│  □ Is the file path correct?                                │
│  □ Is the input the right data type?                        │
│  □ Is the exported CHOP still connected?                    │
│  □ Is the Cook Type set to Always?                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Before You Leave

In your notebook:

> **Write one debugging habit you didn't have before today — and one error you now know how to read.**

---

*IXDSN 3500 — CCA Interaction Design*
