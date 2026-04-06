"""Tests for maintenance_schedule tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from med_vehicle_intelligence.tools.maintenance import maintenance_schedule


def test_low_mileage():
    result = maintenance_schedule(
        vehicle_year=2023,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        current_mileage=8000,
    )
    assert "Oil and filter change" in result
    assert "Maintenance Schedule" in result


def test_mid_mileage():
    result = maintenance_schedule(
        vehicle_year=2020,
        vehicle_make="Honda",
        vehicle_model="Civic",
        current_mileage=35000,
    )
    assert "Engine air filter" in result or "Cabin air filter" in result


def test_high_mileage():
    result = maintenance_schedule(
        vehicle_year=2018,
        vehicle_make="Ford",
        vehicle_model="F-150",
        current_mileage=67000,
    )
    assert "Spark plug" in result or "Transmission" in result or "Coolant" in result


def test_100k_mileage():
    result = maintenance_schedule(
        vehicle_year=2015,
        vehicle_make="Toyota",
        vehicle_model="Camry",
        current_mileage=105000,
    )
    assert "Timing belt" in result or "fluid" in result.lower()


def test_upsells_shown():
    result = maintenance_schedule(
        vehicle_year=2020,
        vehicle_make="Toyota",
        vehicle_model="RAV4",
        current_mileage=45000,
    )
    assert "Upsells" in result or "upsell" in result.lower()


def test_vehicle_notes():
    result = maintenance_schedule(
        vehicle_year=2019,
        vehicle_make="Chevrolet",
        vehicle_model="Silverado",
        current_mileage=55000,
    )
    assert "Known Issues" in result or "Silverado" in result


def test_old_vehicle_age_notes():
    result = maintenance_schedule(
        vehicle_year=2010,
        vehicle_make="Honda",
        vehicle_model="Civic",
        current_mileage=130000,
    )
    assert "Age-Based Notes" in result or "rubber" in result.lower()
