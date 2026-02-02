"""CLI entry point for LLM Computer Use v2."""
import argparse
import sys
import os

__version__ = "0.5.0"

def load_api_key(keys_file: str = None) -> str:
    """Load API key from file or environment."""
    if keys_file and os.path.exists(keys_file):
        with open(keys_file, "r") as f:
            for line in f:
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get("ANTHROPIC_API_KEY", "")

def main():
    parser = argparse.ArgumentParser(
        description="LLM Computer Use - Desktop automation via LLM vision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m llm_computer_use_v2 "Click the Start button"
  python -m llm_computer_use_v2 -x "Open Notepad"
  python -m llm_computer_use_v2 -n 5 -k api-keys.txt "What time is it?"
        """
    )
    
    parser.add_argument("task", nargs="?", help="Task description")
    parser.add_argument("--execute", "-x", action="store_true", help="Execute actions (default: dry-run)")
    parser.add_argument("--max-iterations", "-n", type=int, default=10, help="Max iterations (default: 10)")
    parser.add_argument("--model", "-m", default="claude-sonnet-4-5", help="Model (default: claude-sonnet-4-5)")
    parser.add_argument("--keys-file", "-k", help="API keys file path")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    parser.add_argument("--save-log", "-s", action="store_true", help="Save session log")
    parser.add_argument("--version", "-V", action="version", version=f"llm-computer-use {__version__}")
    
    args = parser.parse_args()
    
    if not args.task:
        parser.print_help()
        sys.exit(0)
    
    api_key = load_api_key(args.keys_file)
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found")
        print("Set via environment or --keys-file")
        sys.exit(1)
    
    from .core import AgentSession
    
    session = AgentSession(
        task_prompt=args.task,
        max_iterations=args.max_iterations,
        dry_run=not args.execute,
        model=args.model,
    )
    
    def confirm_action(action):
        print(f"\nHIGH-RISK: {action.action_type.value}")
        if action.coordinate:
            print(f"  Coordinate: {action.coordinate}")
        if action.text:
            print(f"  Text: {action.text[:50]}...")
        if action.key:
            print(f"  Key: {action.key}")
        return input("Allow? (y/N): ").strip().lower() == "y"
    
    if args.execute:
        session.set_confirm_callback(confirm_action)
    
    try:
        summary = session.run(verbose=not args.quiet)
    except KeyboardInterrupt:
        print("\nInterrupted")
        summary = {"status": "cancelled", "error": "User interrupt"}
    
    if args.save_log:
        print(f"\nLog: {session.save_log()}")
    
    if not args.quiet:
        print(f"\n{'='*60}\nSESSION SUMMARY\n{'='*60}")
        print(f"Status:      {summary.get('status', 'unknown')}")
        print(f"Model:       {summary.get('model', 'unknown')}")
        print(f"Iterations:  {summary.get('iterations', 0)}/{summary.get('max_iterations', 0)}")
        print(f"Actions:     {summary.get('actions_count', 0)}")
        print(f"Tokens:      {summary.get('total_input_tokens', 0)} in / {summary.get('total_output_tokens', 0)} out")
        print(f"Duration:    {summary.get('total_duration_ms', 0):.0f} ms (API: {summary.get('total_api_latency_ms', 0):.0f} ms)")
        print(f"Cost:        ${summary.get('estimated_cost_usd', 0):.6f} USD")
        if summary.get("error"):
            print(f"Error:       {summary['error']}")
        print(f"{'='*60}")
    
    sys.exit(0 if summary.get("status") == "completed" else 1)

if __name__ == "__main__":
    main()
