# Vercel Deployment Quick Start

## Step 1: Deploy Backend (Railway - Recommended)

### 1. Sign up at [Railway.app](https://railway.app)

### 2. Create New Project

- Click "New Project"
- Select "Deploy from GitHub repo"
- Select your `stockmaster` repository

### 3. Configure Backend Service

- Root Directory: Leave empty (Railway will detect backend folder)
- Railway auto-detects Python and installs from requirements.txt

### 4. Add PostgreSQL Database

- In your project, click "New" → "Database" → "PostgreSQL"
- Railway automatically sets `DATABASE_URL` environment variable

### 5. Set Environment Variables

Go to your service → Variables tab and add:

```
SECRET_KEY=<generate-with-command-below>
FRONTEND_URL=https://your-app.vercel.app
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
```

**Generate SECRET_KEY:**

```bash
# On Windows PowerShell
python -c "import secrets; print(secrets.token_hex(32))"

# Or use online generator: https://generate-secret.vercel.app/32
```

### 6. Deploy

- Click "Deploy"
- Wait for deployment to complete
- Copy your backend URL (e.g., `https://stockmaster-production.up.railway.app`)

### 7. Create Admin User

- Once deployed, go to Railway dashboard
- Click your service → "3 dots" → "Open Shell"
- Run: `python backend/create_admin.py`
- Note the admin credentials

---

## Step 2: Deploy Frontend (Vercel)

### 1. Sign up at [Vercel.com](https://vercel.com)

### 2. Import Project

- Click "Add New" → "Project"
- Import your GitHub repository

### 3. Configure Build Settings

- **Framework Preset:** Vite
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### 4. Add Environment Variable

- Go to "Environment Variables"
- Add:
  - **Name:** `VITE_API_URL`
  - **Value:** Your Railway backend URL (e.g., `https://stockmaster-production.up.railway.app`)

### 5. Deploy

- Click "Deploy"
- Wait for deployment (usually 1-2 minutes)
- You'll get a URL like: `https://stockmaster-username.vercel.app`

---

## Step 3: Update Backend CORS

### 1. Go back to Railway

- Go to your backend service → Variables
- Update `FRONTEND_URL` to your Vercel URL
- Click "Redeploy"

---

## Step 4: Test Your Deployment

### 1. Open your Vercel URL

### 2. You should see the login page

### 3. Try creating an account via signup

### 4. Test login with new account or admin credentials

### 5. Test all features:

- Dashboard
- Products (create, search)
- Operations (receipts, deliveries)
- Logout
- Forgot Password (check email)

---

## Gmail App Password Setup (For Password Reset)

### 1. Enable 2-Factor Authentication

- Go to [Google Account Security](https://myaccount.google.com/security)
- Enable "2-Step Verification"

### 2. Create App Password

- Go to "App passwords" (search in settings)
- Select "Mail" and "Other"
- Name it "StockMaster"
- Copy the 16-character password

### 3. Add to Railway Environment Variables

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

### 4. Test Password Reset

- Click "Forgot Password" on login page
- Enter email
- Check inbox for OTP
- Complete password reset

---

## Troubleshooting

### Backend Not Responding

- Check Railway logs for errors
- Verify DATABASE_URL is set
- Check if PostgreSQL is running

### Frontend Can't Connect to Backend

- Verify VITE_API_URL in Vercel matches Railway URL
- Check Railway logs for CORS errors
- Ensure FRONTEND_URL in Railway matches Vercel URL

### Database Errors

- Check if tables are created (Railway logs show this on first deploy)
- Manually create admin user via Railway shell

### Email Not Sending

- Verify Gmail App Password is correct
- Check SMTP settings in Railway
- View Railway logs for email errors

---

## Cost (Free Tiers)

✅ **Vercel:** Free forever for hobby projects
✅ **Railway:** $5 credit/month, deploys ~$0.02/hour
✅ **PostgreSQL:** Included in Railway (1GB free)

**Estimated cost:** ~$3-5/month for small usage

---

## Your Deployment URLs

Fill these in after deployment:

- **Backend (Railway):** `____________________`
- **Frontend (Vercel):** `____________________`
- **Admin Email:** `admin@stockmaster.com`
- **Admin Password:** `admin123` (change after first login!)

---

## Next Steps After Deployment

1. ✅ Change admin password
2. ✅ Set up custom domain (optional)
3. ✅ Configure email notifications
4. ✅ Set up database backups (Railway dashboard)
5. ✅ Monitor application logs
6. ✅ Add more users via signup page

---

## Support

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **Issues:** Check DEPLOYMENT_GUIDE.md for detailed troubleshooting

---

**Congratulations! Your app is live! 🚀**
