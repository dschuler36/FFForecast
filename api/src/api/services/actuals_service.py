from typing import List
import math
import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import PlayerStats, WeeklyPredictionBase, WeeklyPredictionStdHalfPPR
from api.services.predictions_service import PredictionsService


class ActualsService:
    def __init__(self, db: AsyncSession, predictions_service: PredictionsService):
        self.db = db
        self.predictions_service = predictions_service

    async def get_actuals_and_predictions_merged(self, season: int, week: int):
        stmt = (
            select(WeeklyPredictionBase, WeeklyPredictionStdHalfPPR.fantasy_points.label('predicted_fantasy_points'),
                   PlayerStats)
            .join(WeeklyPredictionStdHalfPPR, WeeklyPredictionBase.player_id == WeeklyPredictionStdHalfPPR.player_id)
            .join(PlayerStats, (WeeklyPredictionBase.player_id == PlayerStats.player_id) &
                  (WeeklyPredictionBase.season == PlayerStats.season) &
                  (WeeklyPredictionBase.week == PlayerStats.week))
            .where(
                WeeklyPredictionBase.season == season,
                WeeklyPredictionBase.week == week
            )
            .order_by(WeeklyPredictionStdHalfPPR.fantasy_points.desc())
        )
        results = await self.db.execute(stmt)

        # Unpack the results and calculate differences
        unpacked_results = []
        for row in results:
            base_stats = row.WeeklyPredictionBase
            base_stats.predicted_fantasy_points = row.predicted_fantasy_points  # Add predicted fantasy points to base_stats

            actual_stats = {
                "fantasy_points": row.PlayerStats.fantasy_points,  # Actual fantasy points from PlayerStats
                "passing_yards": row.PlayerStats.passing_yards,
                "passing_tds": row.PlayerStats.passing_tds,
                "interceptions": row.PlayerStats.interceptions,
                "fumbles": row.PlayerStats.fumbles,
                "rushing_yards": row.PlayerStats.rushing_yards,
                "rushing_tds": row.PlayerStats.rushing_tds,
                "rushing_2pt_conversions": row.PlayerStats.rushing_2pt_conversions,
                "receptions": row.PlayerStats.receptions,
                "receiving_yards": row.PlayerStats.receiving_yards,
                "receiving_tds": row.PlayerStats.receiving_tds,
                "receiving_2pt_conversions": row.PlayerStats.receiving_2pt_conversions,
                "passing_2pt_conversions": row.PlayerStats.passing_2pt_conversions,
            }

            # Calculate differences
            differences = {}
            for key in actual_stats:
                if key == "fantasy_points":
                    predicted = base_stats.predicted_fantasy_points
                else:
                    predicted = getattr(base_stats, key, 0)
                actual = actual_stats[key] or 0
                differences[key] = actual - predicted

            unpacked_results.append({
                "base": base_stats,
                "actual_stats": actual_stats,
                "differences": differences
            })

        return unpacked_results

    async def get_prediction_accuracy(self, season: int, week: int):
        act_and_preds = await self.get_actuals_and_predictions_merged(season, week)

        # Compute overall accuracy metrics
        metrics = {}
        stat_keys = [
            "fantasy_points", "passing_yards", "passing_tds", "interceptions", "fumbles",
            "rushing_yards", "rushing_tds", "rushing_2pt_conversions",
            "receptions", "receiving_yards", "receiving_tds",
            "receiving_2pt_conversions", "passing_2pt_conversions"
        ]

        def safe_float(value):
            if math.isnan(value) or math.isinf(value):
                return None
            return float(value)

        for key in stat_keys:
            actual_values = [record['actual_stats'][key] for record in act_and_preds]
            predicted_values = [
                getattr(record['base'], "predicted_fantasy_points" if key == "fantasy_points" else key, 0) for record in
                act_and_preds]

            # Convert to numpy arrays for easier calculations
            actual_array = np.array(actual_values)
            predicted_array = np.array(predicted_values)

            # Calculate metrics
            mae = safe_float(np.mean(np.abs(actual_array - predicted_array)))
            mse = safe_float(np.mean((actual_array - predicted_array) ** 2))
            rmse = safe_float(np.sqrt(mse)) if mse is not None else None

            # Calculate R-squared
            if len(actual_array) > 1 and len(predicted_array) > 1:
                correlation_matrix = np.corrcoef(actual_array, predicted_array)
                r_squared = safe_float(correlation_matrix[0, 1] ** 2 if correlation_matrix.size > 1 else 0)
            else:
                r_squared = None

            metrics[key] = {
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse,
                "R-squared": r_squared
            }

        return {
            "individual_records": act_and_preds,
            "overall_metrics": metrics
        }

