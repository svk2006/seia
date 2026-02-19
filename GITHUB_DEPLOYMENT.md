# 🚀 GitHub Deployment Guide - Step by Step

## Overview
You'll deploy to **2 cloud platforms**:
- **Backend**: Railway (Flask API)
- **Frontend**: Vercel (React app)

**Total time: ~30 minutes**

---

## ✅ Prerequisites Checklist

Before starting, make sure you have:
- [ ] GitHub account
- [ ] Code pushed to GitHub (master/main branch)
- [ ] OpenAI API key (from `backend/.env`)
- [ ] OpenWeatherMap API key (already have ✅)
- [ ] `.env` file NOT committed to GitHub (should be in .gitignore)

---

## 📋 Step-by-Step Deployment

### STEP 1: Verify Your GitHub Repository (5 minutes)

#### 1.1 Check your repo is public and contains all files
```bash
cd c:\MyProjects\b2g
git status
git log --oneline | head -5
```

#### 1.2 Verify .env is NOT in Git (IMPORTANT!)
```bash
# This should show that .env is ignored
git check-ignore backend/.env
git check-ignore frontend/.env

# Should output:
# backend/.env
# frontend/.env
```

If it doesn't show these files, add to `.gitignore`:
```bash
echo "backend/.env" >> .gitignore
echo "frontend/.env" >> .gitignore
git add .gitignore
git commit -m "Ensure .env files are ignored"
git push origin master
```

#### 1.3 Verify key files exist
```bash
# Should all exist:
ls backend/app.py
ls backend/llm_service.py
ls backend/models_db.py
ls backend/requirements.txt
ls frontend/src/App.jsx
ls frontend/package.json
ls Procfile
```

---

### STEP 2: Deploy Backend to Railway (10 minutes)

#### 2.1 Create Railway Account
1. Go to **https://railway.app**
2. Click "Start Project"
3. Sign in with **GitHub** (one-click)
4. Authorize Railway to access your GitHub account
5. Skip template selection

#### 2.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub"**
3. Find and select your **`b2g`** repository
4. Click **"Deploy Now"**

Railway will start building automatically.

#### 2.3 Configure Environment Variables
1. Wait for build to complete (green ✅)
2. Click on your **"app"** service in Railway dashboard
3. Go to **"Variables"** tab
4. Add these variables (copy from your `backend/.env`):

| Key | Value |
|-----|-------|
| OPENWEATHER_API_KEY | `6276b4473c4ad27bc33a916505b42188` |
| OPENAI_API_KEY | `sk-proj-JmFJsZghpWPS_1Izxhr4...` (your key) |
| LLM_PROVIDER | `openai` |
| FLASK_ENV | `production` |
| DATABASE_URL | Leave empty - Railway auto-creates this |

5. After adding variables, Railway auto-redeploys

#### 2.4 Get Your Backend URL
1. In Railway dashboard, click **"Settings"**
2. Look for **"Domain"** section
3. Copy your URL (looks like: `https://b2g-production-xxx.up.railway.app`)
4. **Save this URL** - you'll need it for frontend

**Check if backend works:**
```
https://your-railway-url/api/health
```
Should return: `{"status": "ok"}`

---

### STEP 3: Deploy Frontend to Vercel (10 minutes)

#### 3.1 Create Vercel Account
1. Go to **https://vercel.com**
2. Click **"Sign up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel
5. Complete setup

#### 3.2 Import Your GitHub Repository
1. In Vercel dashboard, click **"Add New"** → **"Project"**
2. Select **"Import Git Repository"**
3. Find your **`b2g`** repository
4. Click **"Import"**

#### 3.3 Configure Build Settings
1. **Root Directory**: Select **`frontend`** from dropdown
2. **Framework**: Should auto-select **React**
3. **Build Command**: Keep default `npm run build`
4. Click **"Deploy"**

Vercel will build and deploy automatically.

#### 3.4 Add Environment Variables to Vercel
1. Wait for first deployment to complete
2. Click on your project
3. Go to **"Settings"** → **"Environment Variables"**
4. Add this variable:

| Key | Value |
|-----|-------|
| REACT_APP_API_URL | `https://your-railway-url/api` |

**Example:** `https://b2g-production-xxx.up.railway.app/api`

5. Click **"Save"**
6. Redeploy by clicking **"Deployments"** → **"Redeploy"**

#### 3.5 Get Your Frontend URL
1. In Vercel dashboard, look for **"Domains"**
2. Copy your URL (looks like: `https://b2g-xxxxxx.vercel.app`)
3. **This is your public app URL!**

---

### STEP 4: Test Everything Works (5 minutes)

#### 4.1 Test Frontend Loads
```
Open in browser: https://your-vercel-url
```
You should see:
- ✅ Climate-smart agriculture header
- ✅ Weather card
- ✅ Stress prediction form
- ✅ No connection errors

#### 4.2 Test API Connection
```
Open in browser: https://your-railway-url/api/health
```
Should return: `{"status": "ok"}`

#### 4.3 Test Full Flow
1. Go to your Vercel URL
2. Submit a test crop report:
   - Crop type: `rice`
   - Growth stage: `vegetative`
   - Notes: `Test observation for yellowing`
3. You should see:
   - ✅ Stress level prediction
   - ✅ AI analysis from OpenAI
   - ✅ Recommendations appear
   - ✅ No errors in browser console

#### 4.4 Test API Returns Reports
```
Open in browser: https://your-railway-url/api/reports
```
Should return JSON with your submitted report.

---

## 🎯 What You Now Have

| Component | URL | Status |
|-----------|-----|--------|
| Frontend | `https://your-app.vercel.app` | 🟢 Live |
| Backend API | `https://your-api.up.railway.app/api` | 🟢 Live |
| Database | PostgreSQL on Railway | 🟢 Auto-created |
| AI (OpenAI) | Connected | 🟢 Active |
| Weather API | OpenWeatherMap | 🟢 Working |

---

## 📝 Your Deployment URLs

**Copy these and save them:**

Frontend: `https://____________________________`

Backend API: `https://____________________________/api`

---

## 🔄 Making Updates After Deployment

### To update your live app:

#### Option A: Update Frontend
```bash
cd c:\MyProjects\b2g/frontend

# Make changes to your React code

# Commit and push
git add .
git commit -m "Update frontend"
git push origin master
```
Vercel automatically redeploys on push. ✅

#### Option B: Update Backend
```bash
cd c:\MyProjects\b2g/backend

# Make changes to your Python code

# Commit and push
git add .
git commit -m "Update backend"
git push origin master
```
Railway automatically redeploys on push. ✅

#### Option C: Update Environment Variables
- **Railway**: Go to Settings → Variables → Edit → Save (auto-redeploys)
- **Vercel**: Go to Settings → Environment Variables → Edit → Redeploy

---

## ⚠️ Troubleshooting

### Issue: "Backend returns 502 error"
**Solution:**
1. Wait 60 seconds (Railway may be starting)
2. Check Railway logs: Dashboard → Logs tab
3. Verify all environment variables are set
4. Restart service: Settings → Restart

### Issue: "Frontend shows 'Cannot connect to backend'"
**Solution:**
1. Verify `REACT_APP_API_URL` is set in Vercel environment variables
2. Check the URL is correct: `https://your-railway-url/api`
3. Redeploy Vercel: Deployments → Redeploy

### Issue: "OpenAI API returns 401 error"
**Solution:**
1. Verify API key is correct in Railway Variables
2. Check OpenAI account has available balance
3. Regenerate key if needed: https://platform.openai.com/account/api-keys

### Issue: "Database connection error"
**Solution:**
1. Railway auto-creates DATABASE_URL
2. Don't add DATABASE_URL manually - let Railway provision it
3. Restart backend service

### Issue: "Reports not saving"
**Solution:**
1. Check backend logs for SQL errors
2. Verify DATABASE_URL is set (should auto-populate)
3. Run migrations: SSH into Railway and run
   ```bash
   python -c "from models_db import db; db.create_all()"
   ```

---

## 🛡️ Security Checklist

- [ ] `.env` NOT committed to GitHub
- [ ] `.env` in `.gitignore` ✅
- [ ] API keys ONLY in deployment platform secrets
- [ ] OpenWeatherMap key regenerated (was exposed)
- [ ] Database URL never in code (auto-provisioned)
- [ ] HTTPS enforced (Vercel & Railway do this)
- [ ] CORS properly configured in Flask

---

## 📊 Monitoring Your Deployment

### Check Backend Health
```bash
# Every 5 minutes, check status
curl https://your-railway-url/api/health
```

### View Logs

**Railway logs:**
1. Dashboard → Your Project → App → Logs
2. Look for errors or warnings

**Vercel logs:**
1. Dashboard → Your Project → Deployments
2. Click latest deployment → Runtime logs

### Monitor Performance

**Railway:**
- Metrics tab shows CPU, memory, requests

**Vercel:**
- Analytics tab shows page views, response times

---

## 🎉 You're Live!

Your application is now accessible at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-api.up.railway.app`
- **Database**: PostgreSQL (auto-created on Railway)

**Share your frontend URL with users!**

---

## 📚 Next Steps

1. **Monitor**: Check logs daily for first week
2. **Test**: Submit test reports to verify everything works
3. **Optimize**: Enable caching, add monitoring alerts
4. **Scale**: If traffic increases, upgrade Railway/Vercel tiers

---

## 💡 Tips for Success

1. **Always test locally first**
   ```bash
   python app.py          # Backend
   npm start              # Frontend
   ```

2. **Check environment variables**
   - Railway: Settings → Variables
   - Vercel: Settings → Environment Variables

3. **Monitor logs for errors**
   - Railway: Logs tab
   - Vercel: Deployments → Logs

4. **Redeploy if needed**
   - Railway: Settings → Restart
   - Vercel: Deployments → Redeploy

5. **Git workflow**
   - Make changes locally
   - Test with `npm start` + `python app.py`
   - Commit: `git commit -m "message"`
   - Push: `git push origin master`
   - Auto-deploys on push! ✅

---

## 🆘 Still Having Issues?

Check these files in your project:
- `FINAL_DEPLOYMENT_STEPS.md` - Full technical guide
- `SETUP_CHECKLIST.md` - Complete checklist
- `DEPLOYMENT_GUIDE.md` - Architecture details
- `.env.example` files - Configuration reference

---

**Deployment Complete! 🎊**

Your B2G Climate-Smart Agriculture Advisory System is now live and accessible globally.
