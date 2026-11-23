import pytest

from src.manager import Manager
from src.models import Bill, Parameters, TenantSettlement


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
    ]
    return manager


def test_two_tenants():
    manager = make_manager()
    del manager.tenants["tenant-3"]
    apartment_settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    settlements = manager.create_tenant_settlements(apartment_settlement)

    assert len(settlements) == 2
    assert {s.tenant for s in settlements} == {"tenant-1", "tenant-2"}
    for s in settlements:
        assert isinstance(s, TenantSettlement)
        assert s.apartment_settlement == "apart-polanka"
        assert s.year == 2025
        assert s.month == 1
        assert s.rent_pln == 380.0
        assert s.bills_pln == 75.0
        assert s.total_due_pln == 455.0
        assert s.balance_pln == -455.0


def test_three_tenants():
    manager = make_manager()
    apartment_settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    settlements = manager.create_tenant_settlements(apartment_settlement)

    assert len(settlements) == 3
    for s in settlements:
        assert s.total_due_pln == pytest.approx(910.0 / 3)


def test_one_tenant():
    manager = make_manager()
    manager.tenants = {"tenant-1": manager.tenants["tenant-1"]}
    apartment_settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    settlements = manager.create_tenant_settlements(apartment_settlement)

    assert len(settlements) == 1
    assert settlements[0].tenant == "tenant-1"
    assert settlements[0].rent_pln == 760.0
    assert settlements[0].bills_pln == 150.0
    assert settlements[0].total_due_pln == 910.0
    assert settlements[0].balance_pln == -910.0


def test_no_tenants():
    manager = make_manager()
    manager.tenants = {}
    apartment_settlement = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    settlements = manager.create_tenant_settlements(apartment_settlement)

    assert len(settlements) == 0
    assert settlements == []
