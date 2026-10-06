# Forecasting design

The platform forecasts daily item demand per store. Prophet captures trend, weekly/yearly seasonality and interpretable external regressors. External drivers include Lower Saxony public holidays, Göttingen events, promotions, population/catchment signals and weather. A seasonal-naive baseline is retained to prevent deploying a model that does not beat a simple seven-day repeat.

## Evaluation
Use rolling-origin backtests. Primary metric is WAPE; MAE, RMSE and signed bias are reported. Forecast intervals feed shortage-risk decisions rather than being displayed as cosmetic uncertainty.

## Inventory policy
Lead-time forecast + service-level safety stock forms the reorder point. The recommended order quantity raises the inventory position toward lead-time + review-period demand. This is a decision-support baseline, not a substitute for supplier minimum order quantities, perishability or capacity constraints.
