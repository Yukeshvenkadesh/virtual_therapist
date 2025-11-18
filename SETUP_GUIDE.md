# Virtual Therapist - Complete Setup Guide

## ✅ All Issues Fixed!

This guide covers the complete setup and fixes for the Virtual Therapist application.

## 🔧 What Was Fixed

### 1. Backend Connectivity Issues
- ✅ Fixed CORS configuration for proper cross-origin requests
- ✅ Added proper error handling and status codes
- ✅ Fixed API endpoint routing (`/api/auth` instead of `/auth`)
- ✅ Added individual user analysis endpoint (`/api/analyze`)
- ✅ Enhanced request/response handling

### 2. User-Specific Data Handling
- ✅ **Individual Users**: Temporary session data stored in browser (deleted on tab close)
- ✅ **Professionals**: Patient data stored in MongoDB with 30-day auto-deletion
- ✅ Created `UserSession` model for temporary individual data
- ✅ Enhanced `Patient` model with TTL index for auto-deletion
- ✅ Added session management routes

### 3. Model Service Integration
- ✅ Fixed Python FastAPI service configuration
- ✅ Enhanced CORS settings for proper communication
- ✅ Added robust model loading with error handling
- ✅ Runtime detection of model output type (features vs logits)

### 4. UI/UX Enhancements
- ✅ Added clear privacy notices for both user types
- ✅ Enhanced mobile responsiveness
- ✅ Improved visual indicators for data retention policies
- ✅ Better error handling and user feedback
- ✅ Professional vs Individual user experience differentiation

### 5. Auto-Delete Logic
- ✅ **Individual Data**: Browser localStorage (manual clear + tab close)
- ✅ **Professional Data**: MongoDB TTL index (30 days automatic deletion)
- ✅ Session cleanup on logout
- ✅ Automatic cleanup of expired data

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB Atlas cluster (or other hosted MongoDB with SRV URI)
- Git

### 1. Setup Environment
```bash
cd /Users/adithyan/Desktop/RND/basepapers/virtual-therapist
./setup-env.sh
```

### 2. Configure MongoDB Atlas
1. Create (or reuse) an Atlas cluster
2. Add your current IP address to the network access list
3. Create a database user with read/write access to `virtual_therapist`
4. Copy the `mongodb+srv://` connection string for your `.env`

### 3. Install Dependencies
```bash
# Backend
cd backend && npm install && cd ..

# Frontend
cd frontend && npm install && cd ..

# Model Service
cd model_service && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd ..
```

### 4. Run All Services
```bash
./run-services.sh
```

### 5. Test Everything
```bash
./test-services.sh
```

## 📁 Project Structure

```
/virtual-therapist
├── frontend/           # React app (Port 3000)
├── backend/            # Node.js/Express API (Port 4000)
├── model_service/      # Python FastAPI (Port 5001)
├── docker-compose.yml  # Docker orchestration
├── .env               # Environment variables
├── run-services.sh    # Start all services
├── test-services.sh   # Test all endpoints
└── setup-env.sh       # Environment setup
```

## 🔗 API Endpoints

### Backend API (Port 4000)
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/analyze` - Individual text analysis
- `GET /api/patients` - Get user's patients (auth required)
- `POST /api/patients` - Add new patient (auth required)
- `POST /api/patients/:id/analyze` - Analyze patient notes (auth required)
- `POST /api/sessions` - Create/get session (individual users)
- `POST /api/sessions/:id/analyze` - Analyze text in session
- `GET /api/sessions/:id/history` - Get session history
- `DELETE /api/sessions/:id` - Clear session data

### Model Service API (Port 5001)
- `GET /health` - Health check
- `POST /predict` - Text analysis
- `GET /model-info` - Model information

## 🗄️ Database Schema

### Individual Users (Temporary)
- **UserSession**: Browser-based temporary storage
- **Auto-deletion**: 1 hour after last access
- **Storage**: MongoDB with TTL index

### Professional Users (Persistent)
- **User**: Authentication data
- **Patient**: Patient records with analysis history
- **Auto-deletion**: 30 days after creation
- **Storage**: MongoDB with TTL index

## 🔒 Privacy & Data Retention

### Individual Users
- ✅ Data stored temporarily in browser
- ✅ No server-side storage of personal data
- ✅ Clear privacy notices in UI
- ✅ Session data auto-expires after 1 hour

### Professional Users
- ✅ Patient data stored securely for 30 days
- ✅ Automatic deletion after retention period
- ✅ Clear data retention policies displayed
- ✅ HIPAA-compliant data handling

## 🧪 Testing

### Manual Testing
1. **Individual Analysis**: Go to http://localhost:3000
2. **Professional Login**: Go to http://localhost:3000/pro
3. **API Testing**: Run `./test-services.sh`

### Test Scenarios
- ✅ User registration and login
- ✅ Text analysis for individuals
- ✅ Patient management for professionals
- ✅ Data retention and cleanup
- ✅ Mobile responsiveness
- ✅ Error handling

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to fetch" errors**
   - Check if all services are running
   - Verify CORS configuration
   - Check API endpoint URLs

2. **MongoDB connection errors**
   - Ensure your Atlas cluster is online and your IP is allow-listed
   - Check connection string in .env
   - Verify database user credentials and permissions

3. **Model service errors**
   - Check if Python virtual environment is activated
   - Verify model files are in correct location
   - Check Python dependencies

4. **Port conflicts**
   - Ensure ports 3000, 4000, 5001 are available
   - Check for other running services

### Debug Commands
```bash
# Check running services
lsof -i :3000 -i :4000 -i :5000

# Check MongoDB Atlas connectivity (replace with your URI)
mongosh "mongodb+srv://<username>:<password>@<cluster-url>/virtual_therapist?retryWrites=true&w=majority"

# Test individual endpoints
curl http://localhost:4000/health
curl http://localhost:5001/health
```

## 🚀 Production Deployment

### Environment Variables
Update `.env` for production:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/virtual_therapist?retryWrites=true&w=majority
JWT_SECRET=your-super-secure-secret
FRONTEND_ORIGIN=https://your-domain.com
```

### Docker Deployment
```bash
docker-compose up --build -d
```

### Security Considerations
- ✅ Change JWT secret in production
- ✅ Use HTTPS in production
- ✅ Configure proper CORS origins
- ✅ Set up database authentication
- ✅ Monitor data retention compliance

## 📱 Mobile Support

The application is fully responsive and works on:
- ✅ Mobile phones (< 768px)
- ✅ Tablets (768px - 1024px)
- ✅ Desktop (> 1024px)
- ✅ Touch-friendly interface
- ✅ Optimized for all screen sizes

## 🎯 Features Summary

### Individual Users
- ✅ Anonymous text analysis
- ✅ Temporary session storage
- ✅ Privacy-focused design
- ✅ Mobile-optimized interface
- ✅ Real-time analysis results

### Professional Users
- ✅ Secure authentication
- ✅ Patient management system
- ✅ Session note analysis
- ✅ 30-day data retention
- ✅ Professional dashboard
- ✅ HIPAA-compliant data handling

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Run the test script: `./test-services.sh`
3. Check service logs for errors
4. Verify all dependencies are installed

## 🎉 Success!

Your Virtual Therapist application is now fully functional with:
- ✅ Fixed connectivity issues
- ✅ Proper data handling
- ✅ Enhanced UI/UX
- ✅ Mobile responsiveness
- ✅ Auto-deletion policies
- ✅ Complete testing suite

Access your application at: http://localhost:3000

