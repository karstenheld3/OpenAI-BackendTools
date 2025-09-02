import os
import json

# Input JSON: [ "item" : {"input": "", "reference": "", "output_text": ""}, "item" : {"input": "", "reference": "", "output_text": ""} ] 
# Output JSONL: {"query": "", "ground_truth": "", "response": "", "context": ""}
# Mapping: input -> query, reference -> ground_truth, output_text -> response, context -> context
def convert_from_openai_json_to_azure_ai_jsonl(input_file, output_file):
  
  items = []
  with open(input_file, 'r') as f:
    data = json.load(f)
    
    for entry in data:
      item_data = entry.get('item', {})
      converted_item = {
        "query": item_data.get('input', ''),
        "ground_truth": item_data.get('reference', ''),
        "response": item_data.get('output_text', ''),
        "context": item_data.get('context', '')
      }
      items.append(converted_item)
  
  # Write to JSONL format (one JSON object per line)
  with open(output_file, 'w') as f:
    for item in items:
      f.write(json.dumps(item) + '\n')
  
  print(f"Converted {len(items)} items from {input_file} to {output_file}")
  return items

# Input JSONL: {"query": "", "ground_truth": "", "response": "", "context": ""}
# Output JSON: [ "item" : {"input": "", "reference": "", "output_text": ""}, "item" : {"input": "", "reference": "", "output_text": ""} ] 
# Mapping: query -> input, ground_truth -> reference, response -> output_text, context -> context
def convert_from_azure_ai_jsonl_to_openai_json(input_file, output_file):
  
  items = []
  with open(input_file, 'r') as f:
    for line in f:
      data = json.loads(line)
      items.append({
        "item": {
          "input": data['query'],
          "reference": data['ground_truth'],
          "output_text": data['response'],
          "context": data['context']
        }
      })
  
  # Write the JSON array
  with open(output_file, 'w') as f:
    json.dump(items, f, indent=2)  
  
  print(f"Converted {len(items)} items from {input_file} to {output_file}")
  return items

def convert_from_csv_to_openai_json(input_file, output_file, column_mapping_dict):
  import csv
  items = []
  
  try:
    with open(input_file, 'r', encoding='utf-8-sig') as f:
      reader = csv.DictReader(f)
      for row in reader:
        item_data = {}
        for csv_col, json_attr in column_mapping_dict.items():
          item_data[json_attr] = row.get(csv_col, '')
        items.append({"item": item_data})
  except UnicodeDecodeError:
    # Fallback to cp1252 encoding if UTF-8 fails
    with open(input_file, 'r', encoding='cp1252') as f:
      reader = csv.DictReader(f)
      for row in reader:
        item_data = {}
        for csv_col, json_attr in column_mapping_dict.items():
          item_data[json_attr] = row.get(csv_col, '')
        items.append({"item": item_data})
  
  # Write the JSON array with items on single lines
  with open(output_file, 'w', encoding='utf-8') as f:
    f.write('[\n')
    for i, item in enumerate(items):
      line = '  ' + json.dumps(item)
      if i < len(items)-1:
        line += ','
      f.write(line + '\n')
    f.write(']\n')
  
  print(f"Converted {len(items)} items from {input_file} to {output_file}")
  return items

if __name__ == "__main__":
  openai_eval_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "EvalCalibrationItems-01-SimpleQuestions.json")
  azureai_eval_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "EvalCalibrationItems-01-SimpleQuestions.jsonl")
  
  # Convert Azure AI JSONL to OpenAI JSON
  # convert_from_azure_ai_jsonl_to_openai_json(azureai_eval_file, openai_eval_file)
  
  # Convert back from OpenAI JSON to Azure AI JSONL
  # convert_from_openai_json_to_azure_ai_jsonl(openai_eval_file, azureai_eval_file)

  # Convert CSV to OpenAI JSON
  # csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "DataRobot-CalibrationQuestionsAnswers.csv")
  # converted_csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "EvalCalibrationItems-05-DataRobot.json")
  # convert_from_csv_to_openai_json(csv_file, converted_csv_file, {"question": "input", "answer": "reference", "response": "output_text", "Human Score": "target_score"})
