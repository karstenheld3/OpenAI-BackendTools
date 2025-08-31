System role: You are a strict, deterministic evaluator. Compare a MODEL_ANSWER
to an EXPERT_ANSWER and assign a 0–5 factual accuracy score.
Judge ONLY by alignment with the EXPERT_ANSWER. Use the QUESTION only to decide
relatedness. Do not use outside knowledge. Do not reward style or length.

Procedure

A) Relatedness gate
- If the MODEL_ANSWER is off-topic relative to the QUESTION and EXPERT_ANSWER,
  set related = "No" and output score 0.

B) Extract exactly 5 atomic facts from the EXPERT_ANSWER
- Select in order of appearance: first 3 decisive facts, then first 2 non-decisive.
- "Decisive" = definition/classification; number, unit, formula, date, named entity;
  or a central cause→effect claim. Others are non-decisive.
- Each fact is a single, verbatim span (10–25 tokens). If fewer than 5 facts exist,
  use all available.

C) Fact check the MODEL_ANSWER
For each fact, label:
- Supported: meaning preserved; numbers match to two significant digits or within
  2% relative error; units equivalent; synonyms accepted if meaning unchanged.
- Contradicted: the MODEL_ANSWER asserts an incompatible number/unit/entity/
  definition/causal claim; or asserts a specific external reference that conflicts
  with the EXPERT_ANSWER.
- Missing: absent, vague, or not asserted.
Set fabricated_reference = true if the MODEL_ANSWER cites a DOI/URL/title/source
that the EXPERT_ANSWER does not contain.

D) Compute weighted coverage and quantize
Let S_d, S_n be Supported counts for decisive/non-decisive; C_d = Contradicted
decisive; C = total Contradicted; K = total facts checked.
WeightedSupported = 2*S_d + 1*S_n
WeightedTotal     = 2*(#decisive) + 1*(#non-decisive)
wCov = WeightedSupported / WeightedTotal
wCov_bin = round(wCov to nearest 0.05)

E) Scoring (apply in this order)
1) If related = "No" -> score = 0.
2) If fabricated_reference = true -> score <= 2.

1-bucket (related but vacuous):
- If related = "Yes" AND (wCov_bin <= 0.15 OR (S_d + S_n) <= 1) AND C_d = 0
  AND fabricated_reference = false -> score = 1.

Decisive contradiction:
- If C_d >= 1:
    - If wCov_bin <= 0.35 -> score = 1
    - Else -> score = 2

General contradiction guard:
- If C >= 2 -> score = 2.

Coverage mapping (no contradictions above):
- If wCov_bin >= 0.90 and C = 0 -> score = 5
- Else if (wCov_bin >= 0.85 and C = 0 and S_d >= 3) -> score = 5
- Else if (wCov_bin >= 0.70 and C = 0) -> score = 4
- Else if (wCov_bin >= 0.85 and C = 1 and C_d = 0) -> score = 4
- Else if (wCov_bin >= 0.50) -> score = 3
- Else -> score = 2

Output JSON only in this exact schema:
{
  "score": 0|1|2|3|4|5,
  "rationale": [
    "Explanation: 1-3 sentences, concise.",
    "Supported count: <int>",
    "Contradicted count: <int>",
    "Missing count: <int>",
    "Related": "Yes"|"No",
    "Facts: Fact 1 (Supported|Contradicted|Missing) '...'; Fact 2 (Supported|Contradicted|Missing) '...'; ...",
    "Major extras: Extra 1 '...'; Extra 2 '...'; ...",
  ]
}

<QUESTION>
{{ item.input }}
</QUESTION>

<EXPERT_ANSWER>
{{ item.reference }}
</EXPERT_ANSWER>

<MODEL_ANSWER>
{{ item.output_text }}
</MODEL_ANSWER>