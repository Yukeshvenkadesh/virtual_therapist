# 🤖 Hybrid Model Integration Guide

This guide will help you integrate your trained DistilBERT-BiLSTM-XGBoost hybrid model into the Virtual Therapist system.

## 📋 Prerequisites

- Your trained model from the Jupyter notebook
- Python 3.8+
- All required dependencies installed

## 🚀 Step-by-Step Integration

### Step 1: Save Your Model from Colab

In your Colab notebook, after training, run this code to save your model:

```python
# Save your hybrid model
import torch
import xgboost as xgb
import os
import json

def save_hybrid_model(model, xgb_model, save_path="/content/drive/MyDrive/models/"):
    # Create save directory
    os.makedirs(save_path, exist_ok=True)
    
    # Save PyTorch model
    pytorch_path = os.path.join(save_path, "distilbert_bilstm_hybrid.pth")
    torch.save(model.state_dict(), pytorch_path)
    print(f"✅ PyTorch model saved to: {pytorch_path}")
    
    # Save XGBoost model
    xgb_path = os.path.join(save_path, "xgboost_classifier.json")
    xgb_model.save_model(xgb_path)
    print(f"✅ XGBoost model saved to: {xgb_path}")
    
    return pytorch_path, xgb_path

# Save your models
pytorch_path, xgb_path = save_hybrid_model(model, xgb_model)

# Download files to your local machine
from google.colab import files
files.download(pytorch_path)
files.download(xgb_path)
```

### Step 2: Install Dependencies

```bash
cd backend/analysis_service
pip install -r requirements.txt
```

### Step 3: Upload Your Model

```bash
# Upload your hybrid model files
python upload_hybrid_model.py --pytorch-path /path/to/distilbert_bilstm_hybrid.pth --xgb-path /path/to/xgboost_classifier.json
```

### Step 4: Configure Environment

Create a `.env` file in `backend/analysis_service/`:

```env
FRONTEND_ORIGIN=http://localhost:3000
PORT=5001
HYBRID_PYTORCH_PATH=./model/distilbert_bilstm_hybrid.pth
HYBRID_XGB_PATH=./model/xgboost_classifier.json
```

### Step 5: Test Your Model

```bash
# Test the hybrid model
python test_model.py
```

### Step 6: Start the Analysis Service

```bash
python app.py
```

## 🔧 Model Architecture Details

Your hybrid model consists of:

1. **DistilBERT**: Pre-trained transformer for text encoding
2. **BiLSTM**: Bidirectional LSTM for sequence modeling
3. **XGBoost**: Gradient boosting for final classification

### Model Labels
- **Anxiety**: Anxiety-related mental health patterns
- **Bipolar**: Bipolar disorder patterns  
- **Depression**: Depression-related patterns

## 🧪 Testing Your Integration

### Test with cURL
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel really anxious about my presentation tomorrow"}'
```

### Test with Python
```python
import requests

response = requests.post(
    "http://localhost:5001/predict",
    json={"text": "I feel really anxious about my presentation tomorrow"}
)

print(response.json())
```

### Check Model Info
```bash
curl http://localhost:5001/model-info
```

## 🔍 Troubleshooting

### Common Issues:

1. **Model not loading:**
   - Check file paths in .env
   - Verify model files exist
   - Check console logs for errors

2. **Import errors:**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Prediction errors:**
   - Test with simple text first
   - Check model output format
   - Verify labels match expected format

### Debug Commands:
```bash
# Check if service is running
curl http://localhost:5001/health

# Check model info
curl http://localhost:5001/model-info

# View service logs
python app.py
```

## 📊 Expected Output Format

Your hybrid model should return:

```json
{
  "topPattern": "Anxiety",
  "confidenceScores": [
    {"label": "Anxiety", "score": 0.75},
    {"label": "Bipolar", "score": 0.15},
    {"label": "Depression", "score": 0.10}
  ]
}
```

## 🎯 Complete System Setup

### 1. Install All Dependencies
```bash
# Root dependencies
npm install

# Frontend dependencies
cd frontend && npm install && cd ..

# Auth service dependencies
cd backend/auth_service && npm install && cd ../..

# Analysis service dependencies
cd backend/analysis_service && pip install -r requirements.txt && cd ../..
```

### 2. Start MongoDB
```bash
brew services start mongodb-community  # macOS
# or
sudo systemctl start mongod            # Linux
```

### 3. Start All Services

**Terminal 1 - Auth Service:**
```bash
cd backend/auth_service
npm run dev
```

**Terminal 2 - Analysis Service:**
```bash
cd backend/analysis_service
python app.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Analysis Service**: http://localhost:5001

## 🎉 Success Indicators

You'll know your hybrid model is working when:

1. ✅ Analysis service starts without errors
2. ✅ Model info shows hybrid model loaded
3. ✅ Predictions return your model's labels (Anxiety, Bipolar, Depression)
4. ✅ Frontend can analyze text and show results
5. ✅ Confidence scores are reasonable

## 📞 Support

If you encounter issues:

1. Check the console logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all services are running on the correct ports
4. Test each service individually using the health endpoints
5. Verify your model files are in the correct format

Your hybrid model is now ready to power the Virtual Therapist system! 🚀



























