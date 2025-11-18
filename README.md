# Virtual Therapist

A comprehensive mental health analysis platform that uses AI to analyze text and provide insights into mental health patterns. The system consists of a React frontend, Node.js/Express backend, and Python FastAPI model service.

## Project Structure

```
/virtual-therapist
  /frontend        (React app with Vite)
  /backend         (Node/Express API)
  /model_service   (Python FastAPI)
  docker-compose.yml
  .env.example     (Environment variables template)
```

## Features

- **Individual Analysis**: Users can input their thoughts and get AI-powered mental health pattern analysis
- **Professional Dashboard**: Psychologists can manage patients and analyze session notes
- **Hybrid AI Model**: Combines DistilBERT, BiLSTM, and XGBoost for accurate predictions
- **Mobile Responsive**: Optimized for all device sizes
- **Real-time Analysis**: Fast API responses with confidence scoring
- **History Tracking**: Local storage for individual users and patient management for professionals

## Tech Stack

### Frontend
- React 18 with Vite
- React Router for navigation
- Custom CSS with mobile-first responsive design
- Local storage for history management

### Backend
- Node.js with Express
- MongoDB with Mongoose
- JWT authentication
- CORS enabled for cross-origin requests

### Model Service
- Python FastAPI
- PyTorch for neural networks
- Transformers (DistilBERT)
- XGBoost for classification
- Hybrid model architecture

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB Atlas cluster (or any hosted MongoDB with SRV URI)
- Docker (optional)

### Environment Setup

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Update the `.env` file with your configuration:
```env
# Database
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/virtual_therapist?retryWrites=true&w=majority
MONGODB_DB=virtual_therapist

# JWT Secret (change in production)
JWT_SECRET=your_super_secret_jwt_key_here_change_in_production

# API URLs
AUTH_API_URL=http://localhost:4000/api
ANALYSIS_API_URL=http://localhost:5001

# Frontend URLs
FRONTEND_ORIGIN=http://localhost:3000

# Model Service
HYBRID_PYTORCH_PATH=./model_service/model/hybrid_model.pth
HYBRID_XGB_PATH=./model_service/model/xgboost_classifier.json
```

### Manual Setup

#### 1. Backend Setup
```bash
cd backend
npm install
npm start
```

#### 2. Model Service Setup
```bash
cd model_service
pip install -r requirements.txt
python app.py
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup

```bash
# Ensure .env (with your Atlas URI) exists in the project root

# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

## Model Integration

The system uses a hybrid model architecture:

1. **DistilBERT**: For text understanding and feature extraction
2. **BiLSTM**: For sequence modeling
3. **XGBoost**: For final classification

### Model Files Required

Place these files in `model_service/model/`:
- `hybrid_model.pth` - PyTorch model weights
- `xgboost_classifier.json` - XGBoost classifier (optional)

### Model Detection

The system automatically detects whether to use:
- PyTorch classifier directly (if model outputs logits)
- XGBoost classifier (if model outputs features)

## API Endpoints

### Model Service (Port 5001)
- `GET /health` - Health check
- `POST /predict` - Text analysis
- `GET /model-info` - Model information

### Backend API (Port 4000)
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/patients` - Get patients
- `POST /api/patients` - Add patient
- `POST /api/patients/:id/analyze` - Analyze patient notes

## Mobile Responsiveness

The application is fully responsive with:
- Mobile-first CSS design
- Flexible grid layouts
- Touch-friendly buttons
- Optimized text sizing
- Responsive navigation

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Development

### Running in Development Mode

1. Ensure your MongoDB Atlas cluster allows connections from your current IP
2. Start backend: `cd backend && npm run dev`
3. Start model service: `cd model_service && python app.py`
4. Start frontend: `cd frontend && npm run dev`

### Testing the Model Service

```bash
curl -X POST "http://localhost:5001/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel anxious about my upcoming presentation"}'
```

## Production Deployment

1. Set production environment variables
2. Use Docker Compose for orchestration
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Configure MongoDB with authentication

## Security Considerations

- JWT tokens for authentication
- CORS configuration
- Input validation
- Model files excluded from version control
- Environment variables for sensitive data

## Troubleshooting

### Common Issues

1. **Model not loading**: Check file paths and model file existence
2. **CORS errors**: Verify FRONTEND_ORIGIN configuration
3. **Database connection**: Check MongoDB URI and connectivity
4. **Port conflicts**: Ensure ports 3000, 4000, 5001 are available

### Logs

- Backend: Console output
- Model Service: Console output with detailed model loading info
- Frontend: Browser console

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.