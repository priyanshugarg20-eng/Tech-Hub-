# Aiqube School Management System - Local Development Guide

Complete guide to run the Aiqube School Management System locally with frontend and backend connection.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Manual Setup](#manual-setup)
4. [Frontend-Backend Connection](#frontend-backend-connection)
5. [Database Setup](#database-setup)
6. [Environment Configuration](#environment-configuration)
7. [Running the Application](#running-the-application)
8. [Testing the Connection](#testing-the-connection)
9. [Troubleshooting](#troubleshooting)
10. [Development Workflow](#development-workflow)

## 🔧 Prerequisites

### Required Software
- **Python**: 3.12+ 
- **Node.js**: 18+ LTS
- **Git**: Latest version
- **PostgreSQL**: 13+ (or SQLite for development)
- **Redis**: 6+ (optional for development)

### System Requirements
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 2GB+ free space
- **OS**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+

### Verify Installations
```bash
# Check Python version
python --version  # Should be 3.12+

# Check Node.js version
node --version    # Should be 18+

# Check Git version
git --version

# Check if PostgreSQL is installed
psql --version
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

#### For Linux/macOS:
```bash
# Make script executable
chmod +x quick-start.sh

# Run the setup script
./quick-start.sh
```

#### For Windows:
```bash
# Run the batch file
quick-start.bat
```

### Option 2: Manual Setup
Follow the detailed manual setup instructions below.

## 🛠️ Manual Setup

### Step 1: Clone and Setup Repository

```bash
# Clone the repository
git clone https://github.com/priyanshugarg20-eng/Tech-Hub-.git
cd Tech-Hub-

# Checkout the correct branch
git checkout cursor/develop-school-management-saas-platform-a4c4
```

### Step 2: Backend Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

### Step 4: Database Setup

#### Option A: PostgreSQL (Recommended for full features)

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE aiqube_sms;
CREATE USER aiqube_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE aiqube_sms TO aiqube_user;
\q
```

#### Option B: SQLite (Simpler for development)

```bash
# SQLite is included with Python, no additional setup needed
# The application will automatically use SQLite if PostgreSQL is not configured
```

### Step 5: Environment Configuration

#### Backend Environment (.env file in root directory)

Create `.env` file in the root directory:

```env
# Database Configuration
# For PostgreSQL:
DATABASE_URL=postgresql://aiqube_user:your_password@localhost:5432/aiqube_sms
# For SQLite (development):
# DATABASE_URL=sqlite:///./aiqube_sms.db

# Security
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
ALLOWED_HOSTS=["*"]
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Optional: Email Configuration
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password

# Optional: AI Configuration
# HUGGINGFACE_API_KEY=your-huggingface-api-key

# Optional: Redis Configuration
# REDIS_URL=redis://localhost:6379
```

#### Frontend Environment (.env file in frontend directory)

Create `.env` file in the `frontend` directory:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Aiqube SMS
REACT_APP_VERSION=1.0.0

# Feature Flags
REACT_APP_ENABLE_AI=true
REACT_APP_ENABLE_ADVANCED_FEATURES=true
REACT_APP_ENABLE_ANALYTICS=true

# Development Settings
REACT_APP_DEBUG=true
```

### Step 6: Initialize Database

```bash
# Activate virtual environment (if not already activated)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Run database migrations
alembic upgrade head

# Create initial data (optional)
python scripts/create_initial_data.py
```

## 🔗 Frontend-Backend Connection

### Connection Architecture

```
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐
│   Frontend      │ ◄──────────────► │    Backend      │
│   (React)       │                  │   (FastAPI)     │
│   Port: 3000    │                  │   Port: 8000    │
└─────────────────┘                  └─────────────────┘
         │                                      │
         │                                      │
         ▼                                      ▼
┌─────────────────┐                  ┌─────────────────┐
│   Browser       │                  │   Database      │
│   (localhost)   │                  │   (PostgreSQL)  │
└─────────────────┘                  └─────────────────┘
```

### API Configuration

The frontend connects to the backend through:

1. **Base URL**: `http://localhost:8000` (development)
2. **API Endpoints**: `/api/v1/...`
3. **Authentication**: JWT tokens
4. **CORS**: Configured for local development

### Connection Verification

#### Backend Health Check
```bash
# Test backend directly
curl http://localhost:8000/health
# Expected response: {"status": "healthy", "timestamp": ...}
```

#### Frontend API Connection
```bash
# Test from frontend
curl http://localhost:3000/api/health
# Should proxy to backend
```

## 🗄️ Database Setup

### PostgreSQL Setup (Recommended)

```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt install postgresql postgresql-contrib

# macOS:
brew install postgresql

# Windows:
# Download from https://www.postgresql.org/download/windows/

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql    # macOS

# Create database
sudo -u postgres psql
CREATE DATABASE aiqube_sms;
CREATE USER aiqube_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE aiqube_sms TO aiqube_user;
ALTER USER aiqube_user CREATEDB;
\q
```

### SQLite Setup (Simpler for development)

```bash
# No additional setup needed
# The application will automatically create SQLite database
# Database file will be created at: ./aiqube_sms.db
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Check migration status
alembic current

# Create new migration (if needed)
alembic revision --autogenerate -m "Description of changes"
```

## ⚙️ Environment Configuration

### Backend Environment Variables

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `DATABASE_URL` | Database connection string | Yes | - | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | JWT secret key | Yes | - | `your-super-secret-key` |
| `DEBUG` | Debug mode | No | `False` | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | No | `["*"]` | `["localhost", "127.0.0.1"]` |
| `CORS_ORIGINS` | CORS origins | No | `["http://localhost:3000"]` | `["http://localhost:3000"]` |
| `UPLOAD_DIR` | Upload directory | No | `uploads` | `uploads` |
| `MAX_FILE_SIZE` | Max file size | No | `10485760` | `10485760` |

### Frontend Environment Variables

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `REACT_APP_API_URL` | Backend API URL | Yes | - | `http://localhost:8000` |
| `REACT_APP_APP_NAME` | Application name | No | `Aiqube SMS` | `Aiqube SMS` |
| `REACT_APP_VERSION` | Application version | No | `1.0.0` | `1.0.0` |
| `REACT_APP_ENABLE_AI` | Enable AI features | No | `true` | `true` |
| `REACT_APP_ENABLE_ADVANCED_FEATURES` | Enable advanced features | No | `true` | `true` |

## 🚀 Running the Application

### Step 1: Start Backend Server

```bash
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Start Frontend Server

```bash
# Open new terminal window/tab
cd frontend

# Start frontend development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view aiqube-sms-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.100:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### Step 3: Verify Both Servers

#### Backend Verification
- **URL**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

#### Frontend Verification
- **URL**: `http://localhost:3000`
- **Should show**: Login page or dashboard

## 🧪 Testing the Connection

### Test 1: Backend Health Check

```bash
# Using curl
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": 1234567890.123}
```

### Test 2: Frontend-Backend API Call

```bash
# Test API endpoint
curl http://localhost:8000/api/v1/auth/login

# Expected response:
# {"detail": "Method Not Allowed"}
# (This is expected for GET request to login endpoint)
```

### Test 3: Frontend Application

1. **Open browser**: `http://localhost:3000`
2. **Check console**: Open Developer Tools (F12)
3. **Look for**: No CORS errors in console
4. **Test login**: Try to access the application

### Test 4: API Documentation

1. **Open**: `http://localhost:8000/docs`
2. **Verify**: Swagger UI loads correctly
3. **Test**: Try the `/health` endpoint

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Issue 2: Frontend Won't Start

**Error**: `Cannot find module 'react'`

**Solution**:
```bash
cd frontend
npm install
npm start
```

#### Issue 3: Database Connection Error

**Error**: `psycopg2.OperationalError: connection to server failed`

**Solution**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if not running
sudo systemctl start postgresql

# Check connection
psql -h localhost -U aiqube_user -d aiqube_sms
```

#### Issue 4: CORS Error in Browser

**Error**: `Access to fetch at 'http://localhost:8000/api/v1/...' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
1. Check `.env` file in root directory
2. Ensure `CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]`
3. Restart backend server

#### Issue 5: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

#### Issue 6: Frontend Can't Connect to Backend

**Error**: `Failed to fetch`

**Solution**:
1. Verify backend is running on port 8000
2. Check `REACT_APP_API_URL` in frontend `.env`
3. Ensure no firewall blocking the connection
4. Test with curl: `curl http://localhost:8000/health`

### Debug Commands

```bash
# Check if ports are in use
lsof -i :8000
lsof -i :3000

# Check backend logs
tail -f logs/app.log

# Check frontend build
cd frontend
npm run build

# Test database connection
python -c "from app.core.database import engine; print('Database connected')"
```

## 🔄 Development Workflow

### Typical Development Process

1. **Start Backend**:
   ```bash
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Make Changes**:
   - Backend changes auto-reload
   - Frontend changes auto-reload
   - Both servers run in development mode

4. **Test Changes**:
   - Backend: Check `http://localhost:8000/docs`
   - Frontend: Check `http://localhost:3000`
   - API calls: Use browser dev tools

### Hot Reload

- **Backend**: Changes to Python files auto-reload
- **Frontend**: Changes to React files auto-reload
- **Database**: Restart backend after schema changes

### Debugging

#### Backend Debugging
```bash
# Run with debug logging
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Check logs
tail -f logs/app.log
```

#### Frontend Debugging
```bash
# Open browser dev tools (F12)
# Check Console tab for errors
# Check Network tab for API calls
```

## 📊 Monitoring Local Development

### Backend Monitoring
- **Logs**: `logs/app.log`
- **Health**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs`

### Frontend Monitoring
- **Console**: Browser Developer Tools
- **Network**: Browser Network tab
- **Performance**: Browser Performance tab

### Database Monitoring
```bash
# PostgreSQL
sudo -u postgres psql aiqube_sms

# SQLite
sqlite3 aiqube_sms.db
```

## 🎯 Quick Reference

### Essential Commands

```bash
# Start backend
source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend
cd frontend && npm start

# Check backend health
curl http://localhost:8000/health

# Check frontend
open http://localhost:3000

# Database migration
alembic upgrade head

# Install dependencies
pip install -r requirements.txt  # Backend
cd frontend && npm install       # Frontend
```

### URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | `http://localhost:3000` | React application |
| Backend | `http://localhost:8000` | FastAPI server |
| API Docs | `http://localhost:8000/docs` | Swagger documentation |
| Health Check | `http://localhost:8000/health` | Backend health |

### Environment Files

| File | Location | Purpose |
|------|----------|---------|
| `.env` | Root directory | Backend configuration |
| `.env` | `frontend/` directory | Frontend configuration |

---

## 🎉 Success Indicators

Your local development environment is working correctly when:

✅ **Backend**: `http://localhost:8000/health` returns `{"status": "healthy"}`  
✅ **Frontend**: `http://localhost:3000` loads without errors  
✅ **API Docs**: `http://localhost:8000/docs` shows Swagger UI  
✅ **Database**: No connection errors in backend logs  
✅ **CORS**: No CORS errors in browser console  
✅ **Hot Reload**: Changes to code auto-reload in both servers  

---

**🚀 Your Aiqube School Management System is now running locally with frontend and backend connected!**

For additional help, check the troubleshooting section or refer to the main documentation.