#!/bin/bash

# Virtual Therapist Services Test Script
echo "🧪 Testing Virtual Therapist Services..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local url=$1
    local method=${2:-GET}
    local data=$3
    local expected_status=${4:-200}
    
    echo -n "Testing $method $url... "
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$url")
    else
        response=$(curl -s -w "%{http_code}" -X "$method" "$url")
    fi
    
    status_code="${response: -3}"
    body="${response%???}"
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} (Status: $status_code)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (Status: $status_code, Expected: $expected_status)"
        echo "Response: $body"
        return 1
    fi
}

echo ""
echo "🔍 Testing Backend Service (Port 4000)..."
test_endpoint "http://localhost:4000/health" "GET"

echo ""
echo "🔍 Testing Model Service (Port 5001)..."
test_endpoint "http://localhost:5001/health" "GET"

echo ""
echo "🔍 Testing Authentication Endpoints..."
test_endpoint "http://localhost:4000/api/auth/register" "POST" '{"email":"test@example.com","password":"testpassword123"}' "201"
test_endpoint "http://localhost:4000/api/auth/login" "POST" '{"email":"test@example.com","password":"testpassword123"}' "200"

echo ""
echo "🔍 Testing Analysis Endpoints..."
test_endpoint "http://localhost:4000/api/analyze" "POST" '{"text":"I feel anxious about my presentation tomorrow"}' "200"
test_endpoint "http://localhost:5001/predict" "POST" '{"text":"I feel anxious about my presentation tomorrow"}' "200"

echo ""
echo "🔍 Testing Frontend (Port 5173)..."
test_endpoint "http://localhost:5173" "GET"

echo ""
echo "📊 Test Summary:"
echo "If all tests pass, your Virtual Therapist is working correctly!"
echo ""
echo "🌐 Access URLs:"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:4000"
echo "Model Service: http://localhost:5001"
