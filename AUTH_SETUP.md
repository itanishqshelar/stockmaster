# StockMaster Authentication Setup

## Overview

StockMaster now includes a comprehensive authentication system with:

- User login/signup
- JWT token-based authentication
- Password reset via OTP (email)
- Protected routes (users cannot access app without login)
- Role-based access (staff/manager)

## Backend Changes

### 1. New Dependencies

Added to `requirements.txt`:

```
python-jose[cryptography]  # JWT token handling
passlib[bcrypt]           # Password hashing
email-validator           # Email validation
```

### 2. Updated User Model

`backend/models.py` - User table now includes:

- `hashed_password` - Bcrypt hashed password
- `reset_otp` - 6-digit OTP for password reset
- `otp_expires_at` - OTP expiration timestamp (10 minutes)
- `created_at` - Account creation timestamp

### 3. New Authentication Endpoints

`backend/routers/auth.py`:

- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/forgot-password` - Request OTP for password reset
- `POST /auth/reset-password` - Reset password with OTP
- `GET /auth/me` - Get current user info (requires authentication)

### 4. Authentication Flow

1. User signs up with email, password, full name, and role
2. Password is hashed with bcrypt before storage
3. Login returns JWT token (valid for 30 minutes)
4. Token must be included in Authorization header: `Bearer <token>`
5. Forgot password sends 6-digit OTP to email (10-minute expiry)
6. Reset password validates OTP and updates password

## Frontend Changes

### 1. New Pages

- `frontend/src/pages/Login.tsx` - Login page with forgot password flow
- `frontend/src/pages/Signup.tsx` - User registration page

### 2. Protected Routes

`frontend/src/components/PrivateRoute.tsx`:

- Checks for JWT token in localStorage
- Redirects to login if not authenticated
- Wraps all main app routes (Dashboard, Products, Operations)

### 3. Authentication Flow

1. User lands on login page (no access to app without auth)
2. Can sign up for new account or login with existing credentials
3. On successful login:
   - JWT token saved to localStorage
   - User info saved to localStorage
   - Redirected to dashboard
4. Logout clears localStorage and redirects to login
5. Forgot password flow:
   - Enter email → OTP sent to email
   - Enter OTP + new password → Password reset

### 4. Layout Updates

`frontend/src/components/Layout.tsx`:

- Shows logged-in user's name in sidebar
- Logout button clears session and redirects to login

## Testing

### Default Admin Account

```
Email: admin@stockmaster.com
Password: admin123
Role: manager
```

### Create Additional Users

Use the signup page or run:

```bash
cd backend
python create_admin.py  # Modify script for custom users
```

## Security Notes

### Production Considerations

1. **Change SECRET_KEY**: Update in `backend/routers/auth.py`

   ```python
   SECRET_KEY = "your-secret-key-change-this-in-production"
   ```

2. **Configure Email SMTP**: For production, uncomment and configure email settings in `send_otp_email()` function:

   ```python
   smtp_server = "smtp.gmail.com"
   smtp_port = 587
   sender_email = "your-email@gmail.com"
   sender_password = "your-app-password"  # Use app-specific password
   ```

3. **Use HTTPS**: Always use HTTPS in production for secure token transmission

4. **Environment Variables**: Move sensitive config to `.env` file:
   ```
   SECRET_KEY=your-secret-key
   SMTP_SERVER=smtp.gmail.com
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

### Current Implementation (Development)

- OTP is printed to console (not sent via email)
- Check backend terminal for OTP when testing password reset
- SECRET_KEY is hardcoded (change for production)

## API Usage Examples

### Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "staff"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@stockmaster.com&password=admin123"
```

### Forgot Password

```bash
curl -X POST http://localhost:8000/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@stockmaster.com"}'
```

### Reset Password

```bash
curl -X POST http://localhost:8000/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@stockmaster.com",
    "otp": "123456",
    "new_password": "newpassword123"
  }'
```

### Access Protected Endpoint

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Features

### Login Page

- Email and password fields
- Error handling with user feedback
- "Forgot Password?" link
- Link to signup page
- StockMaster logo with icon

### Signup Page

- Full name, email, password fields
- Password confirmation
- Role selection (staff/manager)
- Password validation (min 6 characters)
- Link to login page
- StockMaster logo with icon

### Forgot Password Flow

- Step 1: Enter email → OTP sent
- Step 2: Enter OTP + new password
- 6-digit OTP validation
- 10-minute expiry for OTP
- Back to login option

### Protected Routes

- All main routes require authentication
- Automatic redirect to login if token missing
- Token persists across browser sessions (localStorage)
- Clean logout functionality

## Running the Application

1. **Start Backend**:

   ```bash
   cd stockmaster
   python -m uvicorn backend.main:app --reload --host 0.0.0.0
   ```

2. **Start Frontend**:

   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application**:

   - Frontend: http://localhost:5174
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **First Login**:
   - Use admin@stockmaster.com / admin123
   - Or create new account via signup page

## Troubleshooting

### Database Schema Issues

If you see column errors, recreate the database:

```bash
cd stockmaster
rm stockmaster.db
python -m uvicorn backend.main:app --reload  # Recreates DB
python backend/create_admin.py  # Recreate admin user
```

### Email Not Sending

- In development, OTP is printed to backend terminal
- Check terminal output when requesting password reset
- For production, configure SMTP settings in auth.py

### Token Expired

- Tokens expire after 30 minutes
- User will be redirected to login automatically
- Login again to get new token

## Next Steps

1. **Email Configuration**: Set up SMTP for production email delivery
2. **Password Requirements**: Add stronger password validation rules
3. **Account Verification**: Add email verification on signup
4. **Session Management**: Add refresh tokens for longer sessions
5. **Admin Panel**: Create admin interface for user management
6. **Audit Logging**: Track authentication events
7. **Two-Factor Auth**: Add 2FA option for enhanced security
