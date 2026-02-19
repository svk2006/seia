#!/usr/bin/env python3
"""Test script for B2G Crop Stress Advisory System"""

import requests
import json
from datetime import datetime

API_BASE = 'http://localhost:5000/api'

# Test cases: (crop, location, observations, conditions)
TEST_CASES = [
    {
        'name': 'Test 1: Rice with Yellowing (Delhi - Hot)',
        'crop_type': 'rice',
        'growth_stage': 'flowering',
        'observations': 'Yellow leaves, reduced growth',
        'latitude': 28.7041,
        'longitude': 77.1025,
        'temperature': 32,
        'humidity': 60,
        'rainfall': 5,
    },
    {
        'name': 'Test 2: Tomato with Wilting (Bangalore - Moderate)',
        'crop_type': 'tomato',
        'growth_stage': 'fruiting',
        'observations': 'Wilting leaves, dry soil, browning edges',
        'latitude': 12.9716,
        'longitude': 77.5946,
        'temperature': 28,
        'humidity': 55,
        'rainfall': 0,
    },
    {
        'name': 'Test 3: Wheat Healthy (Punjab - Optimal)',
        'crop_type': 'wheat',
        'growth_stage': 'grain_fill',
        'observations': 'Normal growth, no visible symptoms',
        'latitude': 31.5204,
        'longitude': 74.3587,
        'temperature': 22,
        'humidity': 65,
        'rainfall': 8,
    },
    {
        'name': 'Test 4: Cotton with Pests (Mumbai - High Humidity)',
        'crop_type': 'cotton',
        'growth_stage': 'boll_formation',
        'observations': 'Leaf spots, insect damage, pest infestation',
        'latitude': 19.0760,
        'longitude': 72.8777,
        'temperature': 30,
        'humidity': 75,
        'rainfall': 15,
    },
    {
        'name': 'Test 5: Sugarcane with Disease (Kolkata - High Humidity)',
        'crop_type': 'sugarcane',
        'growth_stage': 'vegetative',
        'observations': 'Rust spots, leaf disease, yellowing',
        'latitude': 22.5726,
        'longitude': 88.3639,
        'temperature': 26,
        'humidity': 80,
        'rainfall': 20,
    },
]

def run_tests():
    """Run all test cases and report results"""
    print("="*80)
    print("B2G CROP STRESS ADVISORY SYSTEM - TEST SUITE")
    print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print()
    
    results = []
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'='*80}")
        print(f"{test['name']}")
        print(f"{'='*80}")
        
        try:
            # Submit report
            resp = requests.post(f'{API_BASE}/reports', json=test, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            # Extract key metrics
            stress_level = data.get('stress_level', 'N/A')
            confidence = data.get('confidence', 0)
            symptoms = data.get('symptom_analysis', [])
            assessment = data.get('combined_assessment', 'N/A')
            recommendation = data.get('ml_based_recommendation', 'N/A')
            ollama_analysis = data.get('ai_detailed_analysis', 'N/A')
            
            # Print results
            print(f"\n📊 Prediction Results:")
            print(f"   Stress Level: {stress_level} (0=Healthy, 1=Mild, 2=Severe)")
            print(f"   Confidence: {confidence*100:.1f}%")
            print(f"   Detected Symptoms: {len(symptoms)}")
            
            if symptoms:
                print(f"\n🔍 Symptom Analysis:")
                for sys in symptoms:
                    print(f"   • {sys['symptom'].replace('_', ' ').title()}")
                    print(f"     Cause: {sys['cause'][:60]}...")
                    print(f"     Urgent: {'🚨 YES' if sys['is_urgent'] else '✓ No'}")
            
            print(f"\n📋 Assessment:")
            print(f"   {assessment[:100]}...")
            
            print(f"\n🌾 ML Recommendation:")
            print(f"   {recommendation[:100]}...")
            
            if ollama_analysis and ollama_analysis != 'N/A':
                print(f"\n🤖 AI (Ollama) Analysis:")
                print(f"   {ollama_analysis[:100]}...")
            
            # Store result
            results.append({
                'test': test['name'],
                'status': '✓ PASS',
                'stress_level': stress_level,
                'confidence': f"{confidence*100:.1f}%",
                'symptoms_detected': len(symptoms),
            })
            
            print(f"\n✓ Test completed successfully")
            
        except Exception as e:
            print(f"\n✗ Test failed: {str(e)}")
            results.append({
                'test': test['name'],
                'status': '✗ FAIL',
                'error': str(e),
            })
    
    # Summary
    print(f"\n\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    for r in results:
        status_emoji = '✓' if '✓' in r['status'] else '✗'
        print(f"{status_emoji} {r['test']}")
        if 'error' not in r:
            print(f"   Stress Level: {r['stress_level']}, Confidence: {r['confidence']}, Symptoms: {r['symptoms_detected']}")
        else:
            print(f"   Error: {r.get('error', 'Unknown')}")
    
    passed = sum(1 for r in results if '✓' in r['status'])
    print(f"\nResults: {passed}/{len(results)} tests passed")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    run_tests()
