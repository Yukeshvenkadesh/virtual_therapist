# 🤖 Model Integration Guide for Virtual Therapist

This guide will help you integrate your trained mental health analysis model into the Virtual Therapist system.

## 📁 Where to Place Your Model

Your trained model should be placed in:
```
backend/analysis_service/model/
```

## 🔧 Supported Model Formats

### 1. PyTorch Model (.pth file)
- **File name**: `mental_health_model_final.pth` (or any name you prefer)
- **Location**: `backend/analysis_service/model/mental_health_model_final.pth`

### 2. Hugging Face Model Directory
- **Directory name**: Any name (e.g., `custom_model`)
- **Location**: `backend/analysis_service/model/custom_model/`
- **Required files**: `config.json`, `pytorch_model.bin`, `tokenizer.json`, etc.

## 🚀 Step-by-Step Integration Process

### Step 1: Prepare Your Model

#### For PyTorch Models:
```python
# Save your model using one of these methods:

# Method 1: Save complete model
torch.save(model, 'mental_health_model_final.pth')

# Method 2: Save state dict
torch.save({
    'state_dict': model.state_dict(),
    'labels': ['Anxiety', 'Depression', 'Stress', 'Neutral']
}, 'mental_health_model_final.pth')

# Method 3: Save with custom key
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch
}, 'mental_health_model_final.pth')
```

#### For Hugging Face Models:
```python
# Save your model using Hugging Face format
model.save_pretrained('./my_custom_model')
tokenizer.save_pretrained('./my_custom_model')
```

### Step 2: Upload Your Model

#### Option A: Using the Upload Script (Recommended)
```bash
cd backend/analysis_service

# For PyTorch model
python upload_model.py --model-path /path/to/your/model.pth --type pytorch

# For Hugging Face model
python upload_model.py --model-path /path/to/your/model/directory --type huggingface --model-name custom_model
```

#### Option B: Manual Upload
```bash
# Copy your model file/directory to the model folder
cp /path/to/your/model.pth backend/analysis_service/model/
# or
cp -r /path/to/your/model/directory backend/analysis_service/model/custom_model/
```

### Step 3: Configure Environment Variables

Update your `.env` file in `backend/analysis_service/`:

```env
# For PyTorch model file
MODEL_PATH=./model/mental_health_model_final.pth

# For Hugging Face model directory
MODEL_PATH=./model/custom_model

# Other settings
FRONTEND_ORIGIN=http://localhost:3000
PORT=5001
```

### Step 4: Test Your Model

```bash
cd backend/analysis_service
python test_model.py
```

## 🔄 Complete System Setup and Run

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB
- Your trained model

### 1. Install Dependencies

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

### 2. Configure MongoDB Atlas
- Create (or reuse) an Atlas cluster
- Add your current IP address (or 0.0.0.0/0 for testing only)
- Create an application user with read/write access to the target database
- Copy the `mongodb+srv://` connection string for use in `.env`

### 3. Configure Environment Variables

Create `.env` files:

**backend/auth_service/.env:**
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/virtual_therapist?retryWrites=true&w=majority
MONGODB_DB=virtual_therapist
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
FRONTEND_ORIGIN=http://localhost:3000
ANALYSIS_SERVICE_URL=http://localhost:5001/predict
PORT=4000
```

**backend/analysis_service/.env:**
```env
FRONTEND_ORIGIN=http://localhost:3000
PORT=5001
MODEL_PATH=./model/mental_health_model_final.pth
```

### 4. Start All Services

Open 4 separate terminals:

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

**Terminal 3 - Frontend (Vite):**
```bash
cd frontend
npm run dev
```

**Terminal 4 - Next.js App (Optional):**
```bash
npm run dev
```

### 5. Access the Application

- **Frontend (Vite)**: http://localhost:5173
- **Next.js App**: http://localhost:3000
- **Auth Service**: http://localhost:4000
- **Analysis Service**: http://localhost:5001

## 🧪 Testing Your Integration

### Test Analysis Service
```bash
cd backend/analysis_service
python test_model.py
```

### Test with cURL
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel anxious about my presentation tomorrow"}'
```

### Test Frontend
1. Go to http://localhost:5173
2. Enter some text in the text area
3. Click "Analyze Text"
4. Check the results

## 🔍 Troubleshooting

### Common Issues:

1. **Model not loading:**
   - Check MODEL_PATH in .env file
   - Verify model file exists
   - Check console logs for error messages

2. **Import errors:**
   - Ensure all Python dependencies are installed
   - Check Python version compatibility

3. **Connection errors:**
   - Verify all services are running
   - Check port availability
   - Confirm your Atlas cluster is reachable and the IP is allow-listed

4. **Prediction errors:**
   - Test model with simple text first
   - Check model output format
   - Verify labels match expected format

### Debug Commands:
```bash
# Check if services are running
curl http://localhost:4000/health
curl http://localhost:5001/health

# Check MongoDB Atlas connectivity (replace with your URI)
mongosh "mongodb+srv://<username>:<password>@<cluster-url>/virtual_therapist?retryWrites=true&w=majority"

# View analysis service logs
cd backend/analysis_service && python app.py
```

## 📊 Expected Model Output Format

Your model should output predictions in this format:
```json
{
  "topPattern": "Anxiety",
  "confidenceScores": [
    {"label": "Anxiety", "score": 0.75},
    {"label": "Stress", "score": 0.15},
    {"label": "Depression", "score": 0.05},
    {"label": "Neutral", "score": 0.05}
  ]
}
```

## 🎯 Model Requirements

Your model should:
- Accept text input
- Output 4 classes: ["Anxiety", "Depression", "Stress", "Neutral"]
- Return probability scores for each class
- Be compatible with DistilBERT tokenizer (or provide custom tokenizer)

## 🚀 Quick Start Script

Use the automated setup script:
```bash
./start-dev.sh
```

This will:
- Verify that your `.env` file (with Atlas credentials) already exists
- Install all dependencies
- Launch backend, model service, and frontend together
- Provide instructions for stopping the stack cleanly

## 📞 Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all services are running on the correct ports
4. Test each service individually using the health endpoints



























