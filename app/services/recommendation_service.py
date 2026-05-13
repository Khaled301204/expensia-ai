from typing import Dict, List
import datetime

class RecommendationService:
    
    def __init__(self):
        # Average spending benchmarks (Egyptian market)
        self.spending_benchmarks = {
            "Food & Dining": {"min": 2000, "max": 4000, "ideal": 2500},
            "Transportation": {"min": 800, "max": 2000, "ideal": 1200},
            "Shopping": {"min": 1000, "max": 3000, "ideal": 1500},
            "Entertainment": {"min": 500, "max": 1500, "ideal": 800},
            "Bills & Utilities": {"min": 800, "max": 1500, "ideal": 1000},
            "Healthcare": {"min": 300, "max": 1000, "ideal": 500},
            "Education": {"min": 500, "max": 2000, "ideal": 1000},
            "Travel": {"min": 500, "max": 3000, "ideal": 1000},
            "Personal Care": {"min": 300, "max": 1000, "ideal": 500},
        }
    
    def generate_recommendations(
        self, 
        monthly_income: float,
        monthly_expenses: float,
        current_savings: float,
        risk_preference: str,
        expense_breakdown: Dict[str, float],
        goals: List[Dict] = None
    ) -> Dict:
        """
        Generate comprehensive financial recommendations
        """
        # 1. Analyze spending patterns
        spending_insights = self._analyze_spending(expense_breakdown)
        
        # 2. Calculate saving potential
        disposable_income = monthly_income - monthly_expenses
        saving_recommendations = self._generate_saving_plan(
            monthly_income, 
            monthly_expenses, 
            disposable_income,
            current_savings
        )
        
        # 3. Investment suggestions based on risk profile
        investment_suggestions = self._generate_investment_suggestions(
            disposable_income,
            current_savings,
            risk_preference
        )
        
        # 4. Goal planning
        goal_plans = None
        if goals:
            goal_plans = self._generate_goal_plans(goals, disposable_income)
        
        # 5. Calculate overall financial health score
        overall_score = self._calculate_financial_score(
            monthly_income,
            monthly_expenses,
            current_savings,
            expense_breakdown
        )
        
        return {
            "success": True,
            "spending_insights": spending_insights,
            "saving_recommendations": saving_recommendations,
            "investment_suggestions": investment_suggestions,
            "goal_plans": goal_plans,
            "overall_score": overall_score
        }
    
    def _analyze_spending(self, expense_breakdown: Dict[str, float]) -> List[Dict]:
        """
        Analyze spending against benchmarks and provide insights
        """
        insights = []
        
        for category, amount in expense_breakdown.items():
            if category not in self.spending_benchmarks:
                continue
            
            benchmark = self.spending_benchmarks[category]
            ideal = benchmark["ideal"]
            
            # Calculate difference from ideal
            diff_percentage = ((amount - ideal) / ideal) * 100 if ideal > 0 else 0
            
            # Generate insight
            insight = {}
            insight["category"] = category
            insight["current_spending"] = amount
            insight["average_spending"] = ideal
            insight["percentage_diff"] = round(diff_percentage, 1)
            
            if amount > benchmark["max"]:
                insight["insight"] = f"You're spending significantly above average on {category}"
                insight["recommendation"] = f"Consider reducing {category} spending by {amount - ideal:.0f} EGP monthly"
            elif amount < benchmark["min"]:
                insight["insight"] = f"Your {category} spending is below average"
                insight["recommendation"] = f"Your {category} budget is well-optimized"
            elif diff_percentage > 20:
                insight["insight"] = f"You're spending {abs(diff_percentage):.0f}% more than average on {category}"
                insight["recommendation"] = f"Try to reduce {category} by {(amount - ideal) * 0.5:.0f} EGP this month"
            elif diff_percentage < -20:
                insight["insight"] = f"You're spending {abs(diff_percentage):.0f}% less than average on {category}"
                insight["recommendation"] = f"Great job managing {category} expenses!"
            else:
                insight["insight"] = f"Your {category} spending is within healthy range"
                insight["recommendation"] = f"Maintain your current {category} budget"
            
            insights.append(insight)
        
        return insights
    
    def _generate_saving_plan(
        self, 
        monthly_income: float, 
        monthly_expenses: float,
        disposable_income: float,
        current_savings: float
    ) -> Dict:
        """
        Generate personalized saving recommendations
        """
        # Recommended saving rate: 20-30% of income
        ideal_saving = monthly_income * 0.20
        
        if disposable_income < 0:
            # Spending more than earning
            return {
                "monthly_target": 0,
                "breakdown": {},
                "timeline_months": 0,
                "recommendations": [
                    "You're spending more than you earn",
                    f"Reduce expenses by {abs(disposable_income):.0f} EGP monthly",
                    "Focus on cutting non-essential spending",
                    "Consider increasing income sources"
                ]
            }
        
        # Calculate emergency fund target (3-6 months of expenses)
        emergency_target = monthly_expenses * 3
        emergency_needed = max(0, emergency_target - current_savings)
        
        # Breakdown of saving allocation
        if disposable_income >= ideal_saving:
            # Can save comfortably
            breakdown = {
                "emergency_fund": min(disposable_income * 0.50, emergency_needed),
                "investments": disposable_income * 0.30,
                "goals": disposable_income * 0.20
            }
            recommendations = [
                f"Excellent! You can save {disposable_income:.0f} EGP monthly",
                f"Build emergency fund: {breakdown['emergency_fund']:.0f} EGP/month",
                f"Invest for growth: {breakdown['investments']:.0f} EGP/month",
                f"Save for goals: {breakdown['goals']:.0f} EGP/month"
            ]
        else:
            # Tight budget
            breakdown = {
                "emergency_fund": min(disposable_income * 0.70, emergency_needed),
                "flexible": disposable_income * 0.30
            }
            recommendations = [
                f"You can save {disposable_income:.0f} EGP monthly",
                f"Priority: Emergency fund ({breakdown['emergency_fund']:.0f} EGP/month)",
                f"Flexible savings: {breakdown['flexible']:.0f} EGP/month",
                "Focus on building a 3-month safety net first"
            ]
        
        # Calculate timeline to emergency fund
        timeline_months = int(emergency_needed / breakdown.get("emergency_fund", 1)) if emergency_needed > 0 else 0
        
        return {
            "monthly_target": round(disposable_income, 2),
            "breakdown": {k: round(v, 2) for k, v in breakdown.items()},
            "timeline_months": timeline_months,
            "recommendations": recommendations
        }
    
    def _generate_investment_suggestions(
        self,
        disposable_income: float,
        current_savings: float,
        risk_preference: str
    ) -> List[Dict]:
        """
        Generate investment suggestions based on risk profile
        """
        suggestions = []
        
        if disposable_income <= 0:
            return [{
                "type": "NONE",
                "suggested_amount": 0,
                "expected_return": "N/A",
                "risk_level": "N/A",
                "recommendation": "Focus on reducing expenses before investing"
            }]
        
        # Low risk options
        if risk_preference in ["LOW", "MEDIUM"]:
            suggestions.append({
                "type": "SAVINGS_ACCOUNT",
                "suggested_amount": round(disposable_income * 0.30, 2),
                "expected_return": "3-5% annually",
                "risk_level": "Very Low",
                "recommendation": "High-yield savings account for emergency fund and short-term goals"
            })
            
            suggestions.append({
                "type": "GOVERNMENT_BONDS",
                "suggested_amount": round(disposable_income * 0.25, 2),
                "expected_return": "8-12% annually",
                "risk_level": "Low",
                "recommendation": "Egyptian treasury bills or bonds for stable returns"
            })
        
        # Medium risk options
        if risk_preference in ["MEDIUM", "HIGH"]:
            suggestions.append({
                "type": "MUTUAL_FUNDS",
                "suggested_amount": round(disposable_income * 0.30, 2),
                "expected_return": "10-15% annually",
                "risk_level": "Medium",
                "recommendation": "Balanced mutual funds with mix of stocks and bonds"
            })
            
            suggestions.append({
                "type": "GOLD",
                "suggested_amount": round(disposable_income * 0.15, 2),
                "expected_return": "5-10% annually",
                "risk_level": "Low-Medium",
                "recommendation": "Gold as hedge against inflation"
            })
        
        # High risk options
        if risk_preference == "HIGH" and current_savings > 20000:
            suggestions.append({
                "type": "STOCK_MARKET",
                "suggested_amount": round(disposable_income * 0.25, 2),
                "expected_return": "12-20% annually",
                "risk_level": "High",
                "recommendation": "Egyptian Stock Exchange (EGX) for growth potential"
            })
            
            suggestions.append({
                "type": "REAL_ESTATE",
                "suggested_amount": round(current_savings * 0.10, 2),
                "expected_return": "8-12% annually",
                "risk_level": "Medium-High",
                "recommendation": "Real estate investment trusts (REITs) for passive income"
            })
        
        return suggestions[:4]  # Return top 4 suggestions
    
    def _generate_goal_plans(
        self,
        goals: List[Dict],
        disposable_income: float
    ) -> List[Dict]:
        """
        Generate actionable plans for each goal
        """
        goal_plans = []
        
        for goal in goals:
            target = goal.get("target_amount", 0)
            current = goal.get("current_amount", 0)
            deadline_str = goal.get("deadline", "")
            
            # Calculate remaining amount
            remaining = target - current
            
            # Calculate months to deadline
            try:
                deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
                today = datetime.datetime.now()
                months_left = max(1, (deadline.year - today.year) * 12 + (deadline.month - today.month))
            except:
                months_left = 12  # Default to 1 year
            
            # Calculate required monthly saving
            monthly_required = remaining / months_left if months_left > 0 else remaining
            
            # Determine feasibility
            if monthly_required <= disposable_income * 0.30:
                feasibility = "EASY"
                recommendation = f"Very achievable! Save {monthly_required:.0f} EGP monthly ({(monthly_required/disposable_income*100):.0f}% of disposable income)"
            elif monthly_required <= disposable_income * 0.60:
                feasibility = "MODERATE"
                recommendation = f"Achievable with discipline. Save {monthly_required:.0f} EGP monthly ({(monthly_required/disposable_income*100):.0f}% of disposable income)"
            else:
                feasibility = "DIFFICULT"
                recommendation = f"Challenging. Consider extending deadline or saving {disposable_income * 0.60:.0f} EGP monthly"
            
            goal_plans.append({
                "goal_name": goal.get("name", "Unnamed Goal"),
                "target_amount": target,
                "current_amount": current,
                "monthly_saving_required": round(monthly_required, 2),
                "months_to_goal": months_left,
                "feasibility": feasibility,
                "recommendation": recommendation
            })
        
        return goal_plans
    
    def _calculate_financial_score(
        self,
        monthly_income: float,
        monthly_expenses: float,
        current_savings: float,
        expense_breakdown: Dict[str, float]
    ) -> float:
        """
        Calculate overall financial health score (0-100)
        """
        score = 0
        
        # 1. Savings Rate (30 points)
        disposable = monthly_income - monthly_expenses
        savings_rate = (disposable / monthly_income * 100) if monthly_income > 0 else 0
        if savings_rate >= 30:
            score += 30
        elif savings_rate >= 20:
            score += 25
        elif savings_rate >= 10:
            score += 15
        elif savings_rate > 0:
            score += 10
        
        # 2. Emergency Fund (25 points)
        emergency_months = current_savings / monthly_expenses if monthly_expenses > 0 else 0
        if emergency_months >= 6:
            score += 25
        elif emergency_months >= 3:
            score += 20
        elif emergency_months >= 1:
            score += 10
        
        # 3. Spending Discipline (25 points)
        overspending_count = 0
        for category, amount in expense_breakdown.items():
            if category in self.spending_benchmarks:
                if amount > self.spending_benchmarks[category]["max"]:
                    overspending_count += 1
        
        if overspending_count == 0:
            score += 25
        elif overspending_count <= 2:
            score += 15
        elif overspending_count <= 4:
            score += 5
        
        # 4. Income vs Expenses (20 points)
        if monthly_income > monthly_expenses:
            expense_ratio = monthly_expenses / monthly_income
            if expense_ratio <= 0.70:
                score += 20
            elif expense_ratio <= 0.80:
                score += 15
            elif expense_ratio <= 0.90:
                score += 10
            else:
                score += 5
        
        return round(min(score, 100), 1)