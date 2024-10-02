import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def load_historical_data():
    # TODO: Replace this with actual data loading from a database or CSV file
    # For now, we'll create a sample dataset
    dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    occupancy_rates = [50 + 30 * (1 + (i % 365) / 182.5) for i in range(len(dates))]
    df = pd.DataFrame({'ds': dates, 'y': occupancy_rates})
    return df

def preprocess_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['y'].values.reshape(-1, 1))
    return scaled_data, scaler

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length), 0])
        y.append(data[i + seq_length, 0])
    return np.array(X), np.array(y)

def train_lstm_model(X_train, y_train):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
    return model

def train_arima_model(data):
    model = ARIMA(data, order=(1, 1, 1))
    model_fit = model.fit()
    return model_fit

def forecast_lstm(model, X_test, scaler, num_steps):
    predictions = []
    current_batch = X_test[-1].reshape((1, X_test.shape[1], 1))

    for _ in range(num_steps):
        current_pred = model.predict(current_batch)[0]
        predictions.append(current_pred)
        current_batch = np.roll(current_batch, -1, axis=1)
        current_batch[0, -1, 0] = current_pred

    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

def forecast_arima(model, num_steps):
    forecast = model.forecast(steps=num_steps)
    return forecast

def plot_forecasts(actual, lstm_forecast, arima_forecast):
    plt.figure(figsize=(12, 6))
    plt.plot(actual, label='Actual')
    plt.plot(range(len(actual), len(actual) + len(lstm_forecast)), lstm_forecast, label='LSTM Forecast')
    plt.plot(range(len(actual), len(actual) + len(arima_forecast)), arima_forecast, label='ARIMA Forecast')
    plt.legend()
    plt.title('Occupancy Rate Forecasts')
    plt.xlabel('Days')
    plt.ylabel('Occupancy Rate')
    plt.savefig('occupancy_forecasts.png')
    plt.close()

def run_time_series_models():
    # Load and preprocess data
    df = load_historical_data()
    data, scaler = preprocess_data(df)

    # Prepare data for LSTM
    seq_length = 30
    X, y = create_sequences(data, seq_length)
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Train and forecast with LSTM
    lstm_model = train_lstm_model(X_train.reshape((X_train.shape[0], X_train.shape[1], 1)), y_train)
    lstm_forecast = forecast_lstm(lstm_model, X_test, scaler, 30)

    # Train and forecast with ARIMA
    arima_model = train_arima_model(df['y'])
    arima_forecast = forecast_arima(arima_model, 30)

    # Plot forecasts
    actual = df['y'].values[-len(y_test):]
    plot_forecasts(actual, lstm_forecast, arima_forecast)

    return lstm_forecast, arima_forecast

if __name__ == "__main__":
    lstm_forecast, arima_forecast = run_time_series_models()
    print("LSTM Forecast:", lstm_forecast.flatten())
    print("ARIMA Forecast:", arima_forecast)
