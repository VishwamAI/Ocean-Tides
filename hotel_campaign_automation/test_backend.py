import requests
import json
import numpy as np
from sklearn.metrics import mean_squared_error, silhouette_score
from sklearn.preprocessing import StandardScaler

BASE_URL = "http://localhost:8000"  # Adjust if your backend is running on a different port

def test_time_series_forecasting():
    print("Testing Time Series Forecasting Models...")

    # Test LSTM and ARIMA
    response = requests.get(f"{BASE_URL}/forecast_occupancy")
    if response.status_code == 200:
        data = response.json()
        lstm_forecast = data['lstm_forecast']
        arima_forecast = data['arima_forecast']

        print(f"LSTM Forecast: {lstm_forecast[:5]}...")
        print(f"ARIMA Forecast: {arima_forecast[:5]}...")

        # Basic validation (you may want to add more specific tests)
        assert len(lstm_forecast) > 0, "LSTM forecast is empty"
        assert len(arima_forecast) > 0, "ARIMA forecast is empty"
        print("LSTM and ARIMA forecasts received successfully")
    else:
        print(f"Error in forecasting: {response.status_code}")

    # Test Prophet (assuming there's an endpoint for Prophet forecasts)
    response = requests.get(f"{BASE_URL}/prophet_forecast")
    if response.status_code == 200:
        data = response.json()
        prophet_forecast = data['forecast']
        print(f"Prophet Forecast: {prophet_forecast[:5]}...")
        assert len(prophet_forecast) > 0, "Prophet forecast is empty"
        print("Prophet forecast received successfully")
    else:
        print(f"Error in Prophet forecasting: {response.status_code}")

def test_customer_segmentation():
    print("\nTesting Customer Segmentation Models...")

    response = requests.get(f"{BASE_URL}/segment_customers")
    if response.status_code == 200:
        data = response.json()
        kmeans_segments = data['kmeans_segments']
        dbscan_segments = data['dbscan_segments']

        print(f"K-Means Segments: {list(kmeans_segments.keys())}")
        print(f"DBSCAN Segments: {list(dbscan_segments.keys())}")

        # Basic validation
        assert len(kmeans_segments) > 1, "K-Means produced only one segment"
        assert len(dbscan_segments) > 1, "DBSCAN produced only one segment"
        assert all(isinstance(segment, dict) for segment in kmeans_segments.values()), "Invalid K-Means segment data"
        assert all(isinstance(segment, dict) for segment in dbscan_segments.values()), "Invalid DBSCAN segment data"
        print("Customer segmentation completed successfully")
    else:
        print(f"Error in customer segmentation: {response.status_code}")

def test_campaign_trigger():
    print("\nTesting Campaign Trigger Models...")

    # Sample data for testing (adjust based on your model's input requirements)
    test_data = {
        "occupancy_rate": 0.7,
        "season": 1,  # Assuming 1 represents 'summer'
        "day_of_week": 0,  # Assuming 0 represents 'monday'
        "special_event": 0,  # Using 0 for False
        "competitor_prices": 150  # Adding this field as it's in the model
    }

    response = requests.post(f"{BASE_URL}/predict_campaign_trigger", json=test_data)
    if response.status_code == 200:
        data = response.json()
        xgboost_prediction = data['xgboost']['prediction']
        random_forest_prediction = data['random_forest']['prediction']

        print(f"XGBoost Prediction: {xgboost_prediction}")
        print(f"Random Forest Prediction: {random_forest_prediction}")

        # Basic validation
        assert isinstance(xgboost_prediction, (int, float)), "Invalid XGBoost prediction"
        assert isinstance(random_forest_prediction, (int, float)), "Invalid Random Forest prediction"
        print("Campaign trigger predictions received successfully")
    else:
        print(f"Error in campaign trigger prediction: {response.status_code}")

def test_campaign_optimization():
    print("\nTesting Campaign Optimization...")

    response = requests.get(f"{BASE_URL}/optimize_campaign")
    if response.status_code == 200:
        data = response.json()
        if 'message' in data:
            print(f"Campaign Optimization Message: {data['message']}")
            print("No optimal campaign timing found.")
        elif all(key in data for key in ['optimal_start_date', 'optimal_end_date', 'campaign_duration', 'reason']):
            optimal_start_date = data['optimal_start_date']
            optimal_end_date = data['optimal_end_date']
            campaign_duration = data['campaign_duration']
            reason = data['reason']

            print(f"Optimal Start Date: {optimal_start_date}")
            print(f"Optimal End Date: {optimal_end_date}")
            print(f"Campaign Duration: {campaign_duration} days")
            print(f"Reason: {reason}")

            # Basic validation
            assert isinstance(optimal_start_date, str), "Invalid optimal start date"
            assert isinstance(optimal_end_date, str), "Invalid optimal end date"
            assert isinstance(campaign_duration, int), "Invalid campaign duration"
            assert isinstance(reason, str), "Invalid reason"
            print("Campaign optimization completed successfully")
        else:
            print("Unexpected response format from campaign optimization")
    else:
        print(f"Error in campaign optimization: {response.status_code}")

if __name__ == "__main__":
    test_time_series_forecasting()
    test_customer_segmentation()
    test_campaign_trigger()
    test_campaign_optimization()
    print("\nAll tests completed.")
