# SCORE 3. Strategy: NC-A Partial facts (no conclusions). Model: F(9→5), C(0→0), T(5→4), Org=1 → S≈3.24 → 3
# Critique: Output matches five facts (14 lines; ABAB CDCD EFEF GG; iambic pentameter; couplet closes; quatrains develop aspects) and four terms (“iambic pentameter; volta; couplet; quatrain”), omitting “conceit”.

# Test item with hints
{ "item": {
  "input": "Detail the formal features of the Shakespearean (English) sonnet."
  ,"reference": "
    Fact 1: The English sonnet has 14 lines.
    Fact 2: The rhyme scheme is ABAB CDCD EFEF GG.
    Fact 3: Iambic pentameter predominates.
    Fact 4: A volta commonly appears near line nine or in the couplet.
    Fact 5: The final couplet closes or reframes the argument.
    Fact 6: Three quatrains develop aspects of the theme.
    Fact 7: Many were written in the late 16th century.
    Fact 8: Extended metaphors (conceits) are common.
    Fact 9: Sonnets use tight logical turns.
    Terms: iambic pentameter; volta; couplet; quatrain; conceit."
  ,"output_text": "
    An English sonnet runs 14 lines with ABAB CDCD EFEF GG, written largely in iambic pentameter.
    Three quatrains set up material and the closing couplet resolves or pivots the claim; a volta is often associated with that turn."
  , "target_score": 3 }
}

# Final test item
{ "item": {
  "input": "Detail the formal features of the Shakespearean (English) sonnet."
  ,"reference": "
    The English sonnet comprises 14 lines with the rhyme scheme ABAB CDCD EFEF GG, and the prevailing meter is iambic pentameter.
    A volta commonly appears near the ninth line or in the couplet; three quatrains develop facets of a theme before a final couplet closes or reframes the argument.
    Many examples date to the late sixteenth century, and extended metaphors—conceits—often carry the poem's logic through tight turns.
    Key terms include iambic pentameter, volta, couplet, quatrain, and conceit."
  ,"output_text": "
    An English sonnet runs 14 lines with ABAB CDCD EFEF GG, written largely in iambic pentameter.
    Three quatrains set up material and the closing couplet resolves or pivots the claim; a volta is often associated with that turn."
  ,"target_score": 3 }
}


# SCORE 4. Strategy: Conclusion gap (with-conclusions, Physics). Model: F(6→6), C(3→2), T(4→3), Org=1 → S≈4.24 → 4
# Critique: Output matches all 6 facts and 3/4 terms (skips “gravitational potential” as a term), includes 2/3 conclusions (omits the “not about escaping gravity entirely” clarification); similar structure (Org=1) yields stable ratios.

# Test item with hints
{ "item": {
  "input": "State what escape velocity is and the planetary factors that set it."
  ,"reference": "
  Fact 1: Escape velocity is the minimum speed to avoid return without further thrust.
  Fact 2: It depends on the body's mass M.
  Fact 3: It depends on the body's radius R.
  Fact 4: The formula is v = √(2GM/R).
  Fact 5: Earth's escape velocity exceeds the Moon's.
  Fact 6: The projectile's own mass is negligible in the ideal formula.
  Terms: escape velocity; gravitational potential; GM; radius.
  Conclusion 1: Mass and radius jointly determine atmospheric retention capabilities.
  Conclusion 2: The concept does not mean leaving gravity entirely, only not falling back.
  Conclusion 3: Drag and thrust requirements in practice raise the needed speed."
  ,"output_text": "
  Escape velocity is the minimum speed to avoid falling back without additional thrust, and for a spherical body it is v = √(2GM/R).
  Because Earth has larger M and comparable scale, its value is higher than the Moon's.
  In practice, drag and real propulsion needs increase the required speed, and mass and radius together help explain which worlds retain atmospheres.",
  "target_score": 4 }
}

# Final test item
,{ "item": {
  "input": "State what escape velocity is and the planetary factors that set it."
  ,"reference": "
    Escape velocity is the minimum speed required for a body to avoid returning without further thrust.
    For an ideal spherical mass, the value depends on the planet's mass M and radius R with v = √(2GM/R); the projectile's own mass does not appear in this ideal formula, and Earth's escape speed is greater than the Moon's.
    In practice, drag and propulsion needs increase the operational requirement.
    Mass and radius together help explain which worlds retain atmospheres, the concept does not imply leaving gravity entirely but rather not falling back, and engineering constraints raise the needed speed beyond the ideal."
  ,"output_text": "
    Escape velocity is the minimum speed to avoid falling back without additional thrust, and for a spherical body it is v = √(2GM/R).
    Because Earth has larger M and comparable scale, its value is higher than the Moon's.
    In practice, drag and real propulsion needs increase the required speed, and mass and radius together help explain which worlds retain atmospheres."
  ,"target_score": 4 }
}
