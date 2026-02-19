# Quick Code Changes for Deployment

## 1. Frontend Environment Variables

### File: `frontend/.env.example`
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

### File: `frontend/src/App.jsx` - Line 5 (CHANGE THIS)
**BEFORE:**
```jsx
const API_BASE = 'http://localhost:5000/api';
```

**AFTER:**
```jsx
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

---

## 2. Backend Environment Variables

### File: `backend/.env.example`
```
OPENWEATHER_API_KEY=your_key_here
OPENAI_API_KEY=your_openai_key_here
LLM_PROVIDER=openai
DATABASE_URL=sqlite:///reports.db
OLLAMA_URL=http://localhost:11434/api/generate
```

### File: `.gitignore` - ADD THIS LINE
```
.env
```

---

## 3. Create LLM Service File

### File: `backend/llm_service.py` (NEW FILE - CREATE THIS)

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_openai_analysis(symptoms, crop_data):
    """Get analysis from OpenAI API"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        prompt = f"""You are an agricultural expert. Analyze this crop stress situation:
        
Crop: {crop_data.get('crop_type', 'Unknown')}
Growth Stage: {crop_data.get('growth_stage', 'Unknown')}
Symptoms: {symptoms}

Provide:
1. Root cause identification (1-2 sentences)
2. Immediate action (3-4 bullet points)
3. Prevention tips (2-3 points)

Keep response concise and practical."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert agricultural advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        return None


def get_huggingface_analysis(symptoms, crop_data):
    """Get analysis from Hugging Face Inference API"""
    try:
        from huggingface_hub import InferenceClient
        
        client = InferenceClient(
            api_key=os.getenv('HUGGINGFACE_API_KEY')
        )
        
        prompt = f"Agricultural expert: Analyze {crop_data.get('crop_type')} crop stress with symptoms: {symptoms}. Provide 3 immediate actions."
        
        response = client.text_generation(prompt, max_new_tokens=300)
        return response
    except Exception as e:
        print(f"HuggingFace Error: {str(e)}")
        return None


def get_ollama_analysis(symptoms, crop_data):
    """Get analysis from local Ollama (if available)"""
    try:
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
        
        prompt = f"Agricultural analysis for {crop_data.get('crop_type')}: {symptoms}"
        
        response = requests.post(
            ollama_url,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', '')
    except Exception as e:
        print(f"Ollama Error: {str(e)}")
    
    return None


def get_ai_analysis(symptoms, crop_data):
    """
    Get AI analysis using configured provider.
    Tries providers in order: OpenAI > HuggingFace > Ollama > None
    """
    provider = os.getenv('LLM_PROVIDER', 'openai').lower()
    
    print(f"Using LLM provider: {provider}")
    
    if provider == 'openai':
        result = get_openai_analysis(symptoms, crop_data)
        if result:
            return result
            
    elif provider == 'huggingface':
        result = get_huggingface_analysis(symptoms, crop_data)
        if result:
            return result
    
    # Try local Ollama as fallback
    result = get_ollama_analysis(symptoms, crop_data)
    if result:
        return result
    
    # If all else fails, return None and let app use observation-based analysis
    return None
```

---

## 4. Update Backend Requirements

### File: `backend/requirements.txt` - ADD THESE LINES

```
openai==1.3.0
huggingface-hub==0.19.0
flask-sqlalchemy==3.1.1
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

## 5. Update backend/app.py - Add Imports

**Add at top of file:**
```python
import os
from dotenv import load_dotenv
from llm_service import get_ai_analysis

load_dotenv()
```

---

## 6. Database Models File

### File: `backend/models_db.py` (NEW FILE - CREATE THIS)

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_type = db.Column(db.String(100), nullable=False)
    growth_stage = db.Column(db.String(100))
    stress_level = db.Column(db.Integer)
    confidence = db.Column(db.Float)
    observations = db.Column(db.JSON)
    symptom_analysis = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    combined_assessment = db.Column(db.Text)
    action_priority = db.Column(db.JSON)
    ai_analysis = db.Column(db.Text)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'crop_type': self.crop_type,
            'growth_stage': self.growth_stage,
            'stress_level': self.stress_level,
            'confidence': self.confidence,
            'observations': self.observations,
            'symptom_analysis': self.symptom_analysis,
            'recommendations': self.recommendations,
            'combined_assessment': self.combined_assessment,
            'action_priority': self.action_priority,
            'ai_analysis': self.ai_analysis,
            'location': self.location,
            'created_at': self.created_at.isoformat()
        }
```

---

## 7. Create Deployment Files

### File: `Procfile` (NEW FILE - Create in root directory)
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
```

### File: `runtime.txt` (NEW FILE - Create in root directory)
```
python-3.11.0
```

---

## 8. Update app.py Database Configuration

**Add after `app = Flask(__name__)` line:**

```python
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///reports.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models_db import db
db.init_app(app)

with app.app_context():
    db.create_all()
```

---

## 9. Update POST /api/reports Endpoint

**In `backend/app.py`, update the submit_report function:**

```python
@app.route('/api/reports', methods=['POST'])
def submit_report():
    data = request.json
    
    # ... existing validation code ...
    
    # Get AI analysis
    observations_text = ', '.join([obs['symptom'] for obs in observations])
    ai_analysis = get_ai_analysis(observations_text, crop_data)
    
    # Save to database
    from models_db import Report, db
    
    report = Report(
        crop_type=data['crop_type'],
        growth_stage=data['growth_stage'],
        stress_level=stress_level,
        confidence=confidence,
        observations=observations,
        symptom_analysis=symptom_analysis,
        recommendations=recommendations,
        combined_assessment=combined_assessment,
        action_priority=action_priority,
        ai_analysis=ai_analysis,
        location=data.get('location'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    db.session.add(report)
    db.session.commit()
    
    return jsonify({
        'id': report.id,
        'stress_level': report.stress_level,
        'confidence': report.confidence,
        'observations': report.observations,
        'symptom_analysis': report.symptom_analysis,
        'ai_analysis': report.ai_analysis,
        'recommendations': report.recommendations,
        'combined_assessment': report.combined_assessment,
        'action_priority': report.action_priority,
        'ml_based_recommendation': recommendation,
        'ai_detailed_analysis': ai_analysis,
        'timestamp': report.created_at.isoformat()
    }), 201
```

---

## Deployment Checklist

- [ ] Update frontend App.jsx API_BASE
- [ ] Create frontend/.env.example
- [ ] Create backend/.env.example  
- [ ] Add .env to .gitignore
- [ ] Create llm_service.py
- [ ] Create models_db.py
- [ ] Update requirements.txt
- [ ] Create Procfile
- [ ] Create runtime.txt
- [ ] Update app.py imports and database config
- [ ] Get OpenAI API key (platform.openai.com)
- [ ] Get OpenWeatherMap API key
- [ ] Push to GitHub
- [ ] Sign up on Railway.app
- [ ] Deploy backend to Railway
- [ ] Copy DATABASE_URL from Railway
- [ ] Add environment secrets to Railway
- [ ] Deploy frontend to Vercel
- [ ] Set REACT_APP_API_URL in Vercel
- [ ] Test end-to-end through web UI
