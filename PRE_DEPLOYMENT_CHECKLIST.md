# Pre-Deployment Checklist

Use this checklist before deploying to production to ensure everything is configured correctly.

## ✅ Code Preparation

### Backend

- [ ] All routes are working locally
- [ ] Database models are finalized
- [ ] Authentication is tested (signup, login, logout, password reset)
- [ ] Error handling is implemented
- [ ] Sensitive data is in environment variables (no hardcoded secrets)
- [ ] `requirements.txt` is up to date
- [ ] `.env.example` is created with all required variables
- [ ] `Procfile` exists for Railway deployment
- [ ] CORS origins configured for production
- [ ] Database URL supports PostgreSQL format
- [ ] Email SMTP configured (or will configure in production)

### Frontend

- [ ] All pages render correctly
- [ ] Protected routes redirect to login
- [ ] API client uses environment variable for base URL
- [ ] `.env.production` is created
- [ ] `.env.development` is created
- [ ] `vercel.json` is configured
- [ ] No console.log statements in production code (or are intentional)
- [ ] Build command works: `npm run build`
- [ ] Preview build works: `npm run preview`

### Git Repository

- [ ] All code is committed
- [ ] `.gitignore` excludes sensitive files (.env, venv/, node_modules/)
- [ ] README is updated
- [ ] Repository is pushed to GitHub
- [ ] Repository is public (or Vercel/Railway have access)

## 🔐 Security Checklist

- [ ] Generate secure SECRET_KEY (32+ characters)
- [ ] No passwords or API keys in code
- [ ] Environment variables documented in .env.example
- [ ] CORS configured with specific origins (no wildcards)
- [ ] Password hashing implemented (bcrypt)
- [ ] JWT token expiry set (30 minutes recommended)
- [ ] OTP expiry set (10 minutes)
- [ ] HTTPS will be enforced (Vercel does this automatically)
- [ ] SQL injection protected (using SQLAlchemy ORM)
- [ ] XSS protected (React escapes by default)

## 📧 Email Setup

- [ ] Gmail account created or ready
- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password generated for Gmail
- [ ] SMTP settings ready:
  - Server: smtp.gmail.com
  - Port: 587
  - User: your-email@gmail.com
  - Password: 16-character app password

## 🗄️ Database Preparation

- [ ] Decision made: Railway PostgreSQL or external provider
- [ ] Understand that SQLite won't work in production
- [ ] Know that Railway will auto-create DATABASE_URL
- [ ] Plan for database backups (Railway has auto-backup)
- [ ] Initial data/seed strategy decided

## 🎯 Deployment Accounts

- [ ] GitHub account created
- [ ] Railway account created
- [ ] Vercel account created
- [ ] GitHub repository linked to both platforms
- [ ] Payment method added (if needed, though free tier available)

## 📝 Environment Variables Prepared

### Backend (Railway)

```
✓ SECRET_KEY=_________________________
✓ FRONTEND_URL=_______________________
✓ SMTP_SERVER=smtp.gmail.com
✓ SMTP_PORT=587
✓ SMTP_USER=_________________________
✓ SMTP_PASSWORD=_____________________
□ DATABASE_URL (Railway auto-sets)
```

### Frontend (Vercel)

```
✓ VITE_API_URL=_______________________
```

## 🧪 Local Testing Before Deploy

- [ ] Backend starts without errors
- [ ] Frontend connects to backend
- [ ] Can create new user account
- [ ] Can login with created account
- [ ] JWT token is stored in localStorage
- [ ] Protected routes require authentication
- [ ] Logout works correctly
- [ ] Forgot password generates OTP (check console)
- [ ] Password reset works with OTP
- [ ] Can create products
- [ ] Can create warehouses
- [ ] Can perform operations
- [ ] Dashboard shows recent activity
- [ ] All CRUD operations work

## 📊 Deployment Steps Order

1. **Railway Backend First**

   - [ ] Deploy backend
   - [ ] Add PostgreSQL database
   - [ ] Set environment variables
   - [ ] Create admin user
   - [ ] Test API endpoints (/docs)
   - [ ] Note backend URL

2. **Vercel Frontend Second**

   - [ ] Deploy frontend
   - [ ] Set VITE_API_URL to Railway backend
   - [ ] Note frontend URL
   - [ ] Test if site loads

3. **Update Backend CORS**
   - [ ] Update FRONTEND_URL in Railway
   - [ ] Redeploy backend
   - [ ] Test login flow end-to-end

## 🔍 Post-Deployment Testing

- [ ] Frontend loads at Vercel URL
- [ ] Login page displays correctly
- [ ] Can create new account
- [ ] Receive email confirmation (if implemented)
- [ ] Can login with new account
- [ ] JWT token persists across page reload
- [ ] Dashboard loads with no errors
- [ ] Products page works
- [ ] Operations page works
- [ ] Can logout successfully
- [ ] Forgot password sends email to inbox
- [ ] Password reset with OTP works
- [ ] No CORS errors in browser console
- [ ] No 500 errors from backend
- [ ] All images/assets load
- [ ] Mobile responsive (test on phone)

## 📈 Monitoring Setup

- [ ] Railway logs accessible
- [ ] Vercel logs accessible
- [ ] Database monitoring enabled
- [ ] Error tracking configured (optional: Sentry)
- [ ] Uptime monitoring configured (optional: UptimeRobot)

## 📚 Documentation

- [ ] README.md updated with production URLs
- [ ] AUTH_SETUP.md reviewed
- [ ] DEPLOYMENT_GUIDE.md available
- [ ] Admin credentials documented securely
- [ ] API documentation accessible (/docs)

## 🚀 Launch Readiness

- [ ] All above checkboxes checked
- [ ] Stakeholders notified of launch
- [ ] Support plan in place
- [ ] Rollback plan understood
- [ ] Performance baselines noted
- [ ] Budget confirmed (free tier or paid)

## 🎉 Post-Launch

- [ ] Change default admin password
- [ ] Create additional admin users if needed
- [ ] Test with real users
- [ ] Monitor logs for first 24 hours
- [ ] Respond to any errors quickly
- [ ] Gather user feedback
- [ ] Plan for future enhancements

---

## Common Issues Checklist

### If Backend Won't Deploy

- [ ] Check Railway logs for errors
- [ ] Verify requirements.txt includes all packages
- [ ] Check Python version matches runtime.txt
- [ ] Ensure Procfile command is correct
- [ ] Verify DATABASE_URL is set

### If Frontend Won't Deploy

- [ ] Check Vercel build logs
- [ ] Verify package.json has correct scripts
- [ ] Check if build completes locally
- [ ] Ensure root directory set to `frontend`
- [ ] Verify output directory is `dist`

### If Can't Login

- [ ] Check backend logs for errors
- [ ] Verify JWT token is generated
- [ ] Check if token is stored in localStorage
- [ ] Verify CORS allows frontend origin
- [ ] Check network tab for 401/403 errors

### If Email Not Sending

- [ ] Verify Gmail App Password is correct
- [ ] Check SMTP environment variables
- [ ] Look for email errors in backend logs
- [ ] Confirm email address is valid
- [ ] Check spam folder

---

**Print this checklist and check off items as you complete them! ✓**

**Ready to deploy? Follow [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)!**
