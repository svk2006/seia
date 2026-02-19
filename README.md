# 🌾 B2G: Climate-Smart Agriculture Advisory System

A production-ready web platform powered by AI that predicts crop stress and provides actionable farming recommendations to improve yield and climate resilience. Built with ML, LLM integration, and real-time weather data.

**Status:** ✅ Production Ready | 🚀 Deployed | 🌍 Global Accessible

## 🎯 Key Features

✅ **AI-Powered Crop Stress Prediction** - Gradient Boosting ML model (77% accuracy)  
✅ **LLM-Enhanced Analysis** - OpenAI GPT integration for detailed recommendations  
✅ **Real-Time Weather Integration** - OpenWeatherMap API for live data  
✅ **Persistent Database** - PostgreSQL with SQLAlchemy ORM for historical tracking  
✅ **Observation-Based Analysis** - Manual symptom mapping for offline scenarios  
✅ **Climate-Smart Design** - SDG 13 aligned with emission reduction focus  
✅ **Bilingual Support** - English & Tamil interface  
✅ **Interactive Mapping** - Leaflet.js for geospatial visualization  
✅ **Production Deployment** - Railway backend + Vercel frontend  

---

## 🏗️ Architecture

```
B2G Climate-Smart Agriculture
├── Frontend (Vercel CDN)
│   ├── React 18 + TailwindCSS
│   ├── SDG 13 Dark Theme
│   └── Bilingual (EN/TM)
│
├── Backend (Railway)
│   ├── Flask REST API
│   ├── ML Model (GradientBoosting)
│   ├── LLM Service (OpenAI/HuggingFace/Ollama)
│   ├── Weather API (OpenWeatherMap)
│   └── Database ORM (SQLAlchemy)
│
└── Database (PostgreSQL)
    ├── Reports table
    ├── Auto-backups
    └── Indexed queries
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key (free $5 credit)
- OpenWeatherMap API key (free tier)

### 1️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env and add your API keys:
#   OPENAI_API_KEY=sk-...
#   OPENWEATHER_API_KEY=...

# Start backend server
python app.py
```

Backend runs on: **http://localhost:5000**

### 2️⃣ Frontend Setup

```bash
# In new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start
```

Frontend opens on: **http://localhost:3000**

### 3️⃣ Test the Application

1. Submit a crop report with observations
2. View ML stress prediction (0-100% confidence)
3. See AI-generated recommendations from OpenAI
4. Check saved reports in `/api/reports`

---

## 📊 ML Model Details

### Model Specifications
```
Algorithm:       Gradient Boosting Classifier (sklearn)
Training Data:   240+ samples (13 crops × 7 stages)
Accuracy:        77% (tested on validation set)
Inference Time:  ~50ms
Features:        6 (temperature, humidity, rainfall, wind, crop, stage)
Output Classes:  3 (Healthy, Mild Stress, Severe Stress)
```

### Supported Crops
Tomato, Lettuce, Cucumber, Basil, Mint, Pepper, Carrot, Wheat, Maize, Rice, Cotton, Sugarcane, Pulses

### Prediction Pipeline
1. User submits location + crop observations
2. Fetch real-time weather from OpenWeatherMap
3. ML model predicts stress level
4. OpenAI analyzes symptoms for detailed guidance
5. Results saved to PostgreSQL database
6. Report returned with recommendations

---

## 🗂️ Project Structure

```
b2g/
├── backend/
│   ├── app.py                  # Flask API + routes
│   ├── models.py               # ML model & observation analysis
│   ├── utils.py                # Weather API & data helpers
│   ├── llm_service.py          # OpenAI/HuggingFace/Ollama integration
│   ├── models_db.py            # SQLAlchemy ORM models
│   ├── model.pkl               # Trained ML model
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   └── reports.db              # SQLite (local dev)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── translations.js     # English/Tamil strings
│   │   └── index.css           # Tailwind styles
│   ├── public/
│   ├── package.json            # Node dependencies
│   ├── tailwind.config.js      # Tailwind config
│   └── .env.example            # Frontend env template
│
├── Procfile                    # Railway deployment config
├── runtime.txt                 # Python version (3.11)
├── .github/workflows/
│   └── deploy.yml              # GitHub Actions CI/CD
│
├── FINAL_DEPLOYMENT_STEPS.md   # 🚀 Deployment guide
├── SETUP_CHECKLIST.md          # Step-by-step instructions
├── DEPLOYMENT_GUIDE.md         # Technical deep-dive
└── README.md                   # This file
```

---

## 🔌 API Endpoints

### Health Check
```bash
GET /api/health
```
Returns: `{"status": "ok"}`

### Get Weather
```bash
GET /api/weather?lat=28.7041&lon=77.1025
```

### Submit Report & Get Prediction
```bash
POST /api/reports
{
  "latitude": 28.7041,
  "longitude": 77.1025,
  "crop_type": "rice",
  "growth_stage": "vegetative",
  "notes": "Leaves yellowing, some wilting observed"
}
```

Returns:
```json
{
  "id": 1,
  "stress_level": 2,
  "confidence": 77.5,
  "observations": ["yellowing", "wilting"],
  "symptom_analysis": [...],
  "ai_analysis": "Root cause: Nitrogen deficiency...",
  "action_priority": ["Apply nitrogen fertilizer...", "..."]
}
```

### Get All Reports
```bash
GET /api/reports?page=1&per_page=100
```

### Get Metadata
```bash
GET /api/metadata
```

---

## 🌍 Deployment

### Prerequisites for Deployment
- GitHub account with repo pushed
- OpenAI API key
- OpenWeatherMap API key

### Deploy to Production (30 minutes)

**Step 1: Backend to Railway**
```bash
npm install -g @railway/cli
railway login
cd c:\MyProjects\b2g
railway init
railway up
```
Then add environment variables in Railway dashboard.

**Step 2: Frontend to Vercel**
```bash
npm install -g vercel
cd frontend
vercel
```
Set `REACT_APP_API_URL` to your Railway URL.

See [FINAL_DEPLOYMENT_STEPS.md](FINAL_DEPLOYMENT_STEPS.md) for detailed instructions.

---

## 🔐 Environment Variables

### Backend (.env)
```
OPENWEATHER_API_KEY=your_key
OPENAI_API_KEY=sk-your-key
LLM_PROVIDER=openai
DATABASE_URL=postgresql://...
FLASK_ENV=production
```

### Frontend (.env)
```
REACT_APP_API_URL=https://your-api.up.railway.app/api
REACT_APP_ENVIRONMENT=production
```

See `.env.example` files for complete templates.

---

## 🎨 UI Features

### Dashboard Components
- 🌍 Climate Metrics (Resilience %, Emissions ↓, Sustainability)
- 🌤️ Real-time Weather Card
- 📊 Stress Level Prediction Card (color-coded)
- 📝 Report Submission Form
- 🗺️ Interactive Leaflet Map
- 📱 Responsive Design (Mobile/Tablet/Desktop)

### Theme
- **SDG 13**: Climate Action focused
- **Colors**: Blue-950, Cyan-900, Teal-950 gradient
- **Typography**: Clean, readable, accessible
- **Languages**: English & Tamil bilingual support

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | React 18 + TailwindCSS 3 |
| **Backend** | Flask 2.3 + Python 3.11 |
| **ML/AI** | scikit-learn, OpenAI API |
| **Database** | SQLAlchemy + PostgreSQL |
| **Deployment** | Railway (backend) + Vercel (frontend) |
| **Weather API** | OpenWeatherMap |
| **Mapping** | Leaflet.js |
| **CI/CD** | GitHub Actions |

---

## 📈 Accuracy & Performance

### Model Accuracy
- **Overall**: 77% prediction accuracy
- **Healthy Detection**: 95% precision
- **Stress Detection**: 72% recall
- **Inference Time**: <50ms per prediction

### API Performance
| Endpoint | Response Time |
|----------|---------------|
| Weather API | ~500ms |
| ML Prediction | ~50ms |
| LLM Analysis | ~2-5 seconds |
| Report Save | <100ms |
| Get Reports | <200ms |

---

## 🚨 Troubleshooting

### Backend API errors?
```bash
# Check backend is running
curl http://localhost:5000/api/health

# View logs
python app.py

# Check dependencies
pip list | grep -E "openai|flask|sqlalchemy"
```

### Frontend can't connect?
- Verify `REACT_APP_API_URL` in frontend/.env
- Check backend is running on correct port
- Clear browser cache

### LLM not working?
- Verify API key in backend/.env
- Check OpenAI account has credit
- Will fall back to observation-based analysis

### Database errors?
- Check `DATABASE_URL` is set
- For local dev, SQLite is auto-created
- Restart backend to reinitialize

---

## 📚 Documentation

- **[FINAL_DEPLOYMENT_STEPS.md](FINAL_DEPLOYMENT_STEPS.md)** - Deploy to production
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Detailed setup instructions
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Technical architecture  
- **[CODE_CHANGES_NEEDED.md](CODE_CHANGES_NEEDED.md)** - Code reference

---

## 🔄 Development Roadmap

### Phase 1 (Current) ✅
- ✅ ML stress prediction
- ✅ OpenAI LLM integration
- ✅ Database persistence
- ✅ Production deployment

### Phase 2 (Next)
- [ ] Satellite imagery integration (NDVI/EVI)
- [ ] Historical trend analysis (30-day forecasts)
- [ ] Email/SMS alerts
- [ ] User authentication & profiles

### Phase 3 (Future)
- [ ] Mobile app (React Native)
- [ ] Advanced LSTM models
- [ ] Drone imagery processing
- [ ] Admin analytics dashboard
- [ ] Community forum

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test locally with `npm start` and `python app.py`
4. Submit PR with clear description

---

## 📄 License

MIT License - Open for academic & commercial use

---

## 🙏 Acknowledgments

Built for AI Hackathon 2026  
Aligned with **UN SDG 13: Climate Action**  
Focus: Climate-smart agriculture for emerging markets

---

## 📞 Support

- Documentation: See `/docs` folder
- Issues: GitHub Issues
- Email: Contact maintainers

---

**Status**: 🟢 Production Ready | Last Updated: Feb 2026 | Version: 2.0.0
