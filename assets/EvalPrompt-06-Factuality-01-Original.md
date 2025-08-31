You are reviewing whether the chatbot's answer is accurate based on a trusted expert answer.
Focus on whether the chatbots answer gets the important facts right, even if it uses different words.

Then, choose the best matching score below:

- Score 5 (Completely correct): The chatbot's answer accurately captures the main message and key facts of the expert's answer. It might skip small details or use different words, but it's clear, accurate, and not misleading.
- Score 4 (Mostly correct): The chatbot answer is mostly in line with the expert answer. It provides a reasonable understanding. It includes some extra or missing information that the expert didn't mention, but these do not significantly affect the usefulness of the answer.
- Score 3 (Somewhat correct): The chatbot's answer is close to the expert's answer, but it is missing important information. It answers the question but it is not as clear or accurate as the expert answer.
- Score 2 (Wrong or misleading): The chatbot answer overlooks key facts or includes misleading information. It is likely to confuse or mislead readers.
- Score 1 (Completely wrong, but related): The chatbot answer is completely different than the expert answer but it is related to the question.
- Score 0 (Completely wrong and unrelated): The chatbot answer is completely different than the expert answer and it is not related to the question.

Do not penalize for:
- Using different wording, sentence structures or synonyms
- Slightly rephrased sentences
- Minor omissions of non-essential background context
- Minor background information missing that does not affect factual meaning

Provide your judgment and explain clearly and precisely why you chose the score.

The question is
<question>
{{ item.input }}
</question>

The actual answer of the chatbot is
<actualAnswer>
{{ item.output_text }}
</actualAnswer>.

The expected answer is
<expectedAnswer>
{{ item.reference }}
</expectedAnswer>.
