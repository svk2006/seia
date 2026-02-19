import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import subprocess

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# LLM Configuration (choose one)
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')  # 'openai', 'huggingface', or 'ollama'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
OLLAMA_BASE_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///reports.db')

def get_weather_data(lat, lon):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant fields
        weather = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'rainfall': data.get('rain', {}).get('1h', 0),  # mm in last hour
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'location': data['name'],
            'timestamp': datetime.now().isoformat()
        }
        return weather
    except Exception as e:
        print(f"Error fetching weather: {str(e)}")
        # Return fallback data
        return {
            'temperature': 28.0,
            'humidity': 65,
            'rainfall': 5.0,
            'wind_speed': 3.5,
            'description': 'Unable to fetch real data',
            'location': 'Offline Mode',
            'timestamp': datetime.now().isoformat()
        }

def get_ollama_analysis(crop_type, stress_level, temperature, humidity, rainfall, wind_speed, notes):
    """Get detailed crop analysis from Ollama Mistral with deep observation analysis"""
    try:
        stress_names = {0: "healthy", 1: "mild stress", 2: "severe stress"}
        stress_name = stress_names.get(stress_level, "unknown condition")
        
        # Analyze observations for stress indicators
        observation_analysis = ""
        specific_treatments = ""
        if notes:
            indicators = analyze_observations(notes)
            if indicators:
                observation_analysis = f"\nObserver reported symptoms: {', '.join(indicators)}"
                # Request specific treatment for each symptom
                specific_treatments = "\n\nFor EACH symptom detected, provide specific treatment steps (1-2 sentences per symptom)."
        
        prompt = f"""You are an expert agricultural pathologist and crop consultant. Analyze this detailed crop report and provide targeted interventions.

CROP REPORT:
- Crop: {crop_type.upper()}
- ML Stress Assessment: {stress_name} 
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Rainfall: {rainfall}mm
- Wind Speed: {wind_speed} m/s{observation_analysis}

INSTRUCTIONS:
1. Validate the ML assessment against observed symptoms
2. Provide the MOST LIKELY CAUSE for current conditions
3. Recommend 3-4 IMMEDIATE ACTIONS to take within 24-48 hours
4. Suggest PREVENTIVE MEASURES for future{specific_treatments}

Keep advice practical, specific to {crop_type}, and actionable for a farmer.
IMPORTANT: Address each observed issue individually with concrete solutions."""
        
        response = requests.post(
            OLLAMA_BASE_URL,
            json={
                'model': 'mistral',
                'prompt': prompt,
                'stream': False,
                'temperature': 0.7
            },
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        advice = result.get('response', '').strip()
        return advice if advice else None
    except Exception as e:
        print(f"Ollama analysis failed (non-critical): {str(e)}")
        return None

def analyze_observations(notes):
    """Analyze observation text for stress indicators"""
    if not notes:
        return []
    
    notes_lower = notes.lower()
    indicators = []
    
    # Stress indicators
    stress_keywords = {
        'wilting': ['wilting', 'drooping', 'droopy', 'slump'],
        'yellowing': ['yellow', 'yellowing', 'pale', 'chlorotic'],
        'spotting': ['spot', 'spots', 'lesion', 'necrotic', 'blight'],
        'pests': ['insect', 'pest', 'bug', 'mite', 'aphid', 'caterpillar', 'webbing'],
        'disease': ['disease', 'mold', 'fungal', 'powder', 'rust', 'blight', 'scab'],
        'dry': ['drying', 'dry', 'crispy', 'brown edges', 'burnt'],
        'stunting': ['stunted', 'slow growth', 'weak', 'small'],
    }
    
    for condition, keywords in stress_keywords.items():
        if any(kw in notes_lower for kw in keywords):
            indicators.append(condition)
    
    return list(set(indicators))  # Remove duplicates

def estimate_soil_moisture(rainfall, humidity, temperature):
    """Estimate soil moisture based on weather conditions"""
    # Improved heuristic
    base_moisture = 40
    from_rainfall = min(rainfall * 5, 20)  # More rain = more moisture
    from_humidity = (humidity - 50) * 0.3  # Higher humidity means more moisture
    from_temp = max(0, 5 - (temperature - 25) * 0.2)  # Higher temp = less moisture
    
    soil_moisture = base_moisture + from_rainfall + from_humidity + from_temp
    return max(10, min(80, soil_moisture))  # Clamp between 10-80

def validate_report_data(data):
    """Validate incoming report data"""
    required_fields = ['latitude', 'longitude', 'crop_type', 'growth_stage']
    errors = []
    
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate latitude/longitude
    try:
        lat = float(data['latitude'])
        lon = float(data['longitude'])
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            errors.append("Invalid latitude/longitude coordinates")
    except ValueError:
        errors.append("Latitude and longitude must be numeric")
    
    return len(errors) == 0, errors

def save_report_to_file(report_data, reports_file='reports.json'):
    """Save report to JSON file"""
    try:
        # Load existing reports
        if os.path.exists(reports_file):
            with open(reports_file, 'r') as f:
                reports = json.load(f)
        else:
            reports = []
        
        # Add new report
        report_data['id'] = len(reports) + 1
        report_data['timestamp'] = datetime.now().isoformat()
        reports.append(report_data)
        
        # Save back
        with open(reports_file, 'w') as f:
            json.dump(reports, f, indent=2)
        
        return True, report_data
    except Exception as e:
        return False, str(e)

def load_all_reports(reports_file='reports.json'):
    """Load all reports from file"""
    try:
        if os.path.exists(reports_file):
            with open(reports_file, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading reports: {str(e)}")
        return []

def get_crop_types():
    """Get list of supported crops - includes farm and home garden crops"""
    return [
        # Home/Garden Crops
        'tomato', 'lettuce', 'cucumber', 'basil', 'mint', 'pepper', 'carrot',
        # Field Crops
        'wheat', 'maize', 'rice', 'cotton', 'sugarcane', 'pulses'
    ]

def get_growth_stages():
    """Get list of growth stages - varies by crop"""
    stages = [
        'vegetative',    # Early leaf growth
        'flowering',     # Flower/bud formation
        'fruiting',      # Fruit/pod development
        'grain_fill',    # Grain maturation (for cereals)
        'mature',        # Fully mature
        'pod_fill',      # Pod filling (for legumes)
        'boll_formation' # Boll formation (for cotton)
    ]
    return stages
