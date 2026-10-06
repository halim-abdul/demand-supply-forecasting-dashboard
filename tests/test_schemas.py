from demand_supply.schemas import SaleEvent


def test_sale_event_parses():
    event = SaleEvent.model_validate({
        "event_id": "e1", "timestamp": "2026-10-06T12:00:00+02:00", "product_id": "MILK-1L",
        "category": "dairy", "quantity": 2, "unit_price": 1.29
    })
    assert event.quantity == 2
    assert event.store_id == "GOE-001"
