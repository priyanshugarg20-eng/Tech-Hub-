# 🚀 Quick Start Checklist - Local Development

Simple step-by-step checklist to run the Aiqube School Management System locally.

## ✅ Prerequisites Check

- [ ] **Python 3.12+** installed
- [ ] **Node.js 18+** installed  
- [ ] **Git** installed
- [ ] **PostgreSQL** installed (optional, can use SQLite)
- [ ] **4GB+ RAM** available
- [ ] **2GB+ free space** available

## 🛠️ Setup Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/priyanshugarg20-eng/Tech-Hub-.git
cd Tech-Hub-
git checkout cursor/develop-school-management-saas-platform-a4c4
```

### Step 2: Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
cd ..
```

### Step 4: Environment Files

#### Backend (.env in root directory)
```env
DATABASE_URL=sqlite:///./aiqube_sms.db
SECRET_KEY=your-super-secret-key-here
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
```

#### Frontend (.env in frontend directory)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Aiqube SMS
REACT_APP_ENABLE_AI=true
```

### Step 5: Database Setup
```bash
# Run migrations
alembic upgrade head
```

## 🚀 Start Servers

### Terminal 1: Backend
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm start
```

## ✅ Verification Checklist

- [ ] **Backend running**: `http://localhost:8000/health` returns `{"status": "healthy"}`
- [ ] **Frontend running**: `http://localhost:3000` loads without errors
- [ ] **API Docs**: `http://localhost:8000/docs` shows Swagger UI
- [ ] **No CORS errors** in browser console
- [ ] **Database connected** (no errors in backend logs)

## 🔗 URLs to Test

| Service | URL | Expected Result |
|---------|-----|-----------------|
| Frontend | `http://localhost:3000` | Login page loads |
| Backend | `http://localhost:8000` | API root page |
| API Docs | `http://localhost:8000/docs` | Swagger UI |
| Health | `http://localhost:8000/health` | `{"status": "healthy"}` |

## 🛠️ Quick Commands

```bash
# Start backend
source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend
cd frontend && npm start

# Check health
curl http://localhost:8000/health

# Database migration
alembic upgrade head
```

## 🔍 Troubleshooting

### Common Issues:

1. **Backend won't start**: Check virtual environment is activated
2. **Frontend won't start**: Run `npm install` in frontend directory
3. **CORS errors**: Check `.env` file has correct CORS_ORIGINS
4. **Database errors**: Run `alembic upgrade head`
5. **Port in use**: Kill process using port 8000 or 3000

### Debug Commands:
```bash
# Check ports
lsof -i :8000
lsof -i :3000

# Check backend logs
tail -f logs/app.log

# Test database
python -c "from app.core.database import engine; print('DB OK')"
```

## 🎉 Success!

When all checkboxes are green ✅, your local development environment is ready!

**Next Steps:**
- Explore the API documentation at `http://localhost:8000/docs`
- Test the frontend application at `http://localhost:3000`
- Start developing your features!

---

**📚 For detailed instructions, see `LOCAL_DEVELOPMENT_GUIDE.md`**