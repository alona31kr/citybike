"""
Factory Pattern — create domain objects from raw CSV-row dictionaries.

The factory functions hide which concrete subclass is instantiated,
so the rest of the code never needs to import ClassicBike / ElectricBike etc.

Students should:
    - Complete create_user()
    - Optionally add create_trip() and create_maintenance_record()
"""

from datetime import datetime
from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    CasualUser,
    MemberUser,
)


def create_bike(data: dict) -> Bike:
    """Create a Bike (ClassicBike or ElectricBike) from a data dictionary.

    Args:
        data: A dict with at least 'bike_id' and 'bike_type'.

    Returns:
        A ClassicBike or ElectricBike instance.

    Raises:
        ValueError: If bike_type is unknown.

    Example:
        >>> bike = create_bike({"bike_id": "BK200", "bike_type": "electric"})
        >>> isinstance(bike, ElectricBike)
        True
    """
    bike_type = data.get("bike_type", "").lower()

    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            gear_count=int(data.get("gear_count", 7)),
        )
    elif bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 50.0)),
        )
    else:
        raise ValueError(f"Unknown bike_type: {bike_type!r}")


def create_user(data: dict) -> User:
    """Create a User (CasualUser or MemberUser) from a data dictionary.

    Args:
        data: A dict with at least 'user_id', 'name', 'email', 'user_type'.

    Returns:
        A CasualUser or MemberUser instance.

    Raises:
        ValueError: If user_type is unknown.
    """
    user_type = data.get("user_type", "").lower()

    if user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            day_pass_count=int(data.get("day_pass_count", 0)),
        )
    elif user_type == "member":
        # Convert strings to datetime if needed
        start = data.get("membership_start")
        end = data.get("membership_end")
        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        if isinstance(end, str):
            end = datetime.fromisoformat(end)

        return MemberUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            membership_start=start,
            membership_end=end,
            tier=data.get("tier", "basic"),
        )
    else:
        raise ValueError(f"Unknown user_type: {user_type!r}")
