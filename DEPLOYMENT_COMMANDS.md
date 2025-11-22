# Deployment Commands Reference

## Local Testing with Production Settings

### Test Backend with PostgreSQL URL Format

```bash
# Set environment variable
$env:DATABASE_URL="sqlite:///./stockmaster.db"  # Test locally first
$env:SECRET_KEY="test-secret-key"
$env:FRONTEND_URL="http://localhost:5174"

# Run backend
cd stockmaster
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Test Frontend with Production API URL

```bash
# Create .env.local for testing
cd frontend
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run frontend
npm run dev
```

---

## Generate Secure SECRET_KEY

### Option 1: Python

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Option 2: PowerShell

```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

### Option 3: Online

Visit: https://generate-secret.vercel.app/32

---

## Railway CLI Commands

### Install Railway CLI

```bash
npm i -g @railway/cli
```

### Login to Railway

```bash
railway login
```

### Link Local Project to Railway

```bash
cd stockmaster
railway link
```

### View Logs

```bash
railway logs
```

### Run Commands in Production

```bash
# Create admin user
railway run python backend/create_admin.py

# Access Python shell
railway run python

# Run database migrations
railway run python backend/migrate.py
```

### Set Environment Variables via CLI

```bash
railway variables set SECRET_KEY="your-secret-key"
railway variables set FRONTEND_URL="https://your-app.vercel.app"
```

### Deploy from CLI

```bash
railway up
```

---

## Vercel CLI Commands

### Install Vercel CLI

```bash
npm i -g vercel
```

### Login to Vercel

```bash
vercel login
```

### Deploy to Preview

```bash
cd frontend
vercel
```

### Deploy to Production

```bash
cd frontend
vercel --prod
```

### Set Environment Variables

```bash
# Interactive
vercel env add VITE_API_URL

# Or directly
vercel env add VITE_API_URL production
# Then enter: https://your-backend.railway.app
```

### View Logs

```bash
vercel logs https://your-app.vercel.app
```

### View Deployments

```bash
vercel ls
```

---

## Database Commands

### Connect to Railway PostgreSQL

```bash
# Get connection string
railway variables

# Connect via psql (if installed)
railway run psql $DATABASE_URL
```

### Create Tables Manually (if needed)

```sql
-- Run in Railway psql or pgAdmin

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'staff',
    reset_otp VARCHAR(6),
    otp_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Backend will auto-create other tables on first run
```

### Backup Database

```bash
# Railway automatically backs up
# Or manual backup:
railway run pg_dump $DATABASE_URL > backup.sql
```

### Restore Database

```bash
railway run psql $DATABASE_URL < backup.sql
```

---

## Git Commands for Deployment

### Ensure Everything is Committed

```bash
git status
git add .
git commit -m "Add production configuration"
git push origin main
```

### Create Production Branch (Optional)

```bash
git checkout -b production
git push origin production

# Configure Railway/Vercel to deploy from this branch
```

---

## Testing Deployment

### Test Backend API

```bash
# Health check
curl https://your-backend.railway.app/health

# Test signup
curl -X POST https://your-backend.railway.app/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User","role":"staff"}'

# Test login
curl -X POST https://your-backend.railway.app/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@stockmaster.com&password=admin123"

# Test protected endpoint (replace TOKEN)
curl https://your-backend.railway.app/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Test Frontend

1. Open https://your-app.vercel.app
2. Open browser DevTools (F12)
3. Check Console for errors
4. Check Network tab for API calls
5. Try login/signup

---

## Troubleshooting Commands

### Check Railway Service Status

```bash
railway status
```

### View Railway Environment Variables

```bash
railway variables
```

### Restart Railway Service

```bash
railway restart
```

### View Vercel Build Logs

```bash
vercel logs --follow
```

### Check Frontend Build Locally

```bash
cd frontend
npm run build
npm run preview
# Opens local preview of production build
```

### Debug CORS Issues

```bash
# Check backend response headers
curl -I https://your-backend.railway.app/health

# Should include:
# Access-Control-Allow-Origin: https://your-app.vercel.app
```

### Check Database Connection

```bash
# Via Railway
railway run python
>>> from backend.database import engine
>>> engine.connect()
# Should not error
```

---

## Update Commands

### Update Backend Code

```bash
git add backend/
git commit -m "Update backend"
git push origin main
# Railway auto-deploys
```

### Update Frontend Code

```bash
git add frontend/
git commit -m "Update frontend"
git push origin main
# Vercel auto-deploys
```

### Update Environment Variables

```bash
# Railway
railway variables set KEY="value"

# Vercel
vercel env add KEY
```

### Force Redeploy

```bash
# Railway
railway up --force

# Vercel
vercel --prod --force
```

---

## Monitoring Commands

### Watch Railway Logs in Real-time

```bash
railway logs --follow
```

### Check Vercel Analytics

```bash
vercel analytics
```

### Monitor Database Size

```bash
railway run psql $DATABASE_URL -c "SELECT pg_size_pretty(pg_database_size(current_database()));"
```

### Check Active Users (if logged)

```bash
railway run psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

---

## Cleanup Commands

### Remove Deployment

```bash
# Vercel
vercel rm your-project-name

# Railway
railway down
```

### Clear Local Build Files

```bash
# Frontend
cd frontend
rm -rf dist node_modules
npm install
npm run build

# Backend
cd backend
rm -rf __pycache__ *.db
```

---

## Quick Deployment Script (PowerShell)

Save as `deploy.ps1`:

```powershell
# Quick deploy script
Write-Host "Deploying StockMaster..." -ForegroundColor Green

# Check git status
Write-Host "Checking git status..." -ForegroundColor Yellow
git status

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git add .
$message = Read-Host "Commit message"
git commit -m $message

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "Done! Railway and Vercel will auto-deploy." -ForegroundColor Green
Write-Host "Check dashboards for deployment status." -ForegroundColor Cyan
```

Run with:

```bash
.\deploy.ps1
```

---

## Emergency Rollback

### Vercel

```bash
# List deployments
vercel ls

# Promote previous deployment
vercel promote <deployment-url>
```

### Railway

```bash
# Redeploy previous commit
git revert HEAD
git push origin main
```

---

## Performance Testing

### Load Test API

```bash
# Install Apache Bench
# Windows: Download from https://www.apachelounge.com/download/

# Test login endpoint
ab -n 100 -c 10 -p login.json -T application/json \
  https://your-backend.railway.app/auth/login
```

### Monitor Response Times

```bash
# Simple check
curl -w "@curl-format.txt" -o /dev/null -s https://your-backend.railway.app/health

# Create curl-format.txt:
echo "time_total: %{time_total}s\n" > curl-format.txt
```

---

**Keep these commands handy for managing your production deployment! 📋**
