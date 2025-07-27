"""
Advanced Features API endpoints for Aiqube School Management System
Includes blockchain certificates, AR/VR, IoT, gamification, and advanced analytics
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.security import get_current_user, get_current_tenant, RoleChecker
from app.models.user import User, UserRole
from app.services.advanced_features_service import (
    BlockchainCertificateService, ARVRService, IoTService, GamificationService,
    AdvancedAnalyticsService, SmartScheduleService, VoiceAssistantService,
    BiometricService, SmartClassroomService
)
from app.schemas.advanced_features import (
    BlockchainCertificateCreate, BlockchainCertificateUpdate, BlockchainCertificateResponse,
    BlockchainCertificateList, BlockchainCertificateStatus,
    ARVRContentCreate, ARVRContentUpdate, ARVRContentResponse, ARVRContentList,
    ARVRUsageCreate, ARVRUsageResponse, ARVRContentType,
    IoTDeviceCreate, IoTDeviceUpdate, IoTDeviceResponse, IoTDeviceList,
    IoTSensorDataCreate, IoTSensorDataResponse, IoTDeviceType,
    GamificationBadgeCreate, GamificationBadgeUpdate, GamificationBadgeResponse,
    GamificationBadgeList, GamificationBadgeType,
    UserBadgeCreate, UserBadgeResponse, UserBadgeList,
    GamificationPointsResponse, GamificationLeaderboard,
    AdvancedAnalyticsCreate, AdvancedAnalyticsResponse,
    PredictiveModelCreate, PredictiveModelResponse,
    SmartScheduleCreate, SmartScheduleUpdate, SmartScheduleResponse, SmartScheduleList,
    VoiceAssistantCreate, VoiceAssistantResponse,
    BiometricAttendanceCreate, BiometricAttendanceResponse,
    SmartClassroomCreate, SmartClassroomUpdate, SmartClassroomResponse,
    AdvancedAnalyticsReport, IoTDeviceStatus
)

router = APIRouter(prefix="/api/v1/advanced", tags=["Advanced Features"])

# Role checkers
admin_teacher_checker = RoleChecker([UserRole.ADMIN, UserRole.TEACHER])
admin_only_checker = RoleChecker([UserRole.ADMIN])
all_roles_checker = RoleChecker([UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT, UserRole.PARENT])


# ============================================================================
# BLOCKCHAIN CERTIFICATES
# ============================================================================

@router.post("/certificates/", response_model=BlockchainCertificateResponse)
async def create_blockchain_certificate(
    certificate_data: BlockchainCertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Create a new blockchain certificate"""
    try:
        service = BlockchainCertificateService(db)
        certificate = service.create_certificate(certificate_data, current_tenant)
        return certificate
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/certificates/{certificate_id}/issue", response_model=BlockchainCertificateResponse)
async def issue_blockchain_certificate(
    certificate_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Issue a certificate on the blockchain"""
    try:
        service = BlockchainCertificateService(db)
        certificate = service.issue_certificate(certificate_id, current_tenant)
        return certificate
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/certificates/verify/{blockchain_hash}")
async def verify_blockchain_certificate(
    blockchain_hash: str,
    db: Session = Depends(get_db)
):
    """Verify a certificate on the blockchain"""
    try:
        service = BlockchainCertificateService(db)
        result = service.verify_certificate(blockchain_hash)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/certificates/", response_model=BlockchainCertificateList)
async def get_blockchain_certificates(
    student_id: Optional[uuid.UUID] = None,
    status: Optional[BlockchainCertificateStatus] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get blockchain certificates with filtering"""
    try:
        service = BlockchainCertificateService(db)
        result = service.get_certificates(
            current_tenant, student_id, status, page, size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# AR/VR CONTENT
# ============================================================================

@router.post("/arvr/content/", response_model=ARVRContentResponse)
async def create_arvr_content(
    content_data: ARVRContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Create new AR/VR content"""
    try:
        service = ARVRService(db)
        content = service.create_content(content_data, current_tenant, current_user.id)
        return content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/arvr/content/{content_id}", response_model=ARVRContentResponse)
async def get_arvr_content(
    content_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get AR/VR content by ID"""
    try:
        service = ARVRService(db)
        content = service.get_content(content_id, current_tenant)
        return content
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/arvr/content/{content_id}", response_model=ARVRContentResponse)
async def update_arvr_content(
    content_id: uuid.UUID,
    content_data: ARVRContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Update AR/VR content"""
    try:
        service = ARVRService(db)
        content = service.update_content(content_id, content_data, current_tenant)
        return content
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/arvr/usage/", response_model=ARVRUsageResponse)
async def record_arvr_usage(
    usage_data: ARVRUsageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Record AR/VR content usage"""
    try:
        service = ARVRService(db)
        usage = service.record_usage(usage_data, current_tenant, current_user.id)
        return usage
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/arvr/content/", response_model=ARVRContentList)
async def get_arvr_content_list(
    content_type: Optional[ARVRContentType] = None,
    subject: Optional[str] = None,
    grade_level: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get AR/VR content list with filtering"""
    try:
        service = ARVRService(db)
        result = service.get_content_list(
            current_tenant, content_type, subject, grade_level, page, size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# IoT DEVICES
# ============================================================================

@router.post("/iot/devices/", response_model=IoTDeviceResponse)
async def register_iot_device(
    device_data: IoTDeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Register a new IoT device"""
    try:
        service = IoTService(db)
        device = service.register_device(device_data, current_tenant)
        return device
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/iot/devices/{device_id}/status", response_model=IoTDeviceResponse)
async def update_iot_device_status(
    device_id: str,
    status_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Update IoT device status"""
    try:
        service = IoTService(db)
        device = service.update_device_status(device_id, status_data, current_tenant)
        return device
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/iot/sensor-data/", response_model=IoTSensorDataResponse)
async def record_iot_sensor_data(
    sensor_data: IoTSensorDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Record sensor data from IoT device"""
    try:
        service = IoTService(db)
        data = service.record_sensor_data(sensor_data, current_tenant)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/iot/devices/status", response_model=List[IoTDeviceStatus])
async def get_iot_device_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Get status of all IoT devices"""
    try:
        service = IoTService(db)
        status_list = service.get_device_status(current_tenant)
        return status_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/iot/devices/{device_id}/sensor-data", response_model=List[IoTSensorDataResponse])
async def get_iot_sensor_data(
    device_id: uuid.UUID,
    sensor_type: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Get sensor data for a device"""
    try:
        service = IoTService(db)
        from datetime import datetime
        
        start_dt = datetime.fromisoformat(start_time) if start_time else None
        end_dt = datetime.fromisoformat(end_time) if end_time else None
        
        data = service.get_sensor_data(device_id, sensor_type, start_dt, end_dt, current_tenant)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# GAMIFICATION
# ============================================================================

@router.post("/gamification/badges/", response_model=GamificationBadgeResponse)
async def create_gamification_badge(
    badge_data: GamificationBadgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Create a new gamification badge"""
    try:
        service = GamificationService(db)
        badge = service.create_badge(badge_data, current_tenant)
        return badge
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gamification/badges/{badge_id}/award")
async def award_badge(
    badge_id: uuid.UUID,
    user_id: uuid.UUID,
    awarded_by: Optional[uuid.UUID] = None,
    evidence: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Award a badge to a user"""
    try:
        service = GamificationService(db)
        user_badge = service.award_badge(
            user_id, badge_id, current_tenant, awarded_by, evidence
        )
        return {"message": "Badge awarded successfully", "user_badge": user_badge}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/gamification/badges/{badge_id}/progress")
async def update_badge_progress(
    badge_id: uuid.UUID,
    progress: float = Query(..., ge=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Update badge progress for current user"""
    try:
        service = GamificationService(db)
        user_badge = service.update_badge_progress(
            current_user.id, badge_id, progress, current_tenant
        )
        return {"message": "Progress updated successfully", "user_badge": user_badge}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gamification/badges/", response_model=GamificationBadgeList)
async def get_gamification_badges(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get gamification badges"""
    try:
        service = GamificationService(db)
        # This would need to be implemented in the service
        badges = service.db.query(GamificationBadge).filter(
            GamificationBadge.tenant_id == current_tenant
        ).offset((page - 1) * size).limit(size).all()
        
        total = service.db.query(GamificationBadge).filter(
            GamificationBadge.tenant_id == current_tenant
        ).count()
        
        return {
            "badges": badges,
            "total": total,
            "page": page,
            "size": size
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gamification/user/badges", response_model=List[UserBadgeResponse])
async def get_user_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get badges for current user"""
    try:
        service = GamificationService(db)
        badges = service.get_user_badges(current_user.id, current_tenant)
        return badges
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gamification/leaderboard", response_model=List[GamificationLeaderboard])
async def get_gamification_leaderboard(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get gamification leaderboard"""
    try:
        service = GamificationService(db)
        leaderboard = service.get_leaderboard(current_tenant, limit)
        return leaderboard
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# ADVANCED ANALYTICS
# ============================================================================

@router.post("/analytics/generate", response_model=AdvancedAnalyticsResponse)
async def generate_advanced_analytics(
    analytics_data: AdvancedAnalyticsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Generate advanced analytics insights"""
    try:
        service = AdvancedAnalyticsService(db)
        analytics = service.generate_analytics(analytics_data, current_tenant)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analytics/models/", response_model=PredictiveModelResponse)
async def create_predictive_model(
    model_data: PredictiveModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Create a new predictive model"""
    try:
        service = AdvancedAnalyticsService(db)
        model = service.create_predictive_model(model_data, current_tenant)
        return model
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analytics/models/{model_id}/train")
async def train_predictive_model(
    model_id: uuid.UUID,
    training_data: List[Dict[str, Any]],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Train a predictive model"""
    try:
        service = AdvancedAnalyticsService(db)
        result = service.train_model(model_id, training_data, current_tenant)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# SMART SCHEDULING
# ============================================================================

@router.post("/schedules/", response_model=SmartScheduleResponse)
async def create_smart_schedule(
    schedule_data: SmartScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Create a new smart schedule"""
    try:
        service = SmartScheduleService(db)
        schedule = service.create_schedule(schedule_data, current_tenant)
        return schedule
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/schedules/{schedule_id}/optimize", response_model=SmartScheduleResponse)
async def optimize_smart_schedule(
    schedule_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """AI-optimize a schedule"""
    try:
        service = SmartScheduleService(db)
        schedule = service.optimize_schedule(schedule_id, current_tenant)
        return schedule
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/schedules/", response_model=SmartScheduleList)
async def get_smart_schedules(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Get smart schedules"""
    try:
        service = SmartScheduleService(db)
        # This would need to be implemented in the service
        schedules = service.db.query(SmartSchedule).filter(
            SmartSchedule.tenant_id == current_tenant
        ).offset((page - 1) * size).limit(size).all()
        
        total = service.db.query(SmartSchedule).filter(
            SmartSchedule.tenant_id == current_tenant
        ).count()
        
        return {
            "schedules": schedules,
            "total": total,
            "page": page,
            "size": size
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# VOICE ASSISTANT
# ============================================================================

@router.post("/voice/command", response_model=VoiceAssistantResponse)
async def process_voice_command(
    command_data: VoiceAssistantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Process voice command and generate response"""
    try:
        service = VoiceAssistantService(db)
        interaction = service.process_voice_command(command_data, current_tenant, current_user.id)
        return interaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# BIOMETRIC ATTENDANCE
# ============================================================================

@router.post("/biometric/attendance", response_model=BiometricAttendanceResponse)
async def record_biometric_attendance(
    attendance_data: BiometricAttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(all_roles_checker)
):
    """Record biometric attendance"""
    try:
        service = BiometricService(db)
        attendance = service.record_biometric_attendance(
            attendance_data, current_tenant, current_user.id
        )
        return attendance
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/biometric/stats")
async def get_biometric_stats(
    user_id: Optional[uuid.UUID] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Get biometric attendance statistics"""
    try:
        service = BiometricService(db)
        from datetime import datetime
        
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None
        
        stats = service.get_biometric_stats(current_tenant, user_id, start_dt, end_dt)
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# SMART CLASSROOM
# ============================================================================

@router.post("/classrooms/", response_model=SmartClassroomResponse)
async def configure_smart_classroom(
    classroom_data: SmartClassroomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Configure a smart classroom"""
    try:
        service = SmartClassroomService(db)
        classroom = service.configure_smart_classroom(classroom_data, current_tenant)
        return classroom
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/classrooms/{classroom_id}/automation", response_model=SmartClassroomResponse)
async def update_classroom_automation(
    classroom_id: uuid.UUID,
    automation_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_only_checker)
):
    """Update classroom automation settings"""
    try:
        service = SmartClassroomService(db)
        classroom = service.update_classroom_automation(
            classroom_id, automation_data, current_tenant
        )
        return classroom
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/classrooms/{classroom_id}/status")
async def get_classroom_status(
    classroom_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Get smart classroom status"""
    try:
        service = SmartClassroomService(db)
        status = service.get_classroom_status(classroom_id, current_tenant)
        return status
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# ADVANCED FEATURES DASHBOARD
# ============================================================================

@router.get("/dashboard/overview", response_model=AdvancedAnalyticsReport)
async def get_advanced_features_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: uuid.UUID = Depends(get_current_tenant),
    _: bool = Depends(admin_teacher_checker)
):
    """Get overview of all advanced features"""
    try:
        # Count various advanced features
        from app.models.advanced_features import (
            BlockchainCertificate, ARVRContent, IoTDevice, UserBadge,
            VoiceAssistant, BiometricAttendance, SmartClassroom,
            PredictiveModel, SmartSchedule
        )
        
        total_certificates = db.query(BlockchainCertificate).filter(
            BlockchainCertificate.tenant_id == current_tenant
        ).count()
        
        total_arvr_content = db.query(ARVRContent).filter(
            ARVRContent.tenant_id == current_tenant
        ).count()
        
        total_iot_devices = db.query(IoTDevice).filter(
            IoTDevice.tenant_id == current_tenant
        ).count()
        
        total_badges_earned = db.query(UserBadge).filter(
            and_(
                UserBadge.tenant_id == current_tenant,
                UserBadge.is_earned == True
            )
        ).count()
        
        total_voice_interactions = db.query(VoiceAssistant).filter(
            VoiceAssistant.tenant_id == current_tenant
        ).count()
        
        total_biometric_records = db.query(BiometricAttendance).filter(
            BiometricAttendance.tenant_id == current_tenant
        ).count()
        
        smart_classroom_count = db.query(SmartClassroom).filter(
            SmartClassroom.tenant_id == current_tenant
        ).count()
        
        predictive_models_count = db.query(PredictiveModel).filter(
            PredictiveModel.tenant_id == current_tenant
        ).count()
        
        ai_optimized_schedules = db.query(SmartSchedule).filter(
            and_(
                SmartSchedule.tenant_id == current_tenant,
                SmartSchedule.ai_optimized == True
            )
        ).count()
        
        blockchain_verified_certificates = db.query(BlockchainCertificate).filter(
            and_(
                BlockchainCertificate.tenant_id == current_tenant,
                BlockchainCertificate.status == BlockchainCertificateStatus.VERIFIED
            )
        ).count()
        
        return AdvancedAnalyticsReport(
            total_certificates=total_certificates,
            total_arvr_content=total_arvr_content,
            total_iot_devices=total_iot_devices,
            total_badges_earned=total_badges_earned,
            total_voice_interactions=total_voice_interactions,
            total_biometric_records=total_biometric_records,
            smart_classroom_count=smart_classroom_count,
            predictive_models_count=predictive_models_count,
            ai_optimized_schedules=ai_optimized_schedules,
            blockchain_verified_certificates=blockchain_verified_certificates
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))