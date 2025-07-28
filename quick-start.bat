@echo off
REM Aiqube School Management System - Quick Start Script for Windows
REM This script automates the local development setup on Windows

echo 🚀 Starting Aiqube School Management System Setup...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.12+ is required but not installed.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js 18+ is required but not installed.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is required but not installed.
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [SUCCESS] All requirements are met!

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "frontend\build" mkdir frontend\build

REM Setup backend
echo [INFO] Setting up backend...

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

echo [SUCCESS] Backend setup completed!

REM Setup frontend
echo [INFO] Setting up frontend...
cd frontend

REM Install Node.js dependencies
echo [INFO] Installing Node.js dependencies...
npm install

cd ..

echo [SUCCESS] Frontend setup completed!

REM Create environment files
echo [INFO] Creating environment files...

REM Backend .env
if not exist ".env" (
    echo # Database Configuration > .env
    echo DATABASE_URL=postgresql://aiqube_user:your_password@localhost:5432/aiqube_sms >> .env
    echo. >> .env
    echo # Security >> .env
    echo SECRET_KEY=your-super-secret-key-here-make-it-long-and-random >> .env
    echo ALGORITHM=HS256 >> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
    echo. >> .env
    echo # Application Settings >> .env
    echo DEBUG=True >> .env
    echo ALLOWED_HOSTS=["*"] >> .env
    echo CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"] >> .env
    echo. >> .env
    echo # File Upload >> .env
    echo UPLOAD_DIR=uploads >> .env
    echo MAX_FILE_SIZE=10485760 >> .env
    echo. >> .env
    echo # Logging >> .env
    echo LOG_LEVEL=INFO >> .env
    echo LOG_FILE=logs/app.log >> .env
    echo [SUCCESS] Created backend .env file
) else (
    echo [WARNING] Backend .env file already exists
)

REM Frontend .env
if not exist "frontend\.env" (
    echo # API Configuration > frontend\.env
    echo REACT_APP_API_URL=http://localhost:8000 >> frontend\.env
    echo REACT_APP_APP_NAME=Aiqube SMS >> frontend\.env
    echo REACT_APP_VERSION=1.0.0 >> frontend\.env
    echo. >> frontend\.env
    echo # Feature Flags >> frontend\.env
    echo REACT_APP_ENABLE_AI=true >> frontend\.env
    echo REACT_APP_ENABLE_ADVANCED_FEATURES=true >> frontend\.env
    echo REACT_APP_ENABLE_ANALYTICS=true >> frontend\.env
    echo [SUCCESS] Created frontend .env file
) else (
    echo [WARNING] Frontend .env file already exists
)

echo.
echo [INFO] Setup completed! Starting servers...
echo.

REM Start backend server
echo [INFO] Starting backend server...
start "Backend Server" cmd /k "call venv\Scripts\activate.bat && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend server
echo [INFO] Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo 🎉 Setup completed successfully!
echo ==================================================
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/health
echo.
echo The servers are now running in separate windows.
echo Close those windows to stop the servers.
echo.
pause