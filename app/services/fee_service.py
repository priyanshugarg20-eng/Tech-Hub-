from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, date, timedelta
import logging
from decimal import Decimal

from app.models.fees import FeeRecord, Payment, FeeStructure, FeeDiscount, FeeType, PaymentStatus, PaymentMethod
from app.models.student import Student
from app.models.tenant import Tenant
from app.schemas.fees import (
    FeeCreate, FeeUpdate, FeeResponse, FeeList, FeeSearch,
    PaymentCreate, PaymentResponse, PaymentList,
    FeeStructureCreate, FeeStructureResponse,
    FeeDiscountCreate, FeeDiscountResponse,
    FeeStats, PaymentStats
)
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class FeeService:
    """Service class for fee management operations"""
    
    @staticmethod
    def create_fee_record(
        db: Session,
        fee_data: FeeCreate,
        tenant_id: int
    ) -> FeeRecord:
        """Create a new fee record for a student"""
        try:
            # Verify student exists
            student = db.query(Student).filter(
                and_(Student.id == fee_data.student_id, Student.tenant_id == tenant_id)
            ).first()
            if not student:
                raise ValueError("Student not found")
            
            # Create fee record
            fee_record = FeeRecord(
                tenant_id=tenant_id,
                student_id=fee_data.student_id,
                fee_type=fee_data.fee_type,
                academic_year=fee_data.academic_year,
                semester=fee_data.semester,
                amount=fee_data.amount,
                due_date=fee_data.due_date,
                description=fee_data.description,
                is_recurring=fee_data.is_recurring,
                recurring_frequency=fee_data.recurring_frequency,
                late_fee_amount=fee_data.late_fee_amount,
                late_fee_days=fee_data.late_fee_days,
                discount_amount=fee_data.discount_amount,
                discount_reason=fee_data.discount_reason,
                status=PaymentStatus.PENDING,
                created_by=fee_data.created_by
            )
            
            db.add(fee_record)
            db.commit()
            db.refresh(fee_record)
            
            # Send fee notification to student/parent
            if student.user.email:
                NotificationService.send_fee_reminder(
                    student.user.email,
                    student.full_name,
                    fee_record.amount,
                    fee_record.due_date,
                    tenant_id
                )
            
            logger.info(f"Created fee record {fee_record.id} for student {fee_data.student_id}")
            return fee_record
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating fee record: {str(e)}")
            raise
    
    @staticmethod
    def get_fee_records(
        db: Session,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        search: Optional[FeeSearch] = None
    ) -> FeeList:
        """Get paginated fee records with optional filtering"""
        try:
            query = db.query(FeeRecord).filter(FeeRecord.tenant_id == tenant_id)
            
            # Apply search filters
            if search:
                if search.student_id:
                    query = query.filter(FeeRecord.student_id == search.student_id)
                
                if search.fee_type:
                    query = query.filter(FeeRecord.fee_type == search.fee_type)
                
                if search.academic_year:
                    query = query.filter(FeeRecord.academic_year == search.academic_year)
                
                if search.semester:
                    query = query.filter(FeeRecord.semester == search.semester)
                
                if search.status:
                    query = query.filter(FeeRecord.status == search.status)
                
                if search.due_date_from:
                    query = query.filter(FeeRecord.due_date >= search.due_date_from)
                
                if search.due_date_to:
                    query = query.filter(FeeRecord.due_date <= search.due_date_to)
                
                if search.amount_min:
                    query = query.filter(FeeRecord.amount >= search.amount_min)
                
                if search.amount_max:
                    query = query.filter(FeeRecord.amount <= search.amount_max)
            
            # Get total count
            total = query.count()
            
            # Apply pagination and ordering
            records = query.order_by(desc(FeeRecord.due_date), desc(FeeRecord.created_at)).offset(skip).limit(limit).all()
            
            return FeeList(
                records=records,
                total=total,
                skip=skip,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error getting fee records: {str(e)}")
            raise
    
    @staticmethod
    def get_fee_record(db: Session, fee_id: int, tenant_id: int) -> Optional[FeeRecord]:
        """Get a specific fee record by ID"""
        try:
            return db.query(FeeRecord).filter(
                and_(FeeRecord.id == fee_id, FeeRecord.tenant_id == tenant_id)
            ).first()
        except Exception as e:
            logger.error(f"Error getting fee record {fee_id}: {str(e)}")
            raise
    
    @staticmethod
    def update_fee_record(
        db: Session,
        fee_id: int,
        fee_data: FeeUpdate,
        tenant_id: int
    ) -> Optional[FeeRecord]:
        """Update fee record information"""
        try:
            fee_record = FeeService.get_fee_record(db, fee_id, tenant_id)
            if not fee_record:
                return None
            
            # Update fee fields
            update_data = fee_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(fee_record, field, value)
            
            fee_record.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(fee_record)
            
            logger.info(f"Updated fee record {fee_id}")
            return fee_record
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating fee record {fee_id}: {str(e)}")
            raise
    
    @staticmethod
    def record_payment(
        db: Session,
        payment_data: PaymentCreate,
        tenant_id: int
    ) -> Payment:
        """Record a payment against a fee record"""
        try:
            # Verify fee record exists
            fee_record = FeeService.get_fee_record(db, payment_data.fee_record_id, tenant_id)
            if not fee_record:
                raise ValueError("Fee record not found")
            
            # Create payment record
            payment = Payment(
                tenant_id=tenant_id,
                fee_record_id=payment_data.fee_record_id,
                amount=payment_data.amount,
                payment_method=payment_data.payment_method,
                transaction_id=payment_data.transaction_id,
                payment_date=payment_data.payment_date or date.today(),
                notes=payment_data.notes,
                received_by=payment_data.received_by
            )
            
            db.add(payment)
            db.commit()
            db.refresh(payment)
            
            # Update fee record status
            FeeService._update_fee_record_status(db, fee_record)
            
            # Send payment confirmation
            student = fee_record.student
            if student and student.user.email:
                NotificationService.send_payment_confirmation(
                    student.user.email,
                    student.full_name,
                    payment.amount,
                    payment.payment_date,
                    tenant_id
                )
            
            logger.info(f"Recorded payment {payment.id} for fee record {payment_data.fee_record_id}")
            return payment
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error recording payment: {str(e)}")
            raise
    
    @staticmethod
    def get_payments(
        db: Session,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        fee_record_id: Optional[int] = None
    ) -> PaymentList:
        """Get paginated payment records"""
        try:
            query = db.query(Payment).filter(Payment.tenant_id == tenant_id)
            
            if fee_record_id:
                query = query.filter(Payment.fee_record_id == fee_record_id)
            
            # Get total count
            total = query.count()
            
            # Apply pagination and ordering
            payments = query.order_by(desc(Payment.payment_date), desc(Payment.created_at)).offset(skip).limit(limit).all()
            
            return PaymentList(
                payments=payments,
                total=total,
                skip=skip,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error getting payments: {str(e)}")
            raise
    
    @staticmethod
    def get_fee_stats(
        db: Session,
        tenant_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        student_id: Optional[int] = None
    ) -> FeeStats:
        """Get fee statistics"""
        try:
            query = db.query(FeeRecord).filter(FeeRecord.tenant_id == tenant_id)
            
            if start_date:
                query = query.filter(FeeRecord.due_date >= start_date)
            
            if end_date:
                query = query.filter(FeeRecord.due_date <= end_date)
            
            if student_id:
                query = query.filter(FeeRecord.student_id == student_id)
            
            # Get total records and amounts
            total_fees = query.count()
            total_amount = query.with_entities(func.sum(FeeRecord.amount)).scalar() or 0
            
            # Get status counts
            pending_fees = query.filter(FeeRecord.status == PaymentStatus.PENDING).count()
            paid_fees = query.filter(FeeRecord.status == PaymentStatus.PAID).count()
            overdue_fees = query.filter(FeeRecord.status == PaymentStatus.OVERDUE).count()
            partial_fees = query.filter(FeeRecord.status == PaymentStatus.PARTIAL).count()
            
            # Calculate overdue amount
            overdue_amount = query.filter(
                and_(
                    FeeRecord.status == PaymentStatus.OVERDUE,
                    FeeRecord.due_date < date.today()
                )
            ).with_entities(func.sum(FeeRecord.amount)).scalar() or 0
            
            # Calculate collected amount
            collected_amount = db.query(Payment).filter(
                and_(
                    Payment.tenant_id == tenant_id,
                    Payment.payment_date >= (start_date or date.min),
                    Payment.payment_date <= (end_date or date.max)
                )
            ).with_entities(func.sum(Payment.amount)).scalar() or 0
            
            return FeeStats(
                total_fees=total_fees,
                total_amount=float(total_amount),
                pending_fees=pending_fees,
                paid_fees=paid_fees,
                overdue_fees=overdue_fees,
                partial_fees=partial_fees,
                overdue_amount=float(overdue_amount),
                collected_amount=float(collected_amount),
                collection_rate=round((collected_amount / total_amount * 100) if total_amount > 0 else 0, 2)
            )
            
        except Exception as e:
            logger.error(f"Error getting fee stats: {str(e)}")
            raise
    
    @staticmethod
    def create_fee_structure(
        db: Session,
        structure_data: FeeStructureCreate,
        tenant_id: int
    ) -> FeeStructure:
        """Create a new fee structure template"""
        try:
            fee_structure = FeeStructure(
                tenant_id=tenant_id,
                name=structure_data.name,
                description=structure_data.description,
                academic_year=structure_data.academic_year,
                grade_level=structure_data.grade_level,
                fee_type=structure_data.fee_type,
                amount=structure_data.amount,
                due_date=structure_data.due_date,
                is_recurring=structure_data.is_recurring,
                recurring_frequency=structure_data.recurring_frequency,
                late_fee_amount=structure_data.late_fee_amount,
                late_fee_days=structure_data.late_fee_days,
                is_active=structure_data.is_active,
                created_by=structure_data.created_by
            )
            
            db.add(fee_structure)
            db.commit()
            db.refresh(fee_structure)
            
            logger.info(f"Created fee structure {fee_structure.id}")
            return fee_structure
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating fee structure: {str(e)}")
            raise
    
    @staticmethod
    def generate_fees_from_structure(
        db: Session,
        structure_id: int,
        tenant_id: int,
        student_ids: List[int]
    ) -> Dict[str, Any]:
        """Generate fee records for students based on fee structure"""
        try:
            # Get fee structure
            structure = db.query(FeeStructure).filter(
                and_(FeeStructure.id == structure_id, FeeStructure.tenant_id == tenant_id)
            ).first()
            
            if not structure:
                raise ValueError("Fee structure not found")
            
            results = {
                "total": len(student_ids),
                "successful": 0,
                "failed": 0,
                "errors": []
            }
            
            for student_id in student_ids:
                try:
                    # Check if student exists
                    student = db.query(Student).filter(
                        and_(Student.id == student_id, Student.tenant_id == tenant_id)
                    ).first()
                    
                    if not student:
                        raise ValueError(f"Student {student_id} not found")
                    
                    # Check if fee already exists
                    existing_fee = db.query(FeeRecord).filter(
                        and_(
                            FeeRecord.student_id == student_id,
                            FeeRecord.fee_type == structure.fee_type,
                            FeeRecord.academic_year == structure.academic_year,
                            FeeRecord.tenant_id == tenant_id
                        )
                    ).first()
                    
                    if existing_fee:
                        raise ValueError(f"Fee already exists for student {student_id}")
                    
                    # Create fee record
                    fee_record = FeeRecord(
                        tenant_id=tenant_id,
                        student_id=student_id,
                        fee_type=structure.fee_type,
                        academic_year=structure.academic_year,
                        semester=structure.grade_level,  # Using grade_level as semester
                        amount=structure.amount,
                        due_date=structure.due_date,
                        description=structure.description,
                        is_recurring=structure.is_recurring,
                        recurring_frequency=structure.recurring_frequency,
                        late_fee_amount=structure.late_fee_amount,
                        late_fee_days=structure.late_fee_days,
                        status=PaymentStatus.PENDING,
                        created_by=structure.created_by
                    )
                    
                    db.add(fee_record)
                    results["successful"] += 1
                    
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({
                        "student_id": student_id,
                        "error": str(e)
                    })
            
            db.commit()
            
            logger.info(f"Generated fees: {results['successful']} successful, {results['failed']} failed")
            return results
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating fees from structure: {str(e)}")
            raise
    
    @staticmethod
    def send_fee_reminders(
        db: Session,
        tenant_id: int,
        days_before_due: int = 7
    ) -> Dict[str, Any]:
        """Send fee reminders to students with upcoming due dates"""
        try:
            reminder_date = date.today() + timedelta(days=days_before_due)
            
            # Get fees due on reminder date
            fees_due = db.query(FeeRecord).filter(
                and_(
                    FeeRecord.tenant_id == tenant_id,
                    FeeRecord.due_date == reminder_date,
                    FeeRecord.status.in_([PaymentStatus.PENDING, PaymentStatus.PARTIAL])
                )
            ).all()
            
            results = {
                "total": len(fees_due),
                "sent": 0,
                "failed": 0,
                "errors": []
            }
            
            for fee in fees_due:
                try:
                    student = fee.student
                    if student and student.user.email:
                        NotificationService.send_fee_reminder(
                            student.user.email,
                            student.full_name,
                            fee.amount,
                            fee.due_date,
                            tenant_id
                        )
                        results["sent"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append({
                            "fee_id": fee.id,
                            "error": "Student email not found"
                        })
                        
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({
                        "fee_id": fee.id,
                        "error": str(e)
                    })
            
            logger.info(f"Sent fee reminders: {results['sent']} sent, {results['failed']} failed")
            return results
            
        except Exception as e:
            logger.error(f"Error sending fee reminders: {str(e)}")
            raise
    
    @staticmethod
    def _update_fee_record_status(db: Session, fee_record: FeeRecord):
        """Update fee record status based on payments"""
        try:
            # Calculate total paid amount
            total_paid = db.query(Payment).filter(
                Payment.fee_record_id == fee_record.id
            ).with_entities(func.sum(Payment.amount)).scalar() or 0
            
            remaining_amount = fee_record.amount - total_paid
            
            # Update status based on remaining amount
            if remaining_amount <= 0:
                fee_record.status = PaymentStatus.PAID
            elif total_paid > 0:
                fee_record.status = PaymentStatus.PARTIAL
            else:
                # Check if overdue
                if fee_record.due_date < date.today():
                    fee_record.status = PaymentStatus.OVERDUE
                else:
                    fee_record.status = PaymentStatus.PENDING
            
            fee_record.remaining_amount = remaining_amount
            db.commit()
            
        except Exception as e:
            logger.error(f"Error updating fee record status: {str(e)}")
            raise