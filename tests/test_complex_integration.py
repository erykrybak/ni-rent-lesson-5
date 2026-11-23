import pytest

from src.manager import Manager
from src.models import Bill, Parameters


def make_manager():
    manager = Manager(Parameters())
    manager.bills = [
        Bill(
            amount_pln=760.0,
            date_due="2025-02-15",
            apartment="apart-polanka",
            settlement_year=2025,
            settlement_month=1,
            type="rent",
        ),
        Bill(
            amount_pln=150.0,
            date_due="2025-02-12",
            apartment="apart-polanka",
            settlement_year=2025,
            settlement_month=1,
            type="electricity",
        ),
        Bill(
            amount_pln=760.0,
            date_due="2025-03-15",
            apartment="apart-polanka",
            settlement_year=2025,
            settlement_month=2,
            type="rent",
        ),
        Bill(
            amount_pln=50.0,
            date_due="2024-02-10",
            apartment="apart-polanka",
            settlement_year=2024,
            settlement_month=1,
            type="gas",
        ),
        Bill(
            amount_pln=999.0,
            date_due="2025-02-15",
            apartment="apart-other",
            settlement_year=2025,
            settlement_month=1,
            type="rent",
        ),
    ]
    return manager


def test_apartment_does_not_exist():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-nie-ma", 2025, 1) is None


def test_no_bills_in_month():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-polanka", 2025, 5) == 0.0


def test_same_year_different_month():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-polanka", 2025, 3) == 0.0


def test_same_month_different_year():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-polanka", 2024, 1) == 50.0


def test_bills_in_month():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-polanka", 2025, 1) == 910.0
    assert manager.get_apartment_costs("apart-polanka", 2025, 2) == 760.0
    assert manager.get_apartment_costs("apart-polanka", 2024, 1) == 50.0


def test_invalid_month():
    manager = make_manager()
    with pytest.raises(ValueError):
        manager.get_apartment_costs("apart-polanka", 2025, 13)
    with pytest.raises(ValueError):
        manager.get_apartment_costs("apart-polanka", 2025, 0)
    with pytest.raises(ValueError):
        manager.get_apartment_costs("apart-polanka", 2025, -1)


def test_month_without_year():
    manager = make_manager()
    with pytest.raises(ValueError):
        manager.get_apartment_costs("apart-polanka", month=3)


def test_whole_year():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-polanka", 2025) == 1670.0
    assert manager.get_apartment_costs("apart-polanka", 2024) == 50.0
    assert manager.get_apartment_costs("apart-polanka", 2030) == 0.0


def test_whole_history():
    manager = make_manager()
    assert manager.get_apartment_costs("apart-polanka") == 1720.0


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(
        Bill(
            apartment="apart-polanka",
            date_due="2025-03-15",
            settlement_year=2025,
            settlement_month=2,
            amount_pln=1250.0,
            type="rent",
        )
    )

    manager.bills.append(
        Bill(
            apartment="apart-polanka",
            date_due="2024-03-15",
            settlement_year=2024,
            settlement_month=2,
            amount_pln=1150.0,
            type="rent",
        )
    )

    manager.bills.append(
        Bill(
            apartment="apart-polanka",
            date_due="2024-02-02",
            settlement_year=2024,
            settlement_month=1,
            amount_pln=222.0,
            type="electricity",
        )
    )

    costs = manager.get_apartment_costs("apartment-1", 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs("apart-polanka", 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs("apart-polanka", 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs("apart-polanka", 2025, 1)
    assert costs == 910.0

    costs = manager.get_apartment_costs("apart-polanka", 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs("apart-polanka")
    assert costs == 3532.0
