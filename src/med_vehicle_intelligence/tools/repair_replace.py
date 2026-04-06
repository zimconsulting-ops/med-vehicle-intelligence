"""Tool: repair_or_replace — Should you fix your car or start shopping?"""

from ..knowledge.loader import VEHICLE_ISSUES
from ..config import CTA_REPAIR_REPLACE


def repair_or_replace(
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    repair_cost: float,
    vehicle_value: float,
    vehicle_mileage: int = 0,
    annual_repair_spend: float = 0,
) -> str:
    """Get a fix-or-replace recommendation based on repair cost, vehicle value, and situation.

    Args:
        vehicle_year: Model year of the vehicle (e.g., 2015)
        vehicle_make: Vehicle manufacturer (e.g., "Honda")
        vehicle_model: Vehicle model (e.g., "Civic")
        repair_cost: Cost of the repair you're facing in dollars
        vehicle_value: Estimated current market value of the vehicle in dollars (check KBB or Edmunds)
        vehicle_mileage: Current odometer reading in miles (0 if unknown)
        annual_repair_spend: Total spent on non-routine repairs in the past 12 months (0 if unknown)
    """
    vehicle_str = f"{vehicle_year} {vehicle_make} {vehicle_model}"
    vehicle_age = 2026 - vehicle_year

    # Core calculation: repair cost as percentage of vehicle value
    if vehicle_value <= 0:
        return (
            f"## Fix or Replace: {vehicle_str}\n\n"
            "Vehicle value must be greater than $0 to calculate. "
            "Check KBB.com or Edmunds.com for your vehicle's current market value."
        )

    ratio = (repair_cost / vehicle_value) * 100

    # Base recommendation from ratio
    if ratio <= 30:
        recommendation = "FIX"
        ratio_text = (
            f"At {ratio:.0f}% of your vehicle's value, this repair makes financial sense. "
            f"The cost is well below the threshold where replacement becomes the better investment."
        )
        fix_points = 2
        replace_points = 0
    elif ratio <= 50:
        recommendation = "GRAY ZONE"
        ratio_text = (
            f"At {ratio:.0f}% of your vehicle's value, this is in the gray zone. "
            f"The repair isn't clearly worth it or clearly not — other factors will tip the decision."
        )
        fix_points = 0
        replace_points = 0
    elif ratio <= 75:
        recommendation = "LEAN REPLACE"
        ratio_text = (
            f"At {ratio:.0f}% of your vehicle's value, the math leans toward replacement. "
            f"You're spending a significant portion of the vehicle's worth on a single repair."
        )
        fix_points = 0
        replace_points = 1
    else:
        recommendation = "REPLACE"
        ratio_text = (
            f"At {ratio:.0f}% of your vehicle's value, replacement is likely the better financial move. "
            f"This repair costs more than what the vehicle is worth to keep running."
        )
        fix_points = 0
        replace_points = 2

    # Modifiers
    modifiers = []

    if vehicle_mileage > 0:
        if vehicle_mileage > 150000:
            replace_points += 1
            modifiers.append(f"- High mileage ({vehicle_mileage:,} mi) — increases likelihood of additional repairs")
        elif vehicle_mileage < 100000:
            fix_points += 1
            modifiers.append(f"- Moderate mileage ({vehicle_mileage:,} mi) — vehicle likely has significant life remaining")

    if annual_repair_spend > 2000:
        replace_points += 1
        modifiers.append(f"- High recent repair spending (${annual_repair_spend:,.0f}/yr) — pattern of escalating costs")
    elif annual_repair_spend > 0 and annual_repair_spend <= 500:
        fix_points += 1
        modifiers.append(f"- Low recent repair spending (${annual_repair_spend:,.0f}/yr) — vehicle has been reliable")

    if vehicle_age > 15:
        replace_points += 1
        modifiers.append(f"- Vehicle age ({vehicle_age} years) — rubber components, electrical, and body deterioration become factors")
    elif vehicle_age <= 5:
        fix_points += 1
        modifiers.append(f"- Newer vehicle ({vehicle_age} years) — plenty of service life remaining")

    # Final recommendation
    score_diff = fix_points - replace_points
    if score_diff >= 3:
        final = "REPAIR — The math and your situation both support fixing this vehicle."
    elif score_diff >= 1:
        final = "LEAN REPAIR — The balance favors fixing, but it's not overwhelming. Consider how confident you feel about the vehicle's next 12 months."
    elif score_diff >= -1:
        final = "JUDGMENT CALL — The numbers are close. Two questions to break the tie: (1) If you repair it today, would you feel confident driving it for the next 12 months? (2) Can you afford a replacement without financial strain?"
    elif score_diff >= -3:
        final = "LEAN REPLACE — Multiple factors point toward moving on. Start looking, but don't rush into a bad deal."
    else:
        final = "REPLACE — The vehicle has reached the point where continued repairs are unlikely to be a good investment."

    # Replacement cost reality check
    replacement_math = (
        "### The replacement cost reality\n"
        "Before deciding to replace, run these numbers:\n"
        "- Monthly payment: $450-600/mo (typical for used vehicle financing)\n"
        "- Insurance increase: $50-150/mo more than your current vehicle\n"
        "- First-year depreciation: $2,000-5,000\n"
        "- Registration and taxes: varies by state\n"
        f"- **Total first-year cost of replacement: roughly $8,000-14,000**\n"
        f"- **Your repair cost: ${repair_cost:,.0f}**\n\n"
        "A repair that keeps a known vehicle on the road for another 1-2 years "
        "is often cheaper than the first year of a replacement — even when the ratio looks bad."
    )

    # Vehicle-specific notes
    lookup = f"{vehicle_make.lower()}_{vehicle_model.lower().replace('-', '').replace(' ', '_')}"
    vehicle_data = VEHICLE_ISSUES.get("vehicles", {}).get(lookup)
    vehicle_section = ""
    if vehicle_data:
        reliability = vehicle_data.get("reliability", "unknown")
        reliability_text = {
            "above_average": "generally above average — this works in favor of repairing",
            "average": "about average for its class",
            "below_average": "below average — factor this into your decision",
        }.get(reliability, "")
        if reliability_text:
            vehicle_section = f"\n### {vehicle_make} {vehicle_model} reliability\nOverall reliability is {reliability_text}.\n"

    # Build response
    lines = [
        f"## Fix or Replace: {vehicle_str}",
        "",
        f"**Repair cost:** ${repair_cost:,.0f} | **Vehicle value:** ${vehicle_value:,.0f} | **Ratio:** {ratio:.0f}%",
        "",
        f"### {recommendation}",
        "",
        ratio_text,
        "",
    ]

    if modifiers:
        lines.extend([
            "### Additional factors",
            *modifiers,
            "",
        ])

    lines.extend([
        f"### Bottom line",
        final,
        "",
        f"**Score: FIX {fix_points} — REPLACE {replace_points}**",
        "",
        replacement_math,
    ])

    if vehicle_section:
        lines.append(vehicle_section)

    lines.append(CTA_REPAIR_REPLACE)
    return "\n".join(lines)
