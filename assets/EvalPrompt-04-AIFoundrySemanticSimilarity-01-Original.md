Evaluate the degree of similarity between the given output and the ground truth on a scale from 0 to 5, using a chain of thought to ensure step-by-step reasoning before reaching the conclusion.

Consider the following criteria:

- 5: Highly similar - The output and ground truth are nearly identical, with only minor, insignificant differences.
- 4: Somewhat similar - The output is largely similar to the ground truth but has few noticeable differences.
- 3: Moderately similar - There are some evident differences, but the core essence is captured in the output.
- 2: Slightly similar - The output only captures a few elements of the ground truth and contains several differences.
- 1: Not similar - The output is significantly different from the ground truth, with few or no matching elements, but it is still related to the question. 
- 0: Not similar and completely unrelated - Absolutely no relation to the question and complete mismatch with the ground truth.

# Steps

1. Identify and list the key elements present in both the output and the ground truth.
2. Compare these key elements to evaluate their similarities and differences, considering both content and structure.
3. Analyze the semantic meaning conveyed by both the output and the ground truth, noting any significant deviations.
4. Based on these comparisons, categorize the level of similarity according to the defined criteria above.
5. Write out the reasoning for why a particular score is chosen, to ensure transparency and correctness.
6. Assign a similarity score based on the defined criteria above.

# Output Format

Provide the final similarity score as an integer (0, 1, 2, 3, 4, or 5).

# Examples

**Example 1:**

- Output: "The cat sat on the mat."
- Ground Truth: "The feline is sitting on the rug."
- Reasoning: Both sentences describe a cat sitting on a surface, but they use different wording. The structure is slightly different, but the core meaning is preserved. There are noticeable differences, but the overall meaning is conveyed well.
- Similarity Score: 3

**Example 2:**

- Output: "The quick brown fox jumps over the lazy dog."
- Ground Truth: "A fast brown animal leaps over a sleeping canine."
- Reasoning: The meaning of both sentences is very similar, with only minor differences in wording. The structure and intent are well preserved.
- Similarity Score: 4

# Notes

- Always aim to provide a fair and balanced assessment.
- Consider both syntactic and semantic differences in your evaluation.
- Consistency in scoring similar pairs is crucial for accurate measurement.

# Data

<output>
{{ item.output_text }}
</output>

<ground_truth>
{{ item.reference }}
</ground_truth>

<question>
{{ item.input }}
</question>
