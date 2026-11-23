from src.models import (
    Apartment,
    ApartmentSettlement,
    Bill,
    Parameters,
    Tenant,
    TenantSettlement,
    Transfer,
)


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []

        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    def get_apartment_costs(self, apartment_key, year=None, month=None):
        if apartment_key not in self.apartments:
            return None
        if month is not None and (month < 1 or month > 12):
            raise ValueError("Month must be between 1 and 12")
        if month is not None and year is None:
            raise ValueError("Month cannot be given without year")

        total = 0.0
        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            if year is not None and bill.settlement_year != year:
                continue
            if month is not None and bill.settlement_month != month:
                continue
            total += bill.amount_pln
        return total

    def create_apartment_settlement(self, apartment_key, year, month):
        if apartment_key not in self.apartments:
            return None

        total_rent = 0.0
        total_bills = 0.0
        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            if bill.settlement_year != year or bill.settlement_month != month:
                continue
            if bill.type == "rent":
                total_rent += bill.amount_pln
            else:
                total_bills += bill.amount_pln

        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=total_rent,
            total_bills_pln=total_bills,
            total_due_pln=total_rent + total_bills,
        )

    def create_tenant_settlements(self, apartment_settlement):
        tenant_keys = []
        for key, tenant in self.tenants.items():
            if tenant.apartment == apartment_settlement.apartment:
                tenant_keys.append(key)

        settlements = []
        if len(tenant_keys) == 0:
            return settlements

        count = len(tenant_keys)
        for key in tenant_keys:
            rent_share = apartment_settlement.total_rent_pln / count
            bills_share = apartment_settlement.total_bills_pln / count
            total_due = rent_share + bills_share
            settlements.append(
                TenantSettlement(
                    tenant=key,
                    apartment_settlement=apartment_settlement.apartment,
                    month=apartment_settlement.month,
                    year=apartment_settlement.year,
                    rent_pln=rent_share,
                    bills_pln=bills_share,
                    total_due_pln=total_due,
                    balance_pln=-total_due,
                )
            )
        return settlements
