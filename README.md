# Aiqube School Management System

A comprehensive multi-tenant SaaS platform for school management with complete automation and smart features.

## 🚀 Features

### Core Management
- **Student Management** - Complete student lifecycle management
- **Teacher/Staff Management** - Staff profiles, assignments, and performance tracking
- **Attendance System** - Geolocation, QR scanner, and manual attendance tracking
- **Fee Management** - Complete payment tracking for all services
- **Hostel & Transport Management** - Accommodation and transportation services

### Advanced Features
- **LMS Integration** - Courses, assignments, and performance tracking
- **Custom Notification Engine** - Email, SMS, and in-app notifications
- **Reporting Dashboard** - Charts, KPIs, and detailed performance reports
- **Performance & Behavior Tracking** - Student and staff analytics
- **Task Automation & Alerts** - Automated workflows and notifications

### Platform Features
- **Multi-tenant Architecture** - Isolated data per school
- **Subscription System** - Monthly/Yearly plans with admin controls
- **User Roles & Permissions** - Admins, Teachers, Students, Parents, Super Admin

## 🛠 Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT with role-based access
- **File Storage**: Local/Cloud storage
- **Notifications**: Email, SMS integration
- **Geolocation**: GPS tracking for attendance
- **QR Code**: QR generation and scanning

## 📁 Project Structure

```
aiqube-sms/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── students.py
│   │   │   ├── teachers.py
│   │   │   ├── attendance.py
│   │   │   ├── fees.py
│   │   │   ├── hostel.py
│   │   │   ├── transport.py
│   │   │   ├── lms.py
│   │   │   ├── notifications.py
│   │   │   ├── reports.py
│   │   │   ├── subscriptions.py
│   │   │   └── tenants.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── database.py
│   │   └── notifications.py
│   ├── models/
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── teacher.py
│   │   ├── attendance.py
│   │   ├── fees.py
│   │   ├── hostel.py
│   │   ├── transport.py
│   │   ├── lms.py
│   │   ├── subscription.py
│   │   └── tenant.py
│   ├── schemas/
│   │   └── [corresponding schema files]
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── student_service.py
│   │   ├── attendance_service.py
│   │   ├── notification_service.py
│   │   └── subscription_service.py
│   └── utils/
│       ├── geolocation.py
│       ├── qr_generator.py
│       └── validators.py
├── alembic/
├── tests/
├── requirements.txt
├── docker-compose.yml
└── main.py
```

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd aiqube-sms
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Start PostgreSQL
   docker-compose up -d postgres
   
   # Run migrations
   alembic upgrade head
   ```

3. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔐 Authentication

The system uses JWT tokens with role-based access control:
- **Super Admin**: Platform management
- **School Admin**: School-specific management
- **Teacher**: Class and student management
- **Student**: Personal data and assignments
- **Parent**: Child monitoring and payments

## 📊 Multi-Tenant Architecture

Each school operates in complete isolation:
- Separate database schemas per tenant
- Isolated file storage
- Custom branding and configurations
- Independent subscription management

## 💰 Subscription Plans

- **Basic**: Core features for small schools
- **Professional**: Advanced features for medium schools
- **Enterprise**: Full feature set for large institutions

## 🔔 Notifications

Automated notifications for:
- Attendance alerts
- Fee due reminders
- Assignment deadlines
- Performance reports
- System announcements

## 📈 Reporting & Analytics

Comprehensive dashboards with:
- Student performance metrics
- Attendance analytics
- Financial reports
- Staff productivity
- Custom KPI tracking

---

**Built with ❤️ by Aiqube Team**