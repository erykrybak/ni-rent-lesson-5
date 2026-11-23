from src.manager import Manager
from src.models import ApartmentSettlement, Bill, Parameters


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
    ]
    return manager


def test_apartment_settlement_with_bills():
    manager = make_manager()
    settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == "apart-polanka"
    assert settlement.year == 2025
    assert settlement.month == 1
    assert settlement.total_rent_pln == 760.0
    assert settlement.total_bills_pln == 150.0
    assert settlement.total_due_pln == 910.0
    assert (
        settlement.total_rent_pln + settlement.total_bills_pln
        == settlement.total_due_pln
    )
    assert settlement.total_due_pln == manager.get_apartment_costs(
        "apart-polanka", 2025, 1
    )
    assert settlement.total_due_pln > 0


def test_apartment_settlement_without_bills():
    manager = make_manager()
    settlement = manager.create_apartment_settlement("apart-polanka", 2025, 5)

    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == "apart-polanka"
    assert settlement.year == 2025
    assert settlement.month == 5
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_due_pln == 0.0


def test_apartment_settlement_apartment_does_not_exist():
    manager = make_manager()
    assert manager.create_apartment_settlement("apart-nie-ma", 2025, 1) is None
