from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import (
    CropStressModel, 
    get_stress_recommendation, 
    get_stress_label, 
    get_stress_color,
    get_crop_care,
    get_yield_info,
    generate_observation_based_advice
)
from utils import (
    get_weather_data, 
    validate_report_data, 
    save_report_to_file,
    load_all_reports,
    get_crop_types,
    get_growth_stages,
    get_ollama_analysis,
    analyze_observations
)
from models_db import db, Report
from llm_service import get_ai_analysis, get_ollama_analysis

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///reports.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

# Initialize ML model
print("Initializing ML model...")
ml_model = CropStressModel()
ml_model.load_model('model.pkl')

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'}), 200

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get weather data for a location"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
    
    weather = get_weather_data(lat, lon)
    return jsonify(weather), 200

@app.route('/api/predict', methods=['POST'])
def predict_stress():
    """Predict crop stress based on weather and crop data"""
    data = request.json
    
    # Validate input
    required_fields = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'crop_type', 'growth_stage']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        stress_level, confidence = ml_model.predict(
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            rainfall=float(data['rainfall']),
            wind_speed=float(data['wind_speed']),
            crop_type=data['crop_type'].lower(),
            growth_stage=data['growth_stage'].lower()
        )
        
        recommendation = get_stress_recommendation(stress_level)
        label = get_stress_label(stress_level)
        
        return jsonify({
            'stress_level': stress_level,
            'stress_label': label,
            'confidence': round(confidence, 2),
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['POST'])
def submit_report():
    """Submit a crop stress report with observations and get detailed prediction"""
    data = request.json
    
    # Validate report data
    is_valid, errors = validate_report_data(data)
    if not is_valid:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    try:
        lat = float(data['latitude'])
        lon = float(data['longitude'])
        crop_type = data['crop_type'].lower()
        growth_stage = data['growth_stage'].lower()
        observations = data.get('notes', '')
        
        # Get weather data for the location
        weather = get_weather_data(lat, lon)
        
        # Make ML prediction
        stress_level, confidence = ml_model.predict(
            temperature=weather['temperature'],
            humidity=weather['humidity'],
            rainfall=weather['rainfall'],
            wind_speed=weather['wind_speed'],
            crop_type=crop_type,
            growth_stage=growth_stage
        )
        
        # Analyze observations for stress indicators
        observed_symptoms = analyze_observations(observations)
        
        # Generate detailed, observation-based advice
        symptom_advice = generate_observation_based_advice(
            crop_type=crop_type,
            stress_level=stress_level,
            observed_symptoms=observed_symptoms,
            temperature=weather['temperature'],
            humidity=weather['humidity'],
            growth_stage=growth_stage
        )
        
        # Prepare report with crop-specific insights
        recommendation = get_crop_care(stress_level, crop_type)
        yield_info = get_yield_info(crop_type)
        label = get_stress_label(stress_level)
        color = get_stress_color(stress_level)
        
        # Get AI analysis using configured LLM provider
        llm_provider = os.getenv('LLM_PROVIDER', 'openai')
        ai_analysis = None
        symptom_text = ', '.join([s.get('symptom', '') for s in (symptom_advice.get('symptom_analysis', []) or [])])
        
        crop_data_for_llm = {
            'crop_type': crop_type,
            'growth_stage': growth_stage,
            'temperature': weather['temperature'],
            'humidity': weather['humidity'],
            'rainfall': weather['rainfall'],
            'wind_speed': weather['wind_speed'],
            'stress_level': stress_level
        }

        try:
            if llm_provider == 'openai':
                ai_analysis = get_ai_analysis(symptom_text or observations, crop_data_for_llm)
            elif llm_provider == 'ollama':
                ai_analysis = get_ollama_analysis(symptom_text or observations, crop_data_for_llm)
            else:
                ai_analysis = "LLM analysis not configured."
        except Exception as e:
            print(f"LLM analysis failed (non-critical): {str(e)}")
            ai_analysis = "AI analysis failed to generate."

        
        # Save to database instead of JSON file
        report_obj = Report(
            crop_type=crop_type,
            growth_stage=growth_stage,
            stress_level=stress_level,
            confidence=round(confidence, 2),
            observations=observed_symptoms,
            symptom_analysis=symptom_advice.get('symptom_analysis', []),
            recommendations=recommendation,
            combined_assessment=symptom_advice.get('combined_assessment', ''),
            action_priority=symptom_advice.get('action_priority', []),
            ai_analysis=ai_analysis,
            ml_based_recommendation=recommendation,
            location=data.get('location', ''),
            latitude=lat,
            longitude=lon
        )
        
        db.session.add(report_obj)
        db.session.commit()
        
        result = report_obj.to_dict()
        result.update({
            'stress_label': label,
            'color': color,
            'yield_optimization': yield_info,
            'timestamp': report_obj.created_at.isoformat()
        })
        
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all submitted reports from database"""
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        # Fetch reports from database
        reports_query = Report.query.order_by(Report.created_at.desc())
        total = reports_query.count()
        
        reports_page = reports_query.paginate(page=page, per_page=per_page)
        reports = [r.to_dict() for r in reports_page.items]
        
        return jsonify({
            'reports': reports,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': reports_page.pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Get app metadata - crop types, growth stages, etc."""
    return jsonify({
        'crop_types': get_crop_types(),
        'growth_stages': get_growth_stages(),
        'stress_levels': {
            0: 'Healthy',
            1: 'Mild Stress',
            2: 'Severe Stress'
        }
    }), 200

# Serve frontend files (if deployed together)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files"""
    if path != '' and os.path.exists(os.path.join('frontend/build', path)):
        return send_from_directory('frontend/build', path)
    return send_from_directory('frontend/build', 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Flask backend on http://localhost:5000")
    print("ML Model ready for predictions")
    app.run(debug=True, host='0.0.0.0', port=5000)
