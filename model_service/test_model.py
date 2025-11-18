#!/usr/bin/env python3
"""
Model Testing Script for Virtual Therapist Analysis Service

This script tests your trained model to ensure it's working correctly.
"""

import requests
import json
import time
import sys

def test_analysis_service(base_url="http://localhost:5001"):
    """Test the analysis service with sample texts."""
    
    test_cases = [
        {
            "text": "I feel really anxious about my upcoming presentation. My heart is racing and I can't stop worrying.",
            "expected": "Anxiety"
        },
        {
            "text": "I've been feeling really down lately. Nothing seems to bring me joy anymore and I feel hopeless.",
            "expected": "Depression"
        },
        {
            "text": "I'm so overwhelmed with work. The deadlines are piling up and I feel stressed all the time.",
            "expected": "Stress"
        },
        {
            "text": "Today was a normal day. I went to work, had lunch with a friend, and watched a movie.",
            "expected": "Neutral"
        }
    ]
    
    print("🧪 Testing Analysis Service")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to analysis service: {e}")
        print("Make sure the analysis service is running on port 5001")
        return False
    
    # Test prediction endpoint
    print("\n🔍 Testing predictions:")
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/predict",
                json={"text": test_case["text"]},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                predicted = result.get("topPattern", "Unknown")
                confidence = result.get("confidenceScores", [])
                
                # Find confidence for predicted label
                pred_confidence = 0
                for score in confidence:
                    if score["label"] == predicted:
                        pred_confidence = score["score"]
                        break
                
                status = "✅" if predicted == test_case["expected"] else "⚠️"
                print(f"{status} Test {i}: Predicted '{predicted}' (expected '{test_case['expected']}') - Confidence: {pred_confidence:.2%}")
                
                if predicted != test_case["expected"]:
                    all_passed = False
                    
            else:
                print(f"❌ Test {i} failed: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test {i} failed: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your model is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the results above.")
    
    return all_passed

def test_custom_text():
    """Allow user to test with custom text."""
    print("\n📝 Custom Text Testing")
    print("Enter your own text to test (or 'quit' to exit):")
    
    while True:
        text = input("\nText: ").strip()
        if text.lower() in ['quit', 'exit', 'q']:
            break
        
        if len(text) < 5:
            print("Text must be at least 5 characters long.")
            continue
        
        try:
            response = requests.post(
                "http://localhost:5001/predict",
                json={"text": text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                predicted = result.get("topPattern", "Unknown")
                confidence = result.get("confidenceScores", [])
                
                print(f"\n🎯 Prediction: {predicted}")
                print("📊 Confidence Scores:")
                for score in confidence:
                    print(f"   {score['label']}: {score['score']:.2%}")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")

def main():
    print("🚀 Virtual Therapist Model Testing Tool")
    print("=" * 50)
    
    # Test the service
    if test_analysis_service():
        # Ask if user wants to test custom text
        response = input("\nWould you like to test with custom text? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            test_custom_text()
    
    print("\n👋 Testing complete!")

if __name__ == "__main__":
    main()



