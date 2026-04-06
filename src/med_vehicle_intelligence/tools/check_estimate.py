"""Tool: check_estimate — Evaluate whether a repair quote is fair."""

from ..knowledge.loader import REPAIR_COSTS, VEHICLE_ISSUES, SHOP_QUESTIONS
from ..config import CTA_ESTIMATE


def _resolve_repair(repair_type: str) -> tuple[str, dict | None]:
    """Resolve a repair type string to a canonical key and cost data."""
    normalized = repair_type.lower().strip()
    aliases = REPAIR_COSTS["aliases"]

    # Direct alias match
    if normalized in aliases:
        key = aliases[normalized]
    else:
        # Try partial match — alias must be a substantial match (>= 4 chars)
        # to avoid false positives like "ac" matching "flux capacitor"
        key = None
        for alias, canonical in sorted(aliases.items(), key=lambda x: -len(x[0])):
            if len(alias) < 4:
                continue
            if alias in normalized or normalized in alias:
                key = canonical
                break

    if key is None:
        return normalized, None

    # Find the cost data across categories
    for category_data in REPAIR_COSTS["categories"].values():
        if key in category_data:
            return key, category_data[key]

    return key, None


def _get_vehicle_notes(make: str, model: str) -> list[str]:
    """Get known issues for a vehicle if available."""
    lookup = f"{make.lower()}_{model.lower().replace('-', '').replace(' ', '_')}"
    vehicle = VEHICLE_ISSUES.get("vehicles", {}).get(lookup)
    if not vehicle:
        return []

    notes = []
    for issue in vehicle.get("known_issues", []):
        notes.append(
            f"- {issue['issue']} ({issue.get('years', 'various')}): "
            f"typically {issue['typical_cost']}"
        )
    return notes


def check_estimate(
    repair_type: str,
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    quoted_price: float,
    shop_type: str = "independent",
) -> str:
    """Evaluate whether a repair estimate is fair based on national averages.

    Args:
        repair_type: The repair being quoted (e.g., "front brakes", "timing chain", "alternator")
        vehicle_year: Model year of the vehicle (e.g., 2020)
        vehicle_make: Vehicle manufacturer (e.g., "Toyota")
        vehicle_model: Vehicle model (e.g., "Camry")
        quoted_price: The price you were quoted in dollars
        shop_type: Type of shop — "independent" or "dealer" (default: independent)
    """
    key, cost_data = _resolve_repair(repair_type)
    vehicle_str = f"{vehicle_year} {vehicle_make} {vehicle_model}"

    if cost_data is None:
        questions = SHOP_QUESTIONS["contexts"]["evaluating_estimate"]
        q_text = "\n".join(f"- {q}" for q in questions[:3])
        return (
            f"## Estimate Review: {repair_type.title()} — {vehicle_str}\n\n"
            f"I don't have specific benchmark data for '{repair_type}' in my database. "
            f"That doesn't mean the quote is unfair — this repair may have a wide cost range "
            f"depending on your specific vehicle and the parts required.\n\n"
            f"### Questions to ask the shop:\n{q_text}\n\n"
            f"### General guidance:\n"
            f"- Ask for parts and labor broken out separately\n"
            f"- Compare the labor hours quoted against a second shop's estimate\n"
            f"- Check whether OEM or aftermarket parts are being used — "
            f"aftermarket can be 30-50% less\n\n"
            f"National average labor rates: independent shops $120-150/hr, "
            f"dealers $150-200/hr."
            f"{CTA_ESTIMATE}"
        )

    # Get the right price range for shop type
    price_type = "dealer" if shop_type.lower() == "dealer" else "independent"
    price_range = cost_data[price_type]
    low = price_range["low"]
    high = price_range["high"]
    notes = cost_data.get("notes", "")

    # Assess the quote
    if quoted_price < low * 0.8:
        assessment = "BELOW TYPICAL RANGE"
        assessment_detail = (
            f"At ${quoted_price:,.0f}, this is significantly below the typical range. "
            f"This isn't necessarily bad, but verify:\n"
            f"- What quality of parts are being used?\n"
            f"- Is the shop cutting corners on labor time?\n"
            f"- Are there warranty implications?"
        )
    elif quoted_price <= high:
        assessment = "WITHIN TYPICAL RANGE"
        assessment_detail = (
            f"At ${quoted_price:,.0f}, this falls within the normal range "
            f"for this repair at an {price_type} shop."
        )
    elif quoted_price <= high * 1.25:
        pct_over = ((quoted_price - high) / high) * 100
        assessment = "ABOVE TYPICAL RANGE"
        assessment_detail = (
            f"At ${quoted_price:,.0f}, this is about {pct_over:.0f}% above the typical "
            f"high end for an {price_type} shop. This might be justified by your specific "
            f"vehicle, local labor rates, or OEM parts — but it's worth asking for a breakdown."
        )
    else:
        pct_over = ((quoted_price - high) / high) * 100
        assessment = "SIGNIFICANTLY ABOVE TYPICAL RANGE"
        assessment_detail = (
            f"At ${quoted_price:,.0f}, this is about {pct_over:.0f}% above the typical "
            f"high end. Get a second estimate before authorizing this work."
        )

    # Build response
    lines = [
        f"## Estimate Review: {repair_type.title()} — {vehicle_str}",
        "",
        f"**Assessment: {assessment}**",
        "",
        assessment_detail,
        "",
        f"### Typical price range ({price_type} shop)",
        f"- Low: ${low:,}",
        f"- High: ${high:,}",
        f"- Your quote: ${quoted_price:,.0f}",
    ]

    if notes:
        lines.append(f"- Note: {notes}")

    # Add vehicle-specific notes if available
    vehicle_notes = _get_vehicle_notes(vehicle_make, vehicle_model)
    if vehicle_notes:
        lines.extend([
            "",
            f"### Known issues for {vehicle_make} {vehicle_model}",
            *vehicle_notes,
        ])

    # Add questions
    questions = SHOP_QUESTIONS["contexts"]["evaluating_estimate"]
    lines.extend([
        "",
        "### Questions to ask",
        *[f"- {q}" for q in questions[:3]],
    ])

    lines.append(CTA_ESTIMATE)
    return "\n".join(lines)
