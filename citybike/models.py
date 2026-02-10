"""
Domain models for the CityBike Bike-Sharing Analytics platform.

This module defines the class hierarchy:
    Entity (ABC) -> Bike -> ClassicBike, ElectricBike
                 -> Station
                 -> User -> CasualUser, MemberUser
    Trip
    MaintenanceRecord
    BikeShareSystem

TODO for students:
    - Complete the Station, User, CasualUser, MemberUser classes
    - Complete the Trip and MaintenanceRecord classes
    - Implement the BikeShareSystem class
    - Add input validation to all constructors
    - Add @property decorators where appropriate
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------------------------------------------------------------
# Abstract Base Class
# ---------------------------------------------------------------------------

class Entity(ABC):
    """Abstract base class for all domain entities.

    Attributes:
        id: Unique identifier for the entity.
        created_at: Timestamp when the entity was created.
    """

    def __init__(self, id: str, created_at: datetime | None = None) -> None:
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")
        self._id = id
        self._created_at = created_at or datetime.now()

    @property
    def id(self) -> str:
        """Return the entity's unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Return the creation timestamp."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        ...


# ---------------------------------------------------------------------------
# Bike hierarchy
# ---------------------------------------------------------------------------

class Bike(Entity):
    """Represents a bike in the sharing system.

    Attributes:
        bike_type: Either 'classic' or 'electric'.
        status: One of 'available', 'in_use', 'maintenance'.
    """

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(
        self,
        bike_id: str,
        bike_type: str,
        status: str = "available",
    ) -> None:
        super().__init__(id=bike_id)
        if bike_type not in ("classic", "electric"):
            raise ValueError(f"Invalid bike_type: {bike_type}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        return self._bike_type

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        self._status = value

    def __str__(self) -> str:
        return f"Bike({self.id}, {self.bike_type}, {self.status})"

    def __repr__(self) -> str:
        return (
            f"Bike(bike_id={self.id!r}, bike_type={self.bike_type!r}, "
            f"status={self.status!r})"
        )


class ClassicBike(Bike):
    """A classic (non-electric) bike with gears.

    Attributes:
        gear_count: Number of gears (must be positive).
    """

    def __init__(
        self,
        bike_id: str,
        gear_count: int = 7,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="classic", status=status)
        if gear_count <= 0:
            raise ValueError("gear_count must be positive")
        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        return self._gear_count

    def __str__(self) -> str:
        return f"ClassicBike({self.id}, gears={self.gear_count})"

    def __repr__(self) -> str:
        return (
            f"ClassicBike(bike_id={self.id!r}, gear_count={self.gear_count}, "
            f"status={self.status!r})"
        )


class ElectricBike(Bike):
    def __init__(
        self,
        bike_id: str,
        battery_level: float = 100.0,
        max_range_km: float = 50.0,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="electric", status=status)

        if not (0 <= battery_level <= 100):
            raise ValueError("battery_level must be between 0 and 100")

        if max_range_km <= 0:
            raise ValueError("max_range_km must be positive")

        self._battery_level = battery_level
        self._max_range_km = max_range_km

    @property
    def battery_level(self) -> float:
        return self._battery_level

    @property
    def max_range_km(self) -> float:
        return self._max_range_km

    def __str__(self) -> str:
        return (
            f"ElectricBike(id={self.id}, "
            f"battery={self.battery_level}%, "
            f"range={self.max_range_km}km)"
        )

    def __repr__(self) -> str:
        return (
            f"ElectricBike("
            f"bike_id={self.id!r}, "
            f"battery_level={self.battery_level!r}, "
            f"max_range_km={self.max_range_km!r})"
        )


# ---------------------------------------------------------------------------
# Station
# ---------------------------------------------------------------------------

class Station(Entity):
    """Represents a bike-sharing station."""

    def __init__(
        self,
        station_id: str,
        name: str,
        capacity: int,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(id=station_id)

        if capacity <= 0:
            raise ValueError("capacity must be positive")

        if not (-90 <= latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")

        if not (-180 <= longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")

        self._name = name.strip()
        self._capacity = capacity
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    def __str__(self) -> str:
        return f"Station({self.id}, {self.name}, cap={self.capacity})"

    def __repr__(self) -> str:
        return (
            f"Station("
            f"station_id={self.id!r}, "
            f"name={self.name!r}, "
            f"capacity={self.capacity!r}, "
            f"latitude={self.latitude!r}, "
            f"longitude={self.longitude!r})"
        )

# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------

class User(Entity):
    """Base class for a system user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        user_type: str,
    ) -> None:
        super().__init__(id=user_id)

        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")

        if not isinstance(email, str) or "@" not in email:
            raise ValueError("invalid email format")

        if not isinstance(user_type, str) or not user_type.strip():
            raise ValueError("user_type must be a non-empty string")

        self._name = name.strip()
        self._email = email.strip()
        self._user_type = user_type.strip()

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_type(self) -> str:
        return self._user_type

    def __str__(self) -> str:
        return f"User({self.id}, {self.user_type})"

    def __repr__(self) -> str:
        return (
            f"User("
            f"user_id={self.id!r}, "
            f"name={self.name!r}, "
            f"email={self.email!r}, "
            f"user_type={self.user_type!r})"
        )


class CasualUser(User):
    """A casual (non-member) user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        day_pass_count: int = 0,
    ) -> None:
        super().__init__(
            user_id=user_id,
            name=name,
            email=email,
            user_type="casual",
        )

        if not isinstance(day_pass_count, int) or day_pass_count < 0:
            raise ValueError("day_pass_count must be a non-negative integer")

        self._day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        return self._day_pass_count

    def __str__(self) -> str:
        return f"CasualUser({self.id}, day_passes={self.day_pass_count})"

    def __repr__(self) -> str:
        return (
            f"CasualUser("
            f"user_id={self.id!r}, "
            f"name={self.name!r}, "
            f"email={self.email!r}, "
            f"day_pass_count={self.day_pass_count!r})"
        )

from datetime import datetime


class MemberUser(User):
    """A registered member user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        membership_start: datetime = None,
        membership_end: datetime = None,
        tier: str = "basic",
    ) -> None:
        super().__init__(
            user_id=user_id,
            name=name,
            email=email,
            user_type="member",
        )

        if not isinstance(tier, str) or tier.lower() not in {"basic", "premium"}:
            raise ValueError("tier must be 'basic' or 'premium'")

        if membership_start and not isinstance(membership_start, datetime):
            raise ValueError("membership_start must be a datetime")

        if membership_end and not isinstance(membership_end, datetime):
            raise ValueError("membership_end must be a datetime")

        if membership_start and membership_end:
            if membership_end < membership_start:
                raise ValueError(
                    "membership_end must be after membership_start"
                )

        self._tier = tier.lower()
        self._membership_start = membership_start
        self._membership_end = membership_end

    @property
    def tier(self) -> str:
        return self._tier

    @property
    def membership_start(self) -> datetime | None:
        return self._membership_start

    @property
    def membership_end(self) -> datetime | None:
        return self._membership_end

    def __str__(self) -> str:
        return f"MemberUser({self.id}, tier={self.tier})"

    def __repr__(self) -> str:
        return (
            f"MemberUser("
            f"user_id={self.id!r}, "
            f"name={self.name!r}, "
            f"email={self.email!r}, "
            f"tier={self.tier!r}, "
            f"membership_start={self.membership_start!r}, "
            f"membership_end={self.membership_end!r})"
        )


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------

class Trip:
    """Represents a single bike trip.

    TODO:
        - Store all attributes: trip_id, user, bike, start_station,
          end_station, start_time, end_time, distance_km
        - Validate: distance_km >= 0, end_time >= start_time
        - Implement duration_minutes as a @property
        - Implement __str__ and __repr__
    """

    def __init__(
        self,
        trip_id: str,
        user: User,
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
    ) -> None:
        # TODO: validate and store attributes
        pass

    @property
    def duration_minutes(self) -> float:
        """Calculate trip duration in minutes from start and end times."""
        # TODO: compute from end_time - start_time
        return 0.0

    def __str__(self) -> str:
        # TODO
        return f"Trip({self.trip_id})"

    def __repr__(self) -> str:
        # TODO
        return f"Trip(trip_id={self.trip_id!r})"


# ---------------------------------------------------------------------------
# MaintenanceRecord
# ---------------------------------------------------------------------------

class MaintenanceRecord:
    """Represents a maintenance event for a bike.

    TODO:
        - Store: record_id, bike, date, maintenance_type, cost, description
        - Validate: cost >= 0, maintenance_type is one of the allowed types
        - Implement __str__ and __repr__
    """

    VALID_TYPES = {
        "tire_repair",
        "brake_adjustment",
        "battery_replacement",
        "chain_lubrication",
        "general_inspection",
    }

    def __init__(
        self,
        record_id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str = "",
    ) -> None:
        # TODO: validate and store attributes
        pass

    def __str__(self) -> str:
        # TODO
        return "MaintenanceRecord()"

    def __repr__(self) -> str:
        # TODO
        return "MaintenanceRecord()"
