from dataclasses import dataclass
from dotenv import load_dotenv
from openai_backendtools import *
from test_rag_operations import *
import json
import os
import numpy as np

load_dotenv()

# ----------------------------------------------------- START: Evals ----------------------------------------------------------
# Item 01: FAIL - 0% correct
# Item 02: FAIL - 20% correct, 1 similarity ("gene expression")
# Item 03: FAIL - 60% correct, 1 incorrect fact (year "2012" instead of "2015")
# Item 04: PASS - 100% correct, 1 additional fact ("at least three researchers")
# Expected result: 1 of 4 questions correctly answered, 25% correct
Batch01 = [
  { "item" : {
    "input": "Who is Arilena Drovik?"
    ,"reference": "Arilena Drovik is molecular biologist and geneticist. She is a Professor of Molecular Genetics and principal investigator at the Department of Molecular Biology, Lund University, Sweden. She holds a PhD in Molecular Biology from University of Cambridge, UK."
    ,"output_text": "Arilena Drovik is a singer from Albania."
    }
  }
  ,{ "item" : {
    "input": "What was the title of Arilena Drovik's dissertation?"
    ,"reference": "Epigenetic Modulators of Gene Expression in Early Development"
    ,"output_text": "Structural Components of Gene Expression in Latent Mutations"
    }
  }
  ,{ "item" : {
    "input": "What was the title of Arilena Drovik's first scientific publication and where and when was it published?"
    ,"reference": "The title of Arilena Drovik's first scientific article was 'CRISPR-Cas9: Revolutionizing Genome Editing in Modern Molecular Biology'. It was published by the 'The CRISPR Journal' in 2015."
    ,"output_text": "The title of Arilena Drovik's first scientific article was 'CRISPR-Cas9: Revolutionizing Genome Editing in Modern Molecular Biology'. It was published by the 'The CRISPR Journal' in 2012."
    }
  }
  ,{ "item" : {
    "input": "With whom did Arilena Drovik collaborate on scientific publications?"
    ,"reference":
"""Between 2018 and 2020 Arilena Drovik collaborated with the following researchers:
- L. Fernandez and H.S. Wong on the 2018 article 'CRISPR Screening for Essential Non-Coding Elements'
- R. Novak and other authors on the 2020 article 'Next-Generation CRISPR Tools for Precision Genome Engineering'
"""
    ,"output_text":
"""Arilena Drovik has collaborated with at least three researchers between 2018 and 2020:
- on the article 'CRISPR Screening for Essential Non-Coding Elements', published in 2018, with H.S. Wong and L. Fernandez 
- on the article 'Next-Generation CRISPR Tools for Precision Genome Engineering', published in 2020, with R. Novak and other authors
"""
    }
  }
]

# ----------------------------------------------------- END: Evals ------------------------------------------------------------

# ----------------------------------------------------- START: Prompts --------------------------------------------------------
# A very simple judge model prompt
judge_model_prompt_template_1 = """
You are an expert evaluator for a QA system. Compare the generated model output to the reference answer. Score on a 1-5 scale where:
1 = completely incorrect, 3 = partially correct, 5 = completely correct
Also explain your reasoning. Return exactly:

```json
{
  "score": <1-5>,
  "rationale": [ "<reasoning>" ]
}
```

Reference answer:
<reference>
[REFERENCE]
</reference>

Model output:
<model_output>
[MODEL_OUTPUT]
</model_output>
"""

# A detailed judge model prompt using multiple criteria
judge_model_prompt_template_2 = """
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
```

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
# ----------------------------------------------------- END: Prompts ----------------------------------------------------------

# ----------------------------------------------------- START: Tests ----------------------------------------------------------

# Gets all answers for the 'input' in all items using response models and stores them in 'output_text' of each items
def get_answers_from_model_and_return_items(client, vector_store_id, model, items):
  function_name = 'Get answers from model and add to items'
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

# Gets scores for all items using the provided prompt template and add score and rationale to each item
def score_answers_using_judge_model_and_return_items(client, items, prompt_template, judge_model_name):
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
        print(f"    - {truncate_string(r,120) }")
    except json.JSONDecodeError:
      print(f"    Error: Could not parse JSON response: {response.choices[0].message.content}")
      item['item']['score'] = None
      item['item']['rationale'] = ["Error: Could not parse evaluation"]

  log_function_footer(function_name, start_time)
  return items

def score_answers_using_cosine_similarity_and_return_items(client, items, embedding_model="text-embedding-3-small"):
  function_name = 'Evaluate answers using cosine similarity'
  start_time = log_function_header(function_name)

  def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

  def embed_text(text):
    response = retry_on_openai_errors(lambda: client.embeddings.create(
      model=embedding_model,
      input=[text]
    ), indentation=4)
    return response.data[0].embedding

  for idx, item in enumerate(items, 1):
    input = item['item']['input']
    reference = item['item']['reference']
    output_text = item['item'].get('output_text', '')
    print(f"  [ {idx} / {len(items)} ] Query: {truncate_string(input.replace('\n', ' '),120)}")
    print(f"    Reference    : {truncate_string(reference.replace('\n', ' '),100)}")
    print(f"    Model output : {truncate_string(output_text.replace('\n', ' '),100)}")

    try:
      # Get embeddings and calculate similarity
      reference_embedding = embed_text(reference)
      output_embedding = embed_text(output_text)
      similarity = cosine_similarity(reference_embedding, output_embedding)
      
      # Convert similarity score (0-1) to evaluation score (1-5)
      score = int(round(similarity * 4)) + 1
      
      # Add score and rationale to the item
      item['item']['score'] = score
      item['item']['rationale'] = [f"Cosine similarity: {similarity:.3f} (mapped to score {score})"] 
      
      print(f"    Score: {score} (similarity: {similarity:.3f})")
    except Exception as e:
      print(f"    Error: Could not calculate embedding similarity: {str(e)}")
      item['item']['score'] = None
      item['item']['rationale'] = [f"Error: {str(e)}"]

  log_function_footer(function_name, start_time)
  return items


def score_answers_using_score_model_grader_and_return_items(client, items, prompt_template, eval_model):
  function_name = 'Evaluate answers using score model grader'
  start_time = log_function_header(function_name)

  # Create evaluation configuration with custom graders
  eval_cfg = client.evals.create(
    name="answer_quality_evaluation",
    data_source_config={
      "type": "custom",
      "item_schema": {
        "type": "object",
        "properties": {
          "input": {"type": "string"},
          "reference": {"type": "string"},
          "output_text": {"type": "string"}
        },
        "required": ["input", "reference", "output_text"]
      },
      "include_sample_schema": False
    },
    testing_criteria=[
      {
        "type": "score_model",
        "name": "Answer Quality Score",
        "model": eval_model,
        "input": [
          {"role": "system", "content": "You are an expert evaluator. Your task is to evaluate the quality and accuracy of an answer compared to a reference answer."},
          {"role": "user", "content": """
            Question: {{ item.input }}
            Reference Answer: {{ item.reference }}
            Model Answer: {{ item.output_text }}
            
            Rate the answer on a scale of 1-5 where:
            1: Completely incorrect or irrelevant
            2: Mostly incorrect with some valid points
            3: Partially correct with significant gaps
            4: Mostly correct with minor issues
            5: Perfectly correct and complete
            
            Respond with ONLY the score number.
            """
          }
        ],
        "range": [1, 5],
        "pass_threshold": 4
      }
    ]
  )

  # Prepare evaluation data
  eval_data = [{
    "input": item['item']['input'],
    "reference": item['item']['reference'],
    "output_text": item['item'].get('output_text', '')
  } for item in items]

  # Create and run evaluation
  eval_run = client.evals.runs.create(
    name="answer_quality_run",
    eval_id=eval_cfg.id,
    data_source={
      "type": "jsonl",
      "source": {
        "type": "file_content",
        "content": eval_data
      }
    }
  )
  print(f"  Created evaluation run with ID: {eval_run.id}")
  print(f"  View results at: {eval_run.report_url}")

  # Poll for completion
  attempts = 0; max_attempts = 20
  while attempts < max_attempts:
    status = client.evals.runs.retrieve(eval_run.id, eval_id=eval_cfg.id).status
    if status == "completed": 
      print("  Evaluation completed.")
      break
    elif status == "failed": 
      raise RuntimeError("Evaluation failed.")
    else:
      attempts += 1
      print(f"  Waiting for completion... (attempt {attempts} / {max_attempts})")
      time.sleep(5)
  
  if attempts >= max_attempts:
    raise TimeoutError(f"Evaluation timed out after {max_attempts} attempts")

  # Get results and update items
  results = client.evals.runs.list_results(eval_run.id, eval_id=eval_cfg.id)
  for idx, (item, result) in enumerate(zip(items, results.data), 1):
    score = result.score
    reasoning = result.reasoning or "No reasoning provided"
    
    item['item']['score'] = score
    item['item']['rationale'] = [reasoning]
    
    print(f"  [ {idx} / {len(items)} ] Score: {score} ({reasoning})")


  log_function_footer(function_name, start_time)
  return items


def summarize_item_scores(items, min_score: int, indentation: int = 0) -> str:
  # calculate average score
  scores = [item['item']['score'] for item in items if item['item'].get('score') is not None]
  # count all answers as correct that have min_score
  questions_answered_correctly = sum(1 for item in items if item['item'].get('score', 0) >= min_score)
  questions_answered_correctly_percent = questions_answered_correctly / len(items)
  average_score = sum(scores) / len(scores) if scores else 0
  average_score_in_percent = average_score / 5
  indentation_string = " " * indentation
  
  max_chars_question = 20; max_chars_reference = 30; max_chars_answer = 30; max_chars_score = 6
  # Create output table
  table = "\n" + indentation_string + f"{'Question':{max_chars_question}} | {'Reference':{max_chars_reference}} | {'Answer':{max_chars_answer}} | {'Score':<{max_chars_score}}\n"
  table += indentation_string + "-" * (max_chars_question+max_chars_reference+max_chars_answer+max_chars_score+10)
  
  for item in items:
    question = item['item']['input'][:max_chars_question]
    reference = item['item']['reference'][:max_chars_reference]
    answer = item['item'].get('output_text', '')[:max_chars_answer]
    score = item['item'].get('score', 'N/A')
    table += "\n" + indentation_string + f"{question:{max_chars_question}} | {reference:{max_chars_reference}} | {answer:{max_chars_answer}} | {score:<{max_chars_score}}"
  
  summary = indentation_string + f"{questions_answered_correctly} of {len(items)} answers correct ({questions_answered_correctly_percent:.0%}). Average score: {average_score:.2f} ({average_score_in_percent:.0%})."
  return  summary + table

# ----------------------------------------------------- END: Tests ------------------------------------------------------------


# ----------------------------------------------------- START: Main -----------------------------------------------------------

if __name__ == '__main__':
  openai_service_type = os.getenv("OPENAI_SERVICE_TYPE", "openai")
  if openai_service_type == "openai":
    answer_model_name = "gpt-4o-mini"
    eval_model_name = "gpt-4o"
    client = create_openai_client()
  elif openai_service_type == "azure_openai":
    answer_model_name = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
    eval_model_name = os.getenv("AZURE_OPENAI_EVAL_MODEL_DEPLOYMENT_NAME", "gpt-4o")
    azure_openai_use_key_authentication = os.getenv("AZURE_OPENAI_USE_KEY_AUTHENTICATION", "false").lower() in ['true']
    client = create_azure_openai_client(azure_openai_use_key_authentication)

  @dataclass
  class EvalParams: vector_store_name: str; folder_path: str; items: list; answer_model: str; eval_model: str; embedding_model: str; grader_name: str; min_score: int

  params = EvalParams(
    vector_store_name="test_vector_store"
    ,folder_path="./RAGFiles/Batch01"
    ,items = Batch01
    ,answer_model = answer_model_name
    ,eval_model = eval_model_name
    ,embedding_model="text-embedding-3-small"
    ,grader_name="modelgraded.correctness.v1"
    ,min_score=4
  )

  # If use_predefined_model_outputs is set to False, create vector store and get answers from model
  use_predefined_model_outputs = True
  if not use_predefined_model_outputs:
    print("-"*140)
    # Step 1: Create vector store by uploading files
    test_vector_store_with_files = create_test_vector_store_from_folder_path(client,params.vector_store_name, params.folder_path)
    print("-"*140)
    # Step 2: Get answers from model and store in items
    params.items = get_answers_from_model_and_return_items(client, test_vector_store_with_files.vector_store.id, params.answer_model, params.items)
    print("-"*140) 

  # Step 3D: Test eval using score model grader
  params.items = score_answers_using_score_model_grader_and_return_items(client, params.items, judge_model_prompt_template_1, params.eval_model)
  print("."*100 + f"\n    Evaluation results using score model grader:")
  print(summarize_item_scores(params.items, params.min_score, 4))
  print("-"*140)

  # # Step 3A: Test eval using judge model with prompt template 1
  # params.items = score_answers_using_judge_model_and_return_items(client, params.items, judge_model_prompt_template_1, params.eval_model)
  # print("."*100 + f"\n    Evaluation results using judge model '{params.eval_model}' with prompt template 1:")
  # print(summarize_item_scores(params.items, params.min_score, 4) )
  # print("-"*140)
  # # Step 3B: Test eval using judge model with prompt template 2
  # params.items = score_answers_using_judge_model_and_return_items(client, params.items, judge_model_prompt_template_2, params.eval_model)
  # print("."*100 + f"\n    Evaluation results using judge model '{params.eval_model}' with prompt template 2:")
  # print(summarize_item_scores(params.items, params.min_score, 4))
  # print("-"*140)
  # # Step 3C: Test eval using embedding and cosine similarity
  # params.items = score_answers_using_cosine_similarity_and_return_items(client, params.items, params.embedding_model)
  # print("."*100 + f"\n    Evaluation results using embedding with '{params.embedding_model} and cosine similiarity:")
  # print(summarize_item_scores(params.items, params.min_score, 4))
  # print("-"*140)

  # Step 4: Delete vector store including all files
  if not use_predefined_model_outputs: delete_vector_store_by_name(client, params.vector_store_name, True)

# ----------------------------------------------------- END: Main -------------------------------------------------------------
