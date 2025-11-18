import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn.functional as F
from dotenv import load_dotenv

load_dotenv()

try:
    from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except Exception:
    TRANSFORMERS_AVAILABLE = False

# Import hybrid model
try:
    from hybrid_model import HybridModelInference
    HYBRID_MODEL_AVAILABLE = True
except Exception as e:
    print(f"Hybrid model not available: {e}")
    HYBRID_MODEL_AVAILABLE = False

app = Flask(__name__)
CORS(app, origins=[os.getenv("FRONTEND_ORIGIN", "*")])

LABELS = ["Anxiety", "Bipolar", "Depression"]  # Updated to match hybrid model
HYBRID_LABELS = ["Anxiety", "Bipolar", "Depression"]  # Your model's labels

# Model paths
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "model", "mental_health_model.pth")
)
HYBRID_PYTORCH_PATH = os.getenv(
    "HYBRID_PYTORCH_PATH",
    os.path.join(os.path.dirname(__file__), "model", "mental_health_model.pth")
)
HYBRID_XGB_PATH = os.getenv(
    "HYBRID_XGB_PATH", 
    os.path.join(os.path.dirname(__file__), "model", "xgboost_classifier.json")
)
#HYBRID_PYTORCH_PATH = "/Users/adithyan/Desktop/RND/basepapers/virtual-therapist/backend/analysis_service/model/mental_health_model.pth"
#HYBRID_XGB_PATH = "/Users/adithyan/Desktop/RND/basepapers/virtual-therapist/backend/analysis_service/model/xgboost_classifier.json"

tokenizer = None
model = None
hybrid_model = None
device = "cpu"

def load_hybrid_model():
    """Load the hybrid DistilBERT-BiLSTM-XGBoost model."""
    global hybrid_model
    if not HYBRID_MODEL_AVAILABLE:
        print("[analysis_service] Hybrid model not available.")
        return False
    
    try:
        print("[analysis_service] Attempting to load hybrid model...")
        hybrid_model = HybridModelInference(
            model_path=HYBRID_PYTORCH_PATH,
            xgb_path=HYBRID_XGB_PATH
        )
        print("[analysis_service] ✅ Hybrid model loaded successfully!")
        
        # Test the model with a simple prediction to ensure it works
        try:
            test_result = hybrid_model.predict("test")
            print("[analysis_service] ✅ Hybrid model test prediction successful!")
            return True
        except Exception as test_e:
            print(f"[analysis_service] ❌ Hybrid model test failed: {test_e}")
            hybrid_model = None
            return False
            
    except Exception as e:
        print(f"[analysis_service] ❌ Error loading hybrid model: {e}")
        hybrid_model = None
        return False

def load_model():
    global tokenizer, model
    if not TRANSFORMERS_AVAILABLE:
        print("[analysis_service] transformers not available; using heuristic fallback.")
        return
    
    try:
        # Check if MODEL_PATH is a directory (Hugging Face format)
        if os.path.isdir(MODEL_PATH):
            print(f"[analysis_service] Loading Hugging Face model from directory: {MODEL_PATH}")
            tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
            model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
            print(f"[analysis_service] Successfully loaded Hugging Face model from {MODEL_PATH}")
        else:
            # Load base model and tokenizer
            tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
            model = DistilBertForSequenceClassification.from_pretrained(
                "distilbert-base-uncased", num_labels=len(LABELS)
            )
            
            # Load custom weights if available
            if os.path.exists(MODEL_PATH):
                print(f"[analysis_service] Loading custom weights from: {MODEL_PATH}")
                state = torch.load(MODEL_PATH, map_location="cpu")
                
                if isinstance(state, dict):
                    if "state_dict" in state:
                        model.load_state_dict(state["state_dict"])
                        print(f"[analysis_service] Loaded state_dict from {MODEL_PATH}")
                    elif "model_state_dict" in state:
                        model.load_state_dict(state["model_state_dict"])
                        print(f"[analysis_service] Loaded model_state_dict from {MODEL_PATH}")
                    else:
                        # Try to load as state dict directly
                        model.load_state_dict(state)
                        print(f"[analysis_service] Loaded direct state_dict from {MODEL_PATH}")
                else:
                    # Load as complete model
                    model = state
                    print(f"[analysis_service] Loaded complete model from {MODEL_PATH}")
            else:
                print(f"[analysis_service] MODEL_PATH not found at {MODEL_PATH}. Using base DistilBERT weights.")
        
        model.eval()
        print(f"[analysis_service] Model loaded successfully. Device: {device}")
        
    except Exception as e:
        print(f"[analysis_service] Error loading model: {e}")
        print("[analysis_service] Falling back to heuristic analysis")
        tokenizer = None
        model = None

# Load models
# load_model()  # Disable standard model since we have hybrid model weights
# load_hybrid_model()  # Disable due to segfault - using fallback prediction

def fallback_predict(text: str):
    """Enhanced fallback prediction that matches hybrid model labels."""
    text_l = text.lower()
    
    # Start with equal base scores
    scores = {"Anxiety": 0.33, "Bipolar": 0.33, "Depression": 0.33}
    
    # Count keyword matches for more accurate scoring
    anxiety_count = 0
    depression_count = 0
    bipolar_count = 0
    
    # Anxiety indicators
    anxiety_words = ["worry", "worried", "anxious", "anxiety", "panic", "nervous", "fear", "scared", "restless", "uneasy", "tense", "apprehensive", 
                     "replaying", "replay", "ruminating", "ruminate", "overthinking", "overthink", "obsessing", "obsess", 
                     "conversation", "embarrassed", "embarrassing", "awkward", "stupid", "idiot", "foolish", "fool", 
                     "judged", "judging", "criticized", "criticism", "rejected", "rejection", "humiliated", "humiliation",
                     "social", "socially", "people", "others", "everyone", "everybody", "what if", "what ifs"]
    for word in anxiety_words:
        if word in text_l:
            anxiety_count += 1
    
    # Depression indicators
    depression_words = ["sad", "hopeless", "down", "tired", "exhausted", "empty", "worthless", "guilty", "suicidal", "depressed", "melancholy", "gloomy"]
    for word in depression_words:
        if word in text_l:
            depression_count += 1
    
    # Bipolar indicators (mood swings, manic symptoms)
    bipolar_words = ["manic", "euphoric", "hyperactive", "impulsive", "mood", "swing", "high", "low", "irritable", "agitated", "energetic", "racing"]
    for word in bipolar_words:
        if word in text_l:
            bipolar_count += 1
    
    # Apply scoring based on keyword counts
    if anxiety_count > 0:
        scores["Anxiety"] += anxiety_count * 0.3
        scores["Bipolar"] -= anxiety_count * 0.1
        scores["Depression"] -= anxiety_count * 0.1
    
    if depression_count > 0:
        scores["Depression"] += depression_count * 0.3
        scores["Anxiety"] -= depression_count * 0.1
        scores["Bipolar"] -= depression_count * 0.1
    
    if bipolar_count > 0:
        scores["Bipolar"] += bipolar_count * 0.3
        scores["Anxiety"] -= bipolar_count * 0.1
        scores["Depression"] -= bipolar_count * 0.1
    
    # Stress indicators (can contribute to any condition)
    stress_words = ["overwhelmed", "pressure", "deadline", "stressed", "stress", "burnout", "overworked"]
    stress_count = sum(1 for word in stress_words if word in text_l)
    if stress_count > 0:
        scores["Anxiety"] += stress_count * 0.15
        scores["Depression"] += stress_count * 0.1
        scores["Bipolar"] += stress_count * 0.05
    
    # Ensure minimum scores
    for key in scores:
        scores[key] = max(scores[key], 0.1)
    
    # Normalize scores
    total = sum(scores.values())
    norm = {k: v / total for k, v in scores.items()}
    top = max(norm.items(), key=lambda kv: kv[1])[0]
    
    return top, [{"label": k, "score": float(v)} for k, v in sorted(norm.items(), key=lambda kv: -kv[1])]

@app.get("/health")
def health():
    return jsonify({"ok": True, "labels": LABELS, "version": "updated"})

@app.post("/api/analyze")
def analyze():
    """API endpoint that matches the expected frontend/backend interface."""
    return predict()

@app.post("/predict")
def predict():
    try:
        data = request.get_json(force=True)
        text = (data.get("text") or "").strip()
        if len(text) < 5:
            return jsonify({"error": "Text is too short"}), 400

        # Try hybrid model first
        if hybrid_model is not None:
            try:
                result = hybrid_model.predict(text)
                return jsonify(result)
            except Exception as e:
                print(f"[analysis_service] Hybrid model prediction failed: {e}")
                # Fall through to standard model

        # Fallback to standard model
        if model is None or tokenizer is None:
            top, scores = fallback_predict(text)
            return jsonify({"topPattern": top, "confidenceScores": scores})

        inputs = tokenizer([text], truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits.squeeze(0), dim=-1).cpu().numpy().tolist()

        scores = [{"label": LABELS[i], "score": float(probs[i])} for i in range(len(LABELS))]
        scores_sorted = sorted(scores, key=lambda x: -x["score"])
        top = scores_sorted[0]["label"]
        return jsonify({"topPattern": top, "confidenceScores": scores_sorted})
    except Exception as e:
        return jsonify({"error": "Inference error", "detail": str(e)}), 500

@app.get("/model-info")
def model_info():
    """Get information about loaded models."""
    info = {
        "standard_model_loaded": model is not None and tokenizer is not None,
        "hybrid_model_loaded": hybrid_model is not None,
        "available_labels": LABELS,
        "hybrid_labels": HYBRID_LABELS if hybrid_model else None
    }
    
    if hybrid_model:
        info.update(hybrid_model.get_model_info())
    
    return jsonify(info)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    print(f"[analysis_service] Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
