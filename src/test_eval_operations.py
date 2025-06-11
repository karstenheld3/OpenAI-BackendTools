from dataclasses import dataclass
from dotenv import load_dotenv
from openai_backendtools import *
from test_rag_operations import *
import time
import json
import os
import datetime

load_dotenv()

answer_rating_prompt_template = """
## Task

You are an evaluator. Compare a GPT model's output (`output_text`) against a reference answer (`reference`) and assign an **integer score from 0 to 5**. Also provide a brief bullet-point rationale tying each point in your score back to the criteria below.

### 1. Criteria to check

- **Facts (40%)**  
  - Identify each discrete fact in the reference.  
  - Check whether the same fact appears correctly in the model output.  
- **Conclusions (30%)**  
  - Identify key conclusions or judgments in the reference.
  - Check whether the model output reaches the same conclusions.
  - If the reference answer contains no conclusions, the model output is also not required to contain conclusions.
- **Terminology (20%)**  
  - List each key term in the reference.  
  - Check whether the model output uses the same terms.  
- **Organization (10%)**  
  - Compare the high-level structure (sections, ordering) of the model output and reference.  

### 2. Scoring rubric

| Score | Description                                                                                       |
|:-----:|:--------------------------------------------------------------------------------------------------|
| 0     | No matching facts or conclusions; terminology and structure unrelated.                            |
| 1     | Uses similar terminology but no correct facts or conclusions.                                     |
| 2     | At least one fact present but misrepresented; no correct conclusions.                             |
| 3     | Some facts and conclusions correct, but significant gaps; structure and terminology differ.       |
| 4     | All facts and conclusions correct; minor deviations in terminology or organization.               |
| 5     | Perfect alignment: all facts and conclusions correct; matching terminology and structure.         |

### 3. Output format

Return exactly:

```json
{
  "score": <0-5>,
  "rationale": [
    "Fact: <number_of_output_facts> of <number_of_reference_facts> correctly matched. <number_of_additional_output_facts> additional facts in output.",
    "Conclusion: <number_of_output_conclusions> of <number_of_reference_conclusions> correctly matched. <number_of_additional_output_conclusions> additional conclusions in output.",
    "Terminology: <number_of_deviating_terms> deviating terms found.",
    "Organization: matched/mismatched"
  ]
}

### 4. Example

- **Reference:** There are 27 member states in the European Union, and 8 of them use their own national currencies instead of the Euro.
- **Score 0:** Bla bla.
- **Score 1:** Some member states use their own national currencies.
- **Score 2:** 27 member states use their own national currencies.
- **Score 3:** The European Union has 27 member states.
- **Score 4:** The European Union has 27 member states, of which 8 do not use the Euro.
- **Score 5:** The European Union has 27 member states, and 8 of them use their own national currencies instead of the Euro.

### 5. Reference answer

<reference>
[REFERENCE]
</reference>

### 6. Model output

<model_output>
[MODEL_OUTPUT]
</model_output>
"""

# ----------------------------------------------------- START: Evals ----------------------------------------------------------

Batch01 = [
  { "item" : { "input": "Who is Arilena Drovik?", "reference": "Arilena Drovik is molecular biologist and geneticist. She is a Professor of Molecular Genetics and principal investigator at the Department of Molecular Biology, Lund University, Sweden. She holds a PhD in Molecular Biology from University of Cambridge, UK."} }
  ,{ "item" : { "input": "What was the title of Arilena Drovik's dissertation?", "reference": "Epigenetic Modulators of Gene Expression in Early Development"} }
  ,{ "item" : { "input": "What was the title of Arilena Drovik's first scientific publication and where and when was it published?", "reference": "The title of Arilena Drovik's first scientific article was 'CRISPR-Cas9: Revolutionizing Genome Editing in Modern Molecular Biology'. It was published by the 'The CRISPR Journal' in 2015."} }
  ,{ "item" : { "input": "With whom did Arilena Drovik collaborate on scientific publications?", "reference":
"""Between 2018 and 2020 Arilena Drovik collaborated with the following researchers:
- L. Fernandez and H.S. Wong on the 2018 article 'CRISPR Screening for Essential Non-Coding Elements'
- R. Novak and other authors on the 2020 article 'Next-Generation CRISPR Tools for Precision Genome Engineering'
"""} }
]

# ----------------------------------------------------- END: Evals ------------------------------------------------------------


# ----------------------------------------------------- START: Tests ----------------------------------------------------------

# Gets all answers for the 'input' in all items using response models and stores them in 'output_text' of each items
def get_answers_from_model_and_return_items(client, vector_store_id, model, items):
  function_name = 'Get answers from model and add in items'
  start_time = log_function_header(function_name)

  for idx, item in enumerate(items, 1):
    input = item['item']['input']
    print(f"  [ {idx} / {len(items)} ] Query: {input}")
    response = retry_on_openai_errors(lambda: client.responses.create(
      model=model
      ,input=input
      ,tools=[{ "type": "file_search", "vector_store_ids": [vector_store_id] }]
      ,temperature=0
    ), indentation=4)
    output_text = response.output_text
    print(f"    Response: {truncate_string(output_text,80)}")
    item['item']['output_text'] = output_text

  log_function_footer(function_name, start_time)
  return items

# Gets evaluations for all items using the provided prompt template and adds score and rationale to each item
def test_prompt_evaluation_and_return_items(client, items, prompt_template, judge_model_name):
  function_name = 'Evaluate answers and add scores in items'
  start_time = log_function_header(function_name)

  for idx, item in enumerate(items, 1):
    input = item['item']['input']
    reference = item['item']['reference']
    output_text = item['item'].get('output_text', '')
    print(f"  [ {idx} / {len(items)} ] Query: {truncate_string(input.replace('\n', ' '),120)}")
    print(f"    Reference    : {truncate_string(reference.replace('\n', ' '),100)}")
    print(f"    Model output : {truncate_string(output_text.replace('\n', ' '),100)}")
   
    # Replace placeholders in the prompt template
    prompt = prompt_template.replace('[REFERENCE]', reference).replace('[MODEL_OUTPUT]', output_text)
    
    # Call the OpenAI API to evaluate the answer
    response = retry_on_openai_errors(lambda: client.chat.completions.create(
      model=judge_model_name,
      messages=[{"role": "user", "content": prompt}],
      response_format={"type": "json_object"},
      temperature=0
    ), indentation=4)
    
    # Parse the JSON response
    try:
      evaluation = json.loads(response.choices[0].message.content)
      score = evaluation.get('score')
      rationale = evaluation.get('rationale')
      
      # Add score and rationale to the item
      item['item']['score'] = score
      item['item']['rationale'] = rationale
      
      print(f"    Score: {score}")
      for r in rationale:
        print(f"    - {r}")
    except json.JSONDecodeError:
      print(f"    Error: Could not parse JSON response: {response.choices[0].message.content}")
      item['item']['score'] = None
      item['item']['rationale'] = ["Error: Could not parse evaluation"]

  log_function_footer(function_name, start_time)
  return items

# ----------------------------------------------------- END: Tests ------------------------------------------------------------


# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
  openai_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

  if openai_service_type == "openai":
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  @dataclass
  class EvalParams: vector_store_name: str; folder_path: str; model: str; items: list; judge_model_name: str; min_score: int

  params = EvalParams(
    vector_store_name="test_vector_store",
    folder_path="./RAGFiles/Batch01",
    model = openai_model_name,
    items = Batch01,
    judge_model_name = "gpt-4o-mini",
    min_score=4
  )

  print("-"*140)

  # Step 1: Create vector store by uploading files
  test_vector_store_with_files = create_test_vector_store_from_folder_path(client,params.vector_store_name, params.folder_path)

  print("-"*140)

  # Step 2: Get answers from model and store in items
  params.items = get_answers_from_model_and_return_items(client, test_vector_store_with_files.vector_store.id, params.model, params.items)

  print("-"*140)

  # Step 3: Test eval using graders
  params.items = test_prompt_evaluation_and_return_items(client, params.items, answer_rating_prompt_template, params.judge_model_name)

  # calculate average score
  scores = [item['item']['score'] for item in params.items if item['item'].get('score') is not None]

  print("-"*140)
  # count all answers as correct that have min_score
  questions_answered_correctly = sum(1 for item in params.items if item['item'].get('score', 0) >= params.min_score)
  questions_answered_correctly_percent = questions_answered_correctly / len(params.items)
  average_score = sum(scores) / len(scores) if scores else 0
  average_score_in_percent =  average_score / 5
  print(f"Prompt evaluation result: {questions_answered_correctly} of {len(params.items)} answers correct ({questions_answered_correctly_percent:.0%}). Average score: {average_score:.2f} ({average_score_in_percent:.0%}).")

  print("-"*140)

  # Step 4: Delete vector store including all files
  delete_vector_store_by_name(client, params.vector_store_name, True)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
