# StockMaster Vercel Deployment Guide

## Overview

This guide covers deploying StockMaster with production authentication to Vercel (frontend) and a backend hosting service.

## Architecture

```
Frontend (Vercel) → Backend (Railway/Render/Fly.io) → PostgreSQL Database
```

## Prerequisites

- GitHub account (for Vercel deployment)
- Vercel account (free tier works)
- Backend hosting account (Railway/Render/Fly.io)
- PostgreSQL database (can use provider's free tier)

---

## Part 1: Prepare Backend for Production

### 1.1 Update Backend for PostgreSQL

The current SQLite database won't work for production. Update to PostgreSQL:

**Install PostgreSQL adapter:**

```bash
cd backend
pip install psycopg2-binary
pip freeze > requirements.txt
```

**Update `backend/database.py`:**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./stockmaster.db"
)

# Fix for some PostgreSQL connection strings
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 1.2 Environment Variables

**Create `backend/.env.example`:**

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-change-in-production
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FRONTEND_URL=https://your-app.vercel.app
```

### 1.3 Update CORS for Production

**Update `backend/main.py`:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware
import os

load_dotenv()

app = FastAPI(title="StockMaster API")

# Production CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rest of your code...
```

### 1.4 Update Auth Router for Production

**Update `backend/routers/auth.py`:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variable for secret key
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

**Update `send_otp_email()` function for production:**

```python
def send_otp_email(to_email: str, otp: str):
    """Send OTP to user's email"""
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_USER")
    sender_password = os.getenv("SMTP_PASSWORD")

    # In development, print to console
    if not all([smtp_server, sender_email, sender_password]):
        print(f"[DEV] OTP for {to_email}: {otp}")
        return

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = "StockMaster - Password Reset OTP"

        body = f"""
        Hello,

        Your OTP for password reset is: {otp}

        This OTP will expire in 10 minutes.

        If you didn't request this, please ignore this email.

        Best regards,
        StockMaster Team
        """
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        print(f"OTP sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        # Fallback to console in case of email failure
        print(f"[FALLBACK] OTP for {to_email}: {otp}")
```

### 1.5 Create Procfile for Backend Hosting

**Create `backend/Procfile`:**

```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### 1.6 Create runtime.txt (optional, for Python version)

**Create `backend/runtime.txt`:**

```
python-3.12.0
```

---

## Part 2: Deploy Backend

### Option A: Railway (Recommended - Easiest)

1. **Go to [Railway.app](https://railway.app)**
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub and select `stockmaster` repo
5. Select root path: `/backend`
6. Railway will auto-detect Python and install dependencies

**Add PostgreSQL Database:**

1. In your project, click "New" → "Database" → "PostgreSQL"
2. Railway automatically sets `DATABASE_URL` environment variable

**Set Environment Variables:**

1. Go to project settings → Variables
2. Add:

   ```
   SECRET_KEY=generate-a-secure-random-string-here
   FRONTEND_URL=https://your-app.vercel.app
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

3. Click "Deploy" - Railway will build and deploy
4. Copy your backend URL (e.g., `https://stockmaster-backend.up.railway.app`)

### Option B: Render

1. **Go to [Render.com](https://render.com)**
2. Click "New +" → "Web Service"
3. Connect GitHub repo
4. Settings:
   - Name: `stockmaster-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

**Add PostgreSQL:**

1. Create new PostgreSQL database in Render
2. Copy connection string

**Environment Variables:**
Same as Railway above

### Option C: Fly.io

1. **Install Fly CLI:**

   ```bash
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login and launch:**

   ```bash
   cd backend
   fly auth login
   fly launch
   ```

3. Follow prompts to configure and deploy

---

## Part 3: Prepare Frontend for Vercel

### 3.1 Update API URL for Production

**Create `frontend/.env.production`:**

```env
VITE_API_URL=https://your-backend-url.railway.app
```

**Create `frontend/.env.development`:**

```env
VITE_API_URL=http://localhost:8000
```

### 3.2 Update API Client

**Update `frontend/src/api.ts`:**

```typescript
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors (token expired)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 3.3 Update Login and Signup Pages

**Update both files to use environment variable:**

Replace:

```typescript
const API_URL = "http://localhost:8000";
```

With:

```typescript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

**Files to update:**

- `frontend/src/pages/Login.tsx`
- `frontend/src/pages/Signup.tsx`

### 3.4 Create Vercel Configuration

**Create `frontend/vercel.json`:**

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## Part 4: Deploy Frontend to Vercel

### 4.1 Deploy via Vercel Dashboard

1. **Go to [Vercel.com](https://vercel.com)**
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:

   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

5. **Add Environment Variable:**

   - Key: `VITE_API_URL`
   - Value: `https://your-backend-url.railway.app` (from Part 2)

6. Click "Deploy"

### 4.2 Deploy via Vercel CLI (Alternative)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Follow prompts
# Set root directory: ./
# Build command: npm run build
# Output directory: dist

# Set environment variable
vercel env add VITE_API_URL
# Enter your backend URL when prompted

# Deploy to production
vercel --prod
```

---

## Part 5: Post-Deployment Setup

### 5.1 Update Backend CORS

Once you have your Vercel URL, update backend environment variables:

**On Railway/Render:**

```
FRONTEND_URL=https://your-app.vercel.app
```

Redeploy backend if needed.

### 5.2 Create Admin User in Production

**Connect to your production database and run:**

Via Railway CLI:

```bash
railway run python backend/create_admin.py
```

Via Render:

```bash
# SSH into your Render service
python backend/create_admin.py
```

Or manually via database GUI (like pgAdmin):

```sql
-- Hash the password first using bcrypt
-- Then insert:
INSERT INTO users (email, full_name, hashed_password, role, created_at)
VALUES (
  'admin@stockmaster.com',
  'Admin User',
  '$2b$12$...',  -- bcrypt hash of 'admin123'
  'manager',
  NOW()
);
```

### 5.3 Test Production Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Should see login page
3. Try signing up with a new account
4. Test login, logout, forgot password
5. Access dashboard and verify all features work

---

## Part 6: Gmail SMTP Setup (for Password Reset)

### 6.1 Create App Password

1. Go to [Google Account](https://myaccount.google.com)
2. Security → 2-Step Verification (enable if not already)
3. App Passwords → Select app: "Mail" → Select device: "Other"
4. Name it "StockMaster"
5. Copy the generated 16-character password

### 6.2 Add to Environment Variables

**Backend environment variables:**

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

### 6.3 Test Email Sending

1. Use "Forgot Password" on your production site
2. Check email inbox for OTP
3. Verify OTP works for password reset

---

## Part 7: Security Checklist

### Production Security

- [ ] Change `SECRET_KEY` to a secure random string (use: `openssl rand -hex 32`)
- [ ] Set strong `SECRET_KEY` in backend environment variables
- [ ] Enable HTTPS (Vercel does this automatically)
- [ ] Set proper CORS origins (no wildcards in production)
- [ ] Use environment variables for all secrets
- [ ] Enable database SSL connections
- [ ] Set up database backups
- [ ] Add rate limiting to auth endpoints (future enhancement)
- [ ] Enable security headers in Vercel
- [ ] Monitor logs for suspicious activity

### Optional Enhancements

- [ ] Add Sentry for error tracking
- [ ] Set up custom domain
- [ ] Add analytics (Vercel Analytics)
- [ ] Set up CI/CD for automatic deployments
- [ ] Add database migration tool (Alembic)
- [ ] Implement refresh tokens
- [ ] Add email verification on signup
- [ ] Set up monitoring/uptime checks

---

## Part 8: Custom Domain (Optional)

### 8.1 Add Domain to Vercel

1. Go to Vercel project → Settings → Domains
2. Add your domain (e.g., `stockmaster.yourdomain.com`)
3. Follow DNS configuration instructions

### 8.2 Update Environment Variables

Update `FRONTEND_URL` in backend to use custom domain:

```
FRONTEND_URL=https://stockmaster.yourdomain.com
```

---

## Troubleshooting

### Backend Issues

**Database Connection Errors:**

- Check `DATABASE_URL` format
- Ensure database is running
- Check firewall rules allow connections

**CORS Errors:**

- Verify `FRONTEND_URL` matches your Vercel URL exactly
- Check CORS middleware configuration
- Clear browser cache

**500 Internal Server Errors:**

- Check backend logs in Railway/Render dashboard
- Verify all environment variables are set
- Check database connection

### Frontend Issues

**API Not Connecting:**

- Verify `VITE_API_URL` is set in Vercel
- Check backend is running
- Inspect browser console for errors

**Build Fails:**

- Check Node version compatibility
- Run `npm install` locally to verify
- Check build logs in Vercel

**Blank Page After Deployment:**

- Check `vercel.json` rewrites configuration
- Verify build output directory is correct (`dist`)
- Check browser console for errors

---

## Commands Quick Reference

### Backend Deployment (Railway)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run command in production
railway run python backend/create_admin.py
```

### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod

# View logs
vercel logs

# View deployments
vercel ls
```

---

## Cost Estimates (Free Tiers)

- **Vercel:** Free for hobby projects
- **Railway:** $5/month credit, ~$0.02/hour for small apps
- **Render:** Free tier available (sleeps after inactivity)
- **PostgreSQL:** Free tier: 1GB storage (Railway/Render)

---

## Support

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **Render Docs:** https://render.com/docs

---

## Success Checklist

After completing deployment:

- [ ] Frontend accessible at Vercel URL
- [ ] Backend API responding at Railway/Render URL
- [ ] Login page loads correctly
- [ ] Can create new account via signup
- [ ] Can login with credentials
- [ ] JWT token persists across page reloads
- [ ] Protected routes redirect to login when not authenticated
- [ ] Logout works correctly
- [ ] Forgot password sends OTP to email
- [ ] Password reset with OTP works
- [ ] Dashboard displays data correctly
- [ ] Products page loads and works
- [ ] Operations page functions properly
- [ ] All CRUD operations work
- [ ] No CORS errors in browser console

---

**Congratulations! Your StockMaster application is now live in production! 🎉**
