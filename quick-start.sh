#!/bin/bash

# Aiqube School Management System - Quick Start Script
# This script automates the local development setup

set -e  # Exit on any error

echo "🚀 Starting Aiqube School Management System Setup..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required software is installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.12+ is required but not installed."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js 18+ is required but not installed."
        exit 1
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed."
        exit 1
    fi
    
    print_success "All requirements are met!"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Backend setup completed!"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install Node.js dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
    
    print_success "Frontend setup completed!"
}

# Create environment files
create_env_files() {
    print_status "Creating environment files..."
    
    # Backend .env
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://aiqube_user:your_password@localhost:5432/aiqube_sms

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
EOF
        print_success "Created backend .env file"
    else
        print_warning "Backend .env file already exists"
    fi
    
    # Frontend .env
    if [ ! -f "frontend/.env" ]; then
        cat > frontend/.env << EOF
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Aiqube SMS
REACT_APP_VERSION=1.0.0

# Feature Flags
REACT_APP_ENABLE_AI=true
REACT_APP_ENABLE_ADVANCED_FEATURES=true
REACT_APP_ENABLE_ANALYTICS=true
EOF
        print_success "Created frontend .env file"
    else
        print_warning "Frontend .env file already exists"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p uploads
    mkdir -p frontend/build
    
    print_success "Directories created!"
}

# Check if PostgreSQL is running
check_postgresql() {
    print_status "Checking PostgreSQL..."
    
    if ! pg_isready -h localhost -p 5432 &> /dev/null; then
        print_warning "PostgreSQL is not running or not accessible."
        print_warning "Please make sure PostgreSQL is installed and running."
        print_warning "You can start it with: sudo systemctl start postgresql"
    else
        print_success "PostgreSQL is running!"
    fi
}

# Start development servers
start_servers() {
    print_status "Starting development servers..."
    
    # Start backend in background
    print_status "Starting backend server..."
    source venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend in background
    print_status "Starting frontend server..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Servers started!"
    print_status "Backend PID: $BACKEND_PID"
    print_status "Frontend PID: $FRONTEND_PID"
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "=================================================="
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🏥 Health Check: http://localhost:8000/health"
    echo ""
    echo "To stop the servers, press Ctrl+C"
    echo ""
    
    # Wait for user to stop
    wait
}

# Main execution
main() {
    echo "Aiqube School Management System - Quick Start"
    echo "============================================="
    echo ""
    
    # Check requirements
    check_requirements
    
    # Create directories
    create_directories
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Create environment files
    create_env_files
    
    # Check PostgreSQL
    check_postgresql
    
    echo ""
    print_status "Setup completed! Starting servers..."
    echo ""
    
    # Start servers
    start_servers
}

# Handle script interruption
trap 'echo ""; print_warning "Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# Run main function
main "$@"