# Demand Forecast Model Card

## Intended use
Daily SKU/store demand forecasting and inventory decision support for a Göttingen supermarket setting.

## Inputs
Historical sales, prices/promotions, Lower Saxony public holidays, local event calendar, weather variables, and configurable district population/catchment features.

## Outputs
Point forecast, prediction interval, shortage/overstock indicators, reorder point, safety stock, and suggested order quantity.

## Limitations
The repository ships demo/reference data rather than private retailer POS data. Population does not directly determine purchases; it is only a contextual regressor. Event lift values are hypotheses until calibrated on observed sales. Weather forecasts beyond provider horizons require a separate source or climatology. Supplier constraints, substitutions, spoilage, shelf capacity and minimum order quantities need retailer-specific configuration before production use.

## Monitoring
Track WAPE, MAE, signed bias, prediction interval coverage, stockout rate, waste/markdown rate and service level by SKU/category/store. Compare against seasonal-naive before promotion.
