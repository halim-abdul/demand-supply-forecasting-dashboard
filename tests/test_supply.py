import pandas as pd

from demand_supply.forecasting.supply import project_supply_balance


def test_project_supply_balance_uses_inbound_receipts():
    forecast = pd.DataFrame(
        {"ds": pd.date_range("2026-10-07", periods=3), "yhat": [10.0, 10.0, 10.0]}
    )
    inbound = pd.DataFrame({"ds": [pd.Timestamp("2026-10-08")], "quantity": [20.0]})
    projected = project_supply_balance(forecast, on_hand=15.0, inbound=inbound)
    assert projected.projected_stock.tolist() == [5.0, 15.0, 5.0]
    assert not projected.projected_shortage.any()
