# models/forecasting.py
import pandas as pd
from sklearn.linear_model import LinearRegression

def train_and_predict(historical_data):
    # This is a highly simplified example
    df = historical_data.copy()
    df['timestamp'] = pd.to_datetime(df['utc']).astype('int64') // 10**9
    df = df.sort_values('timestamp')

    X = df[['timestamp']]
    y = df['value']

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 24 hours [cite: 27]
    last_timestamp = X.iloc[-1].values[0]
    future_timestamps = [[last_timestamp + 3600 * i] for i in range(1, 25)]
    predictions = model.predict(future_timestamps)
    return predictions