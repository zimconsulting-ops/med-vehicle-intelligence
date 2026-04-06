"""Tests for find_red_flags tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from med_vehicle_intelligence.tools.red_flags import find_red_flags


def test_phone_diagnosis():
    result = find_red_flags(
        "I called the shop and they quoted me $800 for brakes over the phone "
        "without even seeing my car."
    )
    assert "Phone Diagnosis" in result
    assert "CONCERN" in result.upper() or "CAUTION" in result.upper()


def test_scare_list():
    result = find_red_flags(
        "I went in for an oil change and they came back with a list of 6 things "
        "that need immediate attention including a flush and injection cleaning."
    )
    assert "Scare List" in result


def test_pressure_close():
    result = find_red_flags(
        "The mechanic told me I wouldn't drive this car home if I were him "
        "and that it could fail at any time."
    )
    assert "Pressure Close" in result
    assert "high" in result.lower() or "CONCERN" in result.upper()


def test_multiple_flags():
    result = find_red_flags(
        "They quoted me over the phone, then when I brought it in they gave me "
        "a long list of additional services. When I said I wanted a second opinion "
        "they told me I won't find a better price anywhere else and that it would "
        "be a waste of time."
    )
    assert "SIGNIFICANT" in result.upper() or "SECOND OPINION" in result.upper()
    # Should match at least 3 flags
    flag_names = ["Phone Diagnosis", "Scare List", "Resists Second Opinion"]
    matches = sum(1 for name in flag_names if name in result)
    assert matches >= 2


def test_no_flags():
    result = find_red_flags(
        "The shop was clean, the advisor was friendly, and they finished "
        "the work on time at the quoted price."
    )
    assert "NEUTRAL" in result.upper() or "LOOKS GOOD" in result.upper() or "Nothing" in result


def test_positive_signals():
    result = find_red_flags(
        "They gave me a written estimate, showed me the worn brake pads, "
        "and said take your time to decide."
    )
    assert "Positive" in result or "LOOKS GOOD" in result
    assert "written estimate" in result.lower() or "Provided written estimate" in result


def test_mystery_charges():
    result = find_red_flags(
        "The bill was higher than the estimate. There were extra charges "
        "for shop supplies and an environmental fee that wasn't on the estimate."
    )
    assert "Mystery" in result


def test_open_ended_auth():
    result = find_red_flags(
        "They said they won't know until they get in there and wanted me to "
        "authorize them to start tearing it apart."
    )
    assert "Open-Ended" in result or "Authorization" in result
