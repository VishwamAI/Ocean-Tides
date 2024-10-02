import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

def load_campaign_data():
    # TODO: Replace this with actual data loading from a database or CSV file
    # For now, we'll create a sample dataset
    np.random.seed(42)
    n_samples = 1000
    data = {
        'occupancy_rate': np.random.uniform(30, 100, n_samples),
        'season': np.random.choice(['low', 'medium', 'high'], n_samples),
        'day_of_week': np.random.choice(['weekday', 'weekend'], n_samples),
        'special_event': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'competitor_prices': np.random.uniform(80, 200, n_samples),
        'trigger_campaign': np.random.choice([0, 1], n_samples)
    }
    return pd.DataFrame(data)

def preprocess_data(df):
    # Convert categorical variables to numerical
    df['season'] = pd.Categorical(df['season']).codes
    df['day_of_week'] = pd.Categorical(df['day_of_week']).codes

    # Split features and target
    X = df.drop('trigger_campaign', axis=1)
    y = df['trigger_campaign']

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

def train_random_forest(X, y):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X, y)
    return rf_model

def train_xgboost(X, y):
    xgb_model = XGBClassifier(n_estimators=100, random_state=42)
    xgb_model.fit(X, y)
    return xgb_model

def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model_name} Accuracy: {accuracy:.2f}")
    print(f"{model_name} Classification Report:")
    print(classification_report(y_test, y_pred))

def predict_campaign_trigger(model, input_data, scaler):
    # Preprocess input data (ensure it's in the same format as training data)
    try:
        print(f"Input data: {input_data}")
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)[:, 1]
        print(f"Prediction: {prediction[0]}, Probability: {probability[0]}")
        return prediction[0], probability[0]
    except Exception as e:
        print(f"Error in predict_campaign_trigger: {str(e)}")
        raise

def train_and_evaluate_models():
    # Load and preprocess data
    df = load_campaign_data()
    X, y = preprocess_data(df)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and evaluate Random Forest
    rf_model = train_random_forest(X_train, y_train)
    evaluate_model(rf_model, X_test, y_test, "Random Forest")

    # Train and evaluate XGBoost
    xgb_model = train_xgboost(X_train, y_train)
    evaluate_model(xgb_model, X_test, y_test, "XGBoost")

    # Create and fit a new scaler for future predictions
    scaler = StandardScaler()
    scaler.fit(X)

    return rf_model, xgb_model, scaler

if __name__ == "__main__":
    rf_model, xgb_model = train_and_evaluate_models()

    # Example of using the models for prediction
    sample_input = pd.DataFrame({
        'occupancy_rate': [65],
        'season': [1],  # Assuming 1 represents 'medium' season
        'day_of_week': [0],  # Assuming 0 represents 'weekday'
        'special_event': [0],
        'competitor_prices': [150]
    })

    rf_prediction, rf_probability = predict_campaign_trigger(rf_model, sample_input)
    xgb_prediction, xgb_probability = predict_campaign_trigger(xgb_model, sample_input)

    print("\nSample Prediction:")
    print(f"Random Forest: Trigger Campaign = {rf_prediction}, Probability = {rf_probability:.2f}")
    print(f"XGBoost: Trigger Campaign = {xgb_prediction}, Probability = {xgb_probability:.2f}")
