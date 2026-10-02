# Review Template (for the deck's creator)

Copy the block below into a new file named `<Deck> - Review.md`, replace every `<...>`, and delete
the parts you do not need. Keep it short and checkable. Leave out teaching scripts.

---

```markdown
# Review - <deck name>

**File reviewed:** `<name>.pptx` · <N> slides · <Q> questions
**Method:** every question solved independently before comparing with the key. Figures
(<list them>) read from rendered slides, not from the answer text.

**Verdict: <all N keys correct / N-k keys correct>.** <One sentence on what needs fixing.>

| Severity | Count | Items |
|---|---|---|
| 🔴 Content error | n | Q_ (slide _) |
| 🟠 Solution-slide error | n | slide _, slide _ |
| 🟡 Cosmetic | n | listed below |

## Inventory
| # | Slides | Section | Topic | Key | Status |
|---|---|---|---|---|---|

## 🔴 1. <One-line defect title naming the slides>

**The contradiction / The error**

| Source | Statement |
|---|---|
| **Slide _**, <where> | "<quoted word for word>" |
| **Slide _**, <where> | "<quoted word for word>" |

<One line joining the evidence.>

**Consequence:** <what it does to a student; walk all options if "no correct option">.

**Recommended fix (smallest possible change):** <exact replacement text>. Does not touch <...>.

**Alternative considered, not recommended:** <the alternative>. It works, but <disqualifying reason>.

**Also present in <other deck>?** <Both files need the edit.>

## 🟠 2. Slide _: <one-line title>
<Quote the slide, state the error, give the correct working, recommend.>

## 🟡 Cosmetic (none affect correctness)
| # | Slide | Issue | Suggested |
|---|---|---|---|

## Action required before <date>
1. ...
2. ...
The cosmetic list can wait for the next revision.
```

---

## Worked example (fictional)

> Everything below is invented to show the style. It is not from any real deck.

# Review - Grade 7 Practice Test: Motion and Light

**File reviewed:** `G7-Motion-and-Light.pptx` · 24 slides · 8 questions
**Method:** every question solved independently before comparing with the key. Figures
(Q2 ray diagram, Q5 distance-time graph) read from rendered slides, not from the answer text.

**Verdict: 7 of 8 keys correct.** Q5 has no correct option as printed; one solution slide has an arithmetic slip.

| Severity | Count | Items |
|---|---|---|
| 🔴 Content error | 1 | Q5 (slides 14-15) |
| 🟠 Solution-slide error | 1 | slide 9 |
| 🟡 Cosmetic | 2 | listed below |

## 🔴 1. Q5 (slides 14-15): no option gives the average speed

**The error**

| Source | Statement |
|---|---|
| **Slide 14**, stem | "A cyclist covers 12 km in 30 minutes, then 8 km in 30 minutes. Find the average speed." |
| **Slide 14**, options | (A) 8 km/h (B) 10 km/h (C) 12 km/h (D) 40 km/h |
| **Slide 15**, working | "Total distance 20 km, total time 1 h, so average speed = 20 ÷ 2 = 10 km/h" |

The total time is 1 h, so the average speed is 20 km/h. The slide divides by 2.

**Consequence:** (A) ✗ is the second leg's distance read as a speed. (B) ✗ is the keyed answer
and comes from the slip above. (C) ✗ is the first leg's distance read as a speed. (D) ✗ is 20 ÷ 0.5,
using one leg's time. The correct value, 20 km/h, is not on offer. (B) is still the intended key, but it is wrong.

**Recommended fix (smallest possible change):** change option (B) to **20 km/h** and fix the
working on slide 15 to "20 km ÷ 1 h = 20 km/h". Options A, C and D stay, and each still tests a
real slip (distance read as speed, one leg's time used). Q6 is untouched.

**Alternative considered, not recommended:** change the stem to "8 km in 1 hour" so that 10 km/h
is right. It works, but it makes Q5 identical in structure to the worked example on slide 6,
which would let students pattern-match instead of think.

## 🟠 2. Slide 9: Q3 working contradicts the boxed answer
Slide 9 shows "angle of reflection = 40°" in step 2 and "= 50°" in the box. The correct value is
50° (the angle with the *surface* is 40°; the angle with the *normal* is 50°). Change step 2 to 50°.

## 🟡 Cosmetic (none affect correctness)
| # | Slide | Issue | Suggested |
|---|---|---|---|
| 1 | 3 | "a hour" | "an hour" |
| 2 | 20 | Option letter missing on the answer slide | Add "(C)" |

## Action required before the test
1. Q5: change option (B) to 20 km/h and fix slide 15.
2. Slide 9: change "40°" to "50°" in step 2.
The cosmetic list can wait for the next revision.
