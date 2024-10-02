import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta

def load_historical_data():
    # TODO: Replace this with actual data loading from a database or CSV file
    # For now, we'll create a sample dataset
    dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    occupancy_rates = [50 + 30 * (1 + (i % 365) / 182.5) for i in range(len(dates))]
    df = pd.DataFrame({'ds': dates, 'y': occupancy_rates})
    return df

def train_prophet_model(df):
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df)
    return model

def forecast_occupancy(model, periods=90):
    future_dates = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future_dates)
    return forecast

def find_optimal_campaign_timing(forecast, threshold=80):  # Increased threshold
    print(f"Debug: Forecast data shape: {forecast.shape}")
    print(f"Debug: Forecast columns: {forecast.columns}")
    print(f"Debug: First few rows of forecast:\n{forecast.head()}")

    low_occupancy_periods = forecast[forecast['yhat'] < threshold]
    print(f"Debug: Low occupancy periods shape: {low_occupancy_periods.shape}")
    print(f"Debug: Threshold used: {threshold}")
    print(f"Debug: Min yhat: {forecast['yhat'].min()}, Max yhat: {forecast['yhat'].max()}")

    if low_occupancy_periods.empty:
        print("Debug: No low occupancy periods found")
        return None

    optimal_start = low_occupancy_periods['ds'].min()
    optimal_end = low_occupancy_periods['ds'].max()
    duration = (optimal_end - optimal_start).days + 1

    print(f"Debug: Optimal start: {optimal_start}, Optimal end: {optimal_end}, Duration: {duration}")

    return {
        'start_date': optimal_start.strftime('%Y-%m-%d'),
        'end_date': optimal_end.strftime('%Y-%m-%d'),
        'duration': duration
    }

def optimize_campaign_timing():
    # Load historical data
    df = load_historical_data()

    # Train Prophet model
    model = train_prophet_model(df)

    # Generate forecast
    forecast = forecast_occupancy(model)

    # Find optimal campaign timing
    optimal_timing = find_optimal_campaign_timing(forecast)

    if optimal_timing:
        return {
            'optimal_start_date': optimal_timing['start_date'],
            'optimal_end_date': optimal_timing['end_date'],
            'campaign_duration': optimal_timing['duration'],
            'reason': f"Forecasted occupancy rates are below the threshold for {optimal_timing['duration']} days starting from {optimal_timing['start_date']}."
        }
    else:
        return {
            'message': "No optimal campaign timing found. Occupancy rates are forecasted to be above the threshold for the next 90 days."
        }

if __name__ == "__main__":
    result = optimize_campaign_timing()
    print(result)
