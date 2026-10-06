# Architecture

```text
POS / E-commerce / ERP
        |
        v
   n8n webhook ------> FastAPI /api/v1/sales -----> PostgreSQL
        |                                            |
        |                                            v
        +--> weather / calendar / events ----> feature pipeline
                                                     |
                                                     v
                                         Prophet + baselines + ensemble
                                                     |
                                                     v
                                      reorder / shortage / overstock
                                                     |
                        +----------------------------+------------------+
                        v                                               v
                 Streamlit login dashboard                       n8n alerts
```

The design separates event ingestion from slower training jobs. POS writes should remain fast and idempotent. Forecast refreshes can be queued. Dashboard reads prepared artifacts or database views rather than retraining synchronously on every page load.
