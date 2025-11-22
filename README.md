# StockMaster - Inventory Management System

A full-stack inventory management system with **authentication**, product tracking, warehouse management, and operations handling.

## 🚀 Features

- ✅ **Secure Authentication** (JWT + Password Reset via OTP)
- ✅ **Product Management** (CRUD with search)
- ✅ **Warehouse Management** (Multiple locations)
- ✅ **Operations Tracking** (Receipts, Deliveries, Transfers, Adjustments)
- ✅ **Real-time Dashboard** (KPIs, Recent Activity)
- ✅ **Status Workflows** (Order → In Transit → Completed)
- ✅ **Role-based Access** (Staff/Manager)
- ✅ **Production Ready** (Deployable to Vercel + Railway)

## 📚 Tech Stack

- **Frontend:** React 19 + Vite + TypeScript + Tailwind CSS
- **Backend:** FastAPI (Python) + SQLAlchemy
- **Database:** PostgreSQL (production) / SQLite (development)
- **Auth:** JWT Tokens + Bcrypt Password Hashing
- **Email:** SMTP (Gmail for OTP)
- **Hosting:** Vercel (frontend) + Railway (backend)

## 📖 Documentation

- **[AUTH_SETUP.md](./AUTH_SETUP.md)** - Authentication system details
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Complete deployment guide
- **[QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** - Quick start deployment
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture diagrams
- **[DEPLOYMENT_COMMANDS.md](./DEPLOYMENT_COMMANDS.md)** - CLI commands reference
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Feature implementation details

## 🏃 Quick Start (Local Development)

### Prerequisites

- Python 3.12+
- Node.js 18+
- Git

### Backend Setup

```bash
cd stockmaster

# Create virtual environment
python -m venv backend/venv

# Activate (Windows)
.\backend\venv\Scripts\Activate

# Install dependencies
pip install -r backend/requirements.txt

# Create admin user
python backend/create_admin.py

# Run backend
python -m uvicorn backend.main:app --reload --host 0.0.0.0
```

Backend runs on: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on: http://localhost:5174

### Default Login

```
Email: admin@stockmaster.com
Password: admin123
```

## 🌐 Production Deployment

### Quick Deploy (5 minutes)

1. **Deploy Backend to Railway:**

   - Sign up at [Railway.app](https://railway.app)
   - Create new project from GitHub
   - Add PostgreSQL database
   - Set environment variables (see QUICK_DEPLOY.md)
   - Deploy and copy backend URL

2. **Deploy Frontend to Vercel:**

   - Sign up at [Vercel.com](https://vercel.com)
   - Import GitHub repository
   - Set root directory: `frontend`
   - Add env var: `VITE_API_URL=<your-railway-url>`
   - Deploy and get your production URL

3. **Update Backend CORS:**
   - Go to Railway → Variables
   - Set `FRONTEND_URL=<your-vercel-url>`
   - Redeploy

**See [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) for step-by-step instructions.**

## 🔐 Authentication Features

- **Signup:** Create account with email, password, name, role
- **Login:** JWT token-based authentication (30-min expiry)
- **Logout:** Clear session and redirect
- **Forgot Password:** OTP sent to email (10-min expiry)
- **Protected Routes:** Cannot access app without login
- **Token Refresh:** Auto-redirect to login on token expiry

## 🗄️ Database Schema

```
users
├─ id, email, full_name
├─ hashed_password, role
└─ reset_otp, otp_expires_at

products
├─ id, name, sku
├─ category, unit_of_measure
└─ inventory (via relationship)

warehouses
├─ id, name, location
└─ inventory (via relationship)

inventory
├─ id, product_id, warehouse_id
└─ quantity

transactions
├─ id, product_id, warehouse_id
├─ transaction_type, status
├─ quantity, reference, notes
└─ timestamp
```

## 📝 API Endpoints

### Authentication

- `POST /auth/signup` - Create account
- `POST /auth/login` - Login (returns JWT)
- `POST /auth/forgot-password` - Request OTP
- `POST /auth/reset-password` - Reset with OTP
- `GET /auth/me` - Get current user (protected)

### Products

- `GET /products/` - List all products
- `POST /products/` - Create product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Warehouses

- `GET /warehouses/` - List warehouses
- `POST /warehouses/` - Create warehouse
- `GET /warehouses/inventory` - Get inventory summary

### Operations

- `POST /operations/receipts/` - Create receipt
- `POST /operations/deliveries/` - Create delivery
- `POST /operations/transfers/` - Create transfer
- `POST /operations/adjustments/` - Create adjustment
- `PATCH /operations/{id}/status` - Update status
- `GET /operations/recent/` - Get recent activity

**Full API docs:** http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

**Backend (.env):**

```env
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=<generate-with-openssl-rand-hex-32>
FRONTEND_URL=https://your-app.vercel.app
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<gmail-app-password>
```

**Frontend (.env.production):**

```env
VITE_API_URL=https://your-backend.railway.app
```

## 🧪 Testing

```bash
# Backend tests (if implemented)
cd backend
pytest

# Frontend tests (if implemented)
cd frontend
npm test

# Manual testing
- Try signup with new email
- Login with created account
- Test forgot password flow
- Create products and warehouses
- Perform operations
- Check dashboard updates
```

## 📦 Project Structure

```
stockmaster/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB configuration
│   ├── create_admin.py      # Admin user script
│   ├── seed_data.py         # Sample data
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Railway deploy config
│   ├── .env.example        # Environment template
│   └── routers/
│       ├── auth.py         # Authentication
│       ├── products.py     # Product CRUD
│       ├── warehouses.py   # Warehouse CRUD
│       └── operations.py   # Operations handling
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main app + routing
│   │   ├── api.ts           # API client
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Products.tsx
│   │   │   └── Operations.tsx
│   │   └── components/
│   │       ├── Layout.tsx
│   │       ├── PrivateRoute.tsx
│   │       └── OperationModal.tsx
│   ├── package.json
│   ├── vercel.json         # Vercel config
│   ├── .env.production     # Production API URL
│   └── .env.development    # Development API URL
│
└── Documentation/
    ├── AUTH_SETUP.md
    ├── DEPLOYMENT_GUIDE.md
    ├── QUICK_DEPLOY.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT_COMMANDS.md
```

## 🛠️ Development

### Adding New Features

1. **Backend:** Add router in `backend/routers/`
2. **Frontend:** Add page in `frontend/src/pages/`
3. **Update API client:** Add functions in `frontend/src/api.ts`
4. **Add route:** Update `frontend/src/App.tsx`

### Database Migrations

```bash
# Currently using SQLAlchemy auto-create
# For production migrations, consider Alembic:
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "message"
alembic upgrade head
```

## 🚨 Troubleshooting

### Backend won't start

- Check Python version (3.12+)
- Activate virtual environment
- Install all requirements
- Check DATABASE_URL format

### Frontend can't connect to backend

- Verify VITE_API_URL is set
- Check CORS configuration
- Ensure backend is running

### Authentication errors

- Check SECRET_KEY is set
- Verify JWT token format
- Check token expiry (30 minutes)

### Email not sending

- Configure Gmail App Password
- Set SMTP environment variables
- Check Railway logs for email errors

**See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed troubleshooting.**

## 📈 Future Enhancements

- [ ] Add unit tests (pytest, vitest)
- [ ] Implement refresh tokens
- [ ] Add email verification on signup
- [ ] Create admin panel for user management
- [ ] Add audit logging
- [ ] Implement 2FA
- [ ] Add real-time notifications
- [ ] Create mobile app (React Native)
- [ ] Add analytics dashboard
- [ ] Implement barcode scanning

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Vedant Sawant**

- GitHub: [@VedantSawant616](https://github.com/VedantSawant616)

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- React + Vite for lightning-fast frontend
- Railway for easy backend hosting
- Vercel for seamless frontend deployment

---

**Built with ❤️ by Vedant Sawant**
