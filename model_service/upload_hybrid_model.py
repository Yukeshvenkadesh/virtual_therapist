#!/usr/bin/env python3
"""
Hybrid Model Upload Script for Virtual Therapist Analysis Service

This script helps you upload your trained hybrid DistilBERT-BiLSTM-XGBoost model.
"""

import os
import shutil
import argparse
from pathlib import Path

def upload_hybrid_model(pytorch_path, xgb_path, model_name="hybrid_model"):
    """Upload hybrid model files to the model directory."""
    model_dir = Path(__file__).parent / "model"
    model_dir.mkdir(exist_ok=True)
    
    pytorch_target = model_dir / "distilbert_bilstm_hybrid.pth"
    xgb_target = model_dir / "xgboost_classifier.json"
    
    success = True
    
    # Upload PyTorch model
    if not os.path.exists(pytorch_path):
        print(f"❌ Error: PyTorch model file not found at {pytorch_path}")
        success = False
    else:
        try:
            shutil.copy2(pytorch_path, pytorch_target)
            print(f"✅ Successfully uploaded PyTorch model to {pytorch_target}")
        except Exception as e:
            print(f"❌ Error uploading PyTorch model: {e}")
            success = False
    
    # Upload XGBoost model
    if not os.path.exists(xgb_path):
        print(f"❌ Error: XGBoost model file not found at {xgb_path}")
        success = False
    else:
        try:
            shutil.copy2(xgb_path, xgb_target)
            print(f"✅ Successfully uploaded XGBoost model to {xgb_target}")
        except Exception as e:
            print(f"❌ Error uploading XGBoost model: {e}")
            success = False
    
    return success

def update_env_file():
    """Update the .env file with hybrid model paths."""
    env_file = Path(__file__).parent / ".env"
    
    # Read existing .env file
    env_content = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.readlines()
    
    # Update or add hybrid model paths
    updates = {
        "HYBRID_PYTORCH_PATH": "./model/distilbert_bilstm_hybrid.pth",
        "HYBRID_XGB_PATH": "./model/xgboost_classifier.json"
    }
    
    for key, value in updates.items():
        updated = False
        for i, line in enumerate(env_content):
            if line.startswith(f"{key}="):
                env_content[i] = f"{key}={value}\n"
                updated = True
                break
        
        if not updated:
            env_content.append(f"{key}={value}\n")
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(env_content)
    
    print(f"✅ Updated .env file with hybrid model paths")

def main():
    parser = argparse.ArgumentParser(description="Upload hybrid model to Virtual Therapist Analysis Service")
    parser.add_argument("--pytorch-path", required=True, help="Path to your PyTorch model file (.pth)")
    parser.add_argument("--xgb-path", required=True, help="Path to your XGBoost model file (.json)")
    
    args = parser.parse_args()
    
    print("🚀 Virtual Therapist Hybrid Model Upload Tool")
    print("=" * 60)
    
    success = upload_hybrid_model(args.pytorch_path, args.xgb_path)
    
    if success:
        update_env_file()
        print("\n🎉 Hybrid model upload completed successfully!")
        print("\nNext steps:")
        print("1. Restart the analysis service: python app.py")
        print("2. Test the model with: python test_model.py")
        print("3. Check model info: curl http://localhost:5001/model-info")
    else:
        print("\n❌ Hybrid model upload failed. Please check the error messages above.")

if __name__ == "__main__":
    main()



