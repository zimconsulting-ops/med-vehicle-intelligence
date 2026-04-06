"""Tool: find_red_flags — Detect shop interaction warning signs."""

from ..knowledge.loader import RED_FLAGS, SHOP_QUESTIONS
from ..config import CTA_RED_FLAGS


def find_red_flags(description: str) -> str:
    """Analyze a shop interaction for red flags and warning signs.

    Describe what happened at the shop — what they said, what they quoted,
    how they acted — and get an assessment of whether anything seems off.

    Args:
        description: Your description of the shop interaction, estimate, or experience
    """
    text = description.lower()
    flags_data = RED_FLAGS["red_flags"]
    positive_data = RED_FLAGS["positive_signals"]

    # Check for red flags
    matched_flags = []
    for flag in flags_data:
        for keyword in flag["pattern_keywords"]:
            if keyword in text:
                matched_flags.append(flag)
                break  # One match per flag is enough

    # Check for positive signals
    matched_positives = []
    for signal in positive_data:
        for keyword in signal["keywords"]:
            if keyword in text:
                matched_positives.append(signal["signal"])
                break

    # Determine overall assessment
    flag_count = len(matched_flags)
    positive_count = len(matched_positives)

    if flag_count == 0 and positive_count == 0:
        overall = (
            "Nothing in your description triggers specific red flags, "
            "but I also don't see clear positive signals. "
            "Trust your instincts — if something felt off, it's worth investigating."
        )
        severity = "NEUTRAL"
    elif flag_count == 0:
        overall = (
            "No red flags detected, and there are positive signs in your description. "
            "This sounds like a shop that's operating the way a good one should."
        )
        severity = "LOOKS GOOD"
    elif flag_count <= 2:
        high_severity = any(f["severity"] == "high" for f in matched_flags)
        if high_severity:
            overall = (
                "There are concerns worth addressing. At least one is a significant warning sign. "
                "Ask the follow-up questions below before authorizing any work."
            )
            severity = "CONCERNS — PROCEED WITH CAUTION"
        else:
            overall = (
                "There are minor concerns worth noting, but nothing that necessarily means the shop "
                "is acting in bad faith. Ask the follow-up questions to clarify."
            )
            severity = "MINOR CONCERNS"
    else:
        overall = (
            f"Multiple red flags detected ({flag_count}). This pattern suggests you should "
            "get a second opinion from a different shop before authorizing any work. "
            "A good shop has no reason to exhibit these behaviors."
        )
        severity = "SIGNIFICANT CONCERNS — GET A SECOND OPINION"

    # Build response
    lines = [
        "## Shop Interaction Assessment",
        "",
        f"**Overall: {severity}**",
        "",
        overall,
    ]

    if matched_flags:
        lines.extend(["", "### Red Flags Detected"])
        for flag in matched_flags:
            severity_tag = " ⚠️" if flag["severity"] == "high" else ""
            lines.extend([
                f"",
                f"**{flag['name']}**{severity_tag}",
                f"{flag['description']}",
                f"",
                f"*Why it's a problem:* {flag['why_problematic']}",
                f"",
                f"*What to do:* {flag['what_to_do']}",
            ])

    if matched_positives:
        lines.extend([
            "",
            "### Positive Signals",
            *[f"- {signal}" for signal in matched_positives],
        ])

    # Add relevant questions
    if matched_flags:
        questions = SHOP_QUESTIONS["contexts"]["before_approving_repair"]
        lines.extend([
            "",
            "### Questions to Ask",
            *[f"- {q}" for q in questions[:4]],
        ])

    lines.append(CTA_RED_FLAGS)
    return "\n".join(lines)
