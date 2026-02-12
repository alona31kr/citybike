"""
Unit tests for the factory module.

Covers:
    - create_bike (fully implemented)
"""

import pytest

from factories import create_bike, create_user
from models import (
    ClassicBike, ElectricBike, Bike,
    CasualUser, MemberUser, User,
)

# ---------------------------------------------------------------------------
# create_user
# ---------------------------------------------------------------------------

class TestCreateUser:

    def test_creates_casual_user(self) -> None:
        user = create_user({
            "user_id": "U001",
            "name": "Alice",
            "email": "alice@example.com",
            "user_type": "casual",
        })
        assert isinstance(user, CasualUser)
        assert user.id == "U001"
        assert user.user_type == "casual"

    def test_creates_member_user(self) -> None:
        user = create_user({
            "user_id": "U002",
            "name": "Bob",
            "email": "bob@example.com",
            "user_type": "member",
        })
        assert isinstance(user, MemberUser)
        assert user.id == "U002"
        assert user.user_type == "member"

    def test_casual_default_day_passes(self) -> None:
        user = create_user({
            "user_id": "U003",
            "name": "Charlie",
            "email": "charlie@example.com",
            "user_type": "casual",
        })
        assert isinstance(user, CasualUser)
        assert user.day_pass_count == 0

    def test_casual_custom_day_passes(self) -> None:
        user = create_user({
            "user_id": "U004",
            "name": "Dana",
            "email": "dana@example.com",
            "user_type": "casual",
            "day_pass_count": "5",
        })
        assert isinstance(user, CasualUser)
        assert user.day_pass_count == 5

    def test_member_default_tier(self) -> None:
        user = create_user({
            "user_id": "U005",
            "name": "Eve",
            "email": "eve@example.com",
            "user_type": "member",
        })
        assert isinstance(user, MemberUser)
        assert user.tier == "basic"

    def test_case_insensitive_type(self) -> None:
        user = create_user({
            "user_id": "U006",
            "name": "Frank",
            "email": "frank@example.com",
            "user_type": "Member",
        })
        assert isinstance(user, MemberUser)

    def test_unknown_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown user_type"):
            create_user({
                "user_id": "U007",
                "name": "Grace",
                "email": "grace@example.com",
                "user_type": "admin",
            })

    def test_missing_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown user_type"):
            create_user({
                "user_id": "U008",
                "name": "Hank",
                "email": "hank@example.com",
            })

    def test_result_is_user_instance(self) -> None:
        user = create_user({
            "user_id": "U009",
            "name": "Ivy",
            "email": "ivy@example.com",
            "user_type": "casual",
        })
        assert isinstance(user, User)


# ---------------------------------------------------------------------------
# create_bike
# ---------------------------------------------------------------------------

class TestCreateBike:

    def test_creates_classic_bike(self) -> None:
        bike = create_bike({"bike_id": "BK001", "bike_type": "classic"})
        assert isinstance(bike, ClassicBike)
        assert bike.id == "BK001"
        assert bike.bike_type == "classic"

    def test_creates_electric_bike(self) -> None:
        bike = create_bike({"bike_id": "BK002", "bike_type": "electric"})
        assert isinstance(bike, ElectricBike)
        assert bike.id == "BK002"
        assert bike.bike_type == "electric"

    def test_classic_default_gears(self) -> None:
        bike = create_bike({"bike_id": "BK003", "bike_type": "classic"})
        assert isinstance(bike, ClassicBike)
        assert bike.gear_count == 7

    def test_classic_custom_gears(self) -> None:
        bike = create_bike({
            "bike_id": "BK004",
            "bike_type": "classic",
            "gear_count": "21",
        })
        assert isinstance(bike, ClassicBike)
        assert bike.gear_count == 21

    def test_case_insensitive_type(self) -> None:
        bike = create_bike({"bike_id": "BK005", "bike_type": "Classic"})
        assert isinstance(bike, ClassicBike)

    def test_unknown_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown bike_type"):
            create_bike({"bike_id": "BK006", "bike_type": "scooter"})

    def test_missing_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown bike_type"):
            create_bike({"bike_id": "BK007"})

    def test_result_is_bike_instance(self) -> None:
        bike = create_bike({"bike_id": "BK008", "bike_type": "electric"})
        assert isinstance(bike, Bike)
