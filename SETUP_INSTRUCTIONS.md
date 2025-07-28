# Aiqube School Management System - Setup Instructions

Complete setup and deployment guide for the Aiqube School Management System with React 18+ frontend and FastAPI backend.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)
7. [API Documentation](#api-documentation)

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **Network**: Stable internet connection

### Required Software
- **Python**: 3.12+ (Latest stable version)
- **Node.js**: 18+ (Latest LTS version)
- **Git**: Latest version
- **PostgreSQL**: 13+ (For production)
- **Redis**: 6+ (For background tasks)

### Development Tools (Optional)
- **VS Code**: Recommended IDE
- **Postman**: API testing
- **pgAdmin**: Database management

## 🚀 Local Development Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/priyanshugarg20-eng/Tech-Hub-.git
cd Tech-Hub-

# Checkout the development branch
git checkout cursor/develop-school-management-saas-platform-a4c4
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 2.2 Install Python Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### 2.3 Database Setup

```bash
# Install PostgreSQL (if not already installed)

# On Ubuntu/Debian:
sudo apt update
sudo apt install postgresql postgresql-contrib

# On macOS:
brew install postgresql

# On Windows:
# Download from https://www.postgresql.org/download/windows/

# Create database
sudo -u postgres psql
CREATE DATABASE aiqube_sms;
CREATE USER aiqube_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE aiqube_sms TO aiqube_user;
\q
```

#### 2.4 Environment Configuration

Create `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://aiqube_user:your_password@localhost:5432/aiqube_sms

# Security
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS Configuration (Optional)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# AI Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key

# Redis Configuration (for background tasks)
REDIS_URL=redis://localhost:6379

# Application Settings
DEBUG=True
ALLOWED_HOSTS=["*"]
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

#### 2.5 Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Create initial data (optional)
python scripts/create_initial_data.py
```

#### 2.6 Start Backend Server

```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or with custom settings
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info
```

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.2 Install Node.js Dependencies

```bash
# Install dependencies
npm install

# Or using yarn
yarn install
```

#### 3.3 Frontend Environment Configuration

Create `.env` file in the frontend directory:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Aiqube SMS
REACT_APP_VERSION=1.0.0

# Feature Flags
REACT_APP_ENABLE_AI=true
REACT_APP_ENABLE_ADVANCED_FEATURES=true
REACT_APP_ENABLE_ANALYTICS=true

# External Services
REACT_APP_GOOGLE_ANALYTICS_ID=your-ga-id
REACT_APP_SENTRY_DSN=your-sentry-dsn
```

#### 3.4 Start Frontend Development Server

```bash
# Start development server
npm start

# Or using yarn
yarn start
```

### Step 4: Verify Installation

#### 4.1 Check Backend
- Open browser: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### 4.2 Check Frontend
- Open browser: `http://localhost:3000`
- Login with default credentials (if created)

#### 4.3 Default Admin Account

If you ran the initial data script, you can login with:
- **Email**: admin@aiqube.com
- **Password**: admin123

## 🚀 Production Deployment

### Option 1: Traditional Server Deployment

#### 1.1 Server Requirements
- **OS**: Ubuntu 20.04+ (Recommended)
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 20GB+ SSD
- **Domain**: Your domain name

#### 1.2 Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.12 python3.12-venv python3.12-dev
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx redis-server
sudo apt install -y git curl wget

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 1.3 Application Deployment

```bash
# Clone repository
git clone https://github.com/priyanshugarg20-eng/Tech-Hub-.git
cd Tech-Hub-

# Create application user
sudo useradd -m -s /bin/bash aiqube
sudo usermod -aG sudo aiqube

# Switch to application user
sudo su - aiqube

# Setup Python environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install
npm run build
```

#### 1.4 Systemd Service Setup

Create backend service file:

```bash
sudo nano /etc/systemd/system/aiqube-backend.service
```

Add content:

```ini
[Unit]
Description=Aiqube SMS Backend
After=network.target

[Service]
Type=simple
User=aiqube
WorkingDirectory=/home/aiqube/Tech-Hub-
Environment=PATH=/home/aiqube/Tech-Hub-/venv/bin
ExecStart=/home/aiqube/Tech-Hub-/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Create frontend service file:

```bash
sudo nano /etc/systemd/system/aiqube-frontend.service
```

Add content:

```ini
[Unit]
Description=Aiqube SMS Frontend
After=network.target

[Service]
Type=simple
User=aiqube
WorkingDirectory=/home/aiqube/Tech-Hub-/frontend
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 1.5 Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/aiqube-sms
```

Add configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/aiqube-sms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 1.6 Start Services

```bash
# Enable and start services
sudo systemctl enable aiqube-backend
sudo systemctl start aiqube-backend
sudo systemctl enable aiqube-frontend
sudo systemctl start aiqube-frontend

# Check status
sudo systemctl status aiqube-backend
sudo systemctl status aiqube-frontend
```

### Option 2: Docker Deployment

#### 2.1 Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2.2 Docker Compose Setup

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: aiqube_sms
      POSTGRES_USER: aiqube_user
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: .
    environment:
      - DATABASE_URL=postgresql://aiqube_user:your_secure_password@postgres:5432/aiqube_sms
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=your-super-secret-key
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=http://your-domain.com/api
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

#### 2.3 Deploy with Docker

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Environment Configuration

### Backend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `SECRET_KEY` | JWT secret key | Yes | - |
| `ALGORITHM` | JWT algorithm | No | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | No | 30 |
| `SMTP_HOST` | SMTP server host | No | - |
| `SMTP_PORT` | SMTP server port | No | 587 |
| `SMTP_USER` | SMTP username | No | - |
| `SMTP_PASSWORD` | SMTP password | No | - |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | No | - |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | No | - |
| `HUGGINGFACE_API_KEY` | Hugging Face API key | No | - |
| `REDIS_URL` | Redis connection string | No | redis://localhost:6379 |
| `DEBUG` | Debug mode | No | False |
| `ALLOWED_HOSTS` | Allowed hosts | No | ["*"] |
| `CORS_ORIGINS` | CORS origins | No | ["http://localhost:3000"] |

### Frontend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `REACT_APP_API_URL` | Backend API URL | Yes | http://localhost:8000 |
| `REACT_APP_APP_NAME` | Application name | No | Aiqube SMS |
| `REACT_APP_VERSION` | Application version | No | 1.0.0 |
| `REACT_APP_ENABLE_AI` | Enable AI features | No | true |
| `REACT_APP_ENABLE_ADVANCED_FEATURES` | Enable advanced features | No | true |
| `REACT_APP_GOOGLE_ANALYTICS_ID` | Google Analytics ID | No | - |
| `REACT_APP_SENTRY_DSN` | Sentry DSN | No | - |

## 🔍 Troubleshooting

### Common Issues

#### 1. Python Dependencies Issues

```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check Python version
python --version
```

#### 2. Node.js Dependencies Issues

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 3. Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U aiqube_user -d aiqube_sms

# Check database exists
\l
```

#### 4. Port Conflicts

```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :3000

# Kill process if needed
sudo kill -9 <PID>
```

#### 5. Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER /path/to/project
chmod +x scripts/*.sh
```

### Log Files

#### Backend Logs
```bash
# View backend logs
tail -f logs/app.log

# View systemd logs
sudo journalctl -u aiqube-backend -f
```

#### Frontend Logs
```bash
# View frontend logs
tail -f frontend/logs/app.log

# View systemd logs
sudo journalctl -u aiqube-frontend -f
```

### Performance Issues

#### 1. Database Optimization
```sql
-- Analyze database performance
ANALYZE;

-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

#### 2. Memory Issues
```bash
# Check memory usage
free -h

# Check process memory
ps aux --sort=-%mem | head -10
```

## 📚 API Documentation

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com/api`

### Authentication
All API endpoints require JWT authentication except:
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /health`

### Example API Calls

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@aiqube.com",
    "password": "admin123"
  }'
```

#### Get Students
```bash
curl -X GET "http://localhost:8000/api/v1/students" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### AI Chat
```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is photosynthesis?",
    "subject": "biology"
  }'
```

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Security Checklist

### Production Security
- [ ] Change default passwords
- [ ] Use HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Database encryption

### SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring and Maintenance

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Database health
pg_isready -h localhost -p 5432
```

### Backup Strategy
```bash
# Database backup
pg_dump aiqube_sms > backup_$(date +%Y%m%d_%H%M%S).sql

# File backup
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

### Update Process
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt
cd frontend && npm install

# Restart services
sudo systemctl restart aiqube-backend
sudo systemctl restart aiqube-frontend
```

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Check the API documentation
4. Create an issue on GitHub
5. Contact the development team

### Useful Commands
```bash
# Check system status
sudo systemctl status aiqube-backend aiqube-frontend nginx postgresql redis

# View real-time logs
sudo journalctl -f -u aiqube-backend

# Check disk space
df -h

# Check memory usage
free -h

# Check network connections
netstat -tulpn
```

---

**🎉 Congratulations!** Your Aiqube School Management System is now ready to use.

For additional support or questions, please refer to the main README.md file or contact the development team.