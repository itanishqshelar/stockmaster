# 🚀 StockMaster Deployment Guide

## Quick Overview

Your StockMaster app is now ready for production deployment! All necessary configuration files have been added and pushed to GitHub.

---

## 📦 What's Been Added

### Backend Configuration

✅ `Procfile` - Tells hosting services how to run your backend
✅ `runtime.txt` - Specifies Python version
✅ `railway.json` - Railway-specific configuration
✅ `backend/.env.example` - Template for environment variables
✅ Updated `backend/requirements.txt` - All dependencies included
✅ Updated `backend/main.py` - Production-ready CORS settings
✅ Updated `backend/database.py` - PostgreSQL support
✅ Updated `backend/routers/auth.py` - Uses environment variables

### Frontend Configuration

✅ `frontend/vercel.json` - Vercel deployment settings
✅ `frontend/.env.development` - Development API URL
✅ `frontend/.env.production` - Production API URL (update after backend deploy)
✅ Updated `frontend/src/api.ts` - Uses environment variables
✅ All pages use environment-based API URLs

### Git

✅ All changes committed to main branch
✅ Pushed to GitHub: https://github.com/VedantSawant616/stockmaster
✅ `.env` files properly excluded from version control

---

## 🎯 Deployment Steps

### STEP 1: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose `VedantSawant616/stockmaster`
5. Railway will auto-detect the configuration

6. **Add Environment Variables** in Railway dashboard:

   ```
   SECRET_KEY=your-super-secret-key-at-least-32-characters-long-for-jwt
   ENVIRONMENT=production
   FRONTEND_URL=https://your-app-name.vercel.app
   ```

7. **Add PostgreSQL Database**:

   - In Railway dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL` environment variable

8. **Deploy!** Railway will automatically build and deploy
   - Copy your backend URL (e.g., `https://stockmaster-production.up.railway.app`)

### STEP 2: Deploy Frontend to Vercel

1. **Go to Vercel**: https://vercel.com
2. Click "Add New..." → "Project"
3. Import `VedantSawant616/stockmaster` from GitHub
4. **Configure Project**:

   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

5. **Add Environment Variable**:

   - Key: `VITE_API_URL`
   - Value: `https://your-backend-url.up.railway.app` (from Step 1)

6. Click "Deploy"

### STEP 3: Update Backend CORS

1. Go back to Railway dashboard
2. Update `FRONTEND_URL` environment variable:
   ```
   FRONTEND_URL=https://your-app-name.vercel.app
   ```
3. Railway will automatically redeploy

### STEP 4: Create Admin User

**Option A: Using Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link to your project
railway login
railway link

# Run the admin creation script
railway run python backend/create_admin.py
```

**Option B: Manual Database Access**

1. Go to Railway dashboard → PostgreSQL
2. Click "Connect" → "psql"
3. Run SQL to create admin:

```sql
INSERT INTO users (email, full_name, hashed_password, role, created_at)
VALUES (
  'admin@stockmaster.com',
  'Admin User',
  '$2b$12$...',  -- Use bcrypt to hash 'admin123'
  'manager',
  NOW()
);
```

---

## 🔐 Environment Variables Reference

### Backend (Railway)

| Variable        | Description                | Example                               |
| --------------- | -------------------------- | ------------------------------------- |
| `SECRET_KEY`    | JWT secret key (32+ chars) | `your-random-32-char-secret-key-here` |
| `DATABASE_URL`  | Auto-set by Railway        | `postgresql://user:pass@host/db`      |
| `ENVIRONMENT`   | Deployment environment     | `production`                          |
| `FRONTEND_URL`  | Your Vercel URL            | `https://stockmaster.vercel.app`      |
| `SMTP_SERVER`   | (Optional) Email server    | `smtp.gmail.com`                      |
| `SMTP_PORT`     | (Optional) Email port      | `587`                                 |
| `SMTP_USER`     | (Optional) Email user      | `your@email.com`                      |
| `SMTP_PASSWORD` | (Optional) Email password  | `app-password`                        |

### Frontend (Vercel)

| Variable       | Description | Example                              |
| -------------- | ----------- | ------------------------------------ |
| `VITE_API_URL` | Backend URL | `https://stockmaster.up.railway.app` |

---

## ✅ Testing Production Deployment

1. **Visit your Vercel URL**: `https://your-app.vercel.app`
2. You should see the login page
3. Try to access `/` directly - should redirect to `/login`
4. Create a new account via signup
5. Login with your credentials
6. Check that all features work:
   - Dashboard loads with data
   - Products page works
   - Operations page works
   - Logout works

---

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" error:**

- Check that all dependencies are in `requirements.txt`
- Railway should auto-install them

**Database connection error:**

- Ensure PostgreSQL is added in Railway
- Check `DATABASE_URL` is set

**CORS error in frontend:**

- Update `FRONTEND_URL` in Railway
- Redeploy backend

### Frontend Issues

**"Network Error" or API not connecting:**

- Check `VITE_API_URL` in Vercel settings
- Ensure backend URL is correct (no trailing slash)
- Redeploy frontend after fixing

**404 on page refresh:**

- Should be handled by `vercel.json` rewrites
- If not, check that `vercel.json` is in `frontend/` directory

**Build fails:**

- Check Node.js version in Vercel settings
- Try building locally first: `npm run build`

---

## 📝 Post-Deployment Tasks

### Security

- [ ] Change default admin password after first login
- [ ] Set up email SMTP for password reset in production
- [ ] Enable Railway's automatic SSL (should be default)
- [ ] Enable Vercel's automatic SSL (should be default)

### Monitoring

- [ ] Check Railway logs for backend errors
- [ ] Check Vercel logs for frontend errors
- [ ] Set up Railway alerts for downtime
- [ ] Monitor database size (Railway free tier limit)

### Optional Enhancements

- [ ] Add custom domain to Vercel
- [ ] Add custom domain to Railway
- [ ] Set up automated backups for PostgreSQL
- [ ] Add monitoring service (e.g., Sentry)
- [ ] Enable Railway's Redis for caching (if needed)

---

## 📚 Useful Commands

```bash
# View Railway logs
railway logs

# Open Railway dashboard
railway open

# Connect to production database
railway connect postgres

# Redeploy frontend
# (In Vercel dashboard, go to Deployments → click "..." → Redeploy)

# Check deployment status
railway status
```

---

## 🎉 Success Checklist

- [ ] Backend deployed to Railway
- [ ] PostgreSQL database created and connected
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set correctly
- [ ] Admin user created
- [ ] Login page accessible
- [ ] Can create new users via signup
- [ ] Protected routes working (redirect to login)
- [ ] All main features working (Dashboard, Products, Operations)
- [ ] Logout working

---

## 🆘 Need Help?

**Railway Documentation**: https://docs.railway.app
**Vercel Documentation**: https://vercel.com/docs
**FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

**Common Issues**:

- Railway free tier: $5/month credit, good for testing
- Vercel free tier: Unlimited hobby projects
- Database persistence: Railway PostgreSQL persists data
- File uploads: Consider using cloud storage (S3, Cloudinary)

---

## 🔄 Making Updates

After making code changes:

```bash
# 1. Commit and push to GitHub
git add .
git commit -m "Your update message"
git push origin main

# 2. Railway and Vercel will auto-deploy
# No manual steps needed!
```

---

**Your StockMaster app is deployment-ready! 🚀**

Follow the steps above, and you'll have a fully functional production app in about 15 minutes!
