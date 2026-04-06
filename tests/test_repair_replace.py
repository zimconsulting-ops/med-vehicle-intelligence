"""Tests for repair_or_replace tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from med_vehicle_intelligence.tools.repair_replace import repair_or_replace


def test_clear_fix():
    """Under 30% ratio should recommend fix."""
    result = repair_or_replace(
        vehicle_year=2020,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        repair_cost=800,
        vehicle_value=18000,
    )
    assert "FIX" in result
    assert "4%" in result or "5%" in result  # ratio ~4.4%


def test_gray_zone():
    """30-50% ratio should flag as gray zone."""
    result = repair_or_replace(
        vehicle_year=2015,
        vehicle_make="Honda",
        vehicle_model="Civic",
        repair_cost=3000,
        vehicle_value=8000,
    )
    assert "GRAY ZONE" in result or "JUDGMENT" in result


def test_clear_replace():
    """Over 75% ratio should recommend replace."""
    result = repair_or_replace(
        vehicle_year=2008,
        vehicle_make="Ford",
        vehicle_model="F-150",
        repair_cost=4000,
        vehicle_value=4500,
    )
    assert "REPLACE" in result


def test_high_mileage_modifier():
    """High mileage should push toward replace."""
    result = repair_or_replace(
        vehicle_year=2012,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        repair_cost=2000,
        vehicle_value=6000,
        vehicle_mileage=175000,
    )
    assert "175,000" in result
    assert "High mileage" in result or "mileage" in result.lower()


def test_low_mileage_modifier():
    """Low mileage should push toward fix."""
    result = repair_or_replace(
        vehicle_year=2019,
        vehicle_make="Honda",
        vehicle_model="Civic",
        repair_cost=2500,
        vehicle_value=12000,
        vehicle_mileage=65000,
    )
    assert "65,000" in result


def test_high_annual_spend():
    result = repair_or_replace(
        vehicle_year=2013,
        vehicle_make="Chevrolet",
        vehicle_model="Silverado",
        repair_cost=1500,
        vehicle_value=8000,
        annual_repair_spend=3500,
    )
    assert "repair spending" in result.lower() or "$3,500" in result


def test_replacement_cost_math():
    """Should always include replacement cost comparison."""
    result = repair_or_replace(
        vehicle_year=2016,
        vehicle_make="Toyota",
        vehicle_model="RAV4",
        repair_cost=3000,
        vehicle_value=12000,
    )
    assert "replacement cost" in result.lower()
    assert "$450" in result or "payment" in result.lower()


def test_zero_vehicle_value():
    result = repair_or_replace(
        vehicle_year=2010,
        vehicle_make="Honda",
        vehicle_model="Civic",
        repair_cost=1000,
        vehicle_value=0,
    )
    assert "greater than $0" in result
