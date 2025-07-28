# Aiqube School Management System - Production Deployment Guide

Complete guide for deploying the Aiqube School Management System to production environments.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Application Deployment](#application-deployment)
4. [SSL Configuration](#ssl-configuration)
5. [Monitoring & Logging](#monitoring--logging)
6. [Backup Strategy](#backup-strategy)
7. [Security Hardening](#security-hardening)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04+ (Recommended)
- **CPU**: 4+ cores (8+ recommended)
- **RAM**: 8GB+ (16GB recommended)
- **Storage**: 50GB+ SSD
- **Network**: Stable internet connection
- **Domain**: Your domain name

### Software Requirements
- **Python**: 3.12+
- **Node.js**: 18+ LTS
- **PostgreSQL**: 15+
- **Redis**: 7+
- **Nginx**: Latest stable
- **Docker**: 20.10+ (Optional)

## 🚀 Server Setup

### Step 1: Initial Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Set timezone
sudo timedatectl set-timezone UTC

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Step 2: Install Python 3.12

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa

# Install Python 3.12
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3.12-pip

# Set Python 3.12 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1
```

### Step 3: Install Node.js 18

```bash
# Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Install Node.js
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### Step 4: Install PostgreSQL 15

```bash
# Add PostgreSQL repository
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Install PostgreSQL
sudo apt update
sudo apt install -y postgresql-15 postgresql-contrib-15

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 5: Install Redis

```bash
# Install Redis
sudo apt install -y redis-server

# Configure Redis
sudo sed -i 's/supervised no/supervised systemd/' /etc/redis/redis.conf
sudo sed -i 's/# maxmemory <bytes>/maxmemory 256mb/' /etc/redis/redis.conf
sudo sed -i 's/# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/' /etc/redis/redis.conf

# Start and enable Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### Step 6: Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 🚀 Application Deployment

### Step 1: Create Application User

```bash
# Create application user
sudo useradd -m -s /bin/bash aiqube
sudo usermod -aG sudo aiqube

# Set password for aiqube user
sudo passwd aiqube

# Switch to application user
sudo su - aiqube
```

### Step 2: Clone Application

```bash
# Clone repository
git clone https://github.com/priyanshugarg20-eng/Tech-Hub-.git
cd Tech-Hub-

# Checkout production branch
git checkout cursor/develop-school-management-saas-platform-a4c4
```

### Step 3: Setup Backend

```bash
# Create Python virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs uploads
```

### Step 4: Setup Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE aiqube_sms;
CREATE USER aiqube_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE aiqube_sms TO aiqube_user;
ALTER USER aiqube_user CREATEDB;
\q

# Run migrations
source venv/bin/activate
alembic upgrade head
```

### Step 5: Configure Environment

```bash
# Create production .env file
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://aiqube_user:your_secure_password@localhost:5432/aiqube_sms

# Security
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS Configuration
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# AI Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Application Settings
DEBUG=False
ALLOWED_HOSTS=["your-domain.com", "www.your-domain.com"]
CORS_ORIGINS=["https://your-domain.com", "https://www.your-domain.com"]

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Production Settings
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
EOF
```

### Step 6: Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Create production .env
cat > .env << EOF
REACT_APP_API_URL=https://your-domain.com/api
REACT_APP_APP_NAME=Aiqube SMS
REACT_APP_VERSION=1.0.0
REACT_APP_ENABLE_AI=true
REACT_APP_ENABLE_ADVANCED_FEATURES=true
REACT_APP_ENABLE_ANALYTICS=true
EOF

cd ..
```

### Step 7: Create Systemd Services

#### Backend Service

```bash
sudo nano /etc/systemd/system/aiqube-backend.service
```

Add content:

```ini
[Unit]
Description=Aiqube SMS Backend
After=network.target postgresql.service redis-server.service
Wants=postgresql.service redis-server.service

[Service]
Type=simple
User=aiqube
Group=aiqube
WorkingDirectory=/home/aiqube/Tech-Hub-
Environment=PATH=/home/aiqube/Tech-Hub-/venv/bin
Environment=PYTHONPATH=/home/aiqube/Tech-Hub-
ExecStart=/home/aiqube/Tech-Hub-/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=aiqube-backend

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/aiqube/Tech-Hub-/logs /home/aiqube/Tech-Hub-/uploads

[Install]
WantedBy=multi-user.target
```

#### Frontend Service (Optional - for development)

```bash
sudo nano /etc/systemd/system/aiqube-frontend.service
```

Add content:

```ini
[Unit]
Description=Aiqube SMS Frontend
After=network.target aiqube-backend.service
Wants=aiqube-backend.service

[Service]
Type=simple
User=aiqube
Group=aiqube
WorkingDirectory=/home/aiqube/Tech-Hub-/frontend
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=aiqube-frontend

[Install]
WantedBy=multi-user.target
```

### Step 8: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/aiqube-sms
```

Add configuration:

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

# Upstream backend
upstream backend {
    server 127.0.0.1:8000;
}

# Upstream frontend
upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    # Backend API
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 60;
        proxy_connect_timeout 60;
        proxy_send_timeout 60;
    }

    # Login rate limiting
    location /api/v1/auth/login {
        limit_req zone=login burst=5 nodelay;
        
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/aiqube/Tech-Hub-/frontend/build/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /uploads/ {
        alias /home/aiqube/Tech-Hub-/uploads/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Health check
    location /health {
        proxy_pass http://backend;
        access_log off;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/aiqube-sms /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable aiqube-backend
sudo systemctl start aiqube-backend

# Check status
sudo systemctl status aiqube-backend
```

## 🔒 SSL Configuration

### Install Certbot

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Setup Auto-renewal

```bash
# Add to crontab
sudo crontab -e

# Add this line
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring & Logging

### Install Monitoring Tools

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Install logrotate
sudo apt install -y logrotate
```

### Configure Log Rotation

```bash
sudo nano /etc/logrotate.d/aiqube-sms
```

Add content:

```
/home/aiqube/Tech-Hub-/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 aiqube aiqube
    postrotate
        systemctl reload aiqube-backend
    endscript
}
```

### Setup Monitoring Script

```bash
# Create monitoring script
cat > /home/aiqube/monitor.sh << 'EOF'
#!/bin/bash

# Check if services are running
if ! systemctl is-active --quiet aiqube-backend; then
    echo "$(date): Backend service is down!" | mail -s "Aiqube SMS Alert" admin@your-domain.com
    sudo systemctl restart aiqube-backend
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Disk usage is ${DISK_USAGE}%" | mail -s "Aiqube SMS Alert" admin@your-domain.com
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "$(date): Memory usage is ${MEMORY_USAGE}%" | mail -s "Aiqube SMS Alert" admin@your-domain.com
fi
EOF

chmod +x /home/aiqube/monitor.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/aiqube/monitor.sh") | crontab -
```

## 💾 Backup Strategy

### Database Backup

```bash
# Create backup script
cat > /home/aiqube/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/home/aiqube/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump aiqube_sms > $BACKUP_DIR/db_backup_$DATE.sql

# File backup
tar -czf $BACKUP_DIR/uploads_backup_$DATE.tar.gz -C /home/aiqube/Tech-Hub- uploads/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

# Optional: Upload to cloud storage
# gsutil cp $BACKUP_DIR/* gs://your-backup-bucket/
EOF

chmod +x /home/aiqube/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/aiqube/backup.sh") | crontab -
```

## 🔐 Security Hardening

### Firewall Configuration

```bash
# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Fail2ban Setup

```bash
# Install fail2ban
sudo apt install -y fail2ban

# Configure fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Edit configuration
sudo nano /etc/fail2ban/jail.local
```

Add to jail.local:

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600
```

### Security Headers

```bash
# Install mod_security (optional)
sudo apt install -y libapache2-mod-security2
```

## ⚡ Performance Optimization

### Database Optimization

```sql
-- Connect to database
sudo -u postgres psql aiqube_sms

-- Analyze tables
ANALYZE;

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY idx_students_tenant_id ON students(tenant_id);
CREATE INDEX CONCURRENTLY idx_attendance_date ON attendance(attendance_date);
CREATE INDEX CONCURRENTLY idx_fees_due_date ON fees(due_date);

-- Configure PostgreSQL
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Add to postgresql.conf:

```ini
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Connection settings
max_connections = 100

# Logging
log_statement = 'none'
log_min_duration_statement = 1000
```

### Nginx Optimization

```bash
# Edit nginx configuration
sudo nano /etc/nginx/nginx.conf
```

Add to http block:

```nginx
# Worker processes
worker_processes auto;
worker_rlimit_nofile 65535;

# Events
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

# HTTP settings
http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Service Won't Start

```bash
# Check service status
sudo systemctl status aiqube-backend

# Check logs
sudo journalctl -u aiqube-backend -f

# Check permissions
sudo chown -R aiqube:aiqube /home/aiqube/Tech-Hub-
```

#### 2. Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -c "\l"

# Check logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

#### 3. Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Check permissions
sudo chown -R www-data:www-data /var/www/
```

#### 4. SSL Issues

```bash
# Check certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Check SSL configuration
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

### Performance Monitoring

```bash
# Check system resources
htop
iotop
nethogs

# Check disk usage
df -h
du -sh /home/aiqube/Tech-Hub-/*

# Check memory usage
free -h
cat /proc/meminfo

# Check network connections
netstat -tulpn
ss -tulpn
```

### Log Analysis

```bash
# Check application logs
tail -f /home/aiqube/Tech-Hub-/logs/app.log

# Check system logs
sudo journalctl -f

# Check nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 📞 Support

### Emergency Contacts
- **System Administrator**: admin@your-domain.com
- **Development Team**: dev@your-domain.com
- **Hosting Provider**: Your hosting provider support

### Useful Commands

```bash
# Restart all services
sudo systemctl restart aiqube-backend nginx postgresql redis-server

# Check all service status
sudo systemctl status aiqube-backend nginx postgresql redis-server

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

**🎉 Congratulations!** Your Aiqube School Management System is now deployed and ready for production use.

For additional support or questions, please refer to the main documentation or contact the development team.