#!/usr/bin/env python3
"""
Script to save your hybrid DistilBERT-BiLSTM-XGBoost model for Virtual Therapist
Run this in your Colab notebook after training your model.
"""

import torch
import xgboost as xgb
import os
import json

def save_hybrid_model(model, xgb_model, save_path="/content/drive/MyDrive/models/"):
    """
    Save your trained hybrid model in the format required by Virtual Therapist.
    
    Args:
        model: Your trained DistilBERT_BiLSTM_Hybrid model
        xgb_model: Your trained XGBoost model
        save_path: Path to save the models
    """
    
    # Create save directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # Save PyTorch model
    pytorch_path = os.path.join(save_path, "distilbert_bilstm_hybrid.pth")
    torch.save(model.state_dict(), pytorch_path)
    print(f"✅ PyTorch model saved to: {pytorch_path}")
    
    # Save XGBoost model
    xgb_path = os.path.join(save_path, "xgboost_classifier.json")
    xgb_model.save_model(xgb_path)
    print(f"✅ XGBoost model saved to: {xgb_path}")
    
    # Create model info file
    model_info = {
        "pytorch_path": pytorch_path,
        "xgb_path": xgb_path,
        "labels": ["Anxiety", "Bipolar", "Depression"],
        "model_type": "DistilBERT-BiLSTM-XGBoost Hybrid",
        "num_labels": 3,
        "hidden_dim": 256,
        "lstm_layers": 1,
        "dropout_prob": 0.3
    }
    
    info_path = os.path.join(save_path, "model_info.json")
    with open(info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"✅ Model info saved to: {info_path}")
    
    return pytorch_path, xgb_path, info_path

# Example usage in your Colab notebook:
"""
# After training your model, run this:

# Save the models
pytorch_path, xgb_path, info_path = save_hybrid_model(model, xgb_model)

# Download the files to your local machine
from google.colab import files

# Download PyTorch model
files.download(pytorch_path)

# Download XGBoost model  
files.download(xgb_path)

# Download model info
files.download(info_path)

print("🎉 All model files have been saved and are ready for download!")
"""



























