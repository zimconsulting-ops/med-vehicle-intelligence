"""Tool: maintenance_schedule — What maintenance is due based on mileage."""

from ..knowledge.loader import MAINTENANCE, VEHICLE_ISSUES, SHOP_QUESTIONS
from ..config import CTA_MAINTENANCE


def _get_vehicle_notes(make: str, model: str) -> list[str]:
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


def maintenance_schedule(
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    current_mileage: int,
) -> str:
    """Get a maintenance schedule based on your vehicle and current mileage.

    Args:
        vehicle_year: Model year of the vehicle (e.g., 2020)
        vehicle_make: Vehicle manufacturer (e.g., "Toyota")
        vehicle_model: Vehicle model (e.g., "Camry")
        current_mileage: Current odometer reading in miles
    """
    vehicle_str = f"{vehicle_year} {vehicle_make} {vehicle_model}"
    vehicle_age = 2026 - vehicle_year
    intervals = MAINTENANCE["intervals"]

    due_now = []
    coming_up = []

    for interval in intervals:
        interval_miles = interval["mileage"]

        # Find the most recent service point for this interval
        if current_mileage >= interval_miles:
            # How many intervals have passed?
            intervals_passed = current_mileage // interval_miles
            last_due_at = intervals_passed * interval_miles
            next_due_at = (intervals_passed + 1) * interval_miles

            # If we're within one interval of the last due point, it's due now
            # (conservative: if you haven't done it since the last milestone)
            miles_since_due = current_mileage - last_due_at
            if miles_since_due < interval_miles:
                # Recently passed a milestone — these items are due
                for item in interval["items"]:
                    due_now.append({
                        "service": item["service"],
                        "priority": item["priority"],
                        "due_at": last_due_at,
                        "notes": item.get("notes", ""),
                    })

            # Check if next milestone is within 10K
            if next_due_at - current_mileage <= 10000:
                for item in interval["items"]:
                    coming_up.append({
                        "service": item["service"],
                        "priority": item["priority"],
                        "due_at": next_due_at,
                        "notes": item.get("notes", ""),
                    })
        else:
            # Haven't reached this interval yet — is it coming within 10K?
            if interval_miles - current_mileage <= 10000:
                for item in interval["items"]:
                    coming_up.append({
                        "service": item["service"],
                        "priority": item["priority"],
                        "due_at": interval_miles,
                        "notes": item.get("notes", ""),
                    })

    # Deduplicate — if something is in both due_now and coming_up, keep only due_now
    due_services = {item["service"] for item in due_now}
    coming_up = [item for item in coming_up if item["service"] not in due_services]

    # Build response
    lines = [
        f"## Maintenance Schedule: {vehicle_str}",
        f"**Current mileage:** {current_mileage:,} miles | **Vehicle age:** {vehicle_age} years",
        "",
    ]

    if due_now:
        lines.append("### Due Now or Recently Due")
        # Sort by priority
        priority_order = {"critical": 0, "recommended": 1, "low": 2}
        due_now.sort(key=lambda x: priority_order.get(x["priority"], 3))
        for item in due_now:
            priority_tag = f"[{item['priority'].upper()}]" if item["priority"] == "critical" else ""
            note = f" — {item['notes']}" if item["notes"] else ""
            lines.append(f"- {priority_tag} **{item['service']}** (due at {item['due_at']:,} mi){note}")
    else:
        lines.append("### Due Now")
        lines.append("No major services due at this exact mileage. Check your owner's manual for your specific intervals.")

    lines.append("")

    if coming_up:
        lines.append("### Coming Up (next 10,000 miles)")
        for item in coming_up:
            note = f" — {item['notes']}" if item["notes"] else ""
            lines.append(f"- **{item['service']}** (at {item['due_at']:,} mi){note}")
    else:
        lines.append("### Coming Up")
        lines.append("No major interval services in the next 10,000 miles.")

    # Add upsells to watch for
    upsells = MAINTENANCE.get("common_upsells", [])
    if upsells:
        lines.extend(["", "### Common Upsells to Question"])
        for upsell in upsells[:4]:
            lines.append(
                f"- **{upsell['service']}** ({upsell['typical_cost_range']}): "
                f"{upsell['notes']}"
            )

    # Vehicle-specific notes
    vehicle_notes = _get_vehicle_notes(vehicle_make, vehicle_model)
    if vehicle_notes:
        lines.extend([
            "",
            f"### Known Issues for {vehicle_make} {vehicle_model}",
            *vehicle_notes,
        ])

    # Age-based notes
    if vehicle_age >= 8:
        lines.extend([
            "",
            "### Age-Based Notes",
            f"At {vehicle_age} years old, pay extra attention to:",
            "- Rubber components (hoses, belts, bushings) — they deteriorate with age regardless of mileage",
            "- Battery — if original or 4+ years old, get a load test",
            "- Suspension components — inspect struts/shocks for leaks or bounce",
        ])

    lines.append(CTA_MAINTENANCE)
    return "\n".join(lines)
