"""
Advanced Features Models for Aiqube School Management System
Includes blockchain certificates, AR/VR, IoT, gamification, and advanced analytics
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from app.core.database import Base
import uuid


class BlockchainCertificateStatus(enum.Enum):
    PENDING = "pending"
    ISSUED = "issued"
    VERIFIED = "verified"
    REVOKED = "revoked"


class ARVRContentType(enum.Enum):
    VIRTUAL_LAB = "virtual_lab"
    HISTORICAL_SIMULATION = "historical_simulation"
    SCIENCE_EXPERIMENT = "science_experiment"
    MATH_VISUALIZATION = "math_visualization"
    LANGUAGE_IMMERSION = "language_immersion"
    ART_GALLERY = "art_gallery"


class IoTDeviceType(enum.Enum):
    ATTENDANCE_SENSOR = "attendance_sensor"
    ENVIRONMENTAL_MONITOR = "environmental_monitor"
    SECURITY_CAMERA = "security_camera"
    SMART_LIGHTING = "smart_lighting"
    AIR_QUALITY_SENSOR = "air_quality_sensor"
    NOISE_MONITOR = "noise_monitor"


class GamificationBadgeType(enum.Enum):
    ACADEMIC_EXCELLENCE = "academic_excellence"
    ATTENDANCE_PERFECT = "attendance_perfect"
    HELPING_OTHERS = "helping_others"
    INNOVATION = "innovation"
    LEADERSHIP = "leadership"
    SPORTS_ACHIEVEMENT = "sports_achievement"
    ARTS_CREATIVITY = "arts_creativity"
    AI_MASTERY = "ai_mastery"


class BlockchainCertificate(Base):
    """Blockchain-based digital certificates for achievements and qualifications"""
    __tablename__ = "blockchain_certificates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    certificate_type = Column(String(100), nullable=False)  # academic, skill, achievement
    title = Column(String(200), nullable=False)
    description = Column(Text)
    issuer_name = Column(String(100), nullable=False)
    issuer_signature = Column(String(500))  # Digital signature
    blockchain_hash = Column(String(255))  # Blockchain transaction hash
    blockchain_network = Column(String(50), default="ethereum")  # ethereum, polygon, etc.
    status = Column(Enum(BlockchainCertificateStatus), default=BlockchainCertificateStatus.PENDING)
    issued_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    metadata = Column(JSON)  # Additional certificate data
    verification_url = Column(String(500))  # Public verification URL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="blockchain_certificates")
    tenant = relationship("Tenant")


class ARVRContent(Base):
    """AR/VR educational content and experiences"""
    __tablename__ = "arvr_content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content_type = Column(Enum(ARVRContentType), nullable=False)
    subject = Column(String(100), nullable=False)
    grade_level = Column(String(50))
    vr_file_url = Column(String(500))  # VR content file
    ar_marker_url = Column(String(500))  # AR marker image
    ar_content_url = Column(String(500))  # AR content
    duration_minutes = Column(Integer)
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    tags = Column(JSON)  # Array of tags
    is_interactive = Column(Boolean, default=True)
    requires_vr_headset = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    creator = relationship("User")


class ARVRUsage(Base):
    """Track AR/VR content usage and analytics"""
    __tablename__ = "arvr_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("arvr_content.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_duration = Column(Integer)  # Duration in seconds
    completion_percentage = Column(Float)
    interaction_count = Column(Integer, default=0)
    device_type = Column(String(50))  # vr_headset, mobile_ar, desktop
    device_info = Column(JSON)  # Device specifications
    location_data = Column(JSON)  # GPS coordinates if applicable
    performance_metrics = Column(JSON)  # FPS, latency, etc.
    feedback_rating = Column(Integer)  # 1-5 rating
    feedback_comment = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    content = relationship("ARVRContent")
    user = relationship("User")
    tenant = relationship("Tenant")


class IoTDevice(Base):
    """IoT devices for smart campus monitoring"""
    __tablename__ = "iot_devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    device_id = Column(String(100), unique=True, nullable=False)  # Physical device ID
    device_type = Column(Enum(IoTDeviceType), nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    building = Column(String(100))
    room = Column(String(100))
    coordinates = Column(JSON)  # GPS coordinates
    status = Column(String(50), default="active")  # active, inactive, maintenance
    last_seen = Column(DateTime)
    firmware_version = Column(String(50))
    configuration = Column(JSON)  # Device-specific settings
    is_online = Column(Boolean, default=True)
    battery_level = Column(Float)  # For battery-powered devices
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    sensor_data = relationship("IoTSensorData", back_populates="device")


class IoTSensorData(Base):
    """Sensor data from IoT devices"""
    __tablename__ = "iot_sensor_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("iot_devices.id"), nullable=False)
    sensor_type = Column(String(50), nullable=False)  # temperature, humidity, motion, etc.
    value = Column(Float, nullable=False)
    unit = Column(String(20))  # celsius, percent, lux, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(JSON)  # GPS coordinates
    metadata = Column(JSON)  # Additional sensor data
    
    # Relationships
    device = relationship("IoTDevice", back_populates="sensor_data")
    tenant = relationship("Tenant")


class GamificationBadge(Base):
    """Gamification badges and achievements"""
    __tablename__ = "gamification_badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    badge_type = Column(Enum(GamificationBadgeType), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon_url = Column(String(500))
    points_value = Column(Integer, default=0)
    rarity = Column(String(50), default="common")  # common, rare, epic, legendary
    criteria = Column(JSON)  # Achievement criteria
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """User badge assignments and progress"""
    __tablename__ = "user_badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("gamification_badges.id"), nullable=False)
    progress_percentage = Column(Float, default=0.0)
    is_earned = Column(Boolean, default=False)
    earned_at = Column(DateTime)
    awarded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    evidence = Column(JSON)  # Proof of achievement
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    badge = relationship("GamificationBadge", back_populates="user_badges")
    awarded_by_user = relationship("User", foreign_keys=[awarded_by])
    tenant = relationship("Tenant")


class GamificationPoints(Base):
    """User points and leveling system"""
    __tablename__ = "gamification_points"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    total_achievements = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    tenant = relationship("Tenant")


class AdvancedAnalytics(Base):
    """Advanced analytics and machine learning insights"""
    __tablename__ = "advanced_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    analytics_type = Column(String(100), nullable=False)  # predictive, behavioral, performance
    target_entity = Column(String(100))  # student, teacher, class, school
    entity_id = Column(UUID(as_uuid=True))
    prediction_model = Column(String(100))  # Model name/version
    confidence_score = Column(Float)
    prediction_data = Column(JSON)  # Raw prediction data
    insights = Column(JSON)  # Extracted insights
    recommendations = Column(JSON)  # Actionable recommendations
    risk_factors = Column(JSON)  # Risk indicators
    trend_analysis = Column(JSON)  # Trend data
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # When prediction expires
    
    # Relationships
    tenant = relationship("Tenant")


class PredictiveModel(Base):
    """Machine learning models for predictions"""
    __tablename__ = "predictive_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(100), nullable=False)  # classification, regression, clustering
    purpose = Column(String(200), nullable=False)  # dropout_prediction, performance_forecast, etc.
    version = Column(String(50), nullable=False)
    accuracy_score = Column(Float)
    precision_score = Column(Float)
    recall_score = Column(Float)
    f1_score = Column(Float)
    training_data_size = Column(Integer)
    last_trained = Column(DateTime)
    model_file_path = Column(String(500))
    hyperparameters = Column(JSON)
    feature_importance = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")


class SmartSchedule(Base):
    """AI-powered smart scheduling system"""
    __tablename__ = "smart_schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    schedule_type = Column(String(100), nullable=False)  # class, exam, event, maintenance
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(200))
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"))
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"))
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))
    ai_optimized = Column(Boolean, default=False)
    optimization_factors = Column(JSON)  # Factors considered by AI
    conflict_resolved = Column(Boolean, default=False)
    priority_level = Column(String(50), default="normal")  # low, normal, high, urgent
    recurrence_pattern = Column(JSON)  # For recurring schedules
    notifications = Column(JSON)  # Notification settings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    room = relationship("Room")
    teacher = relationship("Teacher")
    class_entity = relationship("Class")


class VoiceAssistant(Base):
    """Voice assistant interactions and commands"""
    __tablename__ = "voice_assistant"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), nullable=False)
    command_type = Column(String(100), nullable=False)  # query, action, navigation
    voice_input = Column(Text)
    processed_command = Column(Text)
    intent = Column(String(100))
    entities = Column(JSON)  # Extracted entities
    response_text = Column(Text)
    response_audio_url = Column(String(500))
    confidence_score = Column(Float)
    execution_success = Column(Boolean)
    execution_time = Column(Float)  # Response time in seconds
    device_info = Column(JSON)  # Device and microphone info
    location_context = Column(JSON)  # Location when command was given
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    tenant = relationship("Tenant")


class BiometricAttendance(Base):
    """Biometric attendance system"""
    __tablename__ = "biometric_attendance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    biometric_type = Column(String(50), nullable=False)  # fingerprint, face, iris, voice
    device_id = Column(String(100))
    verification_method = Column(String(50))  # 1:1, 1:N
    confidence_score = Column(Float)
    liveness_detected = Column(Boolean, default=True)
    spoof_detection = Column(Boolean, default=True)
    location = Column(JSON)  # GPS coordinates
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="success")  # success, failed, timeout
    metadata = Column(JSON)  # Additional biometric data
    
    # Relationships
    user = relationship("User")
    tenant = relationship("Tenant")


class SmartClassroom(Base):
    """Smart classroom configuration and automation"""
    __tablename__ = "smart_classrooms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    automation_enabled = Column(Boolean, default=True)
    lighting_control = Column(Boolean, default=True)
    climate_control = Column(Boolean, default=True)
    audio_system = Column(Boolean, default=True)
    projector_system = Column(Boolean, default=True)
    smart_board = Column(Boolean, default=True)
    occupancy_sensor = Column(Boolean, default=True)
    air_quality_monitor = Column(Boolean, default=True)
    noise_monitor = Column(Boolean, default=True)
    configuration = Column(JSON)  # Room-specific settings
    schedule_automation = Column(JSON)  # Automated schedules
    energy_usage = Column(JSON)  # Energy consumption data
    maintenance_alerts = Column(JSON)  # Maintenance notifications
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    room = relationship("Room")


# Add relationships to existing models
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher

# Add to Student model
Student.blockchain_certificates = relationship("BlockchainCertificate", back_populates="student")

# Add to User model
User.badges = relationship("UserBadge", foreign_keys="UserBadge.user_id")
User.points = relationship("GamificationPoints", back_populates="user")
User.voice_interactions = relationship("VoiceAssistant", back_populates="user")
User.biometric_records = relationship("BiometricAttendance", back_populates="user")