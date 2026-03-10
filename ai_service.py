import os
import base64
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set in environment or .env file.")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def analyze_image(image_bytes: bytes) -> dict:
    if not client:
        return _mock_recommendation()
    
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = """
    Analyze this image and identify the person's face shape, skin tone, gender (if apparent), and current style vibe.
    Based on this, suggest a personalized outfit, footwear, and accessories.
    Also provide brief styling advice regarding color combinations that suit their skin tone, and an occasion where this outfit would be perfect.
    Format the output STRICTLY as valid JSON matching this structure:
    {
      "face_shape": "Value",
      "skin_tone": "Value",
      "gender": "Value",
      "style_vibe": "Value",
      "color_advice": "A brief sentence about color matching",
      "occasion_suggestions": "A brief sentence about suitable occasions",
      "recommendations": {
        "outfit": {
          "name": "Product Name",
          "price": "$99.99",
          "search_query": "specific style of clothing"
        },
        "footwear": {
          "name": "Product Name",
          "price": "$59.99",
          "search_query": "specific style of footwear"
        },
        "accessories": {
          "name": "Product Name",
          "price": "$29.99",
          "search_query": "specific style of accessories"
        }
      }
    }
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-90b-vision-preview",
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        result_content = response.choices[0].message.content
        return json.loads(result_content)
    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return _mock_recommendation()

def chat_with_assistant(message: str) -> str:
    if not client:
        return "I am a fashion assistant! (Placeholder text since API key is not configured.)"
        
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional, helpful, and trendy fashion assistant. Provide succinct styling tips, outfit combinations, and fashion advice based on the user's queries."},
                {"role": "user", "content": message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat_with_assistant: {e}")
        return "I encountered an error trying to process your request."

def _mock_recommendation():
    return {
        "face_shape": "Oval",
        "skin_tone": "Warm",
        "gender": "Unspecified",
        "style_vibe": "Casual Chic",
        "color_advice": "Earthy tones like olive green and mustard yellow will complement your warm undertones beautifully.",
        "occasion_suggestions": "This look is perfect for a weekend brunch or a casual smart-casual office Friday.",
        "recommendations": {
            "outfit": {
                "name": "Navy Blue Blazer & White Tee",
                "price": "$89.99",
                "search_query": "navy blue casual blazer"
            },
            "footwear": {
                "name": "White Leather Sneakers",
                "price": "$65.00",
                "search_query": "white leather minimal sneakers"
            },
            "accessories": {
                "name": "Minimalist Silver Watch",
                "price": "$120.00",
                "search_query": "minimalist silver wrist watch"
            }
        }
    }
