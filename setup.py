#!/usr/bin/env python3
"""
Setup script for Aiqube School Management System
"""

import os
import sys
import subprocess
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.models.tenant import Tenant, TenantStatus, SubscriptionPlan
from app.models.user import User, UserRole, UserStatus
from app.models.student import Student, StudentStatus, StudentGrade
from app.models.teacher import Teacher, TeacherStatus, TeacherQualification
from app.core.security import SecurityUtils


def create_directories():
    """Create necessary directories"""
    directories = [
        "uploads",
        "logs",
        "uploads/students",
        "uploads/teachers",
        "uploads/documents",
        "uploads/qr_codes"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def create_database_tables():
    """Create database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        return False
    return True


def create_super_admin():
    """Create super admin user"""
    db = SessionLocal()
    try:
        # Check if super admin already exists
        existing_admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
        if existing_admin:
            print("✓ Super admin already exists")
            return True
        
        # Create super admin
        super_admin = User(
            id=str(uuid.uuid4()),
            email="admin@aiqube.com",
            username="superadmin",
            hashed_password=SecurityUtils.get_password_hash("admin123"),
            first_name="Super",
            last_name="Admin",
            role=UserRole.SUPER_ADMIN,
            status=UserStatus.ACTIVE,
            is_email_verified=True
        )
        
        db.add(super_admin)
        db.commit()
        print("✓ Super admin created successfully")
        print("  Email: admin@aiqube.com")
        print("  Password: admin123")
        return True
        
    except Exception as e:
        print(f"✗ Error creating super admin: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def create_sample_tenant():
    """Create sample tenant for testing"""
    db = SessionLocal()
    try:
        # Check if sample tenant already exists
        existing_tenant = db.query(Tenant).filter(Tenant.slug == "sample-school").first()
        if existing_tenant:
            print("✓ Sample tenant already exists")
            return existing_tenant.id
        
        # Create sample tenant
        tenant = Tenant(
            id=str(uuid.uuid4()),
            name="Sample School",
            slug="sample-school",
            email="info@sampleschool.com",
            phone="+1234567890",
            school_name="Sample School",
            school_type="Secondary",
            established_year=2020,
            subscription_plan=SubscriptionPlan.PROFESSIONAL,
            subscription_status=TenantStatus.ACTIVE,
            subscription_start_date=datetime.utcnow(),
            subscription_end_date=datetime.utcnow() + timedelta(days=365),
            monthly_fee=199.0,
            annual_fee=1990.0,
            is_active=True,
            is_verified=True
        )
        
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print("✓ Sample tenant created successfully")
        return tenant.id
        
    except Exception as e:
        print(f"✗ Error creating sample tenant: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def create_sample_users(tenant_id):
    """Create sample users for testing"""
    db = SessionLocal()
    try:
        # Create admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            email="admin@sampleschool.com",
            username="schooladmin",
            hashed_password=SecurityUtils.get_password_hash("admin123"),
            first_name="School",
            last_name="Admin",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            tenant_id=tenant_id,
            is_email_verified=True
        )
        
        # Create teacher user
        teacher_user = User(
            id=str(uuid.uuid4()),
            email="teacher@sampleschool.com",
            username="teacher1",
            hashed_password=SecurityUtils.get_password_hash("teacher123"),
            first_name="John",
            last_name="Teacher",
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE,
            tenant_id=tenant_id,
            is_email_verified=True
        )
        
        # Create student user
        student_user = User(
            id=str(uuid.uuid4()),
            email="student@sampleschool.com",
            username="student1",
            hashed_password=SecurityUtils.get_password_hash("student123"),
            first_name="Alice",
            last_name="Student",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            tenant_id=tenant_id,
            is_email_verified=True
        )
        
        db.add_all([admin_user, teacher_user, student_user])
        db.commit()
        
        print("✓ Sample users created successfully")
        print("  Admin: admin@sampleschool.com / admin123")
        print("  Teacher: teacher@sampleschool.com / teacher123")
        print("  Student: student@sampleschool.com / student123")
        
        return {
            "admin": admin_user,
            "teacher": teacher_user,
            "student": student_user
        }
        
    except Exception as e:
        print(f"✗ Error creating sample users: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def create_sample_data(tenant_id, users):
    """Create sample data for testing"""
    db = SessionLocal()
    try:
        # Create sample teacher profile
        teacher = Teacher(
            id=str(uuid.uuid4()),
            user_id=users["teacher"].id,
            tenant_id=tenant_id,
            teacher_id="T001",
            employee_id="EMP001",
            joining_date=datetime.now().date(),
            department="Mathematics",
            designation="Senior Teacher",
            qualification=TeacherQualification.MASTERS,
            specialization="Mathematics",
            experience_years=5,
            status=TeacherStatus.ACTIVE,
            date_of_birth=datetime(1985, 5, 15).date(),
            gender="Male"
        )
        
        # Create sample student profile
        student = Student(
            id=str(uuid.uuid4()),
            user_id=users["student"].id,
            tenant_id=tenant_id,
            student_id="S001",
            admission_number="ADM001",
            admission_date=datetime.now().date(),
            grade=StudentGrade.GRADE_10,
            current_grade=StudentGrade.GRADE_10,
            academic_year="2023-2024",
            status=StudentStatus.ACTIVE,
            date_of_birth=datetime(2008, 3, 20).date(),
            gender="Female"
        )
        
        db.add_all([teacher, student])
        db.commit()
        
        print("✓ Sample data created successfully")
        
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Aiqube School Management System...")
    print("=" * 50)
    
    # Step 1: Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Step 2: Install dependencies
    print("\n2. Installing dependencies...")
    if not install_dependencies():
        print("✗ Setup failed at dependency installation")
        return False
    
    # Step 3: Create database tables
    print("\n3. Creating database tables...")
    if not create_database_tables():
        print("✗ Setup failed at database table creation")
        return False
    
    # Step 4: Create super admin
    print("\n4. Creating super admin...")
    if not create_super_admin():
        print("✗ Setup failed at super admin creation")
        return False
    
    # Step 5: Create sample tenant
    print("\n5. Creating sample tenant...")
    tenant_id = create_sample_tenant()
    if not tenant_id:
        print("✗ Setup failed at sample tenant creation")
        return False
    
    # Step 6: Create sample users
    print("\n6. Creating sample users...")
    users = create_sample_users(tenant_id)
    if not users:
        print("✗ Setup failed at sample user creation")
        return False
    
    # Step 7: Create sample data
    print("\n7. Creating sample data...")
    create_sample_data(tenant_id, users)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and configure your settings")
    print("2. Run: uvicorn main:app --reload")
    print("3. Access the API at: http://localhost:8000")
    print("4. View documentation at: http://localhost:8000/docs")
    print("\n🔑 Default credentials:")
    print("Super Admin: admin@aiqube.com / admin123")
    print("School Admin: admin@sampleschool.com / admin123")
    print("Teacher: teacher@sampleschool.com / teacher123")
    print("Student: student@sampleschool.com / student123")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)