"""MED Vehicle Intelligence MCP Server.

Expert car repair and maintenance advisory tools from a 20-year mechanic veteran.
"""

from mcp.server.fastmcp import FastMCP

from .config import SERVER_NAME, SERVER_VERSION, SERVER_DESCRIPTION
from .tools.check_estimate import check_estimate
from .tools.maintenance import maintenance_schedule
from .tools.repair_replace import repair_or_replace
from .tools.red_flags import find_red_flags

mcp = FastMCP(
    SERVER_NAME,
    version=SERVER_VERSION,
    description=SERVER_DESCRIPTION,
)


@mcp.tool()
def check_repair_estimate(
    repair_type: str,
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    quoted_price: float,
    shop_type: str = "independent",
) -> str:
    """Evaluate whether a car repair estimate is fair based on national price data.

    Compare a repair quote against typical price ranges for independent shops and
    dealers. Returns whether the price is in range, high, or low, plus questions
    to ask the shop.

    Args:
        repair_type: The repair being quoted (e.g., "front brakes", "timing chain", "alternator")
        vehicle_year: Model year of the vehicle (e.g., 2020)
        vehicle_make: Vehicle manufacturer (e.g., "Toyota")
        vehicle_model: Vehicle model (e.g., "Camry")
        quoted_price: The price quoted in dollars
        shop_type: "independent" or "dealer" (default: independent)
    """
    return check_estimate(
        repair_type=repair_type,
        vehicle_year=vehicle_year,
        vehicle_make=vehicle_make,
        vehicle_model=vehicle_model,
        quoted_price=quoted_price,
        shop_type=shop_type,
    )


@mcp.tool()
def get_maintenance_schedule(
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    current_mileage: int,
) -> str:
    """Get a maintenance schedule for your vehicle based on current mileage.

    Returns what maintenance is due now, what's coming in the next 10,000 miles,
    common upsells to question, and vehicle-specific known issues.

    Args:
        vehicle_year: Model year of the vehicle (e.g., 2020)
        vehicle_make: Vehicle manufacturer (e.g., "Toyota")
        vehicle_model: Vehicle model (e.g., "Camry")
        current_mileage: Current odometer reading in miles
    """
    return maintenance_schedule(
        vehicle_year=vehicle_year,
        vehicle_make=vehicle_make,
        vehicle_model=vehicle_model,
        current_mileage=current_mileage,
    )


@mcp.tool()
def should_i_fix_or_replace(
    vehicle_year: int,
    vehicle_make: str,
    vehicle_model: str,
    repair_cost: float,
    vehicle_value: float,
    vehicle_mileage: int = 0,
    annual_repair_spend: float = 0,
) -> str:
    """Get a fix-or-replace recommendation for your vehicle.

    Analyzes repair cost vs vehicle value, mileage, age, and repair history
    to recommend whether to fix your current vehicle or start shopping for
    a replacement. Includes the real cost of replacement for comparison.

    Args:
        vehicle_year: Model year of the vehicle (e.g., 2015)
        vehicle_make: Vehicle manufacturer (e.g., "Honda")
        vehicle_model: Vehicle model (e.g., "Civic")
        repair_cost: Cost of the repair you're facing in dollars
        vehicle_value: Estimated current market value in dollars (check KBB.com or Edmunds.com)
        vehicle_mileage: Current odometer reading in miles (0 if unknown)
        annual_repair_spend: Total spent on non-routine repairs in the past 12 months (0 if unknown)
    """
    return repair_or_replace(
        vehicle_year=vehicle_year,
        vehicle_make=vehicle_make,
        vehicle_model=vehicle_model,
        repair_cost=repair_cost,
        vehicle_value=vehicle_value,
        vehicle_mileage=vehicle_mileage,
        annual_repair_spend=annual_repair_spend,
    )


@mcp.tool()
def check_shop_red_flags(description: str) -> str:
    """Analyze a shop interaction for red flags and warning signs.

    Describe what happened at the shop — what they said, what they quoted,
    how they acted — and get an assessment of whether anything seems
    suspicious. Based on 7 common shop red flags from 20 years of
    automotive industry experience.

    Args:
        description: Your description of the shop interaction or experience
    """
    return find_red_flags(description=description)


def main():
    import os
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        port = int(os.environ.get("PORT", "8000"))
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
