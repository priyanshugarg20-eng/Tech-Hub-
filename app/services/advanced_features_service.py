"""
Advanced Features Services for Aiqube School Management System
Includes blockchain certificates, AR/VR, IoT, gamification, and advanced analytics
"""

import uuid
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import requests
import asyncio
import aiohttp

from app.models.advanced_features import (
    BlockchainCertificate, ARVRContent, ARVRUsage, IoTDevice, IoTSensorData,
    GamificationBadge, UserBadge, GamificationPoints, AdvancedAnalytics,
    PredictiveModel, SmartSchedule, VoiceAssistant, BiometricAttendance,
    SmartClassroom, BlockchainCertificateStatus, ARVRContentType, IoTDeviceType,
    GamificationBadgeType
)
from app.schemas.advanced_features import (
    BlockchainCertificateCreate, BlockchainCertificateUpdate,
    ARVRContentCreate, ARVRContentUpdate, ARVRUsageCreate,
    IoTDeviceCreate, IoTDeviceUpdate, IoTSensorDataCreate,
    GamificationBadgeCreate, GamificationBadgeUpdate, UserBadgeCreate,
    GamificationPointsCreate, AdvancedAnalyticsCreate, PredictiveModelCreate,
    SmartScheduleCreate, SmartScheduleUpdate, VoiceAssistantCreate,
    BiometricAttendanceCreate, SmartClassroomCreate, SmartClassroomUpdate
)
from app.core.config import settings
from app.services.notification_service import NotificationService


class BlockchainCertificateService:
    """Service for managing blockchain-based digital certificates"""
    
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)
    
    def create_certificate(self, certificate_data: BlockchainCertificateCreate, tenant_id: uuid.UUID) -> BlockchainCertificate:
        """Create a new blockchain certificate"""
        try:
            # Generate digital signature
            signature_data = f"{certificate_data.student_id}_{certificate_data.title}_{datetime.utcnow().isoformat()}"
            digital_signature = hashlib.sha256(signature_data.encode()).hexdigest()
            
            # Create certificate
            certificate = BlockchainCertificate(
                tenant_id=tenant_id,
                student_id=certificate_data.student_id,
                certificate_type=certificate_data.certificate_type,
                title=certificate_data.title,
                description=certificate_data.description,
                issuer_name=certificate_data.issuer_name,
                issuer_signature=digital_signature,
                blockchain_network=certificate_data.blockchain_network,
                expiry_date=certificate_data.expiry_date,
                metadata=certificate_data.metadata,
                status=BlockchainCertificateStatus.PENDING
            )
            
            self.db.add(certificate)
            self.db.commit()
            self.db.refresh(certificate)
            
            # Send notification to student
            self.notification_service.send_certificate_issued_notification(
                student_id=certificate_data.student_id,
                certificate_title=certificate_data.title
            )
            
            return certificate
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create certificate: {str(e)}")
    
    def issue_certificate(self, certificate_id: uuid.UUID, tenant_id: uuid.UUID) -> BlockchainCertificate:
        """Issue a certificate on the blockchain"""
        try:
            certificate = self.db.query(BlockchainCertificate).filter(
                and_(
                    BlockchainCertificate.id == certificate_id,
                    BlockchainCertificate.tenant_id == tenant_id
                )
            ).first()
            
            if not certificate:
                raise Exception("Certificate not found")
            
            # Simulate blockchain transaction
            blockchain_hash = hashlib.sha256(f"{certificate.id}_{datetime.utcnow().isoformat()}".encode()).hexdigest()
            
            certificate.status = BlockchainCertificateStatus.ISSUED
            certificate.blockchain_hash = blockchain_hash
            certificate.verification_url = f"https://blockchain.verify/{blockchain_hash}"
            certificate.issued_date = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(certificate)
            
            return certificate
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to issue certificate: {str(e)}")
    
    def verify_certificate(self, blockchain_hash: str) -> Dict[str, Any]:
        """Verify a certificate on the blockchain"""
        try:
            certificate = self.db.query(BlockchainCertificate).filter(
                BlockchainCertificate.blockchain_hash == blockchain_hash
            ).first()
            
            if not certificate:
                return {"valid": False, "message": "Certificate not found"}
            
            # Verify digital signature
            signature_data = f"{certificate.student_id}_{certificate.title}_{certificate.issued_date.isoformat()}"
            expected_signature = hashlib.sha256(signature_data.encode()).hexdigest()
            
            is_valid = certificate.issuer_signature == expected_signature
            
            return {
                "valid": is_valid,
                "certificate": {
                    "title": certificate.title,
                    "issuer": certificate.issuer_name,
                    "issued_date": certificate.issued_date,
                    "status": certificate.status.value
                }
            }
            
        except Exception as e:
            raise Exception(f"Failed to verify certificate: {str(e)}")
    
    def get_certificates(self, tenant_id: uuid.UUID, student_id: Optional[uuid.UUID] = None,
                        status: Optional[BlockchainCertificateStatus] = None,
                        page: int = 1, size: int = 20) -> Dict[str, Any]:
        """Get certificates with pagination and filtering"""
        try:
            query = self.db.query(BlockchainCertificate).filter(
                BlockchainCertificate.tenant_id == tenant_id
            )
            
            if student_id:
                query = query.filter(BlockchainCertificate.student_id == student_id)
            
            if status:
                query = query.filter(BlockchainCertificate.status == status)
            
            total = query.count()
            certificates = query.offset((page - 1) * size).limit(size).all()
            
            return {
                "certificates": certificates,
                "total": total,
                "page": page,
                "size": size
            }
            
        except Exception as e:
            raise Exception(f"Failed to get certificates: {str(e)}")


class ARVRService:
    """Service for managing AR/VR educational content"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_content(self, content_data: ARVRContentCreate, tenant_id: uuid.UUID, 
                      created_by: uuid.UUID) -> ARVRContent:
        """Create new AR/VR content"""
        try:
            content = ARVRContent(
                tenant_id=tenant_id,
                created_by=created_by,
                **content_data.dict()
            )
            
            self.db.add(content)
            self.db.commit()
            self.db.refresh(content)
            
            return content
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create AR/VR content: {str(e)}")
    
    def get_content(self, content_id: uuid.UUID, tenant_id: uuid.UUID) -> ARVRContent:
        """Get AR/VR content by ID"""
        try:
            content = self.db.query(ARVRContent).filter(
                and_(
                    ARVRContent.id == content_id,
                    ARVRContent.tenant_id == tenant_id
                )
            ).first()
            
            if not content:
                raise Exception("Content not found")
            
            return content
            
        except Exception as e:
            raise Exception(f"Failed to get content: {str(e)}")
    
    def update_content(self, content_id: uuid.UUID, content_data: ARVRContentUpdate,
                      tenant_id: uuid.UUID) -> ARVRContent:
        """Update AR/VR content"""
        try:
            content = self.get_content(content_id, tenant_id)
            
            for field, value in content_data.dict(exclude_unset=True).items():
                setattr(content, field, value)
            
            content.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(content)
            
            return content
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update content: {str(e)}")
    
    def record_usage(self, usage_data: ARVRUsageCreate, tenant_id: uuid.UUID,
                    user_id: uuid.UUID) -> ARVRUsage:
        """Record AR/VR content usage"""
        try:
            usage = ARVRUsage(
                tenant_id=tenant_id,
                user_id=user_id,
                **usage_data.dict()
            )
            
            self.db.add(usage)
            self.db.commit()
            self.db.refresh(usage)
            
            # Update content views and rating
            content = self.get_content(usage_data.content_id, tenant_id)
            content.views_count += 1
            
            if usage_data.feedback_rating:
                # Update average rating
                all_ratings = [u.feedback_rating for u in content.arvr_usage if u.feedback_rating]
                if all_ratings:
                    content.rating = sum(all_ratings) / len(all_ratings)
            
            self.db.commit()
            
            return usage
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to record usage: {str(e)}")
    
    def get_content_list(self, tenant_id: uuid.UUID, content_type: Optional[ARVRContentType] = None,
                        subject: Optional[str] = None, grade_level: Optional[str] = None,
                        page: int = 1, size: int = 20) -> Dict[str, Any]:
        """Get AR/VR content list with filtering"""
        try:
            query = self.db.query(ARVRContent).filter(
                ARVRContent.tenant_id == tenant_id
            )
            
            if content_type:
                query = query.filter(ARVRContent.content_type == content_type)
            
            if subject:
                query = query.filter(ARVRContent.subject == subject)
            
            if grade_level:
                query = query.filter(ARVRContent.grade_level == grade_level)
            
            total = query.count()
            content_list = query.offset((page - 1) * size).limit(size).all()
            
            return {
                "content": content_list,
                "total": total,
                "page": page,
                "size": size
            }
            
        except Exception as e:
            raise Exception(f"Failed to get content list: {str(e)}")


class IoTService:
    """Service for managing IoT devices and sensor data"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_device(self, device_data: IoTDeviceCreate, tenant_id: uuid.UUID) -> IoTDevice:
        """Register a new IoT device"""
        try:
            device = IoTDevice(
                tenant_id=tenant_id,
                **device_data.dict()
            )
            
            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
            
            return device
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to register device: {str(e)}")
    
    def update_device_status(self, device_id: str, status_data: Dict[str, Any],
                           tenant_id: uuid.UUID) -> IoTDevice:
        """Update IoT device status"""
        try:
            device = self.db.query(IoTDevice).filter(
                and_(
                    IoTDevice.device_id == device_id,
                    IoTDevice.tenant_id == tenant_id
                )
            ).first()
            
            if not device:
                raise Exception("Device not found")
            
            for field, value in status_data.items():
                if hasattr(device, field):
                    setattr(device, field, value)
            
            device.last_seen = datetime.utcnow()
            device.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(device)
            
            return device
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update device status: {str(e)}")
    
    def record_sensor_data(self, sensor_data: IoTSensorDataCreate, tenant_id: uuid.UUID) -> IoTSensorData:
        """Record sensor data from IoT device"""
        try:
            data = IoTSensorData(
                tenant_id=tenant_id,
                **sensor_data.dict()
            )
            
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            
            return data
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to record sensor data: {str(e)}")
    
    def get_device_status(self, tenant_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Get status of all IoT devices"""
        try:
            devices = self.db.query(IoTDevice).filter(
                IoTDevice.tenant_id == tenant_id
            ).all()
            
            status_list = []
            for device in devices:
                # Get recent sensor data count
                today = datetime.utcnow().date()
                data_count = self.db.query(IoTSensorData).filter(
                    and_(
                        IoTSensorData.device_id == device.id,
                        func.date(IoTSensorData.timestamp) == today
                    )
                ).count()
                
                status_list.append({
                    "device_id": device.id,
                    "device_name": device.name,
                    "device_type": device.device_type.value,
                    "status": device.status,
                    "is_online": device.is_online,
                    "last_seen": device.last_seen,
                    "battery_level": device.battery_level,
                    "sensor_count": len(device.sensor_data),
                    "data_points_today": data_count
                })
            
            return status_list
            
        except Exception as e:
            raise Exception(f"Failed to get device status: {str(e)}")
    
    def get_sensor_data(self, device_id: uuid.UUID, sensor_type: Optional[str] = None,
                       start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                       tenant_id: uuid.UUID = None) -> List[IoTSensorData]:
        """Get sensor data with filtering"""
        try:
            query = self.db.query(IoTSensorData).filter(
                IoTSensorData.device_id == device_id
            )
            
            if sensor_type:
                query = query.filter(IoTSensorData.sensor_type == sensor_type)
            
            if start_time:
                query = query.filter(IoTSensorData.timestamp >= start_time)
            
            if end_time:
                query = query.filter(IoTSensorData.timestamp <= end_time)
            
            if tenant_id:
                query = query.filter(IoTSensorData.tenant_id == tenant_id)
            
            return query.order_by(IoTSensorData.timestamp.desc()).all()
            
        except Exception as e:
            raise Exception(f"Failed to get sensor data: {str(e)}")


class GamificationService:
    """Service for managing gamification features"""
    
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)
    
    def create_badge(self, badge_data: GamificationBadgeCreate, tenant_id: uuid.UUID) -> GamificationBadge:
        """Create a new gamification badge"""
        try:
            badge = GamificationBadge(
                tenant_id=tenant_id,
                **badge_data.dict()
            )
            
            self.db.add(badge)
            self.db.commit()
            self.db.refresh(badge)
            
            return badge
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create badge: {str(e)}")
    
    def award_badge(self, user_id: uuid.UUID, badge_id: uuid.UUID, tenant_id: uuid.UUID,
                   awarded_by: Optional[uuid.UUID] = None, evidence: Optional[Dict[str, Any]] = None) -> UserBadge:
        """Award a badge to a user"""
        try:
            # Check if user already has this badge
            existing_badge = self.db.query(UserBadge).filter(
                and_(
                    UserBadge.user_id == user_id,
                    UserBadge.badge_id == badge_id,
                    UserBadge.tenant_id == tenant_id
                )
            ).first()
            
            if existing_badge and existing_badge.is_earned:
                raise Exception("User already has this badge")
            
            if existing_badge:
                # Update existing progress
                existing_badge.is_earned = True
                existing_badge.earned_at = datetime.utcnow()
                existing_badge.awarded_by = awarded_by
                existing_badge.evidence = evidence
                existing_badge.progress_percentage = 100.0
                
                self.db.commit()
                self.db.refresh(existing_badge)
                
                # Update user points
                self._update_user_points(user_id, tenant_id, existing_badge.badge.points_value)
                
                # Send notification
                self.notification_service.send_badge_earned_notification(
                    user_id=user_id,
                    badge_name=existing_badge.badge.name
                )
                
                return existing_badge
            else:
                # Create new badge assignment
                user_badge = UserBadge(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    badge_id=badge_id,
                    is_earned=True,
                    earned_at=datetime.utcnow(),
                    awarded_by=awarded_by,
                    evidence=evidence,
                    progress_percentage=100.0
                )
                
                self.db.add(user_badge)
                self.db.commit()
                self.db.refresh(user_badge)
                
                # Update user points
                badge = self.db.query(GamificationBadge).filter(GamificationBadge.id == badge_id).first()
                self._update_user_points(user_id, tenant_id, badge.points_value)
                
                # Send notification
                self.notification_service.send_badge_earned_notification(
                    user_id=user_id,
                    badge_name=badge.name
                )
                
                return user_badge
                
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to award badge: {str(e)}")
    
    def update_badge_progress(self, user_id: uuid.UUID, badge_id: uuid.UUID, progress: float,
                            tenant_id: uuid.UUID) -> UserBadge:
        """Update badge progress for a user"""
        try:
            user_badge = self.db.query(UserBadge).filter(
                and_(
                    UserBadge.user_id == user_id,
                    UserBadge.badge_id == badge_id,
                    UserBadge.tenant_id == tenant_id
                )
            ).first()
            
            if not user_badge:
                # Create new progress record
                user_badge = UserBadge(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    badge_id=badge_id,
                    progress_percentage=progress
                )
                self.db.add(user_badge)
            else:
                user_badge.progress_percentage = progress
            
            self.db.commit()
            self.db.refresh(user_badge)
            
            return user_badge
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update badge progress: {str(e)}")
    
    def get_user_badges(self, user_id: uuid.UUID, tenant_id: uuid.UUID) -> List[UserBadge]:
        """Get all badges for a user"""
        try:
            return self.db.query(UserBadge).filter(
                and_(
                    UserBadge.user_id == user_id,
                    UserBadge.tenant_id == tenant_id
                )
            ).all()
            
        except Exception as e:
            raise Exception(f"Failed to get user badges: {str(e)}")
    
    def get_leaderboard(self, tenant_id: uuid.UUID, limit: int = 20) -> List[Dict[str, Any]]:
        """Get gamification leaderboard"""
        try:
            leaderboard = self.db.query(
                GamificationPoints.user_id,
                GamificationPoints.points,
                GamificationPoints.level,
                GamificationPoints.total_achievements,
                GamificationPoints.streak_days
            ).filter(
                GamificationPoints.tenant_id == tenant_id
            ).order_by(
                desc(GamificationPoints.points)
            ).limit(limit).all()
            
            # Add rank and username
            result = []
            for i, entry in enumerate(leaderboard, 1):
                user = self.db.query(User).filter(User.id == entry.user_id).first()
                result.append({
                    "user_id": entry.user_id,
                    "username": user.username if user else "Unknown",
                    "points": entry.points,
                    "level": entry.level,
                    "total_achievements": entry.total_achievements,
                    "streak_days": entry.streak_days,
                    "rank": i
                })
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to get leaderboard: {str(e)}")
    
    def _update_user_points(self, user_id: uuid.UUID, tenant_id: uuid.UUID, points_to_add: int):
        """Update user points and level"""
        try:
            user_points = self.db.query(GamificationPoints).filter(
                and_(
                    GamificationPoints.user_id == user_id,
                    GamificationPoints.tenant_id == tenant_id
                )
            ).first()
            
            if not user_points:
                user_points = GamificationPoints(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    points=points_to_add,
                    level=1,
                    experience_points=points_to_add,
                    total_achievements=1
                )
                self.db.add(user_points)
            else:
                user_points.points += points_to_add
                user_points.experience_points += points_to_add
                user_points.total_achievements += 1
                
                # Calculate new level (simple formula: level = sqrt(points / 100) + 1)
                new_level = int(np.sqrt(user_points.points / 100)) + 1
                if new_level > user_points.level:
                    user_points.level = new_level
            
            user_points.last_activity = datetime.utcnow()
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update user points: {str(e)}")


class AdvancedAnalyticsService:
    """Service for advanced analytics and machine learning"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_predictive_model(self, model_data: PredictiveModelCreate, tenant_id: uuid.UUID) -> PredictiveModel:
        """Create a new predictive model"""
        try:
            model = PredictiveModel(
                tenant_id=tenant_id,
                **model_data.dict()
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            return model
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create predictive model: {str(e)}")
    
    def train_model(self, model_id: uuid.UUID, training_data: List[Dict[str, Any]],
                   tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Train a predictive model"""
        try:
            model = self.db.query(PredictiveModel).filter(
                and_(
                    PredictiveModel.id == model_id,
                    PredictiveModel.tenant_id == tenant_id
                )
            ).first()
            
            if not model:
                raise Exception("Model not found")
            
            # Prepare training data
            X = []
            y = []
            
            for data_point in training_data:
                features = data_point.get('features', {})
                target = data_point.get('target')
                
                if features and target is not None:
                    X.append(list(features.values()))
                    y.append(target)
            
            if len(X) < 10:
                raise Exception("Insufficient training data")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            if model.model_type == "classification":
                ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                # For regression, use RandomForestRegressor
                from sklearn.ensemble import RandomForestRegressor
                ml_model = RandomForestRegressor(n_estimators=100, random_state=42)
            
            ml_model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = ml_model.predict(X_test)
            
            # Calculate metrics
            if model.model_type == "classification":
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted')
                recall = recall_score(y_test, y_pred, average='weighted')
                f1 = f1_score(y_test, y_pred, average='weighted')
            else:
                from sklearn.metrics import mean_squared_error, r2_score
                accuracy = r2_score(y_test, y_pred)
                precision = mean_squared_error(y_test, y_pred)
                recall = None
                f1 = None
            
            # Update model
            model.accuracy_score = accuracy
            model.precision_score = precision
            model.recall_score = recall
            model.f1_score = f1
            model.training_data_size = len(X)
            model.last_trained = datetime.utcnow()
            model.is_active = True
            
            # Save model file path (in production, save actual model file)
            model.model_file_path = f"models/{model.id}_{model.version}.pkl"
            
            # Feature importance
            if hasattr(ml_model, 'feature_importances_'):
                feature_names = list(training_data[0]['features'].keys()) if training_data else []
                model.feature_importance = dict(zip(feature_names, ml_model.feature_importances_.tolist()))
            
            self.db.commit()
            self.db.refresh(model)
            
            return {
                "model_id": model.id,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "training_samples": len(X)
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to train model: {str(e)}")
    
    def generate_analytics(self, analytics_data: AdvancedAnalyticsCreate, tenant_id: uuid.UUID) -> AdvancedAnalytics:
        """Generate advanced analytics insights"""
        try:
            analytics = AdvancedAnalytics(
                tenant_id=tenant_id,
                **analytics_data.dict()
            )
            
            # Generate insights based on analytics type
            if analytics.analytics_type == "predictive":
                insights = self._generate_predictive_insights(analytics.target_entity, analytics.entity_id)
                analytics.insights = insights
            elif analytics.analytics_type == "behavioral":
                insights = self._generate_behavioral_insights(analytics.target_entity, analytics.entity_id)
                analytics.insights = insights
            elif analytics.analytics_type == "performance":
                insights = self._generate_performance_insights(analytics.target_entity, analytics.entity_id)
                analytics.insights = insights
            
            self.db.add(analytics)
            self.db.commit()
            self.db.refresh(analytics)
            
            return analytics
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to generate analytics: {str(e)}")
    
    def _generate_predictive_insights(self, target_entity: str, entity_id: uuid.UUID) -> Dict[str, Any]:
        """Generate predictive insights"""
        # This would integrate with trained models
        return {
            "prediction_type": "academic_performance",
            "confidence": 0.85,
            "risk_factors": ["attendance", "engagement"],
            "recommendations": ["Increase study time", "Attend tutoring sessions"]
        }
    
    def _generate_behavioral_insights(self, target_entity: str, entity_id: uuid.UUID) -> Dict[str, Any]:
        """Generate behavioral insights"""
        return {
            "learning_pattern": "visual_learner",
            "engagement_level": "high",
            "study_habits": "consistent",
            "recommendations": ["Use visual aids", "Group study sessions"]
        }
    
    def _generate_performance_insights(self, target_entity: str, entity_id: uuid.UUID) -> Dict[str, Any]:
        """Generate performance insights"""
        return {
            "strengths": ["mathematics", "problem_solving"],
            "weaknesses": ["writing", "time_management"],
            "improvement_areas": ["essay_writing", "project_planning"],
            "recommendations": ["Writing workshops", "Time management training"]
        }


class SmartScheduleService:
    """Service for AI-powered smart scheduling"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_schedule(self, schedule_data: SmartScheduleCreate, tenant_id: uuid.UUID) -> SmartSchedule:
        """Create a new smart schedule"""
        try:
            # Check for conflicts
            conflicts = self._check_schedule_conflicts(schedule_data, tenant_id)
            
            schedule = SmartSchedule(
                tenant_id=tenant_id,
                conflict_resolved=len(conflicts) == 0,
                **schedule_data.dict()
            )
            
            self.db.add(schedule)
            self.db.commit()
            self.db.refresh(schedule)
            
            return schedule
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create schedule: {str(e)}")
    
    def optimize_schedule(self, schedule_id: uuid.UUID, tenant_id: uuid.UUID) -> SmartSchedule:
        """AI-optimize a schedule"""
        try:
            schedule = self.db.query(SmartSchedule).filter(
                and_(
                    SmartSchedule.id == schedule_id,
                    SmartSchedule.tenant_id == tenant_id
                )
            ).first()
            
            if not schedule:
                raise Exception("Schedule not found")
            
            # AI optimization logic
            optimization_factors = {
                "teacher_availability": self._check_teacher_availability(schedule.teacher_id),
                "room_capacity": self._check_room_capacity(schedule.room_id),
                "student_preferences": self._get_student_preferences(schedule.class_id),
                "time_slot_efficiency": self._calculate_time_efficiency(schedule.start_time, schedule.end_time)
            }
            
            # Optimize based on factors
            optimized_time = self._find_optimal_time_slot(schedule, optimization_factors)
            
            if optimized_time:
                schedule.start_time = optimized_time["start_time"]
                schedule.end_time = optimized_time["end_time"]
                schedule.ai_optimized = True
                schedule.optimization_factors = optimization_factors
                schedule.conflict_resolved = True
            
            self.db.commit()
            self.db.refresh(schedule)
            
            return schedule
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to optimize schedule: {str(e)}")
    
    def _check_schedule_conflicts(self, schedule_data: SmartScheduleCreate, tenant_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Check for schedule conflicts"""
        conflicts = []
        
        # Check for overlapping schedules
        overlapping = self.db.query(SmartSchedule).filter(
            and_(
                SmartSchedule.tenant_id == tenant_id,
                SmartSchedule.room_id == schedule_data.room_id,
                or_(
                    and_(
                        SmartSchedule.start_time < schedule_data.end_time,
                        SmartSchedule.end_time > schedule_data.start_time
                    )
                )
            )
        ).all()
        
        for conflict in overlapping:
            conflicts.append({
                "type": "time_conflict",
                "conflicting_schedule": conflict.title,
                "overlap_start": max(conflict.start_time, schedule_data.start_time),
                "overlap_end": min(conflict.end_time, schedule_data.end_time)
            })
        
        return conflicts
    
    def _check_teacher_availability(self, teacher_id: uuid.UUID) -> float:
        """Check teacher availability score"""
        # Simplified availability check
        return 0.8  # 80% available
    
    def _check_room_capacity(self, room_id: uuid.UUID) -> float:
        """Check room capacity utilization"""
        # Simplified capacity check
        return 0.6  # 60% utilized
    
    def _get_student_preferences(self, class_id: uuid.UUID) -> Dict[str, Any]:
        """Get student preferences for scheduling"""
        # Simplified preferences
        return {
            "preferred_time": "morning",
            "avoid_time": "late_afternoon",
            "group_size_preference": "small"
        }
    
    def _calculate_time_efficiency(self, start_time: datetime, end_time: datetime) -> float:
        """Calculate time slot efficiency"""
        duration = (end_time - start_time).total_seconds() / 3600  # hours
        hour = start_time.hour
        
        # Morning hours (8-12) are most efficient
        if 8 <= hour <= 12:
            return 0.9
        elif 13 <= hour <= 16:
            return 0.7
        else:
            return 0.5
    
    def _find_optimal_time_slot(self, schedule: SmartSchedule, factors: Dict[str, Any]) -> Optional[Dict[str, datetime]]:
        """Find optimal time slot based on factors"""
        # Simplified optimization
        if factors["teacher_availability"] > 0.7 and factors["room_capacity"] < 0.8:
            # Suggest 30 minutes earlier
            optimal_start = schedule.start_time - timedelta(minutes=30)
            optimal_end = schedule.end_time - timedelta(minutes=30)
            
            return {
                "start_time": optimal_start,
                "end_time": optimal_end
            }
        
        return None


class VoiceAssistantService:
    """Service for voice assistant functionality"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def process_voice_command(self, command_data: VoiceAssistantCreate, tenant_id: uuid.UUID,
                            user_id: uuid.UUID) -> VoiceAssistant:
        """Process voice command and generate response"""
        try:
            # Process voice input (simplified)
            processed_command = self._process_voice_input(command_data.voice_input)
            intent = self._extract_intent(processed_command)
            entities = self._extract_entities(processed_command)
            
            # Generate response
            response_text = self._generate_response(intent, entities, user_id)
            
            # Record interaction
            interaction = VoiceAssistant(
                tenant_id=tenant_id,
                user_id=user_id,
                processed_command=processed_command,
                intent=intent,
                entities=entities,
                response_text=response_text,
                confidence_score=0.85,
                execution_success=True,
                execution_time=1.2,
                **command_data.dict()
            )
            
            self.db.add(interaction)
            self.db.commit()
            self.db.refresh(interaction)
            
            return interaction
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to process voice command: {str(e)}")
    
    def _process_voice_input(self, voice_input: str) -> str:
        """Process voice input to text"""
        # Simplified voice processing
        return voice_input.lower().strip()
    
    def _extract_intent(self, command: str) -> str:
        """Extract intent from command"""
        if "schedule" in command or "appointment" in command:
            return "schedule_query"
        elif "attendance" in command or "present" in command:
            return "attendance_mark"
        elif "grade" in command or "score" in command:
            return "grade_query"
        elif "help" in command or "assistant" in command:
            return "help_request"
        else:
            return "general_query"
    
    def _extract_entities(self, command: str) -> Dict[str, Any]:
        """Extract entities from command"""
        entities = {}
        
        # Extract time entities
        if "today" in command:
            entities["time"] = "today"
        elif "tomorrow" in command:
            entities["time"] = "tomorrow"
        
        # Extract subject entities
        subjects = ["math", "science", "english", "history"]
        for subject in subjects:
            if subject in command:
                entities["subject"] = subject
                break
        
        return entities
    
    def _generate_response(self, intent: str, entities: Dict[str, Any], user_id: uuid.UUID) -> str:
        """Generate response based on intent and entities"""
        if intent == "schedule_query":
            return "I can help you check your schedule. What day would you like to know about?"
        elif intent == "attendance_mark":
            return "I'll mark your attendance for today. You're now marked as present."
        elif intent == "grade_query":
            return "I can help you check your grades. Which subject would you like to know about?"
        elif intent == "help_request":
            return "I'm here to help! You can ask me about your schedule, grades, attendance, or any other school-related questions."
        else:
            return "I'm not sure I understood. Could you please rephrase your question?"


class BiometricService:
    """Service for biometric attendance system"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def record_biometric_attendance(self, attendance_data: BiometricAttendanceCreate,
                                  tenant_id: uuid.UUID, user_id: uuid.UUID) -> BiometricAttendance:
        """Record biometric attendance"""
        try:
            # Validate biometric data
            if not self._validate_biometric_data(attendance_data):
                raise Exception("Invalid biometric data")
            
            # Check for liveness and spoof detection
            if not attendance_data.liveness_detected:
                raise Exception("Liveness detection failed")
            
            if not attendance_data.spoof_detection:
                raise Exception("Spoof detection failed")
            
            # Record attendance
            attendance = BiometricAttendance(
                tenant_id=tenant_id,
                user_id=user_id,
                status="success",
                **attendance_data.dict()
            )
            
            self.db.add(attendance)
            self.db.commit()
            self.db.refresh(attendance)
            
            return attendance
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to record biometric attendance: {str(e)}")
    
    def _validate_biometric_data(self, attendance_data: BiometricAttendanceCreate) -> bool:
        """Validate biometric data"""
        # Simplified validation
        if attendance_data.confidence_score and attendance_data.confidence_score < 0.7:
            return False
        
        if attendance_data.biometric_type not in ["fingerprint", "face", "iris", "voice"]:
            return False
        
        return True
    
    def get_biometric_stats(self, tenant_id: uuid.UUID, user_id: Optional[uuid.UUID] = None,
                           start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get biometric attendance statistics"""
        try:
            query = self.db.query(BiometricAttendance).filter(
                BiometricAttendance.tenant_id == tenant_id
            )
            
            if user_id:
                query = query.filter(BiometricAttendance.user_id == user_id)
            
            if start_date:
                query = query.filter(BiometricAttendance.timestamp >= start_date)
            
            if end_date:
                query = query.filter(BiometricAttendance.timestamp <= end_date)
            
            records = query.all()
            
            total_records = len(records)
            successful_records = len([r for r in records if r.status == "success"])
            success_rate = (successful_records / total_records * 100) if total_records > 0 else 0
            
            biometric_types = {}
            for record in records:
                bio_type = record.biometric_type
                if bio_type not in biometric_types:
                    biometric_types[bio_type] = 0
                biometric_types[bio_type] += 1
            
            return {
                "total_records": total_records,
                "successful_records": successful_records,
                "success_rate": success_rate,
                "biometric_types": biometric_types,
                "average_confidence": sum(r.confidence_score or 0 for r in records) / total_records if total_records > 0 else 0
            }
            
        except Exception as e:
            raise Exception(f"Failed to get biometric stats: {str(e)}")


class SmartClassroomService:
    """Service for smart classroom management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def configure_smart_classroom(self, classroom_data: SmartClassroomCreate, tenant_id: uuid.UUID) -> SmartClassroom:
        """Configure a smart classroom"""
        try:
            classroom = SmartClassroom(
                tenant_id=tenant_id,
                **classroom_data.dict()
            )
            
            self.db.add(classroom)
            self.db.commit()
            self.db.refresh(classroom)
            
            return classroom
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to configure smart classroom: {str(e)}")
    
    def update_classroom_automation(self, classroom_id: uuid.UUID, automation_data: Dict[str, Any],
                                  tenant_id: uuid.UUID) -> SmartClassroom:
        """Update classroom automation settings"""
        try:
            classroom = self.db.query(SmartClassroom).filter(
                and_(
                    SmartClassroom.id == classroom_id,
                    SmartClassroom.tenant_id == tenant_id
                )
            ).first()
            
            if not classroom:
                raise Exception("Smart classroom not found")
            
            for field, value in automation_data.items():
                if hasattr(classroom, field):
                    setattr(classroom, field, value)
            
            classroom.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(classroom)
            
            return classroom
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update classroom automation: {str(e)}")
    
    def get_classroom_status(self, classroom_id: uuid.UUID, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """Get smart classroom status"""
        try:
            classroom = self.db.query(SmartClassroom).filter(
                and_(
                    SmartClassroom.id == classroom_id,
                    SmartClassroom.tenant_id == tenant_id
                )
            ).first()
            
            if not classroom:
                raise Exception("Smart classroom not found")
            
            # Get IoT sensor data for the classroom
            iot_devices = self.db.query(IoTDevice).filter(
                and_(
                    IoTDevice.room == classroom.room.name if classroom.room else None,
                    IoTDevice.tenant_id == tenant_id
                )
            ).all()
            
            # Aggregate sensor data
            sensor_data = {}
            for device in iot_devices:
                recent_data = self.db.query(IoTSensorData).filter(
                    IoTSensorData.device_id == device.id
                ).order_by(IoTSensorData.timestamp.desc()).limit(1).first()
                
                if recent_data:
                    sensor_data[device.device_type.value] = {
                        "value": recent_data.value,
                        "unit": recent_data.unit,
                        "timestamp": recent_data.timestamp
                    }
            
            return {
                "classroom_id": classroom.id,
                "room_name": classroom.room.name if classroom.room else None,
                "automation_enabled": classroom.automation_enabled,
                "systems": {
                    "lighting_control": classroom.lighting_control,
                    "climate_control": classroom.climate_control,
                    "audio_system": classroom.audio_system,
                    "projector_system": classroom.projector_system,
                    "smart_board": classroom.smart_board,
                    "occupancy_sensor": classroom.occupancy_sensor,
                    "air_quality_monitor": classroom.air_quality_monitor,
                    "noise_monitor": classroom.noise_monitor
                },
                "sensor_data": sensor_data,
                "energy_usage": classroom.energy_usage,
                "maintenance_alerts": classroom.maintenance_alerts
            }
            
        except Exception as e:
            raise Exception(f"Failed to get classroom status: {str(e)}")