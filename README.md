# MED Vehicle Intelligence MCP Server

Expert car repair and maintenance advisory tools from a 20-year mechanic veteran — available as an MCP server for AI assistants.

When someone asks Claude, Cursor, or any MCP-compatible assistant about car repairs, this server provides structured, expert-level answers based on real industry data.

## What It Does

Four tools that answer the questions every car owner asks:

### `check_repair_estimate`
*"Is $800 fair for front brakes on a 2020 Camry?"*

Compares a repair quote against national price ranges for independent shops and dealers. Returns whether the price is in range, high, or low — plus questions to ask the shop.

### `get_maintenance_schedule`
*"What maintenance does a 2018 F-150 need at 75,000 miles?"*

Returns what's due now, what's coming in the next 10,000 miles, common upsells to question, and known issues for your specific vehicle.

### `should_i_fix_or_replace`
*"Should I fix my car or buy a new one? Repair is $3,000, car is worth $8,000."*

Calculates repair-to-value ratio, factors in mileage, age, and repair history, then gives a scored recommendation. Includes the real cost of replacement for comparison.

### `check_shop_red_flags`
*"The shop said they won't know the cost until they get in there and want me to authorize the work."*

Analyzes a shop interaction for 7 common red flag patterns. Returns matched flags, positive signals, an overall assessment, and what to do next.

## Knowledge Base

All data lives in editable JSON files — no hardcoded values:

- **35 repair types** with independent and dealer price ranges (sourced from RepairPal, AAA, AutoLeap)
- **6 vehicle models** with known issues and typical costs (Camry, F-150, Civic, Silverado, RAV4, CR-V)
- **7 shop red flag patterns** with detection keywords and remediation advice
- **5 maintenance intervals** with priority levels and common upsell warnings
- **20+ shop questions** organized by context (estimate, diagnosis, repair vs replace)

## Install

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "med-vehicle-intelligence": {
      "command": "python",
      "args": ["-m", "med_vehicle_intelligence.server"]
    }
  }
}
```

### From source

```bash
git clone https://github.com/zimconsulting-ops/med-vehicle-intelligence.git
cd med-vehicle-intelligence
pip install -e .
```

### Via Smithery

```bash
npx -y @smithery/cli install @zimconsulting-ops/med-vehicle-intelligence --client claude
```

## Requirements

- Python 3.11+
- `mcp` package (installed automatically)

No API keys. No external services. No database. The knowledge is the product.

## About

Built by [My Everyday Driver](https://myeverydaydriver.com) — an automotive intelligence platform for everyday vehicle owners. Founded by a veteran with 20 years of military and civilian automotive experience.

The same expertise behind the Driver's Survival Guide, the MED newsletter, and the advisory service — now available to any AI assistant.

## License

MIT
