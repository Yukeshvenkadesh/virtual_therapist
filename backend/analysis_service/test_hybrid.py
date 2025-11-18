#!/usr/bin/env python3
"""
Test script to debug hybrid model loading issues.
"""

import os
import sys
import torch
from transformers import DistilBertModel, DistilBertTokenizer

def test_distilbert_loading():
    """Test DistilBERT model loading separately."""
    print("Testing DistilBERT model loading...")
    try:
        model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        print("✅ DistilBERT model and tokenizer loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading DistilBERT: {e}")
        return False

def test_model_loading():
    """Test loading the saved model weights."""
    print("Testing model weights loading...")
    try:
        model_path = "model/mental_health_model.pth"
        if not os.path.exists(model_path):
            print(f"❌ Model file not found: {model_path}")
            return False
        
        state_dict = torch.load(model_path, map_location='cpu')
        print(f"✅ Model weights loaded successfully")
        print(f"Number of keys: {len(state_dict.keys())}")
        print(f"First few keys: {list(state_dict.keys())[:5]}")
        return True
    except Exception as e:
        print(f"❌ Error loading model weights: {e}")
        return False

def test_xgboost_loading():
    """Test XGBoost model loading."""
    print("Testing XGBoost model loading...")
    try:
        import xgboost as xgb
        xgb_path = "model/xgboost_classifier.json"
        if not os.path.exists(xgb_path):
            print(f"❌ XGBoost file not found: {xgb_path}")
            return False
        
        model = xgb.XGBClassifier()
        model.load_model(xgb_path)
        print("✅ XGBoost model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading XGBoost model: {e}")
        return False

def test_hybrid_model_step_by_step():
    """Test hybrid model loading step by step."""
    print("Testing hybrid model step by step...")
    
    # Test DistilBERT
    if not test_distilbert_loading():
        return False
    
    # Test model weights
    if not test_model_loading():
        return False
    
    # Test XGBoost
    if not test_xgboost_loading():
        return False
    
    # Test hybrid model class
    try:
        from hybrid_model import DistilBERT_BiLSTM_Hybrid
        print("Testing hybrid model class initialization...")
        
        model = DistilBERT_BiLSTM_Hybrid(
            num_labels=3,
            hidden_dim=256,
            lstm_layers=1,
            dropout_prob=0.3
        )
        print("✅ Hybrid model class initialized successfully")
        
        # Test loading weights
        model_path = "model/mental_health_model.pth"
        state_dict = torch.load(model_path, map_location='cpu')
        model.load_state_dict(state_dict)
        print("✅ Hybrid model weights loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error with hybrid model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Hybrid Model Debug Test ===")
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Current directory: {os.getcwd()}")
    print()
    
    success = test_hybrid_model_step_by_step()
    
    if success:
        print("\n✅ All tests passed! Hybrid model should work.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
