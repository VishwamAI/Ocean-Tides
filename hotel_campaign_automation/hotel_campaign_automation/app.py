from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import psycopg
import google.generativeai as genai
from pydantic import BaseModel
import os
import logging
from hotel_campaign_automation.time_series_models import run_time_series_models
from hotel_campaign_automation.segmentation import segment_customers, analyze_segments
from hotel_campaign_automation.campaign_trigger import train_and_evaluate_models, predict_campaign_trigger
from hotel_campaign_automation.forecasting import load_historical_data, train_prophet_model, forecast_occupancy, optimize_campaign_timing
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Set up Gemini API
genai.configure(api_key="AIzaSyC3ePPmuMYogAHFceXfokvC2xcrY34aRUM")
model = genai.GenerativeModel('gemini-1.5-pro')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class CampaignRequest(BaseModel):
    target_audience: str
    hotel_info: str
    campaign_type: str

class User(BaseModel):
    username: str
    password: str

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: Implement actual user authentication logic
    if form_data.username == "testuser" and form_data.password == "password123":
        return {"access_token": "fake-token", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.post("/generate_campaign")
async def generate_campaign(request: CampaignRequest):
    prompt = f"""
    Generate a marketing campaign for a hotel with the following details:
    Target Audience: {request.target_audience}
    Hotel Information: {request.hotel_info}
    Campaign Type: {request.campaign_type}

    Please provide:
    1. A catchy headline
    2. A brief description (2-3 sentences)
    3. Key selling points (3-5 bullet points)
    """

    response = model.generate_content(prompt)
    return {"campaign_content": response.text}

@app.get("/prophet_forecast")
async def prophet_forecast():
    try:
        logger.info("Starting Prophet forecast")
        df = load_historical_data()
        logger.info(f"Historical data loaded. Shape: {df.shape}")
        model = train_prophet_model(df)
        logger.info("Prophet model trained successfully")
        forecast = forecast_occupancy(model)  # Passing the model as an argument
        logger.info(f"Forecast generated. Shape: {forecast.shape}")
        if isinstance(forecast, pd.DataFrame) and 'yhat' in forecast.columns:
            logger.info("Returning forecast data")
            return {"forecast": forecast['yhat'].tolist()}
        else:
            logger.error(f"Forecast data structure is incorrect. Type: {type(forecast)}, Columns: {forecast.columns if isinstance(forecast, pd.DataFrame) else 'N/A'}")
            raise HTTPException(status_code=500, detail="Forecast data structure is incorrect")
    except Exception as e:
        logger.error(f"Error in prophet_forecast: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/optimize_campaign")
async def optimize_campaign():
    try:
        result = optimize_campaign_timing()
        print(f"Debug: optimize_campaign result: {result}")  # Add logging
        if 'optimal_start_date' not in result:
            print(f"Debug: 'optimal_start_date' not found in result")
            return {"message": "No optimal campaign timing found"}
        return result
    except Exception as e:
        print(f"Debug: Error in optimize_campaign: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Error in optimize_campaign: {str(e)}")

@app.post("/optimize_timing")
async def optimize_timing(hotel_data: dict):
    prompt = f"""
    Based on the following hotel data:
    {hotel_data}

    Suggest the optimal timing for launching a marketing campaign to maximize occupancy during low booking periods.
    Provide:
    1. Recommended start date
    2. Recommended duration
    3. Justification for the timing
    """

    response = model.generate_content(prompt)
    return {"optimized_timing": response.text}

@app.get("/forecast_occupancy")
async def forecast_occupancy():
    lstm_forecast, arima_forecast = run_time_series_models()
    return {
        "lstm_forecast": lstm_forecast.tolist(),
        "arima_forecast": arima_forecast.tolist()
    }

@app.get("/segment_customers")
async def get_customer_segments():
    segmented_data = segment_customers()
    segment_analysis = analyze_segments(segmented_data)
    return {
        "kmeans_segments": segment_analysis['kmeans_segments'],
        "dbscan_segments": segment_analysis['dbscan_segments']
    }

@app.post("/predict_campaign_trigger")
async def predict_trigger(data: dict):
    rf_model, xgb_model, scaler = train_and_evaluate_models()

    input_data = pd.DataFrame(data, index=[0])

    rf_prediction, rf_probability = predict_campaign_trigger(rf_model, input_data, scaler)
    xgb_prediction, xgb_probability = predict_campaign_trigger(xgb_model, input_data, scaler)

    return {
        "random_forest": {
            "prediction": int(rf_prediction),
            "probability": float(rf_probability)
        },
        "xgboost": {
            "prediction": int(xgb_prediction),
            "probability": float(xgb_probability)
        }
    }
