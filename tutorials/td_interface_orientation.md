# TouchDesigner: Interface Orientation
### IXDSN 3500 — Emerging Technologies

**Time:** ~90 minutes | **Team size:** Work individually, compare with your partner

---

## What You're Building

By the end of this worksheet you will have a simple working network that generates a moving visual — noise driving a shape — displayed in a viewer window. Nothing fancy. The goal is to get comfortable moving around the interface before we build anything complex.

---

## Part 1 — The Big Picture (10 min)

Open TouchDesigner. Before you click anything, look at what's on screen.

TouchDesigner is a **node-based** environment. Instead of writing code line by line, you connect **nodes** together. Data flows from left to right through those connections, like water through pipes.

**Locate these four areas on your screen and label them on the diagram below:**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   A: ________________________________________________   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│   B: ________________________________________________   │
│                                                         │
│                                                         │
├──────────────────────────────┬──────────────────────────┤
│                              │                          │
│   C: ________________________│   D: ___________________  │
│                              │                          │
└──────────────────────────────┴──────────────────────────┘
```

> **Hint:** The four areas are — *Network Editor, Viewer, Parameter Panel, Palette*

---

## Part 2 — The Operator Families (15 min)

Every node in TouchDesigner is called an **Operator** (or **OP**). There are four families. Each family handles a different type of data and has its own color.

Fill in the table as you explore. Use the [Tab] key in the Network Editor to open the OP Create Dialog and browse around.

| Color | Family Name | Abbreviation | What kind of data? | One example OP you found |
|-------|-------------|--------------|-------------------|--------------------------|
| Purple | | TOP | | |
| Green | | CHOP | | |
| Blue | | SOP | | |
| Dark grey | | DAT | | |

**A useful mental model:** Think of these like different departments in a studio.
- **TOPs** are the art department — pixels, images, video
- **CHOPs** are the music department — signals, numbers that change over time
- **SOPs** are architecture — 3D geometry and shapes
- **DATs** are the office — text, tables, scripts

> **Quick check:** If you wanted to work with a live webcam feed, which family would you use? ____________

---

## Part 3 — Navigation (10 min)

Practice these controls until they feel automatic. Check each one off as you get comfortable.

**In the Network Editor:**

- [ ] **Middle mouse button drag** — pan around the network
- [ ] **Scroll wheel** — zoom in and out
- [ ] **H key** — fit everything into view (Home)
- [ ] **Tab key** — open the OP Create Dialog
- [ ] **Click a node** — select it and see its parameters on the right
- [ ] **U key** — go up one level (out of a container)
- [ ] **Double-click a node** — go inside it (if it's a container)

**In the Viewer:**

- [ ] **Right-click drag** — rotate (in 3D viewers)
- [ ] **Middle mouse drag** — pan
- [ ] **Scroll** — zoom

> **Note:** If your middle mouse button isn't working, hold **Alt + drag** as an alternative.

---

## Part 4 — Build Your First Network (30 min)

Follow these steps in order. Each step adds one node and connects it to the previous one.

### Step 1 — Create a Noise TOP

1. Click in an empty area of the Network Editor
2. Press **[Tab]** to open the OP Create Dialog
3. Click **TOP** at the top to filter to texture operators
4. Find **Noise** and click it — a purple node appears
5. Click on the node to select it
6. In the Parameter Panel (right side), change **Period** to `0.5`

**What do you see in the node's thumbnail?** ________________________________

---

### Step 2 — Create a Level TOP

1. Press **[Tab]** again
2. Find **Level** (under TOP)
3. Place it to the right of your Noise node
4. **Connect them:** hover over the right edge of the Noise node until you see an output handle, then drag to the left edge of the Level node
5. In Level's parameters, bring **Brightness** up to `1.2`

**What changed in the output?** ________________________________

---

### Step 3 — Create a Geometry SOP

Now we'll add a 3D shape.

1. Press **[Tab]**, switch to **SOP**
2. Add a **Sphere** SOP (it will be blue)
3. Place it below your TOPs — SOPs live separately from TOPs
4. In the Sphere parameters, change **Rows** to `40` and **Cols** to `40`

---

### Step 4 — Create a Geo COMP and link your SOP

1. Press **[Tab]**, switch to **COMP**
2. Add a **Geo** component
3. Connect your Sphere SOP into the Geo component
4. Now right-click on the Geo component → **Viewer** — a floating 3D viewer appears

**What does the sphere look like?** ________________________________

---

### Step 5 — Drive the Sphere with Noise

Now connect your visual (TOP) to the geometry (SOP) to make the sphere react to the noise pattern.

1. Select the **Sphere** SOP
2. In its parameters, find the **Material** or **Texture** field
3. Type the path to your Level TOP — it should look like `/project1/level1`

> **Tip:** You can find any node's path by selecting it and looking at the bottom of the interface, or right-clicking → **Info**.

**Does the texture appear on the sphere?** Yes / No / Partially

If it's not working — what did you try? ________________________________

---

### Step 6 — Make it Move

1. Select your **Noise** TOP
2. In the parameters, find **Transform → Translate X**
3. Right-click on the parameter name → **Export CHOP**

Or try the simpler approach:
- Click the parameter field and type: `absTime.seconds * 0.1`

**What is `absTime.seconds`?** ________________________________

> **Hint:** It's a TouchDesigner built-in expression. What does it count?

---

## Part 5 — Reflect (10 min)

Answer these with your partner. Write your answers — you'll use them in the group share.

**1.** In your own words, what is the difference between a CHOP and a TOP?

_______________________________________________
_______________________________________________

**2.** What does "connecting nodes" actually do? What is flowing between them?

_______________________________________________
_______________________________________________

**3.** Where did you get stuck in Part 4? What did you do about it?

_______________________________________________
_______________________________________________

**4.** One thing that surprised you about how TouchDesigner works:

_______________________________________________
_______________________________________________

---

## Part 6 — Stretch (if you finish early)

Try one or more of these on your own:

- **Add a Camera COMP and a Render TOP** to create a proper 3D render of your sphere
- **Add a second Noise TOP** with different settings and use a **Composite TOP** to blend them together
- **Change your Sphere SOP** to a **Torus SOP** or **Grid SOP** — what happens to the texture?
- **Export your Noise TOP's brightness** as a CHOP signal and use it to drive the sphere's **Scale** parameter

---

## Vocabulary to Know

| Term | Definition |
|------|------------|
| Operator (OP) | A single node that processes data |
| Network | A collection of connected operators |
| Cook | What TD calls "processing" — a node cooks when it calculates its output |
| Parameter | A setting on an operator that controls its behavior |
| Path | The address of a node in the network (like `/project1/noise1`) |
| Expression | A small piece of code typed into a parameter field |
| Wire / Connection | The line between two operators that carries data |

---

## Before You Leave

On a sticky note or in your notebook, write:

> **One thing I can do in TouchDesigner now that I couldn't do 90 minutes ago.**

You'll share this with the group.

---

*IXDSN 3500 — CCA Interaction Design*
