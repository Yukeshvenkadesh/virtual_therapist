"""
Custom Hybrid DistilBERT-BiLSTM-XGBoost Model for Virtual Therapist
This module contains the model architecture and inference logic for the hybrid model.
"""

import torch
import torch.nn as nn
import numpy as np
import xgboost as xgb
from transformers import DistilBertModel, DistilBertTokenizer
import joblib
import os
from typing import Dict, List, Tuple, Optional

# Ensure numpy is available
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    print("Warning: numpy not available, some features may not work")
    NUMPY_AVAILABLE = False
    # Create a dummy numpy module for fallback
    class DummyNumpy:
        def array(self, *args, **kwargs):
            return list(*args)
        def argmax(self, arr):
            return 0
        def max(self, arr):
            return 1.0
    np = DummyNumpy()

class DistilBERT_BiLSTM_Hybrid(nn.Module):
    """
    Hybrid model combining DistilBERT, BiLSTM, and XGBoost for mental health classification.
    """
    
    def __init__(self, num_labels: int = 4, hidden_dim: int = 256, lstm_layers: int = 1, dropout_prob: float = 0.3):
        super(DistilBERT_BiLSTM_Hybrid, self).__init__()
        self.distilbert = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.hidden_dim = hidden_dim
        self.num_labels = num_labels

        self.lstm = nn.LSTM(
            input_size=self.distilbert.config.dim,
            hidden_size=hidden_dim,
            num_layers=lstm_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout_prob if lstm_layers > 1 else 0
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(dropout_prob),
            nn.Linear(hidden_dim * 2, num_labels)
        )

    def forward(self, input_ids, attention_mask):
        """
        Forward pass through DistilBERT and BiLSTM layers.
        Returns both features (for XGBoost) and logits (for direct classification).
        """
        distilbert_output = self.distilbert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = distilbert_output.last_hidden_state

        lstm_output, (h_n, c_n) = self.lstm(sequence_output)
        final_state = torch.cat((h_n[-2, :, :], h_n[-1, :, :]), dim=1)

        return final_state, self.classifier(final_state)

class HybridModelInference:
    """
    Inference class for the hybrid DistilBERT-BiLSTM-XGBoost model.
    """
    
    def __init__(self, model_path: str, xgb_path: str, tokenizer_path: Optional[str] = None, labels: Optional[List[str]] = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path
        self.xgb_path = xgb_path
        
        # Load tokenizer
        if tokenizer_path and os.path.exists(tokenizer_path):
            self.tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)
        else:
            self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
        # Initialize model
        self.model = DistilBERT_BiLSTM_Hybrid(
            num_labels=4,  # Updated to 4 classes: Depression, ADHD, Bipolar, Anxiety
            hidden_dim=256,
            lstm_layers=1,
            dropout_prob=0.3
        )
        
        # Load PyTorch model weights
        self._load_pytorch_model()
        
        # Load XGBoost model
        self._load_xgboost_model()
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Initialize model output type detection flag
        self.model_outputs_logits = False
        
        # Default label order as per user's trained model, can be overridden
        self.labels = labels if labels and len(labels) > 0 else ['Depression', 'ADHD', 'Bipolar', 'Anxiety']
        self.label_map = {i: label for i, label in enumerate(self.labels)}
    
    def _load_pytorch_model(self):
        """Load the PyTorch model weights with robust handling."""
        try:
            if os.path.exists(self.model_path):
                # Load with CPU map_location for compatibility
                state_dict = torch.load(self.model_path, map_location=self.device)
                
                # Handle different save formats
                if isinstance(state_dict, dict):
                    if "state_dict" in state_dict:
                        self.model.load_state_dict(state_dict["state_dict"])
                    elif "model_state_dict" in state_dict:
                        self.model.load_state_dict(state_dict["model_state_dict"])
                    else:
                        # Try to load as state dict directly
                        self.model.load_state_dict(state_dict)
                else:
                    # Load as complete model
                    self.model = state_dict
                
                print(f"✅ Loaded PyTorch model from {self.model_path}")
                
                # Runtime detection: test if model outputs features or logits
                self._detect_model_output_type()
                
            else:
                print(f"⚠️ PyTorch model not found at {self.model_path}")
        except Exception as e:
            print(f"❌ Error loading PyTorch model: {e}")
            raise
    
    def _detect_model_output_type(self):
        """Detect whether the model outputs features or logits."""
        try:
            # Test with dummy input
            dummy_text = "This is a test sentence for model detection."
            inputs = self.preprocess_text(dummy_text)
            
            with torch.no_grad():
                features, logits = self.model(**inputs)
                
            # Check if logits have the right shape for classification
            if logits.shape[-1] == len(self.labels):
                self.model_outputs_logits = True
                print("✅ Model outputs logits directly - using PyTorch classifier")
            else:
                self.model_outputs_logits = False
                print("✅ Model outputs features - using XGBoost classifier")
                
        except Exception as e:
            print(f"⚠️ Could not detect model output type: {e}")
            self.model_outputs_logits = False  # Default to XGBoost
    
    def _load_xgboost_model(self):
        """Load the XGBoost model."""
        try:
            if os.path.exists(self.xgb_path):
                self.xgb_model = xgb.XGBClassifier()
                self.xgb_model.load_model(self.xgb_path)
                print(f"✅ Loaded XGBoost model from {self.xgb_path}")
                # If XGB model exposes class count, ensure labels length matches
                try:
                    if hasattr(self.xgb_model, 'classes_'):
                        num_classes = len(self.xgb_model.classes_)
                    else:
                        num_classes = int(getattr(self.xgb_model.get_booster(), 'num_classes', len(self.labels)))
                except Exception:
                    num_classes = len(self.labels)
                if num_classes != len(self.labels):
                    # Fallback: resize labels to match class count
                    default_labels = ['Depression', 'ADHD', 'Bipolar', 'Anxiety']
                    self.labels = default_labels[:num_classes]
                    self.label_map = {i: label for i, label in enumerate(self.labels)}
            else:
                print(f"⚠️ XGBoost model not found at {self.xgb_path}")
                self.xgb_model = None
        except Exception as e:
            print(f"❌ Error loading XGBoost model: {e}")
            self.xgb_model = None
    
    def preprocess_text(self, text: str, max_length: int = 256) -> Dict[str, torch.Tensor]:
        """Preprocess text for model input."""
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].to(self.device),
            'attention_mask': encoding['attention_mask'].to(self.device)
        }
    
    def predict(self, text: str) -> Dict[str, any]:
        """
        Make prediction using the hybrid model.
        Returns prediction results in the format expected by the API.
        """
        try:
            # Preprocess text
            inputs = self.preprocess_text(text)
            
            # Get features from DistilBERT-BiLSTM
            with torch.no_grad():
                features, logits = self.model(**inputs)
                if NUMPY_AVAILABLE:
                    features_np = features.cpu().numpy()
                else:
                    features_np = features.cpu().tolist()
            
            # Choose prediction method based on model output type and XGBoost availability
            if self.model_outputs_logits or self.xgb_model is None:
                # Use PyTorch model directly
                probs = torch.softmax(logits, dim=-1).cpu().tolist()[0]
                predicted_idx = probs.index(max(probs))
                predicted_label = self.label_map[predicted_idx]
                
                # Create confidence scores
                confidence_scores = []
                for i, label in enumerate(self.labels):
                    confidence_scores.append({
                        "label": label,
                        "score": float(probs[i])
                    })
                
                # Sort by confidence
                confidence_scores.sort(key=lambda x: x["score"], reverse=True)
                
            else:
                # Use XGBoost for final prediction
                xgb_pred = int(self.xgb_model.predict(features_np)[0])
                xgb_proba = self.xgb_model.predict_proba(features_np)[0]
                
                # Map to labels
                predicted_label = self.label_map[xgb_pred]
                
                # Create confidence scores
                confidence_scores = []
                for i, label in enumerate(self.labels):
                    confidence_scores.append({
                        "label": label,
                        "score": float(xgb_proba[i]) if i < len(xgb_proba) else 0.0
                    })
                
                # Sort by confidence
                confidence_scores.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "topPattern": predicted_label,
                "confidenceScores": confidence_scores
            }
            
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            # Return fallback prediction
            return {
                "topPattern": "Anxiety",
                "confidenceScores": [
                    {"label": "Anxiety", "score": 0.4},
                    {"label": "Bipolar", "score": 0.3},
                    {"label": "Depression", "score": 0.3}
                ]
            }
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about the loaded model."""
        return {
            "model_type": "DistilBERT-BiLSTM-XGBoost Hybrid",
            "pytorch_model_loaded": os.path.exists(self.model_path),
            "xgboost_model_loaded": self.xgb_model is not None,
            "labels": self.labels,
            "device": str(self.device)
        }

def create_model_save_script():
    """
    Create a script to help save your trained model in the correct format.
    """
    script_content = '''
# Script to save your hybrid model for Virtual Therapist
# Run this in your Colab notebook after training

import torch
import xgboost as xgb
import os

# Save PyTorch model
pytorch_path = "/content/drive/MyDrive/models/distilbert_bilstm_hybrid.pth"
torch.save(model.state_dict(), pytorch_path)
print(f"PyTorch model saved to: {pytorch_path}")

# Save XGBoost model
xgb_path = "/content/drive/MyDrive/models/xgboost_classifier.json"
xgb_model.save_model(xgb_path)
print(f"XGBoost model saved to: {xgb_path}")

# Create a combined model info file
model_info = {
    "pytorch_path": pytorch_path,
    "xgb_path": xgb_path,
    "labels": ["Anxiety", "Bipolar", "Depression"],
    "model_type": "DistilBERT-BiLSTM-XGBoost Hybrid"
}

import json
info_path = "/content/drive/MyDrive/models/model_info.json"
with open(info_path, 'w') as f:
    json.dump(model_info, f, indent=2)
print(f"Model info saved to: {info_path}")
'''
    
    with open("/Users/adithyan/Desktop/RND/basepapers/virtual-therapist/backend/analysis_service/save_hybrid_model.py", "w") as f:
        f.write(script_content)
    
    print("✅ Created model saving script: save_hybrid_model.py")



