# app/schemas/prediction.py
from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    team1: str
    team2: str

class PredictionResponse(BaseModel):
    predicted_winner: str
    predicted_total_points: float
    predicted_half_points: List[float]
    predicted_quarter_points: List[float]
    over_under: str