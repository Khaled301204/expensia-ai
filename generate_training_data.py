import csv
import json
import random
from datetime import datetime, timedelta

# Egyptian-focused expense patterns
TRAINING_DATA = {
    "Food & Dining": {
        "merchants": [
            # Fast Food
            "McDonald's", "KFC", "Pizza Hut", "Subway", "Hardee's", "Burger King",
            "Domino's Pizza", "Papa John's", "Cook Door", "Kazaz",
            
            # Cafes
            "Starbucks", "Costa Coffee", "Cilantro", "Beano's", "The Coffee Bean",
            "Cafe Greco", "Espresso Lab", "Pottery Cafe",
            
            # Restaurants
            "Chili's", "TGI Fridays", "Andrea's", "Sequoia", "Kazoku",
            "Mori Sushi", "Zooba", "Taboon", "Ovio", "La Poire",
            
            # Egyptian Food
            "Abou Tarek", "El Abd", "Felfela", "Estoril", "Gad",
            "Mohamed Ahmed", "Hadramout", "Al Omda",
            
            # Delivery
            "Talabat", "Uber Eats", "Elmenus", "Otlob",
            
            # Groceries
            "Carrefour", "Metro", "Spinneys", "Seoudi", "Kheir Zaman",
            "Fathalla Market", "Oscar Market", "Panda"
        ],
        "descriptions": [
            "lunch", "dinner", "breakfast", "coffee", "snack", "fast food",
            "restaurant meal", "takeout", "food delivery", "groceries",
            "weekly shopping", "monthly groceries", "family dinner",
            "brunch", "dessert", "shawarma", "koshary", "foul and falafel",
            "pizza order", "burger meal", "sushi dinner", "coffee and cake"
        ],
        "amount_range": (20, 800)
    },
    
    "Transportation": {
        "merchants": [
            # Ride Sharing
            "Uber", "Careem", "InDrive", "DiDi", "Swvl",
            
            # Gas Stations
            "Shell", "Mobil", "Total", "ADNOC", "Misr Petroleum",
            "Wataniya", "Gas Station",
            
            # Public Transport
            "Cairo Metro", "Uber Moto", "Tneen Bike",
            
            # Services
            "Car Wash", "Auto Service", "Parking", "Toll Gate"
        ],
        "descriptions": [
            "uber ride", "careem trip", "taxi", "ride to work", "commute",
            "fuel", "benzene", "benzine", "gasoline", "diesel", "petrol",
            "gas refill", "car wash", "parking fee", "metro ticket",
            "bus fare", "transportation", "ride home", "airport ride",
            "uber to mall", "careem to office", "ride sharing"
        ],
        "amount_range": (10, 500)
    },
    
    "Shopping": {
        "merchants": [
            # Fashion
            "Nike", "Adidas", "Zara", "H&M", "LC Waikiki", "Defacto",
            "Mango", "Pull&Bear", "Bershka", "Marks & Spencer",
            "Splash", "Centrepoint", "Beymen", "Cotton On",
            
            # Online
            "Amazon", "Noon", "Jumia", "Souq.com", "AliExpress",
            
            # Electronics
            "B.TECH", "Xcite", "eXtra", "Vodafone Store", "Orange Store",
            "Samsung Store", "Apple Store", "Mobiles Shop",
            
            # Home
            "IKEA", "Home Centre", "Pottery Barn", "Mobilia", "Kenoz",
            "Mashrabia Gallery", "The One", "Pan Emirates"
        ],
        "descriptions": [
            "shoes", "sneakers", "clothes", "shirt", "pants", "dress",
            "jacket", "t-shirt", "jeans", "shopping", "online order",
            "phone", "laptop", "headphones", "electronics", "gadget",
            "furniture", "home decor", "bedding", "kitchenware",
            "bought shoes", "bought clothes", "new phone", "shopping spree"
        ],
        "amount_range": (50, 10000)
    },
    
    "Entertainment": {
        "merchants": [
            # Streaming
            "Netflix", "Spotify", "Apple Music", "Anghami", "Shahid VIP",
            "Watch it", "Disney+", "Amazon Prime", "YouTube Premium",
            
            # Gaming
            "PlayStation Store", "Xbox Store", "Steam", "Epic Games",
            "Google Play", "App Store",
            
            # Cinema
            "VOX Cinemas", "Cima Club", "Galaxy Cinemas", "Renaissance",
            
            # Sports/Gyms
            "Gold's Gym", "Fitness First", "Energy Gym", "World Gym",
            "Smart Gym", "CrossFit", "Pilates Studio"
        ],
        "descriptions": [
            "netflix subscription", "spotify premium", "movie tickets",
            "cinema", "concert", "gaming", "video games", "game purchase",
            "gym membership", "fitness", "sports", "entertainment",
            "streaming service", "music subscription", "movies",
            "gym session", "personal trainer", "yoga class"
        ],
        "amount_range": (30, 1000)
    },
    
    "Bills & Utilities": {
        "merchants": [
            "WE", "Vodafone Egypt", "Etisalat", "Orange Egypt",
            "Electricity Company", "Water Company", "Gas Company",
            "Internet Provider", "Nile Sat", "beIN Sports"
        ],
        "descriptions": [
            "internet bill", "mobile bill", "phone bill", "wifi",
            "electricity bill", "water bill", "gas bill", "utilities",
            "monthly bills", "landline", "cable tv", "satellite",
            "internet payment", "mobile recharge", "electricity payment"
        ],
        "amount_range": (50, 1500)
    },
    
    "Healthcare": {
        "merchants": [
            # Pharmacies
            "Seif Pharmacy", "Chowefat Pharmacy", "19011 Pharmacy",
            "El Ezaby Pharmacy", "Misr Pharmacy",
            
            # Labs
            "Al Borg Lab", "Biolab", "Al Mokhtabar", "Alpha Lab",
            
            # Hospitals/Clinics
            "Dar Al Fouad", "Saudi German Hospital", "Cleopatra Hospital",
            "Nile Badrawi", "As-Salam International", "Private Clinic",
            "Dentist", "Doctor", "Medical Center"
        ],
        "descriptions": [
            "pharmacy", "medicine", "prescription", "medication",
            "doctor visit", "dentist", "dental checkup", "medical checkup",
            "lab tests", "blood tests", "x-ray", "consultation",
            "healthcare", "hospital visit", "clinic", "medical treatment"
        ],
        "amount_range": (50, 5000)
    },
    
    "Education": {
        "merchants": [
            # Online Learning
            "Udemy", "Coursera", "LinkedIn Learning", "Skillshare",
            
            # Universities (Egyptian)
            "AUC", "GUC", "BUE", "Nile University", "MSA University",
            
            # Language/Training
            "British Council", "Amideast", "ALC", "ILI",
            
            # Books
            "Diwan Bookstore", "Shorouk Bookstore", "Alef Bookstore",
            "Amazon Books", "Jarir Bookstore"
        ],
        "descriptions": [
            "online course", "udemy course", "coursera", "training",
            "tuition", "university fees", "semester fees", "books",
            "education", "certification", "workshop", "seminar",
            "private lessons", "tutoring", "study materials",
            "english course", "language learning"
        ],
        "amount_range": (100, 20000)
    },
    
    "Travel": {
        "merchants": [
            # Airlines
            "EgyptAir", "Flynas", "Air Cairo", "Jazeera Airways",
            "FlyDubai", "Emirates", "Qatar Airways",
            
            # Booking
            "Booking.com", "Airbnb", "Hotels.com", "Expedia", "Agoda",
            
            # Hotels
            "Hilton", "Marriott", "Four Seasons", "Sofitel", "Sheraton"
        ],
        "descriptions": [
            "flight ticket", "plane ticket", "hotel booking", "airbnb",
            "vacation", "travel", "trip", "tourism", "resort",
            "accommodation", "holiday", "weekend getaway",
            "flight to dubai", "hotel stay", "resort booking"
        ],
        "amount_range": (500, 25000)
    },
    
    "Personal Care": {
        "merchants": [
            "Salon", "Barbershop", "Spa", "Beauty Center",
            "The Body Shop", "MAC", "Sephora", "Boots",
            "L'Oréal", "Maybelline", "Pharmacy"
        ],
        "descriptions": [
            "haircut", "hair salon", "barber", "spa", "massage",
            "facial", "cosmetics", "makeup", "skincare", "beauty products",
            "personal care", "grooming", "manicure", "pedicure",
            "hair treatment", "beauty salon"
        ],
        "amount_range": (30, 2000)
    },
    
    "Other": {
        "merchants": [
            "ATM Withdrawal", "Bank Fee", "Insurance Company",
            "Government Office", "Post Office", "Charity",
            "Pet Shop", "Veterinary Clinic", "Laundry", "Dry Cleaning"
        ],
        "descriptions": [
            "cash withdrawal", "bank fees", "insurance payment",
            "donation", "charity", "pet food", "vet visit",
            "laundry", "dry cleaning", "miscellaneous", "other expenses",
            "subscription", "membership", "registration fee"
        ],
        "amount_range": (20, 2000)
    }
}

def generate_expense(category, data):
    """Generate one realistic expense"""
    merchant = random.choice(data["merchants"])
    description = random.choice(data["descriptions"])
    min_amt, max_amt = data["amount_range"]
    amount = random.randint(min_amt, max_amt)
    
    # Vary the format for natural language diversity
    format_type = random.random()
    
    if format_type < 0.25:
        # Just description
        full_description = description
        merchant_field = ""
    elif format_type < 0.5:
        # Description at merchant
        full_description = f"{description} at {merchant}"
        merchant_field = merchant
    elif format_type < 0.75:
        # Description from merchant
        full_description = f"{description} from {merchant}"
        merchant_field = merchant
    else:
        # Paid amount for description
        full_description = f"paid {amount} for {description}"
        merchant_field = ""
    
    return {
        "description": full_description,
        "merchant": merchant_field,
        "category": category,
        "amount": amount
    }

def generate_dataset(total_expenses=1000):
    """Generate complete training dataset with realistic distribution"""
    expenses = []
    
    # Realistic Egyptian spending distribution
    distribution = {
        "Food & Dining": 0.35,      # 35% - Most common
        "Transportation": 0.20,     # 20%
        "Shopping": 0.12,           # 12%
        "Bills & Utilities": 0.10,  # 10%
        "Entertainment": 0.08,      # 8%
        "Healthcare": 0.05,         # 5%
        "Personal Care": 0.04,      # 4%
        "Education": 0.03,          # 3%
        "Travel": 0.02,             # 2%
        "Other": 0.01               # 1%
    }
    
    print("🤖 Generating training data...")
    print()
    
    for category, percentage in distribution.items():
        count = int(total_expenses * percentage)
        data = TRAINING_DATA[category]
        
        for _ in range(count):
            expenses.append(generate_expense(category, data))
        
        print(f"  {category:<20} {count:4} examples")
    
    # Shuffle for realistic mix
    random.shuffle(expenses)
    
    return expenses

def save_to_csv(expenses, filename="synthetic_training_data.csv"):
    """Save to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['description', 'merchant', 'category', 'amount'])
        writer.writeheader()
        writer.writerows(expenses)
    
    print()
    print(f"Saved {len(expenses)} training examples to: {filename}")

def save_to_json(expenses, filename="synthetic_training_data.json"):
    """Save to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {filename}")

def show_samples(expenses, count=10):
    """Show random samples"""
    print()
    print("Random Sample Expenses:")
    print("-" * 80)
    for expense in random.sample(expenses, min(count, len(expenses))):
        desc = expense['description'][:45].ljust(45)
        cat = expense['category'].ljust(20)
        amt = f"{expense['amount']:>6} EGP"
        print(f"  {desc} → {cat} {amt}")

if __name__ == "__main__":
    print("=" * 80)
    print("SYNTHETIC TRAINING DATA GENERATOR")
    print("=" * 80)
    print()
    
    # Generate 1000 realistic expenses
    expenses = generate_dataset(1000)
    
    # Save in both formats
    save_to_csv(expenses)
    save_to_json(expenses)
    
    # Show random samples
    show_samples(expenses)
    
    print()
    print("=" * 80)
    print("DONE! Your training data is ready!")
    print("=" * 80)
    print()
    print("📤 Next step: Upload to /api/bulk-train")
    print("   1. Start server: uvicorn app.main:app --reload --port 8000")
    print("   2. Open: http://localhost:8000/docs")
    print("   3. POST /api/bulk-train")
    print("   4. Upload: synthetic_training_data.csv")
    print()