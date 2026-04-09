# TouchDesigner: Concept → Network
### From Interaction Idea to Node Diagram
#### IXDSN 3500 — Emerging Technologies

**Time:** ~90 minutes | **Work in pairs, build individually**

---

## What This Worksheet Is About

Most TD tutorials start with nodes and work toward an effect. This one works the other way: **you start with an idea and figure out what nodes you need.**

This is the skill that separates people who can follow tutorials from people who can build original work. It's harder — and more useful.

By the end, you'll have translated one of your own interaction concepts into a working network using a structured thinking method you can apply to any project.

---

## The Method

Every interactive system — no matter how complex — answers four questions:

```
1. INPUT     What triggers this? What does it listen to?
2. ANALYZE   What do I extract from that input?
3. TRANSFORM How do I shape that data into something useful?
4. OUTPUT    What does it affect? What does the audience experience?
```

Before you touch TouchDesigner, you answer these four questions on paper. Then you build.

---

## Part 1 — See the Method in Action (15 min)

Here are three worked examples. Read each one and fill in the node column.

---

### Example A — Heartbeat Room

**Concept:** A room that breathes in and out with your pulse. A participant holds a sensor. Their heart rate makes the walls slowly expand and contract.

| Step | Question answered | Data type | Node(s) to use |
|---|---|---|---|
| Input | Heart rate sensor via OSC | CHOP | OSC In CHOP |
| Analyze | Extract BPM as a single number | CHOP | Select CHOP |
| Transform | Convert BPM to a slow oscillation | CHOP | ________________ |
| Output | Drive scale of geometry in 3D scene | SOP/COMP | ________________ |

**What CHOP would you use to convert a BPM number into a smooth oscillating signal?**

_______________________________________________

---

### Example B — Whisper Wall

**Concept:** A wall of text that reacts to your voice. The louder you speak, the more the words scatter and blur. Silence brings them back together.

| Step | Question answered | Data type | Node(s) to use |
|---|---|---|---|
| Input | Microphone | CHOP | Audio Device In CHOP |
| Analyze | Overall volume level | CHOP | Analyze CHOP (RMS) |
| Transform | Smooth + remap to 0–1 | CHOP | Filter → Math CHOP |
| Output | ________________ | TOP | ________________ |

**What TOP operator would let you blur or displace a texture based on a value?**

_______________________________________________

---

### Example C — Shadow Mirror

**Concept:** A camera tracks your silhouette. Your shadow is reflected back at you — but delayed by 5 seconds and gradually fading.

| Step | Question answered | Data type | Node(s) to use |
|---|---|---|---|
| Input | ________________ | TOP | ________________ |
| Analyze | Isolate silhouette | TOP | ________________ |
| Transform | Delay 5 seconds + fade over time | TOP | ________________ |
| Output | Display on screen | TOP | Out TOP |

**What TD node holds onto frames of video so you can play them back with a delay?**

_______________________________________________

---

### What do you notice across all three examples?

Look at the pattern. In every example:
- The **Input** is almost always a __________ or __________
- The **Analyze** step almost always lives in __________
- The **Output** is almost always a __________ or __________

---

## Part 2 — Deconstruct Before You Build (20 min)

Work with your partner. Choose **one** of the concepts below — or propose your own (get approval first).

### Option A — Breath Landscape
The camera watches your chest. When you inhale, a landscape slowly rises. When you exhale, it falls. The system only responds to slow, deliberate breathing — rapid movement is ignored.

### Option B — Crowd Murmur
A microphone listens to the ambient noise in the room. Low murmur = a calm, cool visual. As the room gets louder, the visual becomes more agitated and warm. At peak volume, it fragments entirely.

### Option C — Memory Trace
Every time someone moves in front of the camera, their silhouette is added to a growing composite image — ghosted, semi-transparent. Over time, the accumulation of everyone who passed through becomes visible.

### Option D — Your Own Concept
Describe it here first:

_______________________________________________
_______________________________________________
_______________________________________________

---

### Deconstruction Table

Fill this in **before opening TouchDesigner.**

| Step | Question | Your answer |
|---|---|---|
| **Input** | What does the system listen to or sense? | |
| | What hardware or source provides this? | |
| | What TD node brings this data in? | |
| **Analyze** | What do you extract from the raw input? | |
| | What is the data type of what you extract? | |
| | What node does the analysis? | |
| **Transform** | What shaping does the data need? (smoothing, remapping, delaying, combining...) | |
| | What is the value range you need at the end of this step? | |
| | What node(s) does the transformation? | |
| **Output** | What does the audience see, hear, or feel? | |
| | What parameter drives the effect? | |
| | What node produces the final output? | |

---

### Node Diagram — Draw It

In the space below (or on paper), sketch your network as boxes and arrows **before you build it.** Label each box with a node name and each arrow with a data type.

```
 ┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────┐
 │          │──────►│          │──────►│          │──────►│          │
 │          │       │          │       │          │       │          │
 └──────────┘       └──────────┘       └──────────┘       └──────────┘
  data type: ____    data type: ____    data type: ____    data type: ____


 ┌──────────┐       ┌──────────┐
 │          │──────►│          │
 │          │       │          │
 └──────────┘       └──────────┘
  data type: ____    data type: ____
```

**Nodes I'm not sure about yet:**

_______________________________________________
_______________________________________________

**Assumptions I'm making that might be wrong:**

_______________________________________________
_______________________________________________

---

## Part 3 — Build It (30 min)

Open TouchDesigner and build from your diagram. Follow this order:

### Build sequence

**1. Input first**
Get your source working and verify data is flowing before adding anything else. Middle-click the input node — confirm you see movement or values changing.

- Input node working? ✓ ___

**2. Analyze next**
Add the analysis step. Confirm you're extracting what you expected.

- What value are you getting? ________________________________
- Is it in the range you expected? ________________________________

**3. Transform**
Add your shaping nodes. Check after each one — don't add the next until the current step looks right.

- After remapping, what is your value range? ________________________________
- Did you add a Null CHOP as a stable export point? ✓ ___

**4. Output last**
Build the visual output. Export your CHOP value to the parameter. Verify the connection.

- What parameter did you export to? ________________________________
- Does the output respond to the input? ✓ ___

---

### What broke, and what did you do?

| Problem you hit | What you tried | What worked |
|---|---|---|
| | | |
| | | |
| | | |

---

### Compare your diagram to your built network

Look at the diagram you drew in Part 2 and your actual TD network side by side.

**What is different between your plan and what you built?**

_______________________________________________
_______________________________________________

**What node did you not anticipate needing?**

_______________________________________________

**What node did you plan for but not end up using?**

_______________________________________________

---

## Part 4 — Stress Test (10 min)

A working network isn't finished — it's a starting point. Try each of these and note how your system responds.

**1.** Push the input to its extreme — max volume, very fast movement, or very bright light. Does the output behave? Does it clip, freeze, or go black?

_______________________________________________

**2.** Do the opposite — give it the minimum input (silence, stillness). Does the output settle gracefully?

_______________________________________________

**3.** Disconnect the input node. Does the rest of the network fail gracefully or produce errors?

_______________________________________________

**4.** What would you want to add to make this more robust or expressive?

_______________________________________________
_______________________________________________

---

## Part 5 — Present to Your Partner (5 min each)

Take turns. You have 5 minutes to explain your network to your partner. Cover:

- **What the interaction is** — what does the audience do and what happens?
- **What the data does** — trace the signal from input to output
- **One thing that didn't work as planned** — and how you resolved it

Your partner's job is to ask one question you haven't answered yet.

**Your partner's question:**

_______________________________________________

**Your answer (or: what you'd need to figure out):**

_______________________________________________
_______________________________________________

---

## Part 6 — Reflect (10 min)

**1.** What is the hardest part of this method — concept, deconstruction, or building? Why?

_______________________________________________
_______________________________________________

**2.** What node did you discover today that you want to remember for your project?

_______________________________________________

**3.** Looking at your final network, what would you do differently if you started over?

_______________________________________________
_______________________________________________

**4.** Write one sentence that describes your interaction concept to someone who has never used TouchDesigner:

_______________________________________________
_______________________________________________

---

## Part 7 — Stretch (if you finish early)

- **Add a second input layer.** If you used audio, add camera motion too — combine them with a **Math CHOP** to make the system react to both simultaneously.
- **Add a feedback loop.** Connect your output back into an earlier part of the chain using a **Feedback TOP** or **Trail CHOP**. What happens to the behavior over time?
- **Make it fail gracefully.** Add a **Limit CHOP** to cap your values so nothing goes out of range. Add a **Null CHOP** at every major junction so you can inspect the signal at any point.
- **Document your network.** Add **Text DAT** nodes next to each major section with a comment explaining what it does. You should be able to hand this network to someone else and have them understand it.

---

## Reference — The Four Questions

Print or copy this. Use it every time you start a new project.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. INPUT      What does the system sense?                  │
│                → Almost always a CHOP or TOP               │
│                                                             │
│  2. ANALYZE    What do I extract from the raw input?        │
│                → Usually a CHOP (Analyze, Select, Filter)   │
│                                                             │
│  3. TRANSFORM  How do I shape the data I need?              │
│                → Math, Lag, Limit, Logic, Merge CHOPs       │
│                                                             │
│  4. OUTPUT     What does the audience experience?           │
│                → TOP (visual), SOP/COMP (3D), Audio (CHOP)  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Bridge nodes — when you need to cross families:**

| From | To | Use |
|---|---|---|
| CHOP | TOP parameter | Export CHOP |
| CHOP | TOP pixels | CHOP to TOP |
| TOP | CHOP | TOP to CHOP |
| SOP | TOP | Render TOP |
| DAT | CHOP | DAT to CHOP |

---

## Common Stuck Points

| You're stuck because... | Try this |
|---|---|
| You don't know which node does X | Tab → search by function, not name. Also: [derivative.ca/wiki](https://derivative.ca/wiki) |
| Your value isn't in the right range | Add a Math CHOP and adjust From/To Range |
| The output isn't responding | Check the export — select the target node and look for the green lock icon on the parameter |
| The system reacts but feels wrong | Adjust Filter or Lag CHOP — the feeling is in the smoothing |
| The network works but you can't explain it | Slow down and trace each wire — what data type, what value range, at every step |

---

## Before You Leave

On a sticky note:

> **Write your four-question answer for your next project idea — even if you don't know all the nodes yet.**
>
> Input: ________________________________
> Analyze: ________________________________
> Transform: ________________________________
> Output: ________________________________

Bring this to next class.

---

*IXDSN 3500 — CCA Interaction Design*
