# app/services/prediction.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

class BasketballPredictor:
    def __init__(self):
        self.winner_model = None
        self.total_points_model = None
        self.half_points_model = None
        self.quarter_points_model = None
        self.scaler = StandardScaler()

    async def fetch_and_preprocess_data(self, team1, team2):
        # This function should be implemented to fetch data from your endpoint
        # and preprocess it for the model
        # For now, we'll just return some dummy data
        return pd.DataFrame({
            'team1_wins': [3], 'team1_losses': [2], 'team2_wins': [4], 'team2_losses': [1],
            'team1_avg_points': [100], 'team2_avg_points': [98],
            'pre_match_odds_team1': [1.8], 'pre_match_odds_team2': [2.1],
            'over_under_line': [195.5]
        })

    def train_models(self, X, y_winner, y_total, y_half, y_quarter):
        X_scaled = self.scaler.fit_transform(X)
        
        self.winner_model = RandomForestClassifier(n_estimators=100)
        self.winner_model.fit(X_scaled, y_winner)

        self.total_points_model = RandomForestRegressor(n_estimators=100)
        self.total_points_model.fit(X_scaled, y_total)

        self.half_points_model = RandomForestRegressor(n_estimators=100)
        self.half_points_model.fit(X_scaled, y_half)

        self.quarter_points_model = RandomForestRegressor(n_estimators=100)
        self.quarter_points_model.fit(X_scaled, y_quarter)

    async def predict(self, team1, team2):
        X = await self.fetch_and_preprocess_data(team1, team2)
        X_scaled = self.scaler.transform(X)

        winner = self.winner_model.predict(X_scaled)[0]
        total_points = self.total_points_model.predict(X_scaled)[0]
        half_points = self.half_points_model.predict(X_scaled)[0]
        quarter_points = self.quarter_points_model.predict(X_scaled)[0]

        over_under_line = X['over_under_line'].values[0]
        over_under = "Over" if total_points > over_under_line else "Under"

        return {
            "predicted_winner": team1 if winner == 1 else team2,
            "predicted_total_points": round(float(total_points), 2),
            "predicted_half_points": [round(float(half_points[0]), 2), round(float(half_points[1]), 2)],
            "predicted_quarter_points": [round(float(q), 2) for q in quarter_points],
            "over_under": over_under
        }

    def save_models(self):
        joblib.dump(self.winner_model, 'winner_model.joblib')
        joblib.dump(self.total_points_model, 'total_points_model.joblib')
        joblib.dump(self.half_points_model, 'half_points_model.joblib')
        joblib.dump(self.quarter_points_model, 'quarter_points_model.joblib')
        joblib.dump(self.scaler, 'scaler.joblib')

    def load_models(self):
        self.winner_model = joblib.load('winner_model.joblib')
        self.total_points_model = joblib.load('total_points_model.joblib')
        self.half_points_model = joblib.load('half_points_model.joblib')
        self.quarter_points_model = joblib.load('quarter_points_model.joblib')
        self.scaler = joblib.load('scaler.joblib')

predictor = BasketballPredictor()
# predictor.load_models()  # Uncomment this line after you've trained and saved the models
