from __future__ import annotations
from dataclasses import dataclass, field
import pandas as pd
from prophet import Prophet

DEFAULT_REGRESSORS = [
    "is_public_holiday", "event_lift", "temperature_2m_max", "temperature_2m_min",
    "precipitation_sum", "snowfall_sum", "promotion", "population_share"
]


@dataclass
class ProphetDemandModel:
    interval_width: float = 0.90
    seasonality_mode: str = "multiplicative"
    regressors: list[str] = field(default_factory=lambda: DEFAULT_REGRESSORS.copy())
    model: Prophet | None = None
    fitted_regressors: list[str] = field(default_factory=list)

    def fit(self, history: pd.DataFrame) -> "ProphetDemandModel":
        data = history.copy().sort_values("ds")
        if len(data) < 30:
            raise ValueError("At least 30 daily observations are required")
        self.model = Prophet(
            weekly_seasonality=True,
            yearly_seasonality=len(data) >= 365,
            daily_seasonality=False,
            interval_width=self.interval_width,
            seasonality_mode=self.seasonality_mode,
        )
        self.model.add_seasonality(name="monthly", period=30.4375, fourier_order=5)
        self.fitted_regressors = [c for c in self.regressors if c in data.columns and data[c].notna().any()]
        for column in self.fitted_regressors:
            data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0.0)
            self.model.add_regressor(column, standardize="auto")
        self.model.fit(data[["ds", "y", *self.fitted_regressors]])
        return self

    def predict(self, future: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise RuntimeError("fit must be called before predict")
        frame = future.copy()
        for column in self.fitted_regressors:
            if column not in frame:
                frame[column] = 0.0
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
        pred = self.model.predict(frame[["ds", *self.fitted_regressors]])
        keep = ["ds", "yhat", "yhat_lower", "yhat_upper", "trend", "weekly", "monthly"]
        keep = [c for c in keep if c in pred.columns]
        pred = pred[keep]
        for c in ["yhat", "yhat_lower", "yhat_upper"]:
            if c in pred:
                pred[c] = pred[c].clip(lower=0)
        return pred
