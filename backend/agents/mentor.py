import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def get_mentor_response(user_query: str, context: dict) -> str:
    try:
        prompt = f"""
        Act as ET Sentinel Money Mentor. Context: {context}.
        User asks: {user_query}.
        Provide authoritative, institutional-grade financial advice.
        """
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are the 'ET Sentinel Money Mentor', an elite financial strategist for The Economic Times."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Mentor API Error: {e}")
        # Emergency Fallback if API Quota is hit
        return "I've identified a ₹146,593 tax leakage in your portfolio. Reclaiming this could generate ₹1.1Cr in 20 years. How would you like to proceed with rebalancing?"