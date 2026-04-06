"""Tests for check_estimate tool."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from med_vehicle_intelligence.tools.check_estimate import check_estimate


def test_in_range_estimate():
    result = check_estimate(
        repair_type="front brakes",
        vehicle_year=2020,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        quoted_price=250,
    )
    assert "WITHIN TYPICAL RANGE" in result
    assert "Toyota Camry" in result


def test_high_estimate():
    result = check_estimate(
        repair_type="alternator",
        vehicle_year=2018,
        vehicle_make="Honda",
        vehicle_model="Civic",
        quoted_price=1500,
    )
    assert "ABOVE TYPICAL RANGE" in result or "SIGNIFICANTLY ABOVE" in result


def test_low_estimate():
    result = check_estimate(
        repair_type="timing chain",
        vehicle_year=2016,
        vehicle_make="Chevrolet",
        vehicle_model="Silverado",
        quoted_price=500,
    )
    assert "BELOW TYPICAL RANGE" in result


def test_unknown_repair_type():
    result = check_estimate(
        repair_type="flux capacitor rebuild",
        vehicle_year=2020,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        quoted_price=1000,
    )
    assert "don't have specific benchmark data" in result
    assert "Questions to ask" in result


def test_alias_resolution():
    result = check_estimate(
        repair_type="brakes",
        vehicle_year=2020,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        quoted_price=300,
    )
    assert "WITHIN TYPICAL RANGE" in result


def test_dealer_pricing():
    result = check_estimate(
        repair_type="oil change",
        vehicle_year=2022,
        vehicle_make="Ford",
        vehicle_model="F-150",
        quoted_price=150,
        shop_type="dealer",
    )
    assert "dealer" in result.lower()
    assert "WITHIN TYPICAL RANGE" in result


def test_vehicle_specific_notes():
    result = check_estimate(
        repair_type="starter",
        vehicle_year=2019,
        vehicle_make="Chevrolet",
        vehicle_model="Silverado",
        quoted_price=600,
    )
    assert "Known issues" in result or "Silverado" in result


def test_questions_included():
    result = check_estimate(
        repair_type="water pump",
        vehicle_year=2017,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        quoted_price=700,
    )
    assert "Questions to ask" in result
