# Aiqube School Management System - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aiqube-sms
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Option 2: Manual Deployment

1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup database**
   ```bash
   # Start PostgreSQL
   sudo systemctl start postgresql
   
   # Create database
   sudo -u postgres psql
   CREATE DATABASE aiqube_sms;
   CREATE USER aiqube WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE aiqube_sms TO aiqube;
   \q
   ```

3. **Setup Redis**
   ```bash
   sudo systemctl start redis
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run setup script**
   ```bash
   python setup.py
   ```

6. **Start the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://aiqube:password@localhost:5432/aiqube_sms

# Security
SECRET_KEY=your-secret-key-change-in-production

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
```

### Email Setup (Gmail)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in SMTP_PASSWORD

### SMS Setup (Twilio)

1. Create a Twilio account
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Configure the credentials in .env

## 📊 Database Setup

### Manual Database Creation

```sql
-- Connect to PostgreSQL
sudo -u postgres psql

-- Create database
CREATE DATABASE aiqube_sms;

-- Create user
CREATE USER aiqube WITH PASSWORD 'password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE aiqube_sms TO aiqube;

-- Connect to the database
\c aiqube_sms

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Exit
\q
```

### Database Migrations

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

## 🔐 Security Configuration

### JWT Secret Key

Generate a secure secret key:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### SSL/TLS Setup

For production, configure SSL:

```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Start with SSL
uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

## 🐳 Docker Configuration

### Production Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: aiqube_sms
      POSTGRES_USER: aiqube
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - aiqube_network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - aiqube_network

  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://aiqube:${DB_PASSWORD}@postgres:5432/aiqube_sms
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    networks:
      - aiqube_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - aiqube_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  aiqube_network:
    driver: bridge
```

## 🔄 Background Tasks

### Celery Configuration

```bash
# Start Celery worker
celery -A app.core.celery worker --loglevel=info

# Start Celery beat (scheduler)
celery -A app.core.celery beat --loglevel=info
```

### Redis Configuration

```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis

# Enable Redis on boot
sudo systemctl enable redis
```

## 📈 Monitoring & Logging

### Logging Configuration

```python
# In app/core/config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/aiqube_sms.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Check database connection
python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
```

## 🔧 Production Deployment

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Start with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Systemd Service

Create `/etc/systemd/system/aiqube-sms.service`:

```ini
[Unit]
Description=Aiqube School Management System
After=network.target

[Service]
Type=exec
User=aiqube
WorkingDirectory=/opt/aiqube-sms
Environment=PATH=/opt/aiqube-sms/venv/bin
ExecStart=/opt/aiqube-sms/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable aiqube-sms
sudo systemctl start aiqube-sms
```

### Nginx Configuration

Create `/etc/nginx/sites-available/aiqube-sms`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/aiqube-sms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 Security Checklist

- [ ] Change default passwords
- [ ] Configure SSL/TLS
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure backup strategy
- [ ] Set up monitoring
- [ ] Enable logging
- [ ] Configure CORS properly
- [ ] Set secure headers
- [ ] Regular security updates

## 📋 Default Credentials

After running the setup script:

- **Super Admin**: admin@aiqube.com / admin123
- **School Admin**: admin@sampleschool.com / admin123
- **Teacher**: teacher@sampleschool.com / teacher123
- **Student**: student@sampleschool.com / student123

**⚠️ Change these passwords immediately in production!**

## 🆘 Troubleshooting

### Common Issues

1. **Database connection failed**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Check connection
   psql -h localhost -U aiqube -d aiqube_sms
   ```

2. **Redis connection failed**
   ```bash
   # Check Redis status
   sudo systemctl status redis
   
   # Test connection
   redis-cli ping
   ```

3. **Port already in use**
   ```bash
   # Find process using port
   sudo lsof -i :8000
   
   # Kill process
   sudo kill -9 <PID>
   ```

4. **Permission denied**
   ```bash
   # Fix file permissions
   sudo chown -R aiqube:aiqube /opt/aiqube-sms
   sudo chmod -R 755 /opt/aiqube-sms
   ```

### Logs

Check logs for errors:

```bash
# Application logs
tail -f logs/aiqube_sms.log

# System logs
sudo journalctl -u aiqube-sms -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

## 📞 Support

For support and questions:
- Email: support@aiqube.com
- Documentation: https://docs.aiqube.com
- GitHub Issues: https://github.com/aiqube/sms/issues