from prophet import Prophet
import pandas as pd
from typing import Dict, Optional


class SpendingPredictor:
    """Time-series forecasting for spending prediction using Prophet."""

    def __init__(self):
        # In practice, model persistence should be added.
        self.model: Optional[Prophet] = None

    def train(self, transactions_df: pd.DataFrame):
        df = transactions_df.copy()
        df = df.groupby('date')['amount'].sum().reset_index()
        df.columns = ['ds', 'y']
        m = Prophet(yearly_seasonality=True, weekly_seasonality=False)
        m.fit(df)
        self.model = m

    def predict_next_month(self) -> Dict:
        if self.model is None:
            return {'predicted_total': 0.0, 'forecast_df': None}
        future = self.model.make_future_dataframe(periods=30)
        forecast = self.model.predict(future)
        return {
            'predicted_total': float(forecast.tail(30)['yhat'].sum()),
            'forecast_df': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30)
        }
