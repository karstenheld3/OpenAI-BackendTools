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

if __name__ == "__main__":
  openai_eval_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Eval_Calibration_01_MathScoreModel.json")
  azureai_eval_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Eval_Calibration_01_MathScoreModel.jsonl")
  
  # Convert Azure AI JSONL to OpenAI JSON
  # convert_from_azure_ai_jsonl_to_openai_json(azureai_eval_file, openai_eval_file)
  
  # Convert back from OpenAI JSON to Azure AI JSONL
  convert_from_openai_json_to_azure_ai_jsonl(openai_eval_file, azureai_eval_file)
