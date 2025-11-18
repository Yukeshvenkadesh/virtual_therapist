from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Virtual Therapist Model Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    topPattern: str
    confidenceScores: list

LABELS = ["Anxiety", "Depression", "Stress", "Neutral"]

def fallback_predict(text: str):
    """Enhanced fallback prediction with better keyword matching."""
    text_l = text.lower()
    
    # Initialize scores
    scores = {label: 0.1 for label in LABELS}
    
    # Anxiety keywords
    anxiety_keywords = ["worry", "anxious", "panic", "nervous", "fear", "scared", "worried", "anxiety", "panic", "restless", "uneasy"]
    anxiety_count = sum(1 for word in anxiety_keywords if word in text_l)
    if anxiety_count > 0:
        scores["Anxiety"] += 0.3 + (anxiety_count * 0.1)
    
    # Depression keywords
    depression_keywords = ["sad", "hopeless", "down", "tired", "depressed", "depression", "empty", "worthless", "guilty", "suicidal", "hopeless"]
    depression_count = sum(1 for word in depression_keywords if word in text_l)
    if depression_count > 0:
        scores["Depression"] += 0.3 + (depression_count * 0.1)
    
    # Stress keywords
    stress_keywords = ["overwhelmed", "pressure", "deadline", "stressed", "stress", "burnout", "exhausted", "frustrated", "irritated", "tense"]
    stress_count = sum(1 for word in stress_keywords if word in text_l)
    if stress_count > 0:
        scores["Stress"] += 0.3 + (stress_count * 0.1)
    
    # Neutral if no strong indicators
    if anxiety_count == 0 and depression_count == 0 and stress_count == 0:
        scores["Neutral"] = 0.7
    else:
        scores["Neutral"] = 0.1
    
    # Normalize scores
    total = sum(max(v, 0.001) for v in scores.values())
    norm = {k: max(v, 0.001) / total for k, v in scores.items()}
    top = max(norm.items(), key=lambda kv: kv[1])[0]
    
    return top, [{"label": k, "score": float(v)} for k, v in sorted(norm.items(), key=lambda kv: -kv[1])]

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        text = request.text.strip()
        if len(text) < 5:
            raise HTTPException(status_code=400, detail="Text is too short")

        # Use enhanced fallback prediction
        top, scores = fallback_predict(text)
        return {"topPattern": top, "confidenceScores": scores}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.get("/model-info")
async def model_info():
    """Get information about loaded models."""
    return {
        "standard_model_loaded": False,
        "hybrid_model_loaded": False,
        "available_labels": LABELS,
        "hybrid_labels": None,
        "model_type": "Enhanced Fallback Prediction"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "5001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
























