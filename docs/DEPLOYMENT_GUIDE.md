# B2G Climate-Smart Agriculture - GitHub Deployment Guide

## 🚨 CRITICAL ISSUES IDENTIFIED

### Issue #1: Ollama Mistral Won't Work in Production (BLOCKER)
**Problem:** Ollama is a LOCAL AI tool that requires:
- Installation on the user's machine
- Running locally on `localhost:11434`
- GPU resources on their computer

**Why it fails in cloud:**
- Cloud servers can't assume users have Ollama installed
- Cannot deploy Ollama centrally and share it (licensing & resource constraints)
- Each deployment instance would need separate Ollama setup

**Solution:** Replace Ollama with a cloud API-based LLM:
- **Option A:** OpenAI API (GPT-3.5/4 - cost: ~$0.002/request)
- **Option B:** Hugging Face Inference API (free tier available)
- **Option C:** Google Vertex AI (enterprise option)
- **Option D:** Local Ollama for users who want it (optional feature)

---

### Issue #2: Hardcoded API Endpoints
**Problem:** Frontend hardcoded to `localhost:5000`
```jsx
const API_BASE = 'http://localhost:5000/api';  // ❌ Won't work in production
```

**Problem:** Backend hardcoded to Ollama at `localhost:11434`
```python
OLLAMA_BASE_URL = 'http://localhost:11434/api/generate'  # ❌ Won't work
```

**Solution:** Use environment variables
```jsx
// Frontend
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

---

### Issue #3: API Key Exposed on GitHub
**Problem:** OpenWeatherMap API key in `.env` is publicly visible
```
OPENWEATHER_API_KEY=6276b4473c4ad27bc33a916505b42188  # ❌ EXPOSED!
```

**Risk:** Anyone can use your API key, causing:
- Quota exhaustion
- Unexpected charges
- Rate limiting

**Solution:** Add `.env` to `.gitignore` and use GitHub Secrets

---

### Issue #4: File-Based Storage Won't Persist
**Problem:** Reports stored as `reports.json` in local files
```python
def save_report_to_file(report):
    with open('reports.json', 'r') as f:
        # ❌ In cloud, this file gets deleted when app restarts
```

**Why it fails:** Cloud deployments are stateless - files are deleted on every restart

**Solution:** Use a database:
- **Option A:** MongoDB (free tier, cloud-hosted)
- **Option B:** PostgreSQL (free tier on Railway/Render)
- **Option C:** Firebase Firestore (Google, free tier)

---

## ✅ STEP-BY-STEP DEPLOYMENT GUIDE

### Phase 1: Prepare Codebase (30 minutes)

#### Step 1.1: Secure API Keys
```bash
# 1. Remove exposed API key from Git history
git filter-branch --env-filter '
  if [ "$GIT_COMMIT" = "<commit_with_key>" ]
  then
    export GIT_AUTHOR_NAME="Your Name"
    export GIT_AUTHOR_EMAIL="your@email.com"
    export GIT_COMMITTER_NAME="Your Name"
    export GIT_COMMITTER_EMAIL="your@email.com"
  fi
'

# 2. Force push (be careful!)
git push --force origin master

# 3. Verify .env is in .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

#### Step 1.2: Update Frontend for Environment Variables
Create `.env.example` file:

```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

Update `frontend/src/App.jsx` line 5:
```jsx
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

#### Step 1.3: Update Backend for Environment Variables
Update `backend/utils.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# OpenWeather API
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# LLM Configuration (choose one)
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')  # 'openai', 'huggingface', or 'ollama'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///reports.db')
```

---

### Phase 2: Replace Ollama with Cloud LLM (45 minutes)

#### Option A: Use OpenAI API (Recommended - Most Reliable)

**Step 2A.1: Install OpenAI library**
```bash
cd backend
pip install openai
pip freeze > requirements.txt
```

**Step 2A.2: Create new file `backend/llm_service.py`:**

```python
import os
from openai import OpenAI

def get_ai_analysis(symptoms, crop_data):
    """Get analysis from OpenAI instead of Ollama"""
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""
    Analyze this crop stress situation and provide actionable recommendations:
    
    Crop: {crop_data['crop_type']}
    Growth Stage: {crop_data['growth_stage']}
    Observed Symptoms: {symptoms}
    
    Provide:
    1. Root cause identification
    2. 3-4 immediate actions
    3. Prevention measures
    4. Expected recovery time
    
    Keep response concise and practical.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agricultural expert specialized in crop stress management."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def get_ollama_analysis(symptoms, crop_data):
    """Fallback to local Ollama if available"""
    import requests
    import json
    
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
    
    try:
        prompt = f"Analyze: {crop_data['crop_type']} with {symptoms}"
        response = requests.post(
            ollama_url,
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('response', '')
    except:
        pass
    
    return None  # Fall back to default recommendations
```

**Step 2A.3: Update `backend/app.py` POST /api/reports endpoint:**

```python
from llm_service import get_ai_analysis, get_ollama_analysis

@app.route('/api/reports', methods=['POST'])
def submit_report():
    # ... existing validation code ...
    
    # Try OpenAI first, fall back to Ollama
    llm_provider = os.getenv('LLM_PROVIDER', 'openai')
    
    if llm_provider == 'openai':
        ai_analysis = get_ai_analysis(observations, crop_data)
    elif llm_provider == 'ollama':
        ai_analysis = get_ollama_analysis(observations, crop_data)
    else:
        ai_analysis = "Using observation-based analysis only"
    
    # ... rest of endpoint ...
```

---

#### Option B: Use Hugging Face Inference API (Free Tier)

**Step 2B.1: Install library**
```bash
pip install huggingface-hub
```

**Step 2B.2: Add to `backend/llm_service.py`:**

```python
from huggingface_hub import InferenceClient

def get_huggingface_analysis(symptoms, crop_data):
    """Use free Hugging Face inference API"""
    
    client = InferenceClient(
        api_key=os.getenv('HUGGINGFACE_API_KEY')
    )
    
    prompt = f"""Analyze crop stress for {crop_data['crop_type']} 
    showing {symptoms}. Provide 3 immediate actions."""
    
    response = client.text_generation(prompt)
    return response
```

---

### Phase 3: Add Database Support (60 minutes)

#### Step 3.1: Install SQLAlchemy
```bash
pip install flask-sqlalchemy python-dotenv
pip freeze > requirements.txt
```

#### Step 3.2: Create `backend/models_db.py`:**

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_type = db.Column(db.String(100), nullable=False)
    growth_stage = db.Column(db.String(100))
    stress_level = db.Column(db.Integer)
    confidence = db.Column(db.Float)
    observations = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    ai_analysis = db.Column(db.Text)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'crop_type': self.crop_type,
            'stress_level': self.stress_level,
            'confidence': self.confidence,
            'observations': self.observations,
            'recommendations': self.recommendations,
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat()
        }
```

#### Step 3.3: Update `backend/app.py`:**

```python
from flask_sqlalchemy import SQLAlchemy
from models_db import db, Report
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///reports.db'
)
db.init_app(app)

with app.app_context():
    db.create_all()

# Update report endpoint to save to database
@app.route('/api/reports', methods=['POST'])
def submit_report():
    # ... existing validation and analysis code ...
    
    # Save to database instead of JSON file
    report = Report(
        crop_type=data['crop_type'],
        growth_stage=data['growth_stage'],
        stress_level=stress_level,
        confidence=confidence,
        observations=observations,
        recommendations=recommendations,
        ai_analysis=ai_analysis,
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    db.session.add(report)
    db.session.commit()
    
    return jsonify({
        'id': report.id,
        'stress_level': report.stress_level,
        'confidence': report.confidence,
        # ... other fields ...
    }), 201

# Get reports from database
@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = Report.query.order_by(Report.created_at.desc()).limit(100).all()
    return jsonify([r.to_dict() for r in reports]), 200
```

---

### Phase 4: Choose Hosting Platform (Varies)

#### Option A: Deploy on Vercel (Frontend) + Railway (Backend)
**Estimated time: 30 minutes**
**Cost: Free tier available**

**Frontend to Vercel:**
```bash
1. Install Vercel CLI: npm install -g vercel
2. cd frontend
3. vercel
4. Follow prompts, link to GitHub repo
5. Set environment variable: REACT_APP_API_URL=https://your-api.railway.app/api
```

**Backend to Railway:**
```bash
1. Go to railway.app, sign up with GitHub
2. Create new project
3. Connect to your GitHub repo
4. Set environment variables:
   - OPENWEATHER_API_KEY=your_key
   - OPENAI_API_KEY=your_key (if using OpenAI)
   - DATABASE_URL=auto-generated
   - LLM_PROVIDER=openai
5. Railway auto-deploys on git push
```

**Create `Procfile` in backend root:**
```
web: gunicorn app:app
```

**Add to `backend/requirements.txt`:**
```
gunicorn==21.2.0
flask-cors==4.0.0
```

---

#### Option B: Deploy on Heroku (Older, Paid)
**Note: Heroku free tier discontinued. Minimum $5/month**

---

#### Option C: Deploy Both on Azure (Enterprise)
**https://azure.microsoft.com/en-us/services/app-service/**

---

### Phase 5: Setup Environment Variables in GitHub

#### GitHub Secrets Setup:

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

2. Add these secrets:
```
OPENWEATHER_API_KEY = (your key)
OPENAI_API_KEY = (get from platform.openai.com)
DATABASE_URL = (Railway/Railway provides this)
LLM_PROVIDER = openai
```

3. Create `.github/workflows/deploy.yml` for auto-deployment:

```yaml
name: Deploy

on:
  push:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up
```

---

## 🎯 Summary: What Changes Are Needed

| Issue | Current | Fix | Time |
|-------|---------|-----|------|
| **Ollama** | `localhost:11434` | OpenAI/HuggingFace API | 45 min |
| **API Endpoints** | Hardcoded localhost | Environment variables | 15 min |
| **API Keys** | Exposed in .env | GitHub Secrets | 10 min |
| **Storage** | JSON files | Database (PostgreSQL/MongoDB) | 60 min |
| **Frontend Build** | Development only | Production build config | 10 min |
| **Hosting** | None | Railway + Vercel | 30 min |
| **Auto-Deploy** | Manual | GitHub Actions | 15 min |
| **Total** | **Non-deployable** | **Production-ready** | **~3 hours** |

---

## 🚀 Quick Start Recommended Deployment Path

1. **Replace Ollama** with OpenAI API (most reliable, not free but worth it)
2. **Add environment variables** to frontend/backend
3. **Add database** for persistence
4. **Deploy backend** to Railway (pick up DATABASE_URL automatically)
5. **Deploy frontend** to Vercel (auto-redeployed on git push)
6. **Setup GitHub Secrets** for API keys

---

## ❓ Will Ollama Work if Users Install It Locally?

**Answer: YES, but with caveats**

If you want to support **local Ollama as optional feature**:

```python
# backend/llm_service.py
def get_analysis(symptoms, crop_data):
    # Try cloud LLM first
    if os.getenv('LLM_PROVIDER') == 'openai':
        return get_ai_analysis(symptoms, crop_data)
    
    # Fall back to local Ollama if user has it running
    ollama = get_ollama_analysis(symptoms, crop_data)
    if ollama:
        return ollama
    
    # Final fallback to rule-based analysis
    return generate_observation_based_advice(symptoms, crop_data)
```

**This allows:**
- ✅ Users with Ollama running locally use it
- ✅ Cloud users use OpenAI/HuggingFace
- ✅ Graceful fallback to rule-based analysis

---

## 🔐 Security Checklist Before Deploying

- [ ] No API keys in code
- [ ] `.env` file in `.gitignore`
- [ ] Database passwords in secrets, not code
- [ ] HTTPS enforced (handled by Vercel/Railway)
- [ ] CORS properly configured (not `*`)
- [ ] Input validation on all endpoints
- [ ] Rate limiting added
- [ ] Error messages don't expose system details

---

## 📝 Files to Create/Modify

### New Files to Create:
```
backend/llm_service.py          # LLM provider abstraction
backend/models_db.py            # Database models
.github/workflows/deploy.yml    # Auto-deployment
frontend/.env.example           # Environment variables template
backend/.env.example            # Environment variables template
Procfile                        # Heroku/Railway deployment config
```

### Files to Modify:
```
frontend/src/App.jsx            # Use process.env.REACT_APP_API_URL
backend/app.py                  # Database + new LLM service
backend/utils.py                # Environment variables
backend/requirements.txt         # Add new dependencies
.gitignore                      # Add .env
```

---

## 💡 Next Steps

1. **Choose your LLM provider:** OpenAI (recommended) or Hugging Face
2. **Choose your host:** Railway (backend) + Vercel (frontend)
3. **Implement changes** following Phase 1-5 above
4. **Test locally** with `python app.py` and `npm start`
5. **Deploy to GitHub** and let CI/CD handle the rest

Would you like me to implement any of these changes automatically?
