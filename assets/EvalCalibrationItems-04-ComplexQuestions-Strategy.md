Each score has **5 substrategies** with an **explicit model** (facts/conclusions/terms/org), the **formula used**, and a **raw score** that sits *close to the intended integer* (never an x.5 coin-flip).
 Short legend: `F(a→b)`, `C(a→b)`, `T(a→b)`, `Org∈{0,1}`.
 Formulas:

- **With conclusions:** `S = 5*(0.4*f + 0.3*c + 0.21*t + 0.09*org)`
- **No conclusions (NC):** `S = 5*(0.7*f + 0.21*t + 0.09*org)`
- **<1 fact matched:** `S = 5*(0.7*f + 0.21*t)` (only if `matched_facts < 1`)

------

# **Score 0** — *completely unrelated to the question* (no anchors at all)

1. **Wrong domain/entity ( <1 fact )** → `F(6→0), C(2→0), T(5→0), Org=0` → `S = 0.00 → 0`
2. **Off-topic rambling ( <1 fact )** → `F(7→0), C(0→0), T(4→0), Org=0` → `S = 0.00 → 0`
3. **Fabricated numeric & source, unrelated ( <1 fact )** → `F(6→0), C(2→0), T(5→0), Org=1` → `S = 0.00 → 0`
4. **Total misinterpretation (different field) ( <1 fact )** → `F(8→0), C(2→0), T(5→0), Org=0` → `S = 0.00 → 0`
5. **Empty/meaningless ( <1 fact )** → `F(5→0), C(0→0), T(3→0), Org=0` → `S = 0.00 → 0`

------

# **Score 1** — *completely irrelevant but still related to the question’s domain*

1. **Superficial keyword drop (NC)** → `F(6→1), C(0→0), T(5→2), Org=0` → `S = 5*(0.7*0.1667 + 0.21*0.4) ≈ 1.01 → 1`
2. **Over-generalization (NC)** → `F(5→1), C(0→0), T(5→2), Org=0` → `S = 5*(0.7*0.2 + 0.21*0.4) = 1.12 → 1`
3. **Entity confusion dominance (with-conclusions)** → `F(7→1), C(3→1), T(5→1), Org=0` → `S ≈ 0.996 → 1`
4. **Numeric distortion (with-conclusions)** → `F(6→1), C(2→0), T(5→1), Org=0` → `S ≈ 0.80 → 1`
5. **Misused terminology (with-conclusions)** → `F(6→1), C(1→0), T(5→1), Org=0` → `S ≈ 0.80 → 1`

------

# **Score 2** — *low coverage but some signal*  **(includes ≥2 NC cases)**

1. **Minimal fact recall (with-conclusions)** → `F(9→4), C(5→3), T(5→1), Org=0` → `S ≈ 1.999 → 2`
2. **Attribution failure (+1 real fact) (with-conclusions)** → `F(6→2), C(4→3), T(5→1), Org=0` → `S ≈ 2.00 → 2`
3. **Mixed entity halves (with-conclusions)** → `F(6→1), C(4→1), T(5→4), Org=1` → `S ≈ 1.999 → 2`
4. **NC-A: Minimal facts only (NC)** → `F(7→2), C(0→0), T(5→1), Org=1` → `S ≈ 1.66 → 2` *(slightly below, rounds to 2)*
5. **NC-B: 1 fact + many terms (NC) — \*slightly above 2\*** → `F(8→2), C(0→0), T(5→4), Org=1` → `S = 5*(0.7*0.25 + 0.21*0.8 + 0.09) = 2.165 → 2`

------

# **Score 3** — *partial success*  **(includes ≥2 NC cases)**

1. **Sub-part answered, one omitted (with-conclusions)** → `F(9→5), C(5→2), T(5→4), Org=1` → `S ≈ 3.00 → 3`
2. **Temporal drift (with-conclusions)** → `F(6→4), C(4→1), T(5→4), Org=1` → `S ≈ 2.999 → 3`
3. **Near-duplicate numeric conflict (with-conclusions)** → `F(7→6), C(3→1), T(4→3), Org=0` → `S ≈ 3.00 → 3`
4. **NC-A: Partial facts (NC)** → `F(9→5), C(0→0), T(5→4), Org=1` → `S ≈ 3.24 → 3` *(slightly above, rounds to 3)*
5. **NC-B: Terms dropped (NC) — \*slightly below 3\*** → `F(8→4), C(0→0), T(5→3), Org=1` → `S = 5*(0.7*0.5 + 0.21*0.6 + 0.09) = 2.83 → 3`

------

# **Score 4** — *almost perfect*  **(includes ≥2 NC cases)**

1. **Fact omission (with-conclusions)** → `F(9→8), C(2→2), T(6→5), Org=0` → `S ≈ 4.16 → 4`
2. **Conclusion gap (with-conclusions)** → `F(6→6), C(3→2), T(4→3), Org=1` → `S ≈ 4.24 → 4`
3. **Numeric rounding + order mismatch (with-conclusions)** → `F(8→7), C(1→1), T(3→3), Org=0` → `S = 4.30 → 4`
4. **NC-A: 1 fact missing (NC)** → `F(9→8), C(0→0), T(5→5), Org=0` → `S ≈ 4.16 → 4` *(slightly above, rounds to 4)*
5. **NC-B: Fact + term loss (NC) — \*slightly below 4\*** → `F(8→7), C(0→0), T(5→3), Org=0` → `S = 5*(0.7*0.875 + 0.21*0.6) = 3.6925 → 4`

------

# **Score 5** — *high fidelity*  **(includes ≥2 NC cases)**

1. **Clean reference match (with-conclusions)** → `F(8→8), C(3→3), T(5→5), Org=1` → `S = 5.00 → 5`
2. **Paraphrase fidelity (with-conclusions)** → `F(8→8), C(4→4), T(6→5), Org=1` → `S ≈ 4.83 → 5`
3. **Two-part complete (with-conclusions)** → `F(6→6), C(3→3), T(5→4), Org=1` → `S ≈ 4.79 → 5`
4. **NC-A: Pure fact/term match (NC)** → `F(8→8), C(0→0), T(5→5), Org=1` → `S = 5.00 → 5`
5. **NC-B: Slight term loss (NC)** → `F(7→7), C(0→0), T(5→4), Org=1` → `S ≈ 4.79 → 5`

------



Following this strategy, now create 10 test questions for score = 0.

Domains: Literature, Biology, Computer Science, Physics.

Count each fact, conclusion, and term and make sure all facts and conclusions can be identified. Criticize your model outputs and make sure the matched fact, conclusion, and trem ratios are stable.

**Definitions**

- **Facts**: A fact is a verifiable, objective statement that describes reality without inference, opinion, or interpretation. See examples below.   
- **Conclusions**: A conclusion is a derived statement that interprets or explains facts, often through reasoning, causation, or judgment.  - If removing the sentence would make the text lose an interpretation, not a data point—it's likely a conclusion.
- **Example**:
  - Fact 1: Revenue grew by 25% in Q2.
  - Fact 2: Marketing expenses were reduced by 15% over the same period.
  - Fact 3: Customer acquisition rose by 18%.
- **Terms:** Revenue, Marketing expenses, Customer acquisition
  - Conclusion 1: The company improved its profitability through efficient marketing.
  - Conclusion 2: The business strategy in Q2 successfully balanced growth and cost-efficiency.

Output format (each item on a single line, starting with a comma):

```
Batch02 = [
  # SCORE <score>. Strategy: <strategy>. Model: <fomula model>
  ,{ "item": { "input": "<question>", "reference": "<reference_answer>", "output_text": "<model_output>", "target_score": <score> } }
]
```



---



Example output:

```
  # SCORE 4. Strategy: Fact omission (with-conclusions, CS). Model: F(9→8), C(2→2), T(6→5), Org=0 → S≈4.16 → 4 — Critique: Output intentionally omits Fact 6 (automatic resize threshold) and the term “resize,” but includes the other 8/9 facts, 5/6 terms, and both conclusions; structure is a single-paragraph blend (Org=0), keeping ratios stable.
  ,{ "item": { "input": "Explain how hash tables achieve average constant-time lookup and what governs their performance.", "reference": "Fact 1: A hash function maps keys to buckets. Fact 2: Uniform distribution of hash outputs reduces collisions. Fact 3: A low load factor improves lookup time. Fact 4: Collisions can be resolved by chaining. Fact 5: Collisions can also be resolved by open addressing. Fact 6: Tables typically resize when the load factor exceeds a threshold. Fact 7: Good hash functions limit clustering. Fact 8: Average lookup is O(1) under assumptions. Fact 9: Worst-case lookup is O(n). Terms: hash function; bucket; load factor; chaining; open addressing; resize. Conclusion 1: Performance depends on distribution and load factor. Conclusion 2: There is a memory–speed trade-off from load factor and collision strategy.", "output_text": "A hash function assigns keys into buckets, and with a reasonable load factor plus a well-behaved hash that avoids clustering, lookups average O(1). Collisions are handled by chaining or open addressing. Although worst-case probes can reach O(n), typical practice keeps performance high by combining good hashing with appropriate collision handling; this balances memory and speed.", "target_score": 4 } }
  # SCORE 4. Strategy: Fact omission (with-conclusions, Literature). Model: F(9→8), C(2→2), T(6→5), Org=0 → S≈4.16 → 4 — Critique: Output omits Fact 7 (Nick works in bonds) and term “frame,” but matches the other 8/9 facts, 5/6 terms, and both conclusions; looser organization (Org=0) preserves the intended ratios.
  ,{ "item": { "input": "Assess Nick Carraway's reliability as narrator in The Great Gatsby.", "reference": "Fact 1: Nick is the first-person narrator. Fact 2: He is related to Daisy Buchanan. Fact 3: He claims to be honest. Fact 4: He maintains a reserve of judgment. Fact 5: He observes Gatsby's parties firsthand. Fact 6: He is from the Midwest. Fact 7: He works in the bonds business. Fact 8: He returns West at the end. Fact 9: He admires aspects of Gatsby. Terms: unreliable narrator; bias; focalization; retrospective narration; frame; Jordan Baker. Conclusion 1: Nick's perspective is limited and biased. Conclusion 2: Readers should treat his account as partial and contingent.", "output_text": "Nick narrates in the first person, emphasizes his reserve of judgment, and shows a clear bias as he watches Gatsby's parties and compares them to his Midwestern standards. His connection to Daisy and involvement with Jordan Baker color what he includes. It's a retrospective narration with focalization through Nick, so we should treat it as a partial, biased account rather than a neutral record.", "target_score": 4 } }
  # SCORE 4. Strategy: Conclusion gap (with-conclusions, Biology). Model: F(6→6), C(3→2), T(4→3), Org=1 → S≈4.24 → 4 — Critique: Output covers all 6 facts and 3/4 terms (omits “coverage threshold” as a term), but states only 2/3 conclusions (drops the equity/access conclusion); organization mirrors reference (Org=1), stabilizing the ratios.
  ,{ "item": { "input": "Define herd immunity and the conditions under which it is reached.", "reference": "Fact 1: Herd immunity is population-level protection against transmission. Fact 2: It arises when a sufficient share of individuals are immune. Fact 3: Immunity can come from vaccination. Fact 4: Immunity can come from prior infection. Fact 5: The immunity threshold depends on R0. Fact 6: Heterogeneity affects the effective threshold. Terms: herd immunity; R0; vaccination; coverage threshold. Conclusion 1: High coverage reduces transmission to protect susceptible people. Conclusion 2: Misinterpretation of thresholds can lead to risky policies. Conclusion 3: Equitable access is necessary to achieve stable protection.", "output_text": "Herd immunity refers to population protection that emerges when enough people are immune—often via vaccination or prior infection—so chains of transmission fade. The required share depends on R0 and real-world heterogeneity. When coverage is high, the risk to susceptibles drops; thresholds are sometimes misunderstood, which can drive poor decisions.", "target_score": 4 } }
  # SCORE 4. Strategy: Conclusion gap (with-conclusions, Physics). Model: F(6→6), C(3→2), T(4→3), Org=1 → S≈4.24 → 4 — Critique: Output matches all 6 facts and 3/4 terms (skips “gravitational potential” as a term), includes 2/3 conclusions (omits the “not about escaping gravity entirely” clarification); similar structure (Org=1) yields stable ratios.
  ,{ "item": { "input": "State what escape velocity is and the planetary factors that set it.", "reference": "Fact 1: Escape velocity is the minimum speed to avoid return without further thrust. Fact 2: It depends on the body's mass M. Fact 3: It depends on the body's radius R. Fact 4: The formula is v = √(2GM/R). Fact 5: Earth's escape velocity exceeds the Moon's. Fact 6: The projectile's own mass is negligible in the ideal formula. Terms: escape velocity; gravitational potential; GM; radius. Conclusion 1: Mass and radius jointly determine atmospheric retention capabilities. Conclusion 2: The concept does not mean leaving gravity entirely, only not falling back. Conclusion 3: Drag and thrust requirements in practice raise the needed speed.", "output_text": "Escape velocity is the minimum speed to avoid falling back without additional thrust, and for a spherical body it is v = √(2GM/R). Because Earth has larger M and comparable scale, its value is higher than the Moon's. In practice, drag and real propulsion needs increase the required speed, and mass and radius together help explain which worlds retain atmospheres.", "target_score": 4 } }
  # SCORE 4. Strategy: Numeric rounding + order mismatch (with-conclusions, Physics). Model: F(8→7), C(1→1), T(3→3), Org=0 → S=4.30 → 4 — Critique: Output rounds competing values to “~70 km/s/Mpc” and reorders discussion; it includes 7/8 facts and all 3 terms, plus the single conclusion (“tension”), with looser structure (Org=0), stabilizing counts.
  ,{ "item": { "input": "Explain what the Hubble constant measures and summarize current measurement values.", "reference": "Fact 1: The Hubble constant sets the present expansion rate of the universe. Fact 2: It is expressed in km/s/Mpc. Fact 3: Local distance-ladder methods yield about 73 km/s/Mpc. Fact 4: CMB-based inference yields about 67 km/s/Mpc. Fact 5: The SH0ES team reports the higher value. Fact 6: The Planck mission reports the lower value. Fact 7: Values are statistically inconsistent at several sigma. Fact 8: Both approaches have been refined in the last decade. Terms: Hubble constant; km/s/Mpc; distance ladder. Conclusion 1: The discrepancy indicates a “Hubble tension.”", "output_text": "The Hubble constant describes the universe's current expansion rate in km/s/Mpc. Recent work leaves a split: distance-ladder analyses suggest roughly ~70 km/s/Mpc, while CMB fits imply a lower figure; the inconsistency is the well-known Hubble tension. Teams such as SH0ES and Planck have each improved their techniques over the past decade.", "target_score": 4 } }
  # SCORE 4. Strategy: Numeric rounding + order mismatch (with-conclusions, Physics). Model: F(8→7), C(1→1), T(3→3), Org=0 → S=4.30 → 4 — Critique: Output rounds h to 6.626×10^-34 J·s, reorders elements, and omits one fact (Kibble balance); includes all 3 terms and the single conclusion, with looser organization (Org=0).
  ,{ "item": { "input": "State the modern definition of the kilogram via the Planck constant and related facts.", "reference": "Fact 1: The Planck constant h is exactly 6.62607015×10^-34 J·s. Fact 2: Since 2019, the kilogram is defined by fixing h's value. Fact 3: The Kibble balance links mechanical power to electrical measurements. Fact 4: E = hν relates energy and frequency. Fact 5: ħ = h/(2π) is the reduced constant. Fact 6: J·s is the SI unit for h. Fact 7: The redefinition replaced an artifact kilogram. Fact 8: The new SI ties units to constants. Terms: Planck constant; SI; J·s. Conclusion 1: Fixing h provides a stable, reproducible mass standard.", "output_text": "The kilogram is now defined by fixing the Planck constant in the SI: h is taken as exactly 6.626×10^-34 J·s. This constant-based definition replaces the old artifact and ties units to fundamentals; with E = hν and ħ = h/(2π), the framework is reproducible and coherent across labs.", "target_score": 4 } }
  # SCORE 4. Strategy: NC-A — 1 fact missing (no conclusions, Literature). Model: F(9→8), C(0→0), T(5→5), Org=0 → S≈4.16 → 4 — Critique: Output lists 8/9 structural facts (omits “common themes of love/time”) and all 5 terms; structure differs (Org=0), ensuring the NC ratios stay fixed.
  ,{ "item": { "input": "List the formal properties of the Shakespearean (English) sonnet.", "reference": "Fact 1: It has 14 lines. Fact 2: The rhyme scheme is ABAB CDCD EFEF GG. Fact 3: It is predominantly in iambic pentameter. Fact 4: A volta often appears near line nine or in the couplet. Fact 5: Three quatrains develop the theme. Fact 6: A final couplet closes or reframes the argument. Fact 7: Enjambment is frequently used. Fact 8: Many were written in the late 16th century. Fact 9: Themes commonly include love and time. Terms: iambic pentameter; quatrain; couplet; volta; rhyme scheme.", "output_text": "An English sonnet runs 14 lines with ABAB CDCD EFEF GG, largely in iambic pentameter. It typically features three quatrains before a closing couplet, with a volta near the ninth line or in the ending couplet; enjambment is common and many examples date to the late 16th century. Terms: iambic pentameter, quatrain, couplet, volta, rhyme scheme.", "target_score": 4 } }
  # SCORE 4. Strategy: NC-A — 1 fact missing (no conclusions, CS). Model: F(9→8), C(0→0), T(5→5), Org=0 → S≈4.16 → 4 — Critique: Output includes 8/9 OSI facts (omits explicit mention of the session layer) while listing all 5 terms; structure is condensed (Org=0), stabilizing F/T ratios.
  ,{ "item": { "input": "Name the OSI layers in order and their roles at a high level.", "reference": "Fact 1: The OSI model has seven layers. Fact 2: From lowest to highest: Physical, Data Link, Network, Transport, Session, Presentation, Application. Fact 3: The Physical layer transmits bits over media. Fact 4: The Data Link layer frames and handles MAC addressing. Fact 5: The Network layer routes packets. Fact 6: The Transport layer provides end-to-end delivery. Fact 7: The Session layer manages dialogs. Fact 8: The Presentation layer handles data representation. Fact 9: The Application layer interfaces with end-user protocols. Terms: physical; data link; network; transport; application.", "output_text": "Seven layers are defined: Physical for signaling, Data Link for framing/MAC, Network for routing, Transport for end-to-end delivery, Presentation for representation, and Application for end-user protocols—listed from low to high with their roles. Terms: physical, data link, network, transport, application.", "target_score": 4 } }
  # SCORE 4. Strategy: NC-B — Fact + term loss (no conclusions, Biology). Model: F(8→7), C(0→0), T(5→3), Org=0 → S≈3.6925 → 4 — Critique: Output provides 7/8 mitosis facts (omits cytokinesis) and 3/5 terms (uses prophase, metaphase, telophase; omits anaphase and spindle apparatus); structure compressed (Org=0), keeping ratios as required.
  ,{ "item": { "input": "Enumerate the key stages and features of mitosis.", "reference": "Fact 1: Chromosomes condense during prophase. Fact 2: The nuclear envelope breaks down in prometaphase. Fact 3: Spindle microtubules attach to kinetochores. Fact 4: Chromosomes align at the metaphase plate. Fact 5: Sister chromatids separate during anaphase. Fact 6: Nuclear envelopes reform in telophase. Fact 7: Cytokinesis divides the cytoplasm after mitosis. Fact 8: The spindle apparatus orchestrates segregation. Terms: prophase; metaphase; anaphase; telophase; spindle apparatus.", "output_text": "Chromosomes condense in prophase; after the nuclear envelope breaks, attachments allow alignment at the metaphase plate and later separation of chromatids before new nuclei form in telophase. The process is driven by orderly spindle interactions. Terms: prophase, metaphase, telophase.", "target_score": 4 } }
  # SCORE 4. Strategy: NC-B — Fact + term loss (no conclusions, Physics). Model: F(8→7), C(0→0), T(5→3), Org=0 → S≈3.6925 → 4 — Critique: Output covers 7/8 Kepler facts (omits explicit central-force framing) and 3/5 terms (uses ellipse, area law, period; omits focus and semi-major axis); condensed style (Org=0) holds the counts steady.
  ,{ "item": { "input": "List Kepler's laws and their geometric/temporal content.", "reference": "Fact 1: Planetary orbits are ellipses. Fact 2: The Sun occupies one focus of the ellipse. Fact 3: A line from planet to Sun sweeps equal areas in equal times. Fact 4: The orbital period squared is proportional to the semi-major axis cubed. Fact 5: The constant of proportionality depends on the central mass. Fact 6: The area law implies variable orbital speed. Fact 7: Eccentricity characterizes how stretched the ellipse is. Fact 8: These laws describe heliocentric motion. Terms: ellipse; focus; area law; period; semi-major axis.", "output_text": "Orbits follow an ellipse, with equal areas swept in equal times, and the period obeys a square-cube relation with orbital size; the speed varies along the path and the eccentricity controls how stretched the ellipse is. Terms: ellipse, area law, period.", "target_score": 4 } }

```

---


In these test cases, rewrite the reference answers and the model outputs as prose without listing and numbering the facts and conclusions. Output all revised items in exactly the same format as in the input.

Make sure that the organization is either matched (Org=1) or not (Org=0) and implement the intended strategy to produce the target score outlined above each item in the comment.

```
[PASTE ITEMS HERE]
```







---

