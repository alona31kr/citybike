"""
Unit tests for OOP models.

Covers:
    - Entity (via ClassicBike since Entity is abstract)
    - Bike base class validation
    - ClassicBike creation, properties, validation, __str__, __repr__
"""

import pytest
from datetime import datetime

from models import (
    Bike, ClassicBike, ElectricBike,
    Station, 
    Entity,
    User, CasualUser, MemberUser,
    Trip, MaintenanceRecord
)


# ---------------------------------------------------------------------------
# Entity (tested through concrete subclass ClassicBike)
# ---------------------------------------------------------------------------

class TestEntity:
    """Tests for the abstract Entity base class."""

    def test_entity_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            Entity(id="E001")  # type: ignore[abstract]

    def test_entity_rejects_empty_id(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="", gear_count=5)

    def test_entity_rejects_non_string_id(self) -> None:
        with pytest.raises((ValueError, TypeError)):
            ClassicBike(bike_id=123, gear_count=5)  # type: ignore[arg-type]

    def test_entity_id_property(self) -> None:
        bike = ClassicBike(bike_id="BK001")
        assert bike.id == "BK001"

    def test_entity_created_at_default(self) -> None:
        bike = ClassicBike(bike_id="BK001")
        assert isinstance(bike.created_at, datetime)

    def test_entity_created_at_custom(self) -> None:
        ts = datetime(2024, 6, 15, 12, 0, 0)
        bike = ClassicBike.__new__(ClassicBike)
        Entity.__init__(bike, id="BK001", created_at=ts)
        assert bike.created_at == ts


# ---------------------------------------------------------------------------
# Bike
# ---------------------------------------------------------------------------

class TestBike:
    """Tests for the Bike base class."""

    def test_bike_rejects_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="Invalid bike_type"):
            Bike(bike_id="BK001", bike_type="scooter")

    def test_bike_rejects_invalid_status(self) -> None:
        with pytest.raises(ValueError, match="Invalid status"):
            Bike(bike_id="BK001", bike_type="classic", status="broken")

    def test_bike_default_status(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic")
        assert bike.status == "available"

    def test_bike_type_property(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="electric")
        assert bike.bike_type == "electric"

    def test_bike_status_setter_valid(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic")
        bike.status = "in_use"
        assert bike.status == "in_use"
        bike.status = "maintenance"
        assert bike.status == "maintenance"

    def test_bike_status_setter_invalid(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic")
        with pytest.raises(ValueError, match="Invalid status"):
            bike.status = "destroyed"

    def test_bike_str(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic", status="in_use")
        assert str(bike) == "Bike(BK001, classic, in_use)"

    def test_bike_repr(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic", status="available")
        r = repr(bike)
        assert "BK001" in r
        assert "classic" in r
        assert "available" in r


# ---------------------------------------------------------------------------
# ClassicBike
# ---------------------------------------------------------------------------

class TestClassicBike:
    """Tests for the ClassicBike subclass."""

    def test_creation_defaults(self) -> None:
        bike = ClassicBike(bike_id="BK010")
        assert bike.id == "BK010"
        assert bike.bike_type == "classic"
        assert bike.gear_count == 7
        assert bike.status == "available"

    def test_creation_custom_gears(self) -> None:
        bike = ClassicBike(bike_id="BK011", gear_count=21)
        assert bike.gear_count == 21

    def test_rejects_zero_gears(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="BK012", gear_count=0)

    def test_rejects_negative_gears(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="BK013", gear_count=-3)

    def test_is_instance_of_bike(self) -> None:
        bike = ClassicBike(bike_id="BK014")
        assert isinstance(bike, Bike)
        assert isinstance(bike, Entity)

    def test_str(self) -> None:
        bike = ClassicBike(bike_id="BK015", gear_count=7)
        assert str(bike) == "ClassicBike(BK015, gears=7)"

    def test_repr(self) -> None:
        bike = ClassicBike(bike_id="BK015", gear_count=7, status="available")
        r = repr(bike)
        assert "BK015" in r
        assert "gear_count=7" in r
        assert "available" in r


# ---------------------------------------------------------------------------
# ElectricBike
# ---------------------------------------------------------------------------

class TestElectricBike:
    """Tests for the ElectricBike subclass."""

    def test_creation_defaults(self) -> None:
        bike = ElectricBike(bike_id="EB001")
        assert bike.id == "EB001"
        assert bike.bike_type == "electric"
        assert bike.battery_level == 100.0
        assert bike.max_range_km == 50.0
        assert bike.status == "available"

    def test_creation_custom_values(self) -> None:
        bike = ElectricBike(
            bike_id="EB002",
            battery_level=80.0,
            max_range_km=65.0,
            status="in_use",
        )
        assert bike.battery_level == 80.0
        assert bike.max_range_km == 65.0
        assert bike.status == "in_use"

    def test_rejects_battery_above_100(self) -> None:
        with pytest.raises(ValueError):
            ElectricBike(bike_id="EB003", battery_level=150.0)

    def test_rejects_battery_below_0(self) -> None:
        with pytest.raises(ValueError):
            ElectricBike(bike_id="EB004", battery_level=-5.0)

    def test_rejects_non_positive_range(self) -> None:
        with pytest.raises(ValueError):
            ElectricBike(bike_id="EB005", max_range_km=0)

    def test_is_instance_of_bike_and_entity(self) -> None:
        bike = ElectricBike(bike_id="EB006")
        assert isinstance(bike, Bike)
        assert isinstance(bike, Entity)

    def test_str(self) -> None:
        bike = ElectricBike(bike_id="EB007", battery_level=90.0)
        s = str(bike)
        assert "ElectricBike" in s
        assert "EB007" in s
        assert "90" in s

    def test_repr(self) -> None:
        bike = ElectricBike(
            bike_id="EB008",
            battery_level=75.0,
            max_range_km=55.0,
        )
        r = repr(bike)
        assert "ElectricBike" in r
        assert "EB008" in r
        assert "battery_level=75.0" in r
        assert "max_range_km=55.0" in r


# ---------------------------------------------------------------------------
# Station
# ---------------------------------------------------------------------------

class TestStation:
    """Tests for the Station model."""

    def test_creation_valid(self) -> None:
        station = Station(
            station_id="ST001",
            name="Central Station",
            capacity=20,
            latitude=48.78,
            longitude=9.18,
        )

        assert station.id == "ST001"
        assert station.name == "Central Station"
        assert station.capacity == 20
        assert station.latitude == 48.78
        assert station.longitude == 9.18

    def test_rejects_zero_capacity(self) -> None:
        with pytest.raises(ValueError):
            Station(
                station_id="ST002",
                name="Zero Cap",
                capacity=0,
                latitude=48.7,
                longitude=9.1,
            )

    def test_rejects_negative_capacity(self) -> None:
        with pytest.raises(ValueError):
            Station(
                station_id="ST003",
                name="Negative Cap",
                capacity=-5,
                latitude=48.7,
                longitude=9.1,
            )

    def test_rejects_invalid_latitude(self) -> None:
        with pytest.raises(ValueError):
            Station(
                station_id="ST004",
                name="Bad Lat",
                capacity=10,
                latitude=120.0,
                longitude=9.1,
            )

    def test_rejects_invalid_longitude(self) -> None:
        with pytest.raises(ValueError):
            Station(
                station_id="ST005",
                name="Bad Lon",
                capacity=10,
                latitude=48.7,
                longitude=250.0,
            )

    def test_rejects_empty_name(self) -> None:
        with pytest.raises(ValueError):
            Station(
                station_id="ST006",
                name="   ",
                capacity=10,
                latitude=48.7,
                longitude=9.1,
            )

    def test_is_instance_of_entity(self) -> None:
        station = Station(
            station_id="ST007",
            name="Entity Test",
            capacity=15,
            latitude=48.7,
            longitude=9.1,
        )
        assert isinstance(station, Entity)

    def test_str(self) -> None:
        station = Station(
            station_id="ST008",
            name="Market Square",
            capacity=25,
            latitude=48.75,
            longitude=9.15,
        )
        s = str(station)
        assert "Station" in s
        assert "ST008" in s
        assert "Market Square" in s
        assert "25" in s

    def test_repr(self) -> None:
        station = Station(
            station_id="ST009",
            name="Old Town",
            capacity=30,
            latitude=48.76,
            longitude=9.16,
        )
        r = repr(station)
        assert "Station" in r
        assert "ST009" in r
        assert "Old Town" in r
        assert "capacity=30" in r

# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class TestUser:
    """Tests for the User base class."""

    def test_creation_valid(self) -> None:
        user = User(
            user_id="U001",
            name="Alice",
            email="alice@example.com",
            user_type="casual",
        )

        assert user.id == "U001"
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.user_type == "casual"

    def test_rejects_empty_name(self) -> None:
        with pytest.raises(ValueError):
            User(
                user_id="U002",
                name="   ",
                email="bob@example.com",
                user_type="casual",
            )

    def test_rejects_invalid_email(self) -> None:
        with pytest.raises(ValueError):
            User(
                user_id="U003",
                name="Charlie",
                email="charlieexample.com",
                user_type="member",
            )

    def test_rejects_empty_user_type(self) -> None:
        with pytest.raises(ValueError):
            User(
                user_id="U004",
                name="Dana",
                email="dana@example.com",
                user_type="",
            )

    def test_is_instance_of_entity(self) -> None:
        user = User(
            user_id="U005",
            name="Eve",
            email="eve@example.com",
            user_type="casual",
        )
        assert isinstance(user, Entity)

    def test_str(self) -> None:
        user = User(
            user_id="U006",
            name="Frank",
            email="frank@example.com",
            user_type="member",
        )
        s = str(user)
        assert "User" in s
        assert "U006" in s
        assert "member" in s

    def test_repr(self) -> None:
        user = User(
            user_id="U007",
            name="Grace",
            email="grace@example.com",
            user_type="casual",
        )
        r = repr(user)
        assert "U007" in r
        assert "Grace" in r
        assert "grace@example.com" in r
        assert "casual" in r


# ---------------------------------------------------------------------------
# CasualUser
# ---------------------------------------------------------------------------

class TestCasualUser:
    """Tests for the CasualUser class."""

    def test_creation_defaults(self) -> None:
        user = CasualUser(
            user_id="CU001",
            name="Alice",
            email="alice@example.com",
        )

        assert user.id == "CU001"
        assert user.user_type == "casual"
        assert user.day_pass_count == 0

    def test_creation_custom_day_passes(self) -> None:
        user = CasualUser(
            user_id="CU002",
            name="Bob",
            email="bob@example.com",
            day_pass_count=3,
        )
        assert user.day_pass_count == 3

    def test_rejects_negative_day_pass_count(self) -> None:
        with pytest.raises(ValueError):
            CasualUser(
                user_id="CU003",
                name="Charlie",
                email="charlie@example.com",
                day_pass_count=-1,
            )

    def test_is_instance_of_user(self) -> None:
        user = CasualUser(
            user_id="CU004",
            name="Dana",
            email="dana@example.com",
        )
        assert isinstance(user, User)
        assert isinstance(user, Entity)

    def test_str(self) -> None:
        user = CasualUser(
            user_id="CU005",
            name="Eve",
            email="eve@example.com",
            day_pass_count=2,
        )
        s = str(user)
        assert "CasualUser" in s
        assert "CU005" in s
        assert "2" in s

    def test_repr(self) -> None:
        user = CasualUser(
            user_id="CU006",
            name="Frank",
            email="frank@example.com",
            day_pass_count=1,
        )
        r = repr(user)
        assert "CU006" in r
        assert "Frank" in r
        assert "day_pass_count=1" in r
# ---------------------------------------------------------------------------
# MemberUser
# ---------------------------------------------------------------------------

class TestMemberUser:
    """Tests for the MemberUser class."""

    def test_creation_defaults(self) -> None:
        user = MemberUser(
            user_id="MU001",
            name="Alice",
            email="alice@example.com",
        )

        assert user.id == "MU001"
        assert user.user_type == "member"
        assert user.tier == "basic"
        assert user.membership_start is None
        assert user.membership_end is None

    def test_creation_custom_values(self) -> None:
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)

        user = MemberUser(
            user_id="MU002",
            name="Bob",
            email="bob@example.com",
            membership_start=start,
            membership_end=end,
            tier="premium",
        )

        assert user.tier == "premium"
        assert user.membership_start == start
        assert user.membership_end == end

    def test_rejects_invalid_tier(self) -> None:
        with pytest.raises(ValueError):
            MemberUser(
                user_id="MU003",
                name="Charlie",
                email="charlie@example.com",
                tier="gold",
            )

    def test_rejects_invalid_membership_dates(self) -> None:
        start = datetime(2024, 6, 1)
        end = datetime(2024, 5, 1)

        with pytest.raises(ValueError):
            MemberUser(
                user_id="MU004",
                name="Dana",
                email="dana@example.com",
                membership_start=start,
                membership_end=end,
            )

    def test_is_instance_of_user(self) -> None:
        user = MemberUser(
            user_id="MU005",
            name="Eve",
            email="eve@example.com",
        )
        assert isinstance(user, User)
        assert isinstance(user, Entity)

    def test_str(self) -> None:
        user = MemberUser(
            user_id="MU006",
            name="Frank",
            email="frank@example.com",
            tier="premium",
        )
        s = str(user)
        assert "MemberUser" in s
        assert "MU006" in s
        assert "premium" in s

    def test_repr(self) -> None:
        user = MemberUser(
            user_id="MU007",
            name="Grace",
            email="grace@example.com",
            tier="basic",
        )
        r = repr(user)
        assert "MU007" in r
        assert "Grace" in r
        assert "tier='basic'" in r


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------

class TestTrip:
    """Tests for the Trip class."""

    def setup_method(self) -> None:
        self.user = CasualUser(
            user_id="U001",
            name="Alice",
            email="alice@example.com",
        )
        self.bike = ClassicBike(bike_id="BK001")
        self.start_station = Station(
            station_id="ST001",
            name="Central",
            capacity=10,
            latitude=48.7,
            longitude=9.1,
        )
        self.end_station = Station(
            station_id="ST002",
            name="West End",
            capacity=12,
            latitude=48.8,
            longitude=9.2,
        )

    def test_creation_valid(self) -> None:
        start = datetime(2024, 6, 1, 10, 0)
        end = datetime(2024, 6, 1, 10, 30)

        trip = Trip(
            trip_id="TR001",
            user=self.user,
            bike=self.bike,
            start_station=self.start_station,
            end_station=self.end_station,
            start_time=start,
            end_time=end,
            distance_km=5.2,
        )

        assert trip.trip_id == "TR001"
        assert trip.distance_km == 5.2
        assert trip.duration_minutes == 30.0

    def test_rejects_negative_distance(self) -> None:
        start = datetime(2024, 6, 1, 10, 0)
        end = datetime(2024, 6, 1, 10, 10)

        with pytest.raises(ValueError):
            Trip(
                trip_id="TR002",
                user=self.user,
                bike=self.bike,
                start_station=self.start_station,
                end_station=self.end_station,
                start_time=start,
                end_time=end,
                distance_km=-1.0,
            )

    def test_rejects_invalid_time_order(self) -> None:
        start = datetime(2024, 6, 1, 11, 0)
        end = datetime(2024, 6, 1, 10, 0)

        with pytest.raises(ValueError):
            Trip(
                trip_id="TR003",
                user=self.user,
                bike=self.bike,
                start_station=self.start_station,
                end_station=self.end_station,
                start_time=start,
                end_time=end,
                distance_km=3.0,
            )

    def test_duration_minutes_fractional(self) -> None:
        start = datetime(2024, 6, 1, 10, 0)
        end = datetime(2024, 6, 1, 10, 45, 30)

        trip = Trip(
            trip_id="TR004",
            user=self.user,
            bike=self.bike,
            start_station=self.start_station,
            end_station=self.end_station,
            start_time=start,
            end_time=end,
            distance_km=7.0,
        )

        assert trip.duration_minutes == pytest.approx(45.5)

    def test_str(self) -> None:
        trip = Trip(
            trip_id="TR005",
            user=self.user,
            bike=self.bike,
            start_station=self.start_station,
            end_station=self.end_station,
            start_time=datetime(2024, 6, 1, 9, 0),
            end_time=datetime(2024, 6, 1, 9, 15),
            distance_km=2.0,
        )

        s = str(trip)
        assert "TR005" in s
        assert "U001" in s
        assert "BK001" in s

    def test_repr(self) -> None:
        trip = Trip(
            trip_id="TR006",
            user=self.user,
            bike=self.bike,
            start_station=self.start_station,
            end_station=self.end_station,
            start_time=datetime(2024, 6, 1, 9, 0),
            end_time=datetime(2024, 6, 1, 9, 15),
            distance_km=2.0,
        )

        r = repr(trip)
        assert "TR006" in r
        assert "distance_km" in r

# ---------------------------------------------------------------------------
# MaintenanceRecord
# ---------------------------------------------------------------------------

class TestMaintenanceRecord:
    """Tests for the MaintenanceRecord class."""

    def setup_method(self) -> None:
        self.bike = ClassicBike(bike_id="BK100")
        self.date = datetime(2024, 6, 1)

    def test_creation_valid(self) -> None:
        record = MaintenanceRecord(
            record_id="MR001",
            bike=self.bike,
            date=self.date,
            maintenance_type="tire_repair",
            cost=25.5,
            description="Fixed flat tire",
        )

        assert record.record_id == "MR001"
        assert record.bike == self.bike
        assert record.cost == 25.5
        assert record.maintenance_type == "tire_repair"

    def test_rejects_negative_cost(self) -> None:
        with pytest.raises(ValueError):
            MaintenanceRecord(
                record_id="MR002",
                bike=self.bike,
                date=self.date,
                maintenance_type="brake_adjustment",
                cost=-10.0,
            )

    def test_rejects_invalid_type(self) -> None:
        with pytest.raises(ValueError):
            MaintenanceRecord(
                record_id="MR003",
                bike=self.bike,
                date=self.date,
                maintenance_type="engine_repair",
                cost=30.0,
            )

    def test_rejects_invalid_bike(self) -> None:
        with pytest.raises(TypeError):
            MaintenanceRecord(
                record_id="MR004",
                bike="not_a_bike",  # type: ignore[arg-type]
                date=self.date,
                maintenance_type="tire_repair",
                cost=10.0,
            )

    def test_str(self) -> None:
        record = MaintenanceRecord(
            record_id="MR005",
            bike=self.bike,
            date=self.date,
            maintenance_type="general_inspection",
            cost=40.0,
        )

        s = str(record)
        assert "MR005" in s
        assert "BK100" in s
        assert "general_inspection" in s

    def test_repr(self) -> None:
        record = MaintenanceRecord(
            record_id="MR006",
            bike=self.bike,
            date=self.date,
            maintenance_type="chain_lubrication",
            cost=15.0,
        )

        r = repr(record)
        assert "MR006" in r
        assert "chain_lubrication" in r
