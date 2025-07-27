"""
Advanced Features Schemas for Aiqube School Management System
Includes blockchain certificates, AR/VR, IoT, gamification, and advanced analytics
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid


# Enums
class BlockchainCertificateStatus(str, Enum):
    PENDING = "pending"
    ISSUED = "issued"
    VERIFIED = "verified"
    REVOKED = "revoked"


class ARVRContentType(str, Enum):
    VIRTUAL_LAB = "virtual_lab"
    HISTORICAL_SIMULATION = "historical_simulation"
    SCIENCE_EXPERIMENT = "science_experiment"
    MATH_VISUALIZATION = "math_visualization"
    LANGUAGE_IMMERSION = "language_immersion"
    ART_GALLERY = "art_gallery"


class IoTDeviceType(str, Enum):
    ATTENDANCE_SENSOR = "attendance_sensor"
    ENVIRONMENTAL_MONITOR = "environmental_monitor"
    SECURITY_CAMERA = "security_camera"
    SMART_LIGHTING = "smart_lighting"
    AIR_QUALITY_SENSOR = "air_quality_sensor"
    NOISE_MONITOR = "noise_monitor"


class GamificationBadgeType(str, Enum):
    ACADEMIC_EXCELLENCE = "academic_excellence"
    ATTENDANCE_PERFECT = "attendance_perfect"
    HELPING_OTHERS = "helping_others"
    INNOVATION = "innovation"
    LEADERSHIP = "leadership"
    SPORTS_ACHIEVEMENT = "sports_achievement"
    ARTS_CREATIVITY = "arts_creativity"
    AI_MASTERY = "ai_mastery"


# Blockchain Certificates
class BlockchainCertificateBase(BaseModel):
    certificate_type: str = Field(..., description="Type of certificate")
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    issuer_name: str = Field(..., max_length=100)
    blockchain_network: str = Field(default="ethereum")
    expiry_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class BlockchainCertificateCreate(BlockchainCertificateBase):
    student_id: uuid.UUID
    issuer_signature: Optional[str] = None


class BlockchainCertificateUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[BlockchainCertificateStatus] = None
    blockchain_hash: Optional[str] = None
    verification_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BlockchainCertificateResponse(BlockchainCertificateBase):
    id: uuid.UUID
    student_id: uuid.UUID
    status: BlockchainCertificateStatus
    issued_date: datetime
    blockchain_hash: Optional[str] = None
    verification_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AR/VR Content
class ARVRContentBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    content_type: ARVRContentType
    subject: str = Field(..., max_length=100)
    grade_level: Optional[str] = Field(None, max_length=50)
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    is_interactive: bool = True
    requires_vr_headset: bool = False
    is_public: bool = False


class ARVRContentCreate(ARVRContentBase):
    vr_file_url: Optional[str] = None
    ar_marker_url: Optional[str] = None
    ar_content_url: Optional[str] = None


class ARVRContentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    vr_file_url: Optional[str] = None
    ar_marker_url: Optional[str] = None
    ar_content_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    is_interactive: Optional[bool] = None
    is_public: Optional[bool] = None


class ARVRContentResponse(ARVRContentBase):
    id: uuid.UUID
    vr_file_url: Optional[str] = None
    ar_marker_url: Optional[str] = None
    ar_content_url: Optional[str] = None
    views_count: int
    rating: float
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AR/VR Usage
class ARVRUsageCreate(BaseModel):
    content_id: uuid.UUID
    session_duration: Optional[int] = None
    completion_percentage: Optional[float] = Field(None, ge=0, le=100)
    interaction_count: Optional[int] = None
    device_type: Optional[str] = Field(None, max_length=50)
    device_info: Optional[Dict[str, Any]] = None
    location_data: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    feedback_rating: Optional[int] = Field(None, ge=1, le=5)
    feedback_comment: Optional[str] = None


class ARVRUsageResponse(ARVRUsageCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# IoT Devices
class IoTDeviceBase(BaseModel):
    device_id: str = Field(..., max_length=100)
    device_type: IoTDeviceType
    name: str = Field(..., max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    building: Optional[str] = Field(None, max_length=100)
    room: Optional[str] = Field(None, max_length=100)
    coordinates: Optional[Dict[str, float]] = None
    configuration: Optional[Dict[str, Any]] = None


class IoTDeviceCreate(IoTDeviceBase):
    pass


class IoTDeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    building: Optional[str] = Field(None, max_length=100)
    room: Optional[str] = Field(None, max_length=100)
    coordinates: Optional[Dict[str, float]] = None
    status: Optional[str] = Field(None, max_length=50)
    configuration: Optional[Dict[str, Any]] = None
    is_online: Optional[bool] = None


class IoTDeviceResponse(IoTDeviceBase):
    id: uuid.UUID
    status: str
    last_seen: Optional[datetime] = None
    firmware_version: Optional[str] = None
    is_online: bool
    battery_level: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# IoT Sensor Data
class IoTSensorDataCreate(BaseModel):
    device_id: uuid.UUID
    sensor_type: str = Field(..., max_length=50)
    value: float
    unit: Optional[str] = Field(None, max_length=20)
    location: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None


class IoTSensorDataResponse(IoTSensorDataCreate):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True


# Gamification Badges
class GamificationBadgeBase(BaseModel):
    badge_type: GamificationBadgeType
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    points_value: int = Field(default=0, ge=0)
    rarity: str = Field(default="common", max_length=50)
    criteria: Optional[Dict[str, Any]] = None


class GamificationBadgeCreate(GamificationBadgeBase):
    pass


class GamificationBadgeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    points_value: Optional[int] = Field(None, ge=0)
    rarity: Optional[str] = Field(None, max_length=50)
    criteria: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class GamificationBadgeResponse(GamificationBadgeBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# User Badges
class UserBadgeCreate(BaseModel):
    badge_id: uuid.UUID
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    evidence: Optional[Dict[str, Any]] = None


class UserBadgeUpdate(BaseModel):
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    is_earned: Optional[bool] = None
    evidence: Optional[Dict[str, Any]] = None


class UserBadgeResponse(UserBadgeCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    is_earned: bool
    earned_at: Optional[datetime] = None
    awarded_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Gamification Points
class GamificationPointsBase(BaseModel):
    points: int = Field(default=0, ge=0)
    level: int = Field(default=1, ge=1)
    experience_points: int = Field(default=0, ge=0)
    total_achievements: int = Field(default=0, ge=0)
    streak_days: int = Field(default=0, ge=0)


class GamificationPointsCreate(GamificationPointsBase):
    pass


class GamificationPointsUpdate(BaseModel):
    points: Optional[int] = Field(None, ge=0)
    level: Optional[int] = Field(None, ge=1)
    experience_points: Optional[int] = Field(None, ge=0)
    total_achievements: Optional[int] = Field(None, ge=0)
    streak_days: Optional[int] = Field(None, ge=0)


class GamificationPointsResponse(GamificationPointsBase):
    id: uuid.UUID
    user_id: uuid.UUID
    last_activity: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Advanced Analytics
class AdvancedAnalyticsBase(BaseModel):
    analytics_type: str = Field(..., max_length=100)
    target_entity: Optional[str] = Field(None, max_length=100)
    entity_id: Optional[uuid.UUID] = None
    prediction_model: Optional[str] = Field(None, max_length=100)
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    prediction_data: Optional[Dict[str, Any]] = None
    insights: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    risk_factors: Optional[Dict[str, Any]] = None
    trend_analysis: Optional[Dict[str, Any]] = None


class AdvancedAnalyticsCreate(AdvancedAnalyticsBase):
    expires_at: Optional[datetime] = None


class AdvancedAnalyticsResponse(AdvancedAnalyticsBase):
    id: uuid.UUID
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Predictive Models
class PredictiveModelBase(BaseModel):
    model_name: str = Field(..., max_length=100)
    model_type: str = Field(..., max_length=100)
    purpose: str = Field(..., max_length=200)
    version: str = Field(..., max_length=50)
    hyperparameters: Optional[Dict[str, Any]] = None


class PredictiveModelCreate(PredictiveModelBase):
    pass


class PredictiveModelUpdate(BaseModel):
    model_name: Optional[str] = Field(None, max_length=100)
    accuracy_score: Optional[float] = Field(None, ge=0, le=1)
    precision_score: Optional[float] = Field(None, ge=0, le=1)
    recall_score: Optional[float] = Field(None, ge=0, le=1)
    f1_score: Optional[float] = Field(None, ge=0, le=1)
    model_file_path: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    feature_importance: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class PredictiveModelResponse(PredictiveModelBase):
    id: uuid.UUID
    accuracy_score: Optional[float] = None
    precision_score: Optional[float] = None
    recall_score: Optional[float] = None
    f1_score: Optional[float] = None
    training_data_size: Optional[int] = None
    last_trained: Optional[datetime] = None
    model_file_path: Optional[str] = None
    feature_importance: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Smart Schedule
class SmartScheduleBase(BaseModel):
    schedule_type: str = Field(..., max_length=100)
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = Field(None, max_length=200)
    room_id: Optional[uuid.UUID] = None
    teacher_id: Optional[uuid.UUID] = None
    class_id: Optional[uuid.UUID] = None
    ai_optimized: bool = False
    optimization_factors: Optional[Dict[str, Any]] = None
    priority_level: str = Field(default="normal", max_length=50)
    recurrence_pattern: Optional[Dict[str, Any]] = None
    notifications: Optional[Dict[str, Any]] = None


class SmartScheduleCreate(SmartScheduleBase):
    pass


class SmartScheduleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)
    room_id: Optional[uuid.UUID] = None
    teacher_id: Optional[uuid.UUID] = None
    class_id: Optional[uuid.UUID] = None
    ai_optimized: Optional[bool] = None
    optimization_factors: Optional[Dict[str, Any]] = None
    priority_level: Optional[str] = Field(None, max_length=50)
    recurrence_pattern: Optional[Dict[str, Any]] = None
    notifications: Optional[Dict[str, Any]] = None


class SmartScheduleResponse(SmartScheduleBase):
    id: uuid.UUID
    conflict_resolved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Voice Assistant
class VoiceAssistantCreate(BaseModel):
    session_id: str = Field(..., max_length=100)
    command_type: str = Field(..., max_length=100)
    voice_input: Optional[str] = None
    processed_command: Optional[str] = None
    intent: Optional[str] = Field(None, max_length=100)
    entities: Optional[Dict[str, Any]] = None
    response_text: Optional[str] = None
    response_audio_url: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    execution_success: Optional[bool] = None
    execution_time: Optional[float] = Field(None, ge=0)
    device_info: Optional[Dict[str, Any]] = None
    location_context: Optional[Dict[str, Any]] = None


class VoiceAssistantResponse(VoiceAssistantCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Biometric Attendance
class BiometricAttendanceCreate(BaseModel):
    biometric_type: str = Field(..., max_length=50)
    device_id: Optional[str] = Field(None, max_length=100)
    verification_method: Optional[str] = Field(None, max_length=50)
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    liveness_detected: bool = True
    spoof_detection: bool = True
    location: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None


class BiometricAttendanceResponse(BiometricAttendanceCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True


# Smart Classroom
class SmartClassroomBase(BaseModel):
    room_id: uuid.UUID
    automation_enabled: bool = True
    lighting_control: bool = True
    climate_control: bool = True
    audio_system: bool = True
    projector_system: bool = True
    smart_board: bool = True
    occupancy_sensor: bool = True
    air_quality_monitor: bool = True
    noise_monitor: bool = True
    configuration: Optional[Dict[str, Any]] = None
    schedule_automation: Optional[Dict[str, Any]] = None
    energy_usage: Optional[Dict[str, Any]] = None
    maintenance_alerts: Optional[Dict[str, Any]] = None


class SmartClassroomCreate(SmartClassroomBase):
    pass


class SmartClassroomUpdate(BaseModel):
    automation_enabled: Optional[bool] = None
    lighting_control: Optional[bool] = None
    climate_control: Optional[bool] = None
    audio_system: Optional[bool] = None
    projector_system: Optional[bool] = None
    smart_board: Optional[bool] = None
    occupancy_sensor: Optional[bool] = None
    air_quality_monitor: Optional[bool] = None
    noise_monitor: Optional[bool] = None
    configuration: Optional[Dict[str, Any]] = None
    schedule_automation: Optional[Dict[str, Any]] = None
    energy_usage: Optional[Dict[str, Any]] = None
    maintenance_alerts: Optional[Dict[str, Any]] = None


class SmartClassroomResponse(SmartClassroomBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# List Responses
class BlockchainCertificateList(BaseModel):
    certificates: List[BlockchainCertificateResponse]
    total: int
    page: int
    size: int


class ARVRContentList(BaseModel):
    content: List[ARVRContentResponse]
    total: int
    page: int
    size: int


class IoTDeviceList(BaseModel):
    devices: List[IoTDeviceResponse]
    total: int
    page: int
    size: int


class GamificationBadgeList(BaseModel):
    badges: List[GamificationBadgeResponse]
    total: int
    page: int
    size: int


class UserBadgeList(BaseModel):
    badges: List[UserBadgeResponse]
    total: int
    page: int
    size: int


class SmartScheduleList(BaseModel):
    schedules: List[SmartScheduleResponse]
    total: int
    page: int
    size: int


# Search and Filter Schemas
class AdvancedFeaturesSearch(BaseModel):
    query: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field(None, regex="^(asc|desc)$")
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


# Analytics and Reports
class AdvancedAnalyticsReport(BaseModel):
    total_certificates: int
    total_arvr_content: int
    total_iot_devices: int
    total_badges_earned: int
    total_voice_interactions: int
    total_biometric_records: int
    smart_classroom_count: int
    predictive_models_count: int
    ai_optimized_schedules: int
    blockchain_verified_certificates: int


class GamificationLeaderboard(BaseModel):
    user_id: uuid.UUID
    username: str
    points: int
    level: int
    total_achievements: int
    streak_days: int
    rank: int


class IoTDeviceStatus(BaseModel):
    device_id: uuid.UUID
    device_name: str
    device_type: str
    status: str
    is_online: bool
    last_seen: Optional[datetime] = None
    battery_level: Optional[float] = None
    sensor_count: int
    data_points_today: int