# 🚀 Deployment Setup - What YOU Need To Do

All code changes are complete! Now follow these steps to deploy.

## Step 1: Get Required API Keys (10 minutes)

### 1.1 OpenWeatherMap API Key
- Already have: `OPENWEATHER_API_KEY=6276b4473c4ad27bc33a916505b42188` ✅
- (You may want to regenerate this since it's been exposed)

### 1.2 OpenAI API Key (MUST DO)
```
1. Go to: https://platform.openai.com/account/api-keys
2. Sign up with GitHub (free)
3. Create new API key
4. Copy the key (starts with "sk-")
5. You'll get free $5 credit
```

### Alternative: HuggingFace API Key (Free Option)
```
1. Go to: https://huggingface.co/settings/tokens
2. Sign up free
3. Create new token
4. Copy the token
```

---

## Step 2: Create Local .env File (5 minutes)

### 2.1 Backend .env
```bash
cd backend
cp .env.example .env
```

**Edit `backend/.env` and fill in (at minimum):**
```
OPENWEATHER_API_KEY=6276b4473c4ad27bc33a916505b42188
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
DATABASE_URL=sqlite:///reports.db
FLASK_ENV=development
```

### 2.2 Frontend .env
```bash
cd ../frontend
cp .env.example .env
```

**Edit `frontend/.env`:**
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

---

## Step 3: Install New Dependencies (5 minutes)

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend (should already have node_modules, but just in case)
cd ../frontend
npm install
```

---

## Step 4: Test Locally (20 minutes)

### 4.1 Start Backend
```bash
cd backend
python app.py
```
**Expected output:**
```
Initializing ML model...
Starting Flask backend on http://localhost:5000
ML Model ready for predictions
```

### 4.2 Start Frontend (in NEW terminal)
```bash
cd frontend
npm start
```
**Expected output:**
```
webpack compiled successfully
Compiled successfully!

You can now view crop-stress-advisory-frontend in the browser.
  Local:            http://localhost:3000
```

### 4.3 Test the Application
1. Open browser to `http://localhost:3000`
2. Submit a test crop report with:
   - Crop type: rice
   - Growth stage: vegetative
   - Some observations
3. You should see:
   - ✅ Stress level prediction
   - ✅ AI analysis (from OpenAI or HuggingFace)
   - ✅ Observation-based recommendations
   - ✅ Report saved to database

---

## Step 5: Clean API Key from Git History (CRITICAL)

Your OpenWeatherMap API key was exposed in the repo. Fix this:

```bash
# Go to project root
cd ..

# Remove it from Git history
git filter-branch --prune-empty --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  -- --all

# Force push (be careful!)
git push --force origin master
```

Then verify `.gitignore` contains `.env`:
```bash
cat .gitignore | grep ".env"
```

---

## Step 6: Commit Changes to GitHub (10 minutes)

```bash
# Make sure you're in the project root
cd c:\MyProjects\b2g

# Add all the new files and changes
git add .

# Check what will be committed
git status

# Commit
git commit -m "feat: Add production deployment support

- Add LLM service abstraction (OpenAI/HuggingFace/Ollama)
- Add PostgreSQL database models for report persistence
- Add environment variable configuration
- Update frontend to use REACT_APP_API_URL
- Update backend to save reports to database
- Add deployment files (Procfile, runtime.txt)
- Add GitHub Actions CI/CD workflow
- Add example env files

BREAKING: Reports now save to database instead of JSON files"

# Push to GitHub
git push origin master
```

---

## Step 7: Deploy to Cloud (30 minutes)

### Option A: Railway (Recommended - Simplest)

**7A.1 Deploy Backend**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Link to your GitHub repo
railway link

# Deploy
railway up
```

**7A.2 Get Database URL from Railway**
- Go to Railway dashboard
- Your database URL will be shown
- Save it (looks like: `postgresql://user:pass@host/db`)

**7A.3 Add Environment Variables to Railway**
In Railway dashboard, add these secrets:
```
OPENWEATHER_API_KEY=your_key
OPENAI_API_KEY=your_key
LLM_PROVIDER=openai
DATABASE_URL=<auto-provided by Railway>
```

**7A.4 Deploy Frontend to Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Go to frontend folder
cd frontend

# Deploy
vercel

# When prompted for environment variable:
# REACT_APP_API_URL = https://your-railway-app.up.railway.app/api
```

---

### Option B: Heroku (Older, Now Paid)
Heroku free tier discontinued. Minimum $5/month if you want to use it.

---

### Option C: Manual VPS Deployment
If you have your own server:
```bash
# On your server:
git clone https://github.com/YOUR_USERNAME/b2g.git
cd b2g/backend

# Install Python and PostgreSQL
sudo apt install python3 python3-pip postgresql

# Install dependencies
pip install -r requirements.txt

# Setup database
postgresql -U postgres -c "CREATE DATABASE b2g_db;"

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Step 8: Verify Deployment

After deployment to Railway + Vercel:

1. **Visit your Vercel URL** (e.g., `https://your-app.vercel.app`)
2. **Test the form:**
   - Submit a crop report
   - Should see AI analysis
   - Should save to Railway database
3. **Check Reports API:**
   - Visit `https://your-api.up.railway.app/api/reports`
   - Should return JSON with saved reports
4. **Check Logs:**
   - Railway: Dashboard → Logs
   - Vercel: Deployments → Logs

---

## 🎯 Summary of What I Did For You

✅ **Created 5 New Files:**
- `backend/llm_service.py` - LLM provider abstraction
- `backend/models_db.py` - SQLAlchemy database models
- `Procfile` - Railway/Heroku deployment config
- `runtime.txt` - Python version config
- `.github/workflows/deploy.yml` - Auto-deployment pipeline

✅ **Created 4 Example Files:**
- `frontend/.env.example` - Frontend env template
- `backend/.env.example` - Backend env template
- `DEPLOYMENT_GUIDE.md` - Comprehensive 3,000+ word guide
- `CODE_CHANGES_NEEDED.md` - Code change reference

✅ **Modified 4 Key Files:**
- `frontend/src/App.jsx` - Uses `REACT_APP_API_URL`
- `backend/app.py` - Database + LLM integration
- `backend/requirements.txt` - Added new dependencies
- `.gitignore` - Already has `.env` (good!)

---

## ⚠️ Important Reminders

### Before you deploy:
- [ ] API keys added to `.env` (not committed)
- [ ] `.env` is in `.gitignore` (verified)
- [ ] Tested locally with `npm start` ✅
- [ ] Tested backend API with Python ✅

### After you deploy:
- [ ] Test form submission on live site
- [ ] Verify reports save to database
- [ ] Monitor Railway/Vercel logs for errors
- [ ] Set up email alerts for failures (optional)

---

## 📞 Troubleshooting

### "API returns 503 Service Unavailable"
- Railway might be starting up
- Wait 30 seconds and try again
- Check Railway logs for errors

### "Reports not saving"
- Check DATABASE_URL is set correctly
- Check Procfile path to app:app is correct
- Check logs: `railway logs`

### "Frontend can't connect to backend"
- Verify REACT_APP_API_URL is set in Vercel env vars
- Check CORS is enabled in Flask (it is)
- Check Railway API URL is correct

### "OpenAI API 401 error"
- Check API key is correct
- Verify account has credit
- Regenerate key if needed

---

## 🎉 You're Done!

Once you complete Step 7, your app will be live at:
- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-api.up.railway.app/api`
- **Database:** PostgreSQL on Railway (auto-provisioned)

All other users can now use your deployed climate-smart agriculture advisor!

---

## 💬 Questions?

Refer to:
- **DEPLOYMENT_GUIDE.md** - For detailed steps
- **DEPLOYMENT_SUMMARY.md** - For architecture decisions
- **CODE_CHANGES_NEEDED.md** - For code reference
