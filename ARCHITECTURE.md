# StockMaster Production Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
│                    https://your-app.vercel.app                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VERCEL (Frontend Hosting)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  React + Vite Application                                 │  │
│  │  - Login/Signup Pages                                     │  │
│  │  - Dashboard                                              │  │
│  │  - Products Management                                    │  │
│  │  - Operations                                             │  │
│  │  - Protected Routes (JWT)                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  Environment Variables:                                          │
│  ✓ VITE_API_URL=https://backend.railway.app                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ API Requests
                              │ (Bearer Token Auth)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RAILWAY (Backend Hosting)                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application                                      │  │
│  │  - Authentication (JWT)                                   │  │
│  │  - Product CRUD                                           │  │
│  │  - Warehouse Management                                   │  │
│  │  - Operations (Receipts/Deliveries/Transfers)            │  │
│  │  - Password Reset (OTP via Email)                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  Environment Variables:                                          │
│  ✓ DATABASE_URL=postgresql://...                                │
│  ✓ SECRET_KEY=<secure-random-key>                              │
│  ✓ FRONTEND_URL=https://your-app.vercel.app                    │
│  ✓ SMTP_SERVER=smtp.gmail.com                                  │
│  ✓ SMTP_USER=your-email@gmail.com                              │
│  ✓ SMTP_PASSWORD=<app-password>                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Queries
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              RAILWAY POSTGRESQL (Database)                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tables:                                                  │  │
│  │  - users (email, hashed_password, role, otp)             │  │
│  │  - products (name, sku, category)                        │  │
│  │  - warehouses (name, location)                           │  │
│  │  - inventory (product_id, warehouse_id, quantity)        │  │
│  │  - transactions (type, status, quantity, reference)      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ✓ Automatic backups                                            │
│  ✓ 1GB free tier                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ (Password Reset Flow)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GMAIL SMTP (Email Service)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Sends OTP emails for password reset                     │  │
│  │  - 6-digit OTP                                            │  │
│  │  - 10-minute expiry                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

```
┌─────────┐
│  USER   │
└────┬────┘
     │
     │ 1. Visits site
     ▼
┌─────────────┐
│   Vercel    │
│  (Frontend) │
└────┬────────┘
     │
     │ 2. Not authenticated?
     │ → Redirect to /login
     │
     │ 3. Login Form Submitted
     ▼
┌─────────────┐
│   Railway   │
│  (Backend)  │
└────┬────────┘
     │
     │ 4. Verify credentials
     │ 5. Generate JWT token
     │
     ▼
┌─────────────┐
│ PostgreSQL  │
│ (Database)  │
└─────────────┘
     │
     │ 6. Return token + user info
     ▼
┌─────────────┐
│   Vercel    │
│  (Frontend) │
└────┬────────┘
     │
     │ 7. Store token in localStorage
     │ 8. Redirect to Dashboard
     │
     │ 9. All API requests include:
     │    Authorization: Bearer <token>
     ▼
   SUCCESS!
```

## Password Reset Flow

```
1. User clicks "Forgot Password"
   ↓
2. Enters email
   ↓
3. Backend generates 6-digit OTP
   ↓
4. OTP saved to database (10-min expiry)
   ↓
5. Email sent via Gmail SMTP
   ↓
6. User receives email with OTP
   ↓
7. User enters OTP + new password
   ↓
8. Backend validates OTP & expiry
   ↓
9. Password updated in database
   ↓
10. OTP cleared from database
    ↓
  SUCCESS!
```

## Security Layers

```
┌────────────────────────────────────────────┐
│  1. HTTPS (TLS/SSL)                       │ ← Vercel Auto
│     All traffic encrypted                  │
└────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────┐
│  2. JWT Token Authentication              │ ← 30-min expiry
│     Bearer token in headers                │
└────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────┐
│  3. CORS Policy                           │ ← Whitelist origins
│     Only allow Vercel frontend            │
└────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────┐
│  4. Password Hashing (Bcrypt)             │ ← Never store plain
│     Salt + hash all passwords              │
└────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────┐
│  5. OTP Expiry (10 minutes)               │ ← Time-limited
│     Single-use tokens                      │
└────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────┐
│  6. Environment Variables                  │ ← No hardcoded secrets
│     All secrets in env vars                │
└────────────────────────────────────────────┘
```

## Deployment Checklist

### Before Deployment

- [ ] Update `.env.example` files
- [ ] Generate secure SECRET_KEY
- [ ] Configure Gmail App Password
- [ ] Test locally with environment variables

### Railway Deployment

- [ ] Create Railway account
- [ ] Deploy backend from GitHub
- [ ] Add PostgreSQL database
- [ ] Set all environment variables
- [ ] Create admin user via Railway shell
- [ ] Test API endpoints (use /docs)

### Vercel Deployment

- [ ] Create Vercel account
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Add VITE_API_URL environment variable
- [ ] Deploy and get production URL

### Post-Deployment

- [ ] Update Railway FRONTEND_URL with Vercel URL
- [ ] Test login/signup
- [ ] Test password reset email
- [ ] Test all CRUD operations
- [ ] Change default admin password
- [ ] Set up database backups
- [ ] Monitor logs for errors

## Monitoring

### Railway Dashboard

- View real-time logs
- Monitor CPU/Memory usage
- Check database connections
- View deployment history

### Vercel Dashboard

- View build logs
- Monitor bandwidth usage
- Check function invocations
- View error reports

### Application Health

- Test login flow daily
- Verify email delivery
- Check database queries
- Monitor response times

## Scaling Considerations

### Current Setup (Free Tier)

- Good for: 100-1000 users
- Database: 1GB storage
- Backend: Shared resources
- Frontend: Unlimited bandwidth

### When to Upgrade

- Database > 1GB
- Slow response times
- High concurrent users
- Need 99.9% uptime

### Upgrade Path

1. Railway: $5/month → $20/month (dedicated resources)
2. Database: Upgrade storage/connections
3. Add Redis for caching
4. Implement load balancing
5. Add CDN for static assets

---

**Your StockMaster app is production-ready with enterprise-grade authentication! 🔐**
