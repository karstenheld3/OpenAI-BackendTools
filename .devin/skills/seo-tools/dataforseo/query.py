"""DataForSEO API Query Script.

Subcommands: balance, keywords, serp, competitors, backlinks
Docs: https://docs.dataforseo.com/v3/

Examples:
    python query.py balance
    python query.py keywords "AI compliance"
    python query.py keywords "regulatory reporting" --location 2840 --lang de --limit 30
    python query.py serp "DORA automation software"
    python query.py competitors yourdomain.com
    python query.py backlinks competitor.com
"""

import argparse
import json
import sys

import requests

API_KEYS_PATH = r"E:\Dev\.tools\.api-keys.txt"
BASE_URL_LIVE = "https://api.dataforseo.com/v3"
BASE_URL_SANDBOX = "https://sandbox.dataforseo.com/v3"


def load_credentials(path: str = API_KEYS_PATH) -> dict:
    """Load API keys from .api-keys.txt file."""
    keys = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                keys[k] = v
    return keys


def get_headers(keys: dict) -> dict:
    """Build request headers with Basic Auth."""
    return {
        "Authorization": f"Basic {keys['DATAFORSEO_BASE64']}",
        "Content-Type": "application/json",
    }


BASE_URL = BASE_URL_LIVE


def api_post(endpoint: str, body: list, headers: dict) -> dict:
    """POST to DataForSEO API with error handling."""
    print(f"Querying '{endpoint}'...", file=sys.stderr)
    r = requests.post(f"{BASE_URL}/{endpoint}", headers=headers, data=json.dumps(body), timeout=30)
    if r.status_code != 200:
        try:
            err = r.json()
            msg = err.get("status_message", r.text[:200])
        except (ValueError, KeyError):
            msg = r.text[:200]
        if r.status_code == 403 and "verify" in msg.lower():
            print("Account not verified. Verify at: 'https://app.dataforseo.com/'", file=sys.stderr)
        else:
            print(f"Request failed -> HTTP {r.status_code} -> {msg}", file=sys.stderr)
            print("HINT: If account is unverified, all data endpoints fail. Verify at: 'https://app.dataforseo.com/'", file=sys.stderr)
        sys.exit(1)
    data = r.json()
    if data["status_code"] != 20000:
        print(f"API error -> {data['status_code']} -> {data['status_message']}", file=sys.stderr)
        print("HINT: If account is unverified, all data endpoints fail. Verify at: 'https://app.dataforseo.com/'", file=sys.stderr)
        sys.exit(1)
    task = data["tasks"][0]
    if task["status_code"] != 20000:
        print(f"Task error -> {task['status_code']} -> {task['status_message']}", file=sys.stderr)
        print("HINT: If account is unverified, all data endpoints fail. Verify at: 'https://app.dataforseo.com/'", file=sys.stderr)
        sys.exit(1)
    return task


def cmd_balance(args, headers):
    """Check account balance and usage stats."""
    print("Fetching account balance...", file=sys.stderr)
    r = requests.get(f"{BASE_URL_LIVE}/appendix/user_data", headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()["tasks"][0]["result"][0]["money"]
    print(f"Balance:      ${data['balance']:.2f}")
    print(f"Total spent:  ${data['total']:.2f}")
    print(f"Limit/day:    ${data.get('limit_daily', '[UNKNOWN]')}")


def cmd_keywords(args, headers):
    """Get keyword suggestions for a seed keyword. Cost: $0.0006/task."""
    task = api_post("dataforseo_labs/google/keyword_suggestions/live", [{
        "keyword": args.keyword,
        "location_code": args.location,
        "language_code": args.lang,
        "limit": args.limit,
        "include_seed_keyword": True,
    }], headers)

    items = task["result"][0]["items"]
    if not items:
        print("0 suggestions found.")
        return

    print(f"{'Keyword':<45} {'Volume':>7} {'Diff':>5} {'CPC':>6} {'Intent':<12}")
    print("-" * 85)
    sorted_items = sorted(items, key=lambda x: (x.get("keyword_info", {}).get("search_volume") or 0), reverse=True)
    for item in sorted_items[:args.limit]:
        ki = item.get("keyword_info", {})
        kp = item.get("keyword_properties", {})
        si = item.get("search_intent_info", {})
        kw = item.get("keyword", "")
        vol = ki.get("search_volume") or 0
        diff = kp.get("keyword_difficulty") or 0
        cpc = ki.get("cpc") or 0.0
        intent = si.get("main_intent", "")
        print(f"{kw:<45} {vol:>7} {diff:>5} {cpc:>6.2f} {intent:<12}")

    print(f"\n{len(items)} suggestions found. Cost: ~$0.0006.")


def cmd_serp(args, headers):
    """Get live SERP results for a keyword. Cost: $0.002/task."""
    task = api_post("serp/google/organic/live/advanced", [{
        "keyword": args.keyword,
        "location_code": args.location,
        "language_code": args.lang,
        "device": args.device,
    }], headers)

    result = task["result"][0]
    items = result.get("items", [])
    organics = [i for i in items if i.get("type") == "organic"]

    print(f"SERP for: keyword='{args.keyword}' (location={args.location}, device='{args.device}')")
    print(f"{result.get('se_results_count', '[UNKNOWN]')} total results.")
    print(f"\n{'#':>3} {'Domain':<35} {'Title':<50}")
    print("-" * 90)
    for o in organics[:10]:
        pos = o.get("rank_absolute", "?")
        domain = (o.get("domain") or "")[:34]
        title = (o.get("title") or "")[:49]
        print(f"{pos:>3} {domain:<35} {title:<50}")

    # Show AI Overview if present
    ai_items = [i for i in items if i.get("type") == "ai_overview"]
    if ai_items:
        print(f"\n[AI Overview present - {len(ai_items)} block(s)]")

    print(f"\nCost: ~$0.002.")


def cmd_competitors(args, headers):
    """Find SERP competitors for a domain. Cost: $0.0006/task."""
    task = api_post("dataforseo_labs/google/competitors_domain/live", [{
        "target": args.domain,
        "location_code": args.location,
        "language_code": args.lang,
        "limit": args.limit,
    }], headers)

    items = task["result"][0].get("items", [])
    if not items:
        print(f"0 competitors found for '{args.domain}'.")
        return

    print(f"Competitors for: target='{args.domain}' (location={args.location})")
    print(f"\n{'Domain':<40} {'AvgPos':>7} {'Overlap':>8} {'Keywords':>9} {'Traffic':>10}")
    print("-" * 78)
    for item in items[:args.limit]:
        domain = (item.get("domain") or "")[:39]
        avg_pos = item.get("avg_position") or 0
        intersections = item.get("intersections") or 0
        fdm = item.get("full_domain_metrics", {}).get("organic", {})
        keywords = fdm.get("count") or 0
        traffic = fdm.get("etv") or 0
        print(f"{domain:<40} {avg_pos:>7.1f} {intersections:>8} {keywords:>9} {traffic:>10.0f}")

    print(f"\n{len(items)} competitors found. Cost: ~$0.0006.")


def cmd_backlinks(args, headers):
    """Get backlink summary for a domain. Cost: $0.002/task."""
    task = api_post("backlinks/summary/live", [{
        "target": args.domain,
        "internal_list_limit": 0,
        "backlinks_status_type": "all",
    }], headers)

    result = task["result"][0]
    print(f"Backlink summary for: target='{args.domain}'")
    print(f"\n  Total backlinks:     {result.get('backlinks', 0):>10,}")
    print(f"  Referring domains:   {result.get('referring_domains', 0):>10,}")
    print(f"  Referring IPs:       {result.get('referring_ips', 0):>10,}")
    print(f"  Referring subnets:   {result.get('referring_subnets', 0):>10,}")
    print(f"  Domain rank:         {result.get('rank', 0):>10}")
    print(f"  Broken backlinks:    {result.get('broken_backlinks', 0):>10,}")
    print(f"  Broken pages:        {result.get('broken_pages', 0):>10,}")

    print(f"\nCost: ~$0.002.")


def main():
    parser = argparse.ArgumentParser(
        description="DataForSEO API CLI - SEO data queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Location codes: 2276=Germany, 2840=US, 2826=UK, 2250=France",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # balance
    sub.add_parser("balance", help="Check account balance")

    # keywords
    p_kw = sub.add_parser("keywords", help="Keyword suggestions (cost: $0.0006)")
    p_kw.add_argument("keyword", help="Seed keyword")
    p_kw.add_argument("--location", type=int, default=2276, help="Location code (default: 2276=Germany)")
    p_kw.add_argument("--lang", default="en", help="Language code (default: en)")
    p_kw.add_argument("--limit", type=int, default=30, help="Max results (default: 30, max: 700)")

    # serp
    p_serp = sub.add_parser("serp", help="Live SERP results (cost: $0.002)")
    p_serp.add_argument("keyword", help="Search query")
    p_serp.add_argument("--location", type=int, default=2276, help="Location code (default: 2276=Germany)")
    p_serp.add_argument("--lang", default="en", help="Language code (default: en)")
    p_serp.add_argument("--device", default="desktop", choices=["desktop", "mobile"], help="Device type")

    # competitors
    p_comp = sub.add_parser("competitors", help="Find SERP competitors (cost: $0.0006)")
    p_comp.add_argument("domain", help="Target domain (e.g., yourdomain.com)")
    p_comp.add_argument("--location", type=int, default=2276, help="Location code (default: 2276=Germany)")
    p_comp.add_argument("--lang", default="en", help="Language code (default: en)")
    p_comp.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")

    # backlinks
    p_bl = sub.add_parser("backlinks", help="Backlink summary (cost: $0.002)")
    p_bl.add_argument("domain", help="Target domain (e.g., competitor.com)")

    parser.add_argument("--sandbox", action="store_true", help="Use sandbox (dummy data, still requires verification)")

    args = parser.parse_args()

    global BASE_URL
    if args.sandbox:
        BASE_URL = BASE_URL_SANDBOX
        print("[SANDBOX MODE - results are dummy data]\n")

    keys = load_credentials()
    headers = get_headers(keys)

    commands = {
        "balance": cmd_balance,
        "keywords": cmd_keywords,
        "serp": cmd_serp,
        "competitors": cmd_competitors,
        "backlinks": cmd_backlinks,
    }
    commands[args.command](args, headers)


if __name__ == "__main__":
    main()
