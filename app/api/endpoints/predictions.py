# app/api/endpoints/predictions.py
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction import predictor
from app.models.user import User

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_game(request: PredictionRequest, current_user: User = Depends(get_current_user)):
    prediction = await predictor.predict(request.team1, request.team2)
    return PredictionResponse(**prediction)

@router.post("/retrain")
async def retrain_models(current_user: User = Depends(get_current_user)):
    if current_user.username != "admin":  # Add proper admin check
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Here you would fetch your training data
    X = pd.DataFrame()  # Your feature data
    y_winner = pd.Series()  # Winner labels
    y_total = pd.Series()  # Total points
    y_half = pd.DataFrame()  # Half points
    y_quarter = pd.DataFrame()  # Quarter points
    
    predictor.train_models(X, y_winner, y_total, y_half, y_quarter)
    predictor.save_models()
    return {"message": "Models retrained and saved successfully"}