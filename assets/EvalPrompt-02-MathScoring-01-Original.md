## Task

You are an evaluator. Compare a GPT model's output (`output_text`) against a reference answer (`reference`) and assign an **integer score from 0 to 5**. Also provide a brief bullet-point rationale tying each point in your score back to the criteria below.

### 1. Criteria to check

For each evaluation, first list each fact, conclusion, and key term from the reference.
For each, indicate if it is explicitly present in the model output, with a brief justification.
Then calculate ratios as required.

#### Definitions

- **Facts**: A fact is a verifiable, objective statement that describes reality without inference, opinion, or interpretation. See examples below.  
- **Conclusions**: A conclusion is a derived statement that interprets or explains facts, often through reasoning, causation, or judgment.
  - If removing the sentence would make the text lose an interpretation, not a data point—it's likely a conclusion.
- **Example**:
  - Fact 1: Revenue grew by 25% in Q2.
  - Fact 2: Marketing expenses were reduced by 15% over the same period.
  - Fact 3: Customer acquisition rose by 18%.
  - Terms: Revenue, Marketing expenses, Customer acquisition
  - Conclusion 1: The company improved its profitability through efficient marketing.
  - Conclusion 2: The business strategy in Q2 successfully balanced growth and cost-efficiency.

#### Scoring

- **Facts (40%)**  
  - Identify each discrete fact in the reference.
  - Do not count evaluative, causal, or interpretive language as facts—even if they contain data.
  - Check whether the same fact appears correctly in the model output.
  - Calculate the ratio of matched facts: facts_ratio = (matched_facts / total_facts)  
  - Individual words or numbers count as separate facts only if each is an essential and irreducible part of the statement.
  - Example with 4 facts: "Switzerland has 4 official languages: German, French, Italian, Romansh."
  - Example with 2 fact: ""Teaching is her bread and butter, but writing poetry is her true passion."
- **Conclusions (30%)**  
  - Identify key conclusions or judgments.
  - Do not re-count previously identified facts as conclusions. Only count statements that derive or infer meaning from facts.
  - Check whether the model output reaches the same conclusions.
  - Calculate the ratio of matched conclusions: conclusions_ratio = (matched_conclusions / total_conclusions)
  - All conclusions have to be explicitly stated in the model output. Implicit conclusions do not count as matched.
- **Terminology (21%)**  
  - List each key term in the reference without counting values and numeric expressions ('10 orders', '20%', 'less than 5') as terms.
  - Check whether the model output uses the same terms.
  - Calculate the ratio of matched terms: terms_ratio = (matched_terms / total_terms)
    - If total_terms > 0, then terms_ratio = (matched_terms / total_terms)
    - If total_terms == 0, set terms_ratio = 1
    - If no terms are matched, terms_ratio = 0
- **Organization (9%)**
  - Compare the high-level structure (sections, ordering) of the model output and reference.
  - Calculate the ratio of matched organization (0 or 1): organization_ratio = 0 for very different, 1 for comparable

### 2. Scoring model

- **If total_conclusions > 0:**
  - score = 5 * ( (facts_ratio * 0.4) + (conclusions_ratio * 0.3) + (terms_ratio * 0.21) + (organization_ratio * 0.09) )
- **If total_conclusions == 0:**
  - score = 5 * ( (facts_ratio * 0.7) + (terms_ratio * 0.21) + (organization_ratio * 0.09) )
- **If matched_facts < 1:**
  - score = 5 * ( (facts_ratio * 0.7) + (terms_ratio * 0.21) )
- IMPORTANT: Round the score to the nearest integer number

### 3. Score verification

Verify that the score calculation is correct by breaking it down to smaller steps.

### 4. Output format

Return exactly:

```json
{
  "score": <0-5>,
  "rationale": [
    "Fact: <number_of_output_facts> of <number_of_reference_facts> correctly matched.",
    "Conclusion: <number_of_output_conclusions> of <number_of_reference_conclusions> correctly matched.",
    "Terminology: <number_of_output_terms> of <number_of_reference_terms> terms correctly matched.",
    "Organization: matched/mismatched",
    "Score: <score_rounded> ≈ <score_exact> = <score_calculation>"
  ]
}
```

### 5. Examples

- **Reference:** There are 27 member states in the European Union, and 8 of them use their own national currencies instead of the Euro.
- 2 Facts: 1) There are 27 member states in the European Union, 2) 8 of them use their own national currencies instead of the Euro.
- 4 Terms: 1) European Union, 2) Member states, 3) Euro, 4) National currencies 
- **Score 0 = 5 * ( (0 * 0.7) + (0 * 0.2) + (0 * 0.1) ):** Bla bla.
- **Score 1 = 5 * ( (0 * 0.7) + (1 * 0.2) + (0 * 0.1) ):** The Euro is the currency of the European Union. But some member states use their own national currencies.
- **Score 2 = 5 * ( (0.5 * 0.7) + (0.25 * 0.2) + (0 * 0.1) ):** There are 27 member states.
- **Score 3 = 5 * ( (0.5 * 0.7) + (1 * 0.2) + (1 * 0.1) ):** Some of the 27 member states of the European Union do not use the Euro but their own national currencies.
- **Score 4 = 5 * ( (1 * 0.7) + (0.5 * 0.2) + (0 * 0.1) ):** Not all European Union member states have adopted the Euro as their currency. Out of the total 27, 8 countries chose to retain their national currencies.
- **Score 5 = 5 * ( (1 * 0.7) + (1 * 0.2) + (1 * 0.1) ):** The European Union has 27 member states, and 8 of them use their own national currencies instead of the Euro.

### 6. Data

<input>
{{ item.input }}
</input>

<reference>
{{ item.reference }}
</reference>

<model_output>
{{ item.output_text }}
</model_output>