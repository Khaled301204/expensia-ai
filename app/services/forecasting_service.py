from typing import Dict, List
from datetime import datetime, timedelta
import statistics

class ForecastingService:
    
    def forecast_next_month(self, historical_data: Dict[str, List[Dict]]) -> Dict:
        """
        Forecast next month's spending by category
        
        Args:
            historical_data: {
                "Food & Dining": [{"month": "2026-01", "amount": 3000}, ...],
                "Transportation": [{"month": "2026-01", "amount": 1500}, ...],
            }
        
        Returns:
            Forecast by category with trends
        """
        if not historical_data:
            return self._get_empty_forecast()
        
        forecasts_by_category = {}
        total_predicted = 0
        
        for category, monthly_data in historical_data.items():
            if not monthly_data or len(monthly_data) < 2:
                continue
            
            # Sort by month
            sorted_data = sorted(monthly_data, key=lambda x: x.get("month", ""))
            
            # Get last 3-6 months
            recent_data = sorted_data[-6:] if len(sorted_data) >= 6 else sorted_data
            amounts = [float(d.get("amount", 0)) for d in recent_data]
            
            # Simple linear regression for prediction
            prediction = self._predict_next_value(amounts)
            current = amounts[-1] if amounts else 0
            
            # Determine trend
            if len(amounts) >= 2:
                change = ((prediction - current) / current * 100) if current > 0 else 0
                
                if prediction > current * 1.05:
                    trend = "UP"
                elif prediction < current * 0.95:
                    trend = "DOWN"
                else:
                    trend = "STABLE"
            else:
                trend = "STABLE"
                change = 0
            
            forecasts_by_category[category] = {
                "predicted": round(prediction, 2),
                "current_month": round(current, 2),
                "trend": trend,
                "change_percentage": round(change, 1)
            }
            
            total_predicted += prediction
        
        # Calculate confidence based on data consistency
        confidence = self._calculate_confidence(historical_data)
        
        # Get next month string
        next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m")
        
        return {
            "success": True,
            "total_predicted": round(total_predicted, 2),
            "by_category": forecasts_by_category,
            "confidence": confidence,
            "forecast_month": next_month
        }
    
    def _predict_next_value(self, values: List[float]) -> float:
        """
        Simple linear regression to predict next value
        """
        if not values:
            return 0
        
        if len(values) == 1:
            return values[0]
        
        # Calculate trend using simple moving average with growth rate
        if len(values) >= 3:
            # Use weighted average (recent months weighted higher)
            weights = list(range(1, len(values) + 1))
            weighted_avg = sum(v * w for v, w in zip(values, weights)) / sum(weights)
            
            # Calculate growth rate
            first_half = values[:len(values)//2]
            second_half = values[len(values)//2:]
            
            avg_first = statistics.mean(first_half)
            avg_second = statistics.mean(second_half)
            
            if avg_first > 0:
                growth_rate = (avg_second - avg_first) / avg_first
            else:
                growth_rate = 0
            
            # Predict next value
            prediction = weighted_avg * (1 + growth_rate * 0.5)  # Dampened growth
            
            return max(0, prediction)  # Can't be negative
        else:
            # Not enough data, use simple average
            return statistics.mean(values)
    
    def _calculate_confidence(self, historical_data: Dict) -> float:
        """
        Calculate forecast confidence based on data quality
        """
        if not historical_data:
            return 0.0
        
        total_months = 0
        total_consistency = 0
        
        for category, monthly_data in historical_data.items():
            if len(monthly_data) < 2:
                continue
            
            amounts = [float(d.get("amount", 0)) for d in monthly_data]
            
            # Check data consistency (lower variance = higher confidence)
            if len(amounts) >= 2:
                avg = statistics.mean(amounts)
                stdev = statistics.stdev(amounts)
                
                # Coefficient of variation (lower is better)
                cv = (stdev / avg) if avg > 0 else 1
                
                # Convert to confidence (0-1)
                consistency = max(0, 1 - cv)
                
                total_consistency += consistency
                total_months += 1
        
        if total_months == 0:
            return 0.5
        
        base_confidence = total_consistency / total_months
        
        # Bonus for more data
        data_bonus = min(0.2, len(historical_data) * 0.02)
        
        final_confidence = min(0.95, base_confidence + data_bonus)
        
        return round(final_confidence, 2)
    
    def _get_empty_forecast(self) -> Dict:
        """Return empty forecast when no data"""
        next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m")
        
        return {
            "success": False,
            "total_predicted": 0,
            "by_category": {},
            "confidence": 0.0,
            "forecast_month": next_month
        }