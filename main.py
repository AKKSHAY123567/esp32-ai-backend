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
        # Using Gemini Flash for ultra-fast conversational responses
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.prompt,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "ESP32 Voice Assistant Backend is live!"}
