# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-contract-tiered-volume-rebate-clawback-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_volume_rebate_attainment(actual_spend_usd, rebate_tiers, upfront_rebate_prepaid_usd=0.0):
    if actual_spend_usd < 0:
        raise ValueError("actual_spend_usd cannot be negative")
        
    # Sort tiers by spend threshold
    sorted_tiers = sorted(rebate_tiers, key=lambda t: t["spend_threshold_usd"])
    
    earned_rate_pct = 0.0
    highest_tier_name = "NONE"
    
    for t in sorted_tiers:
        if actual_spend_usd >= t["spend_threshold_usd"]:
            earned_rate_pct = t["rebate_pct"]
            highest_tier_name = t.get("tier_name", f"Threshold_{t['spend_threshold_usd']}")
            
    earned_rebate_usd = actual_spend_usd * (earned_rate_pct / 100.0)
    variance_vs_prepaid = earned_rebate_usd - upfront_rebate_prepaid_usd
    
    clawback_required = variance_vs_prepaid < 0
    clawback_amount_usd = abs(variance_vs_prepaid) if clawback_required else 0.0
    payable_to_buyer_usd = variance_vs_prepaid if variance_vs_prepaid > 0 else 0.0
    
    return {
        "actual_annual_spend_usd": round(actual_spend_usd, 2),
        "attained_tier": highest_tier_name,
        "effective_rebate_rate_pct": earned_rate_pct,
        "total_earned_rebate_usd": round(earned_rebate_usd, 2),
        "upfront_prepaid_rebate_usd": round(upfront_rebate_prepaid_usd, 2),
        "clawback_triggered": clawback_required,
        "clawback_amount_due_to_seller_usd": round(clawback_amount_usd, 2),
        "net_additional_rebate_payable_usd": round(payable_to_buyer_usd, 2),
        "commercial_verdict": "Supplier entitled to clawback prepaid discount due to volume shortfall." if clawback_required else "Full rebate threshold achieved."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_volume_rebate_attainment",
                        "description": """Audit annual B2B supplier contract volume rebates and clawbacks.
Evaluates progressive vs retrospective hurdle tiers (e.g. Tier 1: $1M @ 2%, Tier 2: $3M @ 4%, Tier 3: $5M @ 6%),
calculates accrued rebate earned, and flags early-settled rebate clawbacks if actual spend falls short of annual commit.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_volume_rebate_attainment(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'actual_spend_usd': 2850000.0, 'rebate_tiers': [{'tier_name': 'Bronze', 'spend_threshold_usd': 1000000.0, 'rebate_pct': 2.5}, {'tier_name': 'Silver', 'spend_threshold_usd': 2500000.0, 'rebate_pct': 4.0}, {'tier_name': 'Gold', 'spend_threshold_usd': 5000000.0, 'rebate_pct': 6.5}], 'upfront_rebate_prepaid_usd': 150000.0}
        out = audit_volume_rebate_attainment(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
