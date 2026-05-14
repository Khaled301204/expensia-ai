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
            "Electronics & Tech",
            "Other"
        ]
        
        # Training data - DESCRIPTION FOCUSED (merchant optional)
        self.training_data = [
            # Food & Dining - Focus on food-related descriptions
            ("lunch meal", "Food & Dining"),
            ("dinner eating", "Food & Dining"),
            ("breakfast morning meal", "Food & Dining"),
            ("coffee drink", "Food & Dining"),
            ("food order", "Food & Dining"),
            ("restaurant dining", "Food & Dining"),
            ("cafe snack", "Food & Dining"),
            ("groceries shopping", "Food & Dining"),
            ("pizza order", "Food & Dining"),
            ("burger meal", "Food & Dining"),
            ("chicken food", "Food & Dining"),
            ("sandwich lunch", "Food & Dining"),
            ("supermarket groceries", "Food & Dining"),
            ("fast food", "Food & Dining"),
            ("delivery food", "Food & Dining"),
            ("snack quick bite", "Food & Dining"),
            ("bakery bread", "Food & Dining"),
            ("ice cream dessert", "Food & Dining"),
            ("sushi japanese food", "Food & Dining"),
            ("pasta italian", "Food & Dining"),
            
            # Transportation - Focus on transport/travel descriptions
            ("taxi ride", "Transportation"),
            ("uber trip", "Transportation"),
            ("ride sharing", "Transportation"),
            ("gas fuel", "Transportation"),
            ("petrol station", "Transportation"),
            ("car wash", "Transportation"),
            ("parking fee", "Transportation"),
            ("metro ticket", "Transportation"),
            ("bus fare", "Transportation"),
            ("public transport", "Transportation"),
            ("toll road", "Transportation"),
            ("car maintenance", "Transportation"),
            ("vehicle service", "Transportation"),
            ("oil change", "Transportation"),
            ("tire repair", "Transportation"),
            ("bike rental", "Transportation"),
            ("train ticket", "Transportation"),
            ("subway pass", "Transportation"),
            
            # Shopping - Focus on purchase descriptions
            ("shopping clothes", "Shopping"),
            ("bought shoes", "Shopping"),
            ("purchase items", "Shopping"),
            ("online shopping", "Shopping"),
            ("store bought", "Shopping"),
            ("mall shopping", "Shopping"),
            ("fashion clothing", "Shopping"),
            ("electronics gadget", "Shopping"),
            ("appliance purchase", "Shopping"),
            ("furniture bought", "Shopping"),
            ("accessories shopping", "Shopping"),
            ("jewelry purchase", "Shopping"),
            ("toys games", "Shopping"),
            ("sports equipment", "Shopping"),
            ("home decor", "Shopping"),
            ("book shopping", "Shopping"),
            
            # Entertainment - Focus on fun/leisure descriptions
            ("movie cinema", "Entertainment"),
            ("film ticket", "Entertainment"),
            ("streaming subscription", "Entertainment"),
            ("music premium", "Entertainment"),
            ("game purchase", "Entertainment"),
            ("video game", "Entertainment"),
            ("concert ticket", "Entertainment"),
            ("show event", "Entertainment"),
            ("theater play", "Entertainment"),
            ("amusement park", "Entertainment"),
            ("sports event", "Entertainment"),
            ("hobby leisure", "Entertainment"),
            ("entertainment subscription", "Entertainment"),
            
            # Bills & Utilities - Focus on recurring payment descriptions
            ("electricity bill", "Bills & Utilities"),
            ("power bill", "Bills & Utilities"),
            ("water utility", "Bills & Utilities"),
            ("internet bill", "Bills & Utilities"),
            ("wifi service", "Bills & Utilities"),
            ("phone bill", "Bills & Utilities"),
            ("mobile service", "Bills & Utilities"),
            ("rent payment", "Bills & Utilities"),
            ("gas utility", "Bills & Utilities"),
            ("cable tv", "Bills & Utilities"),
            ("insurance payment", "Bills & Utilities"),
            ("subscription monthly", "Bills & Utilities"),
            
            # Healthcare - Focus on medical descriptions
            ("pharmacy medicine", "Healthcare"),
            ("doctor visit", "Healthcare"),
            ("medical appointment", "Healthcare"),
            ("hospital bill", "Healthcare"),
            ("dental checkup", "Healthcare"),
            ("teeth cleaning", "Healthcare"),
            ("lab test", "Healthcare"),
            ("prescription drugs", "Healthcare"),
            ("clinic consultation", "Healthcare"),
            ("health checkup", "Healthcare"),
            ("eye exam", "Healthcare"),
            ("therapy session", "Healthcare"),
            
            # Education - Focus on learning descriptions
            ("course fee", "Education"),
            ("online course", "Education"),
            ("training workshop", "Education"),
            ("book textbook", "Education"),
            ("tuition payment", "Education"),
            ("school fee", "Education"),
            ("certification exam", "Education"),
            ("learning subscription", "Education"),
            ("school supplies", "Education"),
            ("stationery items", "Education"),
            
            # Travel - Focus on trip/vacation descriptions
            ("hotel booking", "Travel"),
            ("accommodation stay", "Travel"),
            ("flight ticket", "Travel"),
            ("airplane travel", "Travel"),
            ("vacation trip", "Travel"),
            ("travel booking", "Travel"),
            ("rental stay", "Travel"),
            ("travel insurance", "Travel"),
            ("visa application", "Travel"),
            ("passport fee", "Travel"),
            ("luggage baggage", "Travel"),
            ("tourist attraction", "Travel"),
            
            # Personal Care - Focus on self-care descriptions
            ("haircut grooming", "Personal Care"),
            ("salon service", "Personal Care"),
            ("gym membership", "Personal Care"),
            ("fitness training", "Personal Care"),
            ("spa treatment", "Personal Care"),
            ("massage therapy", "Personal Care"),
            ("cosmetics beauty", "Personal Care"),
            ("skincare products", "Personal Care"),
            ("barbershop shave", "Personal Care"),
            ("nail salon", "Personal Care"),
            ("wellness service", "Personal Care"),
            
            # Other - Miscellaneous
            ("miscellaneous expense", "Other"),
            ("other payment", "Other"),
            ("general purchase", "Other"),
        ]
        
        # Load or train model
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("Categorization model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Training new model...")
                self._train_model()
        else:
            print("No existing model found. Training new model...")
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
        
        print("Model trained successfully!")
        print(f"Training samples: {len(X_train)}")
    
    def _save_model(self):
        """Save the trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")
    
    def categorize(self, description: str, merchant: str = None, amount: float = None) -> dict:
        """
        Categorize an expense based on description (merchant is optional)
        
        Args:
            description: REQUIRED - Main expense description (e.g., "lunch", "taxi ride")
            merchant: OPTIONAL - Merchant name (e.g., "Pizza Hut", "Uber") - improves accuracy
            amount: OPTIONAL - Amount (not currently used, available for future features)
        
        Returns:
            dict with category, confidence, and alternatives
        
        Examples:
            categorize("lunch") -> "Food & Dining"
            categorize("lunch", "Pizza Hut") -> "Food & Dining" (higher confidence)
            categorize("taxi ride") -> "Transportation"
            categorize("bought shoes", "Nike") -> "Shopping"
        """
        # Validate description is provided
        if not description or not description.strip():
            raise ValueError("Description is required for categorization")
        
        # Primary text is the description
        text = description.lower().strip()
        
        # Add merchant only if provided and not empty (optional bonus)
        if merchant and merchant.strip():
            text = f"{text} {merchant.lower().strip()}"
        
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
    
    def add_training_data(self, description: str, merchant: str = None, category: str = None):
        """
        Add new training data and retrain the model
        
        Args:
            description: Expense description
            merchant: Optional merchant name
            category: Correct category
        """
        # Build training text (description is primary)
        text = description.lower().strip()
        if merchant and merchant.strip():
            text = f"{text} {merchant.lower().strip()}"
        
        self.training_data.append((text, category))
        
        # Retrain model with new data
        self._train_model()
        
        return {
            "message": "Model retrained with new data",
            "total_samples": len(self.training_data)
        }