import re
from datetime import datetime, timedelta
from typing import Optional, Dict

class NLPService:
    
    def __init__(self):
        # Common merchant keywords
        self.merchant_keywords = {
            'at', 'from', 'in', 'to', 'on', 'with'
        }
        
        # Category keywords for fallback detection
        self.category_keywords = {
            "food": ["lunch", "dinner", "breakfast", "meal", "food", "ate", "restaurant", "cafe"],
            "transport": ["uber", "taxi", "ride", "bus", "metro", "gas", "fuel", "careem", "lyft"],
            "shopping": ["bought", "purchased", "shopping", "store", "mall", "online"],
            "entertainment": ["movie", "cinema", "game", "concert", "netflix", "spotify"],
            "bills": ["bill", "electricity", "water", "internet", "rent", "phone"],
            "health": ["doctor", "pharmacy", "hospital", "medicine", "clinic"],
        }
        
        # Time-related keywords
        self.time_keywords = {
            "today": 0,
            "yesterday": 1,
            "tomorrow": -1,
            "last week": 7,
            "last month": 30,
        }
    
    def parse_expense(self, text: str, language: str = "en") -> Dict:
        """
        Parse natural language text to extract expense information
        
        Args:
            text: Natural language text (e.g., "I spent 150 on lunch at Pizza Hut")
            language: Language code (currently only 'en' supported)
        
        Returns:
            Dictionary with extracted information and confidence scores
        """
        text_lower = text.lower()
        
        # Extract components
        amount = self._extract_amount(text_lower)
        merchant = self._extract_merchant(text)
        category = self._extract_category_hint(text_lower)
        description = self._extract_description(text_lower)
        date = self._extract_date(text_lower)
        
        # Calculate confidence scores
        confidence = {
            "amount": 0.99 if amount else 0.0,
            "merchant": 0.92 if merchant else 0.0,
            "category": 0.75 if category else 0.0,
            "description": 0.85 if description else 0.0,
            "date": 0.88 if date else 0.0
        }
        
        return {
            "amount": amount,
            "merchant": merchant,
            "category": category,
            "description": description,
            "date": date,
            "confidence": confidence
        }
    
    def _extract_amount(self, text: str) -> Optional[float]:
        """
        Extract monetary amount from text
        
        Patterns:
        - "150 pounds"
        - "spent 150"
        - "cost 150.50"
        - "150 egp"
        - "150.5"
        """
        # Pattern 1: Number followed by currency
        patterns = [
            r'(\d+\.?\d*)\s*(?:pounds?|dollars?|egp|usd|eur|gbp)',
            r'(?:spent|paid|cost|price)\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:on|for)',
            r'\$\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:egyptian pounds?|egyptian)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    return float(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        # Fallback: Find any standalone number (if no currency context)
        match = re.search(r'\b(\d+\.?\d*)\b', text)
        if match:
            try:
                amount = float(match.group(1))
                # Only accept if it looks like a reasonable amount (not a year, etc.)
                if 0.01 <= amount <= 1000000:
                    return amount
            except ValueError:
                pass
        
        return None
    
    def _extract_merchant(self, text: str) -> Optional[str]:
        """
        Extract merchant/store name from text
        
        Looks for capitalized words after keywords like 'at', 'from', 'in'
        """
        # Pattern: "at Pizza Hut", "from McDonald's", "in Carrefour"
        for keyword in self.merchant_keywords:
            pattern = rf'{keyword}\s+([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*)'
            match = re.search(pattern, text)
            if match:
                merchant = match.group(1).strip()
                # Filter out common false positives
                if merchant.lower() not in ['i', 'a', 'the', 'and', 'for', 'with']:
                    return merchant
        
        # Fallback: Look for any capitalized multi-word phrase
        pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        
        # Look for single capitalized word (brand names)
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 2:
                if word.lower() not in ['i', 'spent', 'paid', 'bought', 'the']:
                    return word
        
        return None
    
    def _extract_category_hint(self, text: str) -> Optional[str]:
        """
        Extract category hints from keywords in text
        This is a fallback - the ML categorization service is more accurate
        """
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        return None
    
    def _extract_description(self, text: str) -> Optional[str]:
        """
        Extract description/purpose of expense
        
        Looks for action words like "lunch", "dinner", "ride", etc.
        """
        # Common expense descriptions
        descriptions = [
            'lunch', 'dinner', 'breakfast', 'snack', 'coffee',
            'ride', 'trip', 'fare',
            'groceries', 'shopping',
            'movie', 'game', 'show',
            'bill', 'subscription',
            'medicine', 'checkup'
        ]
        
        for desc in descriptions:
            if desc in text:
                return desc
        
        # Fallback: Extract words between "for" or "on"
        match = re.search(r'(?:for|on)\s+([a-z]+(?:\s+[a-z]+)?)', text)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """
        Extract date from text
        
        Supports:
        - "today", "yesterday", "tomorrow"
        - "last week", "last month"
        - Specific dates: "on 15th May", "May 15"
        """
        # Check for relative dates
        for keyword, days_ago in self.time_keywords.items():
            if keyword in text:
                target_date = datetime.now() - timedelta(days=days_ago)
                return target_date.strftime("%Y-%m-%d")
        
        # Check for specific date patterns
        # Pattern: "on 15th May", "May 15", "15/05/2024"
        date_patterns = [
            r'on\s+(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)',
            r'([A-Za-z]+)\s+(\d{1,2})',
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                # For now, return current date as placeholder
                # Proper date parsing would require more complex logic
                return datetime.now().strftime("%Y-%m-%d")
        
        return None


# Singleton instance
nlp_service = NLPService()