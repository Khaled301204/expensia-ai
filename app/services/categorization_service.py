import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

class CategorizationService:
    
    def __init__(self):
        self.model_path = "app/models/ml_models/categorizer.pkl"
        self.model = None
        self.categories = [
            "Food & Dining",
            "Transportation",
            "Shopping",
            "Entertainment",
            "Bills & Utilities",
            "Healthcare",
            "Education",
            "Travel",
            "Personal Care",
            "Other"
        ]
        
        # Training data (expanded dataset)
        self.training_data = [
            # Food & Dining
            ("lunch at restaurant", "Food & Dining"),
            ("dinner pizza hut", "Food & Dining"),
            ("coffee starbucks", "Food & Dining"),
            ("breakfast mcdonalds", "Food & Dining"),
            ("grocery store", "Food & Dining"),
            ("food delivery", "Food & Dining"),
            ("restaurant bill", "Food & Dining"),
            ("kfc chicken", "Food & Dining"),
            ("subway sandwich", "Food & Dining"),
            ("burger king", "Food & Dining"),
            ("dominos pizza", "Food & Dining"),
            ("cafe costa", "Food & Dining"),
            ("supermarket shopping", "Food & Dining"),
            ("carrefour groceries", "Food & Dining"),
            
            # Transportation
            ("uber ride", "Transportation"),
            ("taxi fare", "Transportation"),
            ("gas station", "Transportation"),
            ("fuel petrol", "Transportation"),
            ("car wash", "Transportation"),
            ("parking fee", "Transportation"),
            ("metro ticket", "Transportation"),
            ("bus fare", "Transportation"),
            ("careem ride", "Transportation"),
            ("lyft trip", "Transportation"),
            ("toll road", "Transportation"),
            ("car maintenance", "Transportation"),
            ("oil change", "Transportation"),
            
            # Shopping
            ("amazon purchase", "Shopping"),
            ("clothes shopping", "Shopping"),
            ("shoes bought", "Shopping"),
            ("electronics store", "Shopping"),
            ("online shopping", "Shopping"),
            ("zara clothes", "Shopping"),
            ("h&m shopping", "Shopping"),
            ("noon order", "Shopping"),
            ("jumia purchase", "Shopping"),
            ("mall shopping", "Shopping"),
            ("nike shoes", "Shopping"),
            ("adidas store", "Shopping"),
            
            # Entertainment
            ("movie ticket", "Entertainment"),
            ("cinema vox", "Entertainment"),
            ("netflix subscription", "Entertainment"),
            ("spotify premium", "Entertainment"),
            ("game purchase", "Entertainment"),
            ("concert ticket", "Entertainment"),
            ("theater show", "Entertainment"),
            ("youtube premium", "Entertainment"),
            ("playstation game", "Entertainment"),
            ("xbox game pass", "Entertainment"),
            
            # Bills & Utilities
            ("electricity bill", "Bills & Utilities"),
            ("water bill", "Bills & Utilities"),
            ("internet bill", "Bills & Utilities"),
            ("phone bill", "Bills & Utilities"),
            ("rent payment", "Bills & Utilities"),
            ("gas bill", "Bills & Utilities"),
            ("we internet", "Bills & Utilities"),
            ("vodafone mobile", "Bills & Utilities"),
            ("etisalat bill", "Bills & Utilities"),
            
            # Healthcare
            ("pharmacy medicine", "Healthcare"),
            ("doctor visit", "Healthcare"),
            ("hospital bill", "Healthcare"),
            ("dental checkup", "Healthcare"),
            ("lab test", "Healthcare"),
            ("prescription drugs", "Healthcare"),
            ("clinic consultation", "Healthcare"),
            
            # Education
            ("course fee", "Education"),
            ("book purchase", "Education"),
            ("tuition payment", "Education"),
            ("udemy course", "Education"),
            ("coursera subscription", "Education"),
            ("school supplies", "Education"),
            
            # Travel
            ("hotel booking", "Travel"),
            ("flight ticket", "Travel"),
            ("airbnb stay", "Travel"),
            ("booking.com hotel", "Travel"),
            ("travel insurance", "Travel"),
            ("visa fee", "Travel"),
            
            # Personal Care
            ("haircut salon", "Personal Care"),
            ("gym membership", "Personal Care"),
            ("spa treatment", "Personal Care"),
            ("cosmetics", "Personal Care"),
            ("barbershop", "Personal Care"),
        ]
        
        # Load or train model
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("✅ Categorization model loaded successfully")
            except Exception as e:
                print(f"⚠️ Error loading model: {e}")
                print("🔄 Training new model...")
                self._train_model()
        else:
            print("📚 No existing model found. Training new model...")
            self._train_model()
    
    def _train_model(self):
        """Train the categorization model"""
        # Prepare training data
        X_train = [desc for desc, _ in self.training_data]
        y_train = [cat for _, cat in self.training_data]
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                lowercase=True,
                max_features=1000,
                ngram_range=(1, 2),  # Use unigrams and bigrams
                stop_words='english'
            )),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Save the model
        self._save_model()
        
        print("✅ Model trained successfully!")
        print(f"📊 Training samples: {len(X_train)}")
    
    def _save_model(self):
        """Save the trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 Model saved to {self.model_path}")
    
    def categorize(self, description: str, merchant: str = None, amount: float = None) -> dict:
        """
        Categorize an expense based on description and optional merchant
        
        Args:
            description: Expense description
            merchant: Optional merchant name
            amount: Optional amount (not used in current model but available for future)
        
        Returns:
            dict with category, confidence, and alternatives
        """
        # Combine description and merchant for better accuracy
        text = description.lower()
        if merchant:
            text = f"{text} {merchant.lower()}"
        
        # Get prediction
        category = self.model.predict([text])[0]
        
        # Get confidence scores for all categories
        probabilities = self.model.predict_proba([text])[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[::-1][:3]
        
        alternatives = []
        for idx in top_indices[1:]:  # Skip the first one (main prediction)
            alternatives.append({
                "category": self.model.classes_[idx],
                "confidence": float(probabilities[idx])
            })
        
        return {
            "category": category,
            "confidence": float(probabilities[self.model.classes_.tolist().index(category)]),
            "alternatives": alternatives
        }
    
    def add_training_data(self, description: str, merchant: str, category: str):
        """
        Add new training data and retrain the model
        
        Args:
            description: Expense description
            merchant: Merchant name
            category: Correct category
        """
        text = description.lower()
        if merchant:
            text = f"{text} {merchant.lower()}"
        
        self.training_data.append((text, category))
        
        # Retrain model with new data
        self._train_model()
        
        return {"message": "Model retrained with new data", "total_samples": len(self.training_data)}