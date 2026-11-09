import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import requests

app = FastAPI()

# Initialize Google GenAI client and API keys from environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_gemini(request: QueryRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.prompt,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather")
def get_weather(city: str = "Gudiyatham"):
    if not WEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="Weather API key not configured on server")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=data.get("message", "Error fetching weather"))
        
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "ESP32 Voice Assistant Backend is live!"}
    
