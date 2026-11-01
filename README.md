# genpark-agentic-commerce-contract-tiered-volume-rebate-clawback-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

B2B buyer-seller retrospective volume rebate tiers, hurdle threshold attainment & shortfall clawback auditor.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `audit_volume_rebate_attainment`
- **Category**: `agentic_commerce`

### Method Documentation
Audit annual B2B supplier contract volume rebates and clawbacks.
Evaluates progressive vs retrospective hurdle tiers (e.g. Tier 1: $1M @ 2%, Tier 2: $3M @ 4%, Tier 3: $5M @ 6%),
calculates accrued rebate earned, and flags early-settled rebate clawbacks if actual spend falls short of annual commit.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "audit_volume_rebate_attainment",
    "arguments": {
    "actual_spend_usd": 2850000.0,
    "rebate_tiers": [
        {
            "tier_name": "Bronze",
            "spend_threshold_usd": 1000000.0,
            "rebate_pct": 2.5
        },
        {
            "tier_name": "Silver",
            "spend_threshold_usd": 2500000.0,
            "rebate_pct": 4.0
        },
        {
            "tier_name": "Gold",
            "spend_threshold_usd": 5000000.0,
            "rebate_pct": 6.5
        }
    ],
    "upfront_rebate_prepaid_usd": 150000.0
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
