#!/usr/bin/env python3
"""
analyze-costs.py - Analyze costs from token usage files.

Usage:
  python analyze-costs.py --input-folder transcriptions/ --output-file costs.json
"""

import os, sys, json, argparse
from pathlib import Path
from datetime import datetime, timezone

UNKNOWN = '[UNKNOWN]'

DEFAULT_PRICING = {
    "openai": {
        "gpt-5.2": {"input_per_1m": 1.75, "output_per_1m": 14.00, "currency": "USD"},
        "gpt-5.1": {"input_per_1m": 1.25, "output_per_1m": 10.00, "currency": "USD"},
        "gpt-5": {"input_per_1m": 1.25, "output_per_1m": 10.00, "currency": "USD"},
        "gpt-5-mini": {"input_per_1m": 0.25, "output_per_1m": 2.00, "currency": "USD"},
        "gpt-5-nano": {"input_per_1m": 0.05, "output_per_1m": 0.40, "currency": "USD"},
        "gpt-5.2-pro": {"input_per_1m": 21.00, "output_per_1m": 168.00, "currency": "USD"},
        "gpt-5-pro": {"input_per_1m": 15.00, "output_per_1m": 120.00, "currency": "USD"},
        "gpt-4.1": {"input_per_1m": 2.00, "output_per_1m": 8.00, "currency": "USD"},
        "gpt-4.1-mini": {"input_per_1m": 0.40, "output_per_1m": 1.60, "currency": "USD"},
        "gpt-4.1-nano": {"input_per_1m": 0.10, "output_per_1m": 0.40, "currency": "USD"},
        "gpt-4o": {"input_per_1m": 2.50, "output_per_1m": 10.00, "currency": "USD"},
        "gpt-4o-mini": {"input_per_1m": 0.15, "output_per_1m": 0.60, "currency": "USD"},
        "o4-mini": {"input_per_1m": 1.10, "output_per_1m": 4.40, "currency": "USD"},
        "o3-mini": {"input_per_1m": 1.10, "output_per_1m": 4.40, "currency": "USD"},
        "o3-deep-research": {"input_per_1m": 10.00, "output_per_1m": 40.00, "currency": "USD"},
        "o1": {"input_per_1m": 15.00, "output_per_1m": 60.00, "currency": "USD"},
        "o1-mini": {"input_per_1m": 1.10, "output_per_1m": 4.40, "currency": "USD"},
        "o1-pro": {"input_per_1m": 150.00, "output_per_1m": 600.00, "currency": "USD"}
    },
    "anthropic": {
        "claude-opus-4-1-20250805": {"input_per_1m": 15.00, "output_per_1m": 75.00, "currency": "USD"},
        "claude-opus-4-20250514": {"input_per_1m": 15.00, "output_per_1m": 75.00, "currency": "USD"},
        "claude-sonnet-4-20250514": {"input_per_1m": 3.00, "output_per_1m": 15.00, "currency": "USD"},
        "claude-3-7-sonnet-20250219": {"input_per_1m": 3.00, "output_per_1m": 15.00, "currency": "USD"},
        "claude-3-5-sonnet-20241022": {"input_per_1m": 3.00, "output_per_1m": 15.00, "currency": "USD"},
        "claude-3-5-haiku-20241022": {"input_per_1m": 0.80, "output_per_1m": 4.00, "currency": "USD"},
        "claude-3-haiku-20240307": {"input_per_1m": 0.25, "output_per_1m": 1.25, "currency": "USD"}
    }
}


def load_pricing(pricing_file: Path) -> dict:
    """Load pricing from file or use defaults."""
    if pricing_file and pricing_file.exists():
        data = json.loads(pricing_file.read_text(encoding='utf-8'))
        return data.get("pricing", data)
    return DEFAULT_PRICING


def detect_provider(model_id: str) -> str:
    """Detect provider from model ID."""
    model_lower = model_id.lower()
    if model_lower.startswith(('gpt-', 'o1-', 'o3-', 'o4-')):
        return 'openai'
    if model_lower.startswith('claude'):
        return 'anthropic'
    return 'unknown'


def calculate_cost(model: str, input_tokens: int, output_tokens: int, pricing: dict) -> dict:
    """Calculate cost for token usage."""
    provider = detect_provider(model)
    provider_pricing = pricing.get(provider, {})
    model_pricing = provider_pricing.get(model)
    
    if not model_pricing:
        for key in provider_pricing:
            if key in model or model in key:
                model_pricing = provider_pricing[key]
                break
    
    if not model_pricing:
        return {
            "input_cost": 0,
            "output_cost": 0,
            "total_cost": 0,
            "currency": "USD",
            "pricing_found": False
        }
    
    input_cost = (input_tokens / 1_000_000) * model_pricing["input_per_1m"]
    output_cost = (output_tokens / 1_000_000) * model_pricing["output_per_1m"]
    
    return {
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(input_cost + output_cost, 6),
        "currency": model_pricing.get("currency", "USD"),
        "pricing_found": True
    }


def find_token_usage_files(input_folder: Path) -> list:
    """Find all token usage files in folder."""
    usage_files = []
    for f in input_folder.rglob("_token_usage_*.json"):
        usage_files.append(f)
    return usage_files


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze costs from token usage files.')
    parser.add_argument('--input-folder', type=Path, required=True, help='Folder with token usage JSON files')
    parser.add_argument('--output-file', type=Path, required=True, help='Output JSON file')
    parser.add_argument('--pricing', type=Path, help='Custom pricing JSON file')
    return parser.parse_args()


def main():
    args = parse_args()
    
    if not args.input_folder.exists():
        print(f"[ERROR] Input folder not found: {args.input_folder}", file=sys.stderr)
        sys.exit(1)
    
    pricing = load_pricing(args.pricing)
    usage_files = find_token_usage_files(args.input_folder)
    
    if not usage_files:
        print(f"[WARN] No token usage files found in {args.input_folder}", file=sys.stderr)
        print("Looking for files matching: _token_usage_*.json", file=sys.stderr)
    
    model_costs = {}
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0
    
    for usage_file in usage_files:
        try:
            data = json.loads(usage_file.read_text(encoding='utf-8'))
            model = data.get("model", "unknown")
            input_tokens = data.get("total_input_tokens", 0)
            output_tokens = data.get("total_output_tokens", 0)
            calls = data.get("calls", 0)
            
            cost_info = calculate_cost(model, input_tokens, output_tokens, pricing)
            
            if model not in model_costs:
                model_costs[model] = {
                    "model": model,
                    "provider": detect_provider(model),
                    "total_input_tokens": 0,
                    "total_output_tokens": 0,
                    "total_calls": 0,
                    "input_cost": 0,
                    "output_cost": 0,
                    "total_cost": 0,
                    "currency": cost_info["currency"],
                    "pricing_found": cost_info["pricing_found"]
                }
            
            model_costs[model]["total_input_tokens"] += input_tokens
            model_costs[model]["total_output_tokens"] += output_tokens
            model_costs[model]["total_calls"] += calls
            model_costs[model]["input_cost"] += cost_info["input_cost"]
            model_costs[model]["output_cost"] += cost_info["output_cost"]
            model_costs[model]["total_cost"] += cost_info["total_cost"]
            
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens
            total_cost += cost_info["total_cost"]
            
            print(f"Processed: {usage_file.name} ({model}: {input_tokens}+{output_tokens} tokens, ${cost_info['total_cost']:.4f})", file=sys.stderr)
            
        except Exception as e:
            print(f"[WARN] Could not process {usage_file}: {e}", file=sys.stderr)
    
    for model in model_costs:
        model_costs[model]["input_cost"] = round(model_costs[model]["input_cost"], 6)
        model_costs[model]["output_cost"] = round(model_costs[model]["output_cost"], 6)
        model_costs[model]["total_cost"] = round(model_costs[model]["total_cost"], 6)
    
    output = {
        "summary": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_cost": round(total_cost, 4),
            "currency": "USD",
            "models_used": len(model_costs)
        },
        "by_model": list(model_costs.values()),
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "files_processed": len(usage_files)
    }
    
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n=== Cost Analysis ===", file=sys.stderr)
    print(f"Total tokens: {total_input_tokens:,} in + {total_output_tokens:,} out = {total_input_tokens + total_output_tokens:,}", file=sys.stderr)
    print(f"Total cost: ${total_cost:.4f} USD", file=sys.stderr)
    print(f"Output: {args.output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
