"""
Notification service for sending emails, SMS, and push notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import json

from app.core.config import settings
from app.models.user import User
from app.models.tenant import Tenant

logger = logging.getLogger(__name__)


class NotificationService:
    """Notification service for sending various types of notifications"""
    
    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """Send email notification"""
        try:
            if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
                logger.warning("SMTP credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email or settings.SMTP_USERNAME
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    async def send_sms(
        to_phone: str,
        message: str,
        from_phone: Optional[str] = None
    ) -> bool:
        """Send SMS notification using Twilio"""
        try:
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
                logger.warning("Twilio credentials not configured")
                return False
            
            from twilio.rest import Client
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=message,
                from_=from_phone or settings.TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            
            logger.info(f"SMS sent successfully to {to_phone}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_phone}: {str(e)}")
            return False
    
    @staticmethod
    async def send_push_notification(
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send push notification (placeholder for future implementation)"""
        try:
            # This would integrate with Firebase Cloud Messaging or similar
            logger.info(f"Push notification sent to user {user_id}: {title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send push notification to user {user_id}: {str(e)}")
            return False
    
    @staticmethod
    async def send_welcome_email(email: str, full_name: str) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to Aiqube School Management System"
        
        html_content = f"""
        <html>
        <body>
            <h2>Welcome to Aiqube School Management System!</h2>
            <p>Dear {full_name},</p>
            <p>Thank you for registering with Aiqube School Management System. We're excited to have you on board!</p>
            <p>Please verify your email address by clicking the link below:</p>
            <p><a href="{settings.ALLOWED_HOSTS[0]}/verify-email">Verify Email</a></p>
            <p>If you have any questions, please don't hesitate to contact our support team.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        return await NotificationService.send_email(email, subject, html_content)
    
    @staticmethod
    async def send_verification_email(email: str, full_name: str, token: str) -> bool:
        """Send email verification link"""
        subject = "Verify Your Email Address"
        
        verification_url = f"{settings.ALLOWED_HOSTS[0]}/verify-email/{token}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Verify Your Email Address</h2>
            <p>Dear {full_name},</p>
            <p>Please click the link below to verify your email address:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account, please ignore this email.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        return await NotificationService.send_email(email, subject, html_content)
    
    @staticmethod
    async def send_password_reset_email(email: str, full_name: str, token: str) -> bool:
        """Send password reset email"""
        subject = "Reset Your Password"
        
        reset_url = f"{settings.ALLOWED_HOSTS[0]}/reset-password?token={token}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Reset Your Password</h2>
            <p>Dear {full_name},</p>
            <p>You requested to reset your password. Click the link below to set a new password:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        return await NotificationService.send_email(email, subject, html_content)
    
    @staticmethod
    async def send_attendance_alert(
        user: User,
        attendance_status: str,
        date: str,
        class_name: Optional[str] = None
    ) -> bool:
        """Send attendance alert notification"""
        if not user.get_notification_preferences().get('attendance_alerts', True):
            return True
        
        subject = f"Attendance Alert - {date}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Attendance Alert</h2>
            <p>Dear {user.full_name},</p>
            <p>Your attendance for {date} has been marked as <strong>{attendance_status}</strong>.</p>
            {f'<p>Class: {class_name}</p>' if class_name else ''}
            <p>If you believe this is an error, please contact your teacher or administrator.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        success = await NotificationService.send_email(user.email, subject, html_content)
        
        # Send SMS if enabled
        if user.get_notification_preferences().get('sms', False) and user.phone:
            sms_message = f"Attendance Alert: {attendance_status} on {date}"
            await NotificationService.send_sms(user.phone, sms_message)
        
        return success
    
    @staticmethod
    async def send_fee_reminder(
        user: User,
        fee_amount: float,
        due_date: str,
        fee_type: str
    ) -> bool:
        """Send fee reminder notification"""
        if not user.get_notification_preferences().get('fee_reminders', True):
            return True
        
        subject = f"Fee Reminder - {fee_type}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Fee Reminder</h2>
            <p>Dear {user.full_name},</p>
            <p>This is a reminder that your {fee_type} fee of ${fee_amount:.2f} is due on {due_date}.</p>
            <p>Please ensure timely payment to avoid any late fees.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        success = await NotificationService.send_email(user.email, subject, html_content)
        
        # Send SMS if enabled
        if user.get_notification_preferences().get('sms', False) and user.phone:
            sms_message = f"Fee Reminder: ${fee_amount:.2f} {fee_type} due on {due_date}"
            await NotificationService.send_sms(user.phone, sms_message)
        
        return success
    
    @staticmethod
    async def send_grade_update(
        user: User,
        subject_name: str,
        grade: str,
        semester: str
    ) -> bool:
        """Send grade update notification"""
        if not user.get_notification_preferences().get('grade_updates', True):
            return True
        
        subject = f"Grade Update - {subject_name}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Grade Update</h2>
            <p>Dear {user.full_name},</p>
            <p>Your grade for {subject_name} in {semester} has been updated to <strong>{grade}</strong>.</p>
            <p>You can view your complete academic record in your student portal.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        success = await NotificationService.send_email(user.email, subject, html_content)
        
        # Send SMS if enabled
        if user.get_notification_preferences().get('sms', False) and user.phone:
            sms_message = f"Grade Update: {subject_name} - {grade} ({semester})"
            await NotificationService.send_sms(user.phone, sms_message)
        
        return success
    
    @staticmethod
    async def send_assignment_deadline(
        user: User,
        assignment_title: str,
        due_date: str,
        subject_name: str
    ) -> bool:
        """Send assignment deadline reminder"""
        if not user.get_notification_preferences().get('assignment_deadlines', True):
            return True
        
        subject = f"Assignment Deadline Reminder - {assignment_title}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Assignment Deadline Reminder</h2>
            <p>Dear {user.full_name},</p>
            <p>This is a reminder that your assignment "{assignment_title}" for {subject_name} is due on {due_date}.</p>
            <p>Please ensure timely submission to avoid any penalties.</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        success = await NotificationService.send_email(user.email, subject, html_content)
        
        # Send SMS if enabled
        if user.get_notification_preferences().get('sms', False) and user.phone:
            sms_message = f"Assignment Due: {assignment_title} - {subject_name} due {due_date}"
            await NotificationService.send_sms(user.phone, sms_message)
        
        return success
    
    @staticmethod
    async def send_system_announcement(
        users: List[User],
        title: str,
        message: str,
        announcement_type: str = "general"
    ) -> Dict[str, int]:
        """Send system announcement to multiple users"""
        results = {"success": 0, "failed": 0}
        
        for user in users:
            try:
                success = await NotificationService.send_email(
                    user.email,
                    f"System Announcement: {title}",
                    f"""
                    <html>
                    <body>
                        <h2>{title}</h2>
                        <p>{message}</p>
                        <p>Best regards,<br>The Aiqube Team</p>
                    </body>
                    </html>
                    """
                )
                
                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                logger.error(f"Failed to send announcement to {user.email}: {str(e)}")
                results["failed"] += 1
        
        return results
    
    @staticmethod
    async def send_subscription_expiry_reminder(
        tenant: Tenant,
        days_remaining: int
    ) -> bool:
        """Send subscription expiry reminder to tenant admin"""
        admin_users = [user for user in tenant.users if user.role in ["admin", "super_admin"]]
        
        if not admin_users:
            return False
        
        subject = f"Subscription Expiry Reminder - {days_remaining} days remaining"
        
        html_content = f"""
        <html>
        <body>
            <h2>Subscription Expiry Reminder</h2>
            <p>Dear School Administrator,</p>
            <p>Your Aiqube School Management System subscription will expire in {days_remaining} days.</p>
            <p>To ensure uninterrupted service, please renew your subscription before the expiry date.</p>
            <p>Current Plan: {tenant.subscription_plan.value.title()}</p>
            <p>Expiry Date: {tenant.subscription_end_date}</p>
            <p>Best regards,<br>The Aiqube Team</p>
        </body>
        </html>
        """
        
        success_count = 0
        for admin in admin_users:
            if await NotificationService.send_email(admin.email, subject, html_content):
                success_count += 1
        
        return success_count > 0