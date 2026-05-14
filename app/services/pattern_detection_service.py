from typing import List, Dict
from datetime import datetime
from collections import defaultdict
import statistics

class PatternDetectionService:
    
    def analyze_patterns(self, transactions: List[Dict]) -> Dict:
        """
        Analyze all spending patterns from transaction history
        
        Args:
            transactions: List of {date, category, amount, merchant, day_of_week}
        
        Returns:
            Complete pattern analysis
        """
        if not transactions or len(transactions) < 10:
            return self._get_empty_analysis()
        
        temporal = self._detect_temporal_patterns(transactions)
        behavioral = self._detect_behavioral_patterns(transactions)
        anomalies = self._detect_anomalies(transactions)
        trends = self._detect_trends(transactions)
        
        return {
            "success": True,
            "temporal_patterns": temporal,
            "behavioral_patterns": behavioral,
            "anomalies": anomalies,
            "trends": trends
        }
    
    def _detect_temporal_patterns(self, transactions: List[Dict]) -> Dict:
        """Detect time-based spending patterns"""
        
        # Separate weekend vs weekday
        weekend_spending = []
        weekday_spending = []
        
        for t in transactions:
            day = t.get("day_of_week", "").upper()
            amount = float(t.get("amount", 0))
            
            if day in ["SATURDAY", "SUNDAY"]:
                weekend_spending.append(amount)
            else:
                weekday_spending.append(amount)
        
        # Calculate averages
        weekday_avg = statistics.mean(weekday_spending) if weekday_spending else 0
        weekend_avg = statistics.mean(weekend_spending) if weekend_spending else 0
        
        # Detect weekend overspending (if weekend > 1.5x weekday)
        weekend_overspending = weekend_avg > weekday_avg * 1.5 if weekday_avg > 0 else False
        
        percentage_diff = ((weekend_avg - weekday_avg) / weekday_avg * 100) if weekday_avg > 0 else 0
        
        # Detect payday spike (compare early vs late month)
        early_month = []  # Days 1-10
        late_month = []   # Days 20-31
        
        for t in transactions:
            try:
                date_str = t.get("date", "")
                if isinstance(date_str, str):
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    date_obj = date_str
                
                day = date_obj.day
                amount = float(t.get("amount", 0))
                
                if 1 <= day <= 10:
                    early_month.append(amount)
                elif 20 <= day <= 31:
                    late_month.append(amount)
            except:
                continue
        
        early_avg = statistics.mean(early_month) if early_month else 0
        late_avg = statistics.mean(late_month) if late_month else 0
        
        payday_spike = early_avg > late_avg * 1.3 if late_avg > 0 else False
        
        return {
            "weekend_overspending": weekend_overspending,
            "weekday_average": round(weekday_avg, 2),
            "weekend_average": round(weekend_avg, 2),
            "percentage_difference": round(percentage_diff, 1),
            "payday_spike": payday_spike,
            "early_month_average": round(early_avg, 2),
            "late_month_average": round(late_avg, 2)
        }
    
    def _detect_behavioral_patterns(self, transactions: List[Dict]) -> Dict:
        """Detect spending behavior patterns"""
        
        # Count by day of week
        day_totals = defaultdict(float)
        for t in transactions:
            day = t.get("day_of_week", "UNKNOWN")
            amount = float(t.get("amount", 0))
            day_totals[day] += amount
        
        primary_day = max(day_totals.items(), key=lambda x: x[1])[0] if day_totals else "UNKNOWN"
        
        # Count by category
        category_totals = defaultdict(float)
        for t in transactions:
            category = t.get("category", "Other")
            amount = float(t.get("amount", 0))
            category_totals[category] += amount
        
        primary_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else "Other"
        
        # Calculate category preferences (percentage of total)
        total_spending = sum(category_totals.values())
        category_preferences = {
            cat: round((amt / total_spending * 100), 1) 
            for cat, amt in category_totals.items()
        } if total_spending > 0 else {}
        
        return {
            "primary_spending_day": primary_day,
            "primary_spending_category": primary_category,
            "category_preferences": category_preferences
        }
    
    def _detect_anomalies(self, transactions: List[Dict]) -> List[Dict]:
        """Detect unusual spending events"""
        
        anomalies = []
        
        # Group by category
        by_category = defaultdict(list)
        for t in transactions:
            category = t.get("category", "Other")
            amount = float(t.get("amount", 0))
            by_category[category].append((t, amount))
        
        # Find outliers (> 2x average in category)
        for category, items in by_category.items():
            if len(items) < 3:
                continue
            
            amounts = [amt for _, amt in items]
            avg = statistics.mean(amounts)
            stdev = statistics.stdev(amounts) if len(amounts) > 1 else 0
            
            for transaction, amount in items:
                if amount > avg * 2.5:  # Significant outlier
                    anomalies.append({
                        "date": transaction.get("date", ""),
                        "category": category,
                        "amount": round(amount, 2),
                        "normal_amount": round(avg, 2),
                        "reason": f"{round(amount/avg, 1)}x higher than usual"
                    })
        
        # Sort by date (most recent first) and limit to top 5
        anomalies.sort(key=lambda x: x["date"], reverse=True)
        return anomalies[:5]
    
    def _detect_trends(self, transactions: List[Dict]) -> Dict:
        """Detect spending trends over time"""
        
        trends = {}
        
        # Group by category and month
        by_category_month = defaultdict(lambda: defaultdict(float))
        
        for t in transactions:
            try:
                date_str = t.get("date", "")
                if isinstance(date_str, str):
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    date_obj = date_str
                
                month_key = date_obj.strftime("%Y-%m")
                category = t.get("category", "Other")
                amount = float(t.get("amount", 0))
                
                by_category_month[category][month_key] += amount
            except:
                continue
        
        # Analyze trend for each category
        for category, monthly_data in by_category_month.items():
            if len(monthly_data) < 2:
                continue
            
            # Sort by month
            sorted_months = sorted(monthly_data.items())
            amounts = [amt for _, amt in sorted_months]
            
            # Simple trend detection (compare first half vs second half)
            mid = len(amounts) // 2
            first_half_avg = statistics.mean(amounts[:mid])
            second_half_avg = statistics.mean(amounts[mid:])
            
            if second_half_avg > first_half_avg * 1.1:
                direction = "INCREASING"
                change = ((second_half_avg - first_half_avg) / first_half_avg * 100)
                insight = f"Spending increased by {round(change, 0)}% over time"
            elif second_half_avg < first_half_avg * 0.9:
                direction = "DECREASING"
                change = ((first_half_avg - second_half_avg) / first_half_avg * 100)
                insight = f"Spending decreased by {round(change, 0)}% over time"
            else:
                direction = "STABLE"
                change = 0
                insight = "Spending remains relatively stable"
            
            trends[category] = {
                "direction": direction,
                "change_percentage": round(change, 1),
                "insight": insight
            }
        
        return trends
    
    def _get_empty_analysis(self) -> Dict:
        """Return empty analysis when not enough data"""
        return {
            "success": False,
            "temporal_patterns": {
                "weekend_overspending": False,
                "weekday_average": 0,
                "weekend_average": 0,
                "percentage_difference": 0,
                "payday_spike": False,
                "early_month_average": 0,
                "late_month_average": 0
            },
            "behavioral_patterns": {
                "primary_spending_day": "UNKNOWN",
                "primary_spending_category": "Other",
                "category_preferences": {}
            },
            "anomalies": [],
            "trends": {}
        }