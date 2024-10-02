
# Hotel Campaign Automation

## Project Overview
This project aims to optimize marketing campaigns and improve occupancy rates for hotels using the Gemini API version 1.5. It integrates various machine learning models for time series forecasting, customer segmentation, and campaign triggering.

## Setup Instructions

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/VishwamAI/Ocean-Tides.git
   cd Ocean-Tides/hotel_campaign_automation
   ```

2. Install dependencies using Poetry:
   ```bash
   pip install poetry
   poetry install
   ```

3. Run the FastAPI application:
   ```bash
   poetry run uvicorn hotel_campaign_automation.app:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd Ocean-Tides/hotel_campaign_automation/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React application:
   ```bash
   npm start
   ```

## Backend Details
- **Time Series Forecasting Models**: LSTM, ARIMA, Prophet
- **Customer Segmentation Models**: K-Means, DBScan
- **Campaign Trigger Models**: XGBoost, Random Forest
- **Framework**: FastAPI
- **Endpoints**: Content generation, campaign optimization

## Frontend Details
- **Framework**: React
- **Styling**: Chakra UI
- **Pages**: Home, Login, Dashboard
- **Routing**: React Router

## Usage Instructions
1. Access the application at `http://localhost:3000`.
2. Log in using your credentials.
3. Navigate through the dashboard to view and manage campaigns.

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License Information
This project is licensed under the MIT License.
