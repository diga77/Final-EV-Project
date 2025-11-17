"""
AI API Module for EV Range Predictor
Provides intelligent insights and responses using HuggingFace API
"""

import os
from openai import OpenAI
from typing import Optional, Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()


class EVAIAssistant:
    """AI Assistant for Electric Vehicle insights and recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI assistant with HuggingFace API"""
        self.api_key = os.getenv("HF_TOK")                  
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=self.api_key,
        )
        self.model = "deepseek-ai/DeepSeek-V3.2-Exp:novita"
    
    def get_vehicle_recommendation(self, vehicle_info: Dict[str, Any], predicted_range: float) -> str:
        """Get AI recommendation for a specific vehicle"""
        prompt = f"""You are an expert electric vehicle consultant. Provide a professional recommendation for this vehicle.

Vehicle Details:
- Make: {vehicle_info.get('Make', 'Unknown')}
- Model: {vehicle_info.get('Model', 'Unknown')}
- Year: {vehicle_info.get('Model Year', 'Unknown')}
- Type: {vehicle_info.get('Electric Vehicle Type', 'Unknown')}
- Price: ${vehicle_info.get('Base MSRP', 0):,.0f}
- Predicted Range: {predicted_range:.1f} miles
- Location: {vehicle_info.get('State', 'Unknown')}

Provide a 2-3 sentence professional insight about:
1. Whether this range is competitive for this vehicle class and price point
2. Best use cases and real-world recommendations
Keep it concise, professional, and user-friendly."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to generate AI insights: {str(e)[:100]}"
    
    def get_maintenance_tips(self, vehicle_type: str, age: int) -> str:
        """Get maintenance and care tips for the vehicle"""
        prompt = f"""You are an EV maintenance expert. Provide maintenance tips for a {age}-year-old {vehicle_type}.

Provide 3-4 key maintenance points in bullet format for:
- Battery health management
- Charging recommendations
- Seasonal care
Keep it practical and actionable."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to generate maintenance tips: {str(e)[:100]}"
    
    def get_charging_strategy(self, predicted_range: float, daily_commute: float) -> str:
        """Get optimal charging strategy based on range and usage"""
        prompt = f"""You are an EV charging expert. Provide optimal charging strategy for a vehicle with {predicted_range:.0f} miles range and {daily_commute:.0f} miles daily commute.

Provide practical recommendations for:
1. Charging frequency
2. Optimal charging times
3. Home vs public charging strategy
Keep it concise and actionable."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to generate charging strategy: {str(e)[:100]}"
    
    def answer_ev_question(self, question: str) -> str:
        """Answer general EV-related questions"""
        prompt = f"""You are an expert electric vehicle consultant with deep knowledge about EVs, charging, batteries, and sustainability.
        
User Question: {question}

Provide a helpful, accurate, and professional response. Keep it concise (2-3 sentences) and practical."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to answer question: {str(e)[:100]}"
    
    def compare_vehicles(self, vehicle1_info: Dict, vehicle1_range: float, 
                        vehicle2_info: Dict, vehicle2_range: float) -> str:
        """Compare two vehicles based on their specifications and ranges"""
        prompt = f"""Compare these two electric vehicles as an expert consultant:

Vehicle 1:
- Make/Model: {vehicle1_info.get('Make')} {vehicle1_info.get('Model')}
- Year: {vehicle1_info.get('Model Year')}
- Type: {vehicle1_info.get('Electric Vehicle Type')}
- Price: ${vehicle1_info.get('Base MSRP', 0):,.0f}
- Predicted Range: {vehicle1_range:.0f} miles

Vehicle 2:
- Make/Model: {vehicle2_info.get('Make')} {vehicle2_info.get('Model')}
- Year: {vehicle2_info.get('Model Year')}
- Type: {vehicle2_info.get('Electric Vehicle Type')}
- Price: ${vehicle2_info.get('Base MSRP', 0):,.0f}
- Predicted Range: {vehicle2_range:.0f} miles

Provide a brief, professional comparison highlighting key differences and which might be better for different use cases."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to compare vehicles: {str(e)[:100]}"


# Demo usage
if __name__ == "__main__":
    print("🚀 EV AI Assistant Demo\n")
    print("=" * 60)
    
    # Initialize assistant
    assistant = EVAIAssistant()
    
    # Demo 1: Get vehicle recommendation
    print("\n1️⃣ VEHICLE RECOMMENDATION")
    print("-" * 60)
    vehicle_info = {
        "Make": "Tesla",
        "Model": "Model 3",
        "Model Year": 2023,
        "Electric Vehicle Type": "BEV",
        "Base MSRP": 46990,
        "State": "CA"
    }
    recommendation = assistant.get_vehicle_recommendation(vehicle_info, 358.5)
    print(f"Vehicle: {vehicle_info['Make']} {vehicle_info['Model']}")
    print(f"Recommendation: {recommendation}\n")
    
    # Demo 2: Get maintenance tips
    print("\n2️⃣ MAINTENANCE TIPS")
    print("-" * 60)
    tips = assistant.get_maintenance_tips("BEV", 2)
    print(f"Maintenance Tips:\n{tips}\n")
    
    # Demo 3: Get charging strategy
    print("\n3️⃣ CHARGING STRATEGY")
    print("-" * 60)
    strategy = assistant.get_charging_strategy(358.5, 50)
    print(f"Charging Strategy:\n{strategy}\n")
    
    # Demo 4: Answer general question
    print("\n4️⃣ EV QUESTION ANSWERING")
    print("-" * 60)
    question = "What is the difference between BEV and PHEV?"
    answer = assistant.answer_ev_question(question)
    print(f"Q: {question}")
    print(f"A: {answer}\n")
    
    print("=" * 60)
    print("✅ Demo completed successfully!")
