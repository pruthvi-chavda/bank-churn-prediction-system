from fastapi import FastAPI
import pandas as pd
from app.schemas import ChurnInputSchema
from fastapi import FastAPI
import joblib

app = FastAPI(title="Bank Churn Prediction API")

model_path = 'models/bank_churn_pipeline.joblib'
model = joblib.load(model_path)
                    
@app.get("/")
def home():
    return {"status": "healthy", "service": "bank-churn-prediction"}

# 4. Prediction route (POST)
@app.post("/predict")
def predict_churn(payload: ChurnInputSchema):
    # Convert incoming Pydantic data into a single-row DataFrame
    input_df = pd.DataFrame([payload.model_dump()])
    
    # Run inference through your Scikit-Learn pipeline
    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])
    print(prediction,probability)
    # Return JSON response
    return {
        "churn_prediction": prediction,
        "churn_probability": round(probability, 4)
    }
    