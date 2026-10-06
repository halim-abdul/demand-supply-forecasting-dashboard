import pandas as pd
from demand_supply.forecasting.inventory import inventory_plan


def test_inventory_shortage_signal():
    fc = pd.DataFrame({"ds": pd.date_range("2026-10-07", periods=7), "yhat": [10]*7})
    plan = inventory_plan(fc, on_hand=5, lead_time_days=3, daily_std=2)
    assert plan["status"] == "SHORTAGE_RISK"
    assert plan["recommended_order_qty"] > 0
