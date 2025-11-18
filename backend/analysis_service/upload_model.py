#!/usr/bin/env python3
"""
Model Upload Script for Virtual Therapist Analysis Service

This script helps you upload and configure your trained model for the analysis service.
"""

import os
import shutil
import argparse
from pathlib import Path

def upload_pytorch_model(model_file_path, model_name="mental_health_model_final.pth"):
    """Upload a PyTorch model file to the model directory."""
    model_dir = Path(__file__).parent / "model"
    model_dir.mkdir(exist_ok=True)
    
    target_path = model_dir / model_name
    
    if not os.path.exists(model_file_path):
        print(f"❌ Error: Model file not found at {model_file_path}")
        return False
    
    try:
        shutil.copy2(model_file_path, target_path)
        print(f"✅ Successfully uploaded model to {target_path}")
        return True
    except Exception as e:
        print(f"❌ Error uploading model: {e}")
        return False

def upload_huggingface_model(model_dir_path, model_name="custom_model"):
    """Upload a Hugging Face model directory to the model directory."""
    model_dir = Path(__file__).parent / "model"
    model_dir.mkdir(exist_ok=True)
    
    target_path = model_dir / model_name
    
    if not os.path.exists(model_dir_path):
        print(f"❌ Error: Model directory not found at {model_dir_path}")
        return False
    
    try:
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(model_dir_path, target_path)
        print(f"✅ Successfully uploaded Hugging Face model to {target_path}")
        return True
    except Exception as e:
        print(f"❌ Error uploading model: {e}")
        return False

def update_env_file(model_path):
    """Update the .env file with the new model path."""
    env_file = Path(__file__).parent / ".env"
    
    # Read existing .env file
    env_content = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.readlines()
    
    # Update or add MODEL_PATH
    updated = False
    for i, line in enumerate(env_content):
        if line.startswith("MODEL_PATH="):
            env_content[i] = f"MODEL_PATH={model_path}\n"
            updated = True
            break
    
    if not updated:
        env_content.append(f"MODEL_PATH={model_path}\n")
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(env_content)
    
    print(f"✅ Updated .env file with MODEL_PATH={model_path}")

def main():
    parser = argparse.ArgumentParser(description="Upload trained model to Virtual Therapist Analysis Service")
    parser.add_argument("--model-path", required=True, help="Path to your trained model file or directory")
    parser.add_argument("--model-name", default="mental_health_model_final.pth", help="Name for the model file (default: mental_health_model_final.pth)")
    parser.add_argument("--type", choices=["pytorch", "huggingface"], default="pytorch", help="Type of model (default: pytorch)")
    
    args = parser.parse_args()
    
    print("🚀 Virtual Therapist Model Upload Tool")
    print("=" * 50)
    
    if args.type == "pytorch":
        success = upload_pytorch_model(args.model_path, args.model_name)
        if success:
            model_path = os.path.join("model", args.model_name)
            update_env_file(model_path)
    else:  # huggingface
        success = upload_huggingface_model(args.model_path, args.model_name)
        if success:
            model_path = os.path.join("model", args.model_name)
            update_env_file(model_path)
    
    if success:
        print("\n🎉 Model upload completed successfully!")
        print("\nNext steps:")
        print("1. Restart the analysis service: python app.py")
        print("2. Test the model with: curl -X POST http://localhost:5001/predict -H 'Content-Type: application/json' -d '{\"text\": \"I feel anxious today\"}'")
    else:
        print("\n❌ Model upload failed. Please check the error messages above.")

if __name__ == "__main__":
    main()



























