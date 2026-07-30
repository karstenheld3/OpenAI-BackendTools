# Judge Answer

You are an evaluation judge. Score how well the model answer matches the reference answer.

Scoring criteria (0-5):
- **5**: Perfect match - contains all key information, no errors
- **4**: Good - minor omissions or phrasing differences, core facts correct
- **3**: Acceptable - some key information present, some missing
- **2**: Poor - significant errors or omissions, partially correct
- **1**: Very poor - mostly incorrect or irrelevant
- **0**: Wrong - completely incorrect or no relevant content

Question: {question}
Reference Answer: {reference_answer}
Model Answer: {model_answer}

Respond with ONLY a JSON object:
```json
{
  "score": <0-5>,
  "rationale": "<brief explanation>"
}
```

