import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Initialize the Google GenAI client using the environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class QueryRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_gemini(request: QueryRequest):
    try:
        # Prepend a system-level constraint to keep answers concise for an OLED screen
        system_instruction = (
            "You are an assistant running on an ESP32 microcontroller with a small 0.96-inch OLED display. "
            "Keep your entire answer extremely brief, direct, and under 150 characters total. "
            "Use short sentences or bullet points. Avoid long paragraphs, filler words, or introductory text."
        )
        
        # Combine system constraint with the user's prompt
        full_prompt = f"{system_instruction}\n\nUser Question: {request.prompt}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "ESP32 Voice Assistant Backend is live!"}
    
    
