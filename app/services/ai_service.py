import asyncio
import aiohttp
import json
import time
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from datetime import datetime, timedelta

from app.models.ai_assistant import (
    AIAssistant, AIConversation, AIMessage, AIKnowledgeBase,
    AIUsageAnalytics, AIPromptTemplate, AIModelType, SubjectCategory
)
from app.schemas.ai_assistant import (
    AIChatRequest, AIChatResponse, AIFeedbackRequest,
    AISearchRequest, AISearchResponse, AIAnalyticsRequest, AIAnalyticsResponse
)
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service class for AI assistant functionality"""
    
    # Free AI model endpoints
    FREE_MODELS = {
        "llama-2-7b": {
            "endpoint": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
            "headers": {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"},
            "max_tokens": 2048,
            "temperature": 0.7
        },
        "mistral-7b": {
            "endpoint": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            "headers": {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"},
            "max_tokens": 2048,
            "temperature": 0.7
        },
        "openhermes-2.5-mistral-7b": {
            "endpoint": "https://api-inference.huggingface.co/models/teknium/OpenHermes-2.5-Mistral-7B",
            "headers": {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"},
            "max_tokens": 2048,
            "temperature": 0.7
        },
        "phi-2": {
            "endpoint": "https://api-inference.huggingface.co/models/microsoft/phi-2",
            "headers": {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"},
            "max_tokens": 2048,
            "temperature": 0.7
        },
        "codellama-7b": {
            "endpoint": "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf",
            "headers": {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"},
            "max_tokens": 2048,
            "temperature": 0.7
        }
    }
    
    # Subject-specific prompts
    SUBJECT_PROMPTS = {
        "mathematics": "You are a helpful mathematics tutor. Explain concepts clearly with step-by-step solutions. Use examples and encourage understanding rather than just giving answers.",
        "science": "You are a helpful science tutor. Explain scientific concepts clearly with real-world examples. Encourage curiosity and critical thinking.",
        "literature": "You are a helpful literature tutor. Help analyze texts, explain themes, and develop writing skills. Encourage creative thinking and interpretation.",
        "history": "You are a helpful history tutor. Explain historical events and contexts clearly. Help students understand cause and effect relationships.",
        "geography": "You are a helpful geography tutor. Explain geographical concepts with maps and real-world examples. Connect theory to practical applications.",
        "computer_science": "You are a helpful computer science tutor. Explain programming concepts clearly with code examples. Encourage problem-solving and logical thinking.",
        "languages": "You are a helpful language tutor. Help with grammar, vocabulary, and language skills. Encourage practice and cultural understanding.",
        "general": "You are a helpful educational assistant. Provide clear, accurate, and educational responses. Encourage learning and understanding."
    }
    
    @staticmethod
    async def chat_with_ai(
        db: Session,
        request: AIChatRequest,
        student_id: int,
        tenant_id: int
    ) -> AIChatResponse:
        """Chat with AI assistant"""
        try:
            start_time = time.time()
            
            # Get or create conversation
            conversation = await AIService._get_or_create_conversation(
                db, request, student_id, tenant_id
            )
            
            # Get AI assistant
            assistant = await AIService._get_ai_assistant(db, request.assistant_id, tenant_id)
            
            # Prepare system prompt
            system_prompt = await AIService._prepare_system_prompt(assistant, request.subject)
            
            # Generate AI response
            ai_response = await AIService._generate_ai_response(
                request.message, system_prompt, assistant
            )
            
            # Calculate metrics
            response_time_ms = int((time.time() - start_time) * 1000)
            tokens_used = len(request.message.split()) + len(ai_response.split())
            cost = tokens_used * assistant.cost_per_token
            
            # Save user message
            user_message = AIMessage(
                conversation_id=conversation.id,
                role="user",
                content=request.message,
                tokens_used=len(request.message.split()),
                cost=len(request.message.split()) * assistant.cost_per_token,
                created_at=datetime.utcnow()
            )
            db.add(user_message)
            
            # Save AI response
            ai_message = AIMessage(
                conversation_id=conversation.id,
                role="assistant",
                content=ai_response,
                tokens_used=len(ai_response.split()),
                cost=cost,
                response_time_ms=response_time_ms,
                model_used=assistant.model_type,
                confidence_score=0.8,  # Placeholder
                created_at=datetime.utcnow()
            )
            db.add(ai_message)
            
            # Update conversation metrics
            conversation.total_tokens_used += tokens_used
            conversation.total_cost += cost
            conversation.updated_at = datetime.utcnow()
            
            db.commit()
            
            return AIChatResponse(
                conversation_id=conversation.id,
                message_id=ai_message.id,
                response=ai_response,
                tokens_used=tokens_used,
                cost=cost,
                response_time_ms=response_time_ms,
                model_used=assistant.model_type,
                confidence_score=0.8
            )
            
        except Exception as e:
            logger.error(f"Error in AI chat: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    async def _get_or_create_conversation(
        db: Session,
        request: AIChatRequest,
        student_id: int,
        tenant_id: int
    ) -> AIConversation:
        """Get existing conversation or create new one"""
        if request.conversation_id:
            conversation = db.query(AIConversation).filter(
                and_(
                    AIConversation.id == request.conversation_id,
                    AIConversation.tenant_id == tenant_id,
                    AIConversation.student_id == student_id
                )
            ).first()
            if conversation:
                return conversation
        
        # Create new conversation
        conversation = AIConversation(
            tenant_id=tenant_id,
            assistant_id=request.assistant_id,
            student_id=student_id,
            subject=request.subject or "General",
            topic=request.topic,
            status="active",
            started_at=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    async def _get_ai_assistant(
        db: Session,
        assistant_id: Optional[int],
        tenant_id: int
    ) -> AIAssistant:
        """Get AI assistant configuration"""
        if assistant_id:
            assistant = db.query(AIAssistant).filter(
                and_(
                    AIAssistant.id == assistant_id,
                    AIAssistant.tenant_id == tenant_id,
                    AIAssistant.is_active == True
                )
            ).first()
            if assistant:
                return assistant
        
        # Get default assistant for tenant
        assistant = db.query(AIAssistant).filter(
            and_(
                AIAssistant.tenant_id == tenant_id,
                AIAssistant.is_active == True
            )
        ).first()
        
        if not assistant:
            # Create default assistant
            assistant = AIAssistant(
                tenant_id=tenant_id,
                name="Default AI Tutor",
                description="Default AI assistant for student support",
                model_type="mistral-7b",
                subject_category="general",
                is_active=True,
                max_tokens=1000,
                temperature=0.7,
                system_prompt="You are a helpful educational assistant.",
                rate_limit_per_minute=60,
                cost_per_token=0.0001,
                created_at=datetime.utcnow()
            )
            db.add(assistant)
            db.commit()
            db.refresh(assistant)
        
        return assistant
    
    @staticmethod
    async def _prepare_system_prompt(
        assistant: AIAssistant,
        subject: Optional[str]
    ) -> str:
        """Prepare system prompt for AI"""
        base_prompt = assistant.system_prompt or "You are a helpful educational assistant."
        
        if subject and subject.lower() in AIService.SUBJECT_PROMPTS:
            subject_prompt = AIService.SUBJECT_PROMPTS[subject.lower()]
            return f"{subject_prompt}\n\n{base_prompt}"
        
        return base_prompt
    
    @staticmethod
    async def _generate_ai_response(
        message: str,
        system_prompt: str,
        assistant: AIAssistant
    ) -> str:
        """Generate AI response using free models"""
        try:
            model_config = AIService.FREE_MODELS.get(assistant.model_type)
            if not model_config:
                # Fallback to mistral-7b
                model_config = AIService.FREE_MODELS["mistral-7b"]
            
            # Prepare prompt
            full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    model_config["endpoint"],
                    headers=model_config["headers"],
                    json={"inputs": full_prompt},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get("generated_text", "I'm sorry, I couldn't generate a response.")
                        elif isinstance(result, dict):
                            return result.get("generated_text", "I'm sorry, I couldn't generate a response.")
                        else:
                            return "I'm sorry, I couldn't generate a response."
                    else:
                        logger.error(f"AI API error: {response.status}")
                        return "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."
                        
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return "I'm sorry, I encountered an error. Please try again later."
    
    @staticmethod
    async def get_conversations(
        db: Session,
        tenant_id: int,
        student_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[AIConversation]:
        """Get AI conversations"""
        query = db.query(AIConversation).filter(AIConversation.tenant_id == tenant_id)
        
        if student_id:
            query = query.filter(AIConversation.student_id == student_id)
        
        return query.order_by(desc(AIConversation.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    async def get_conversation_messages(
        db: Session,
        conversation_id: int,
        tenant_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[AIMessage]:
        """Get messages for a conversation"""
        return db.query(AIMessage).filter(
            and_(
                AIMessage.conversation_id == conversation_id,
                AIConversation.tenant_id == tenant_id
            )
        ).join(AIConversation).order_by(AIMessage.created_at).offset(skip).limit(limit).all()
    
    @staticmethod
    async def submit_feedback(
        db: Session,
        feedback: AIFeedbackRequest,
        tenant_id: int
    ) -> bool:
        """Submit feedback for AI message"""
        try:
            message = db.query(AIMessage).filter(
                and_(
                    AIMessage.id == feedback.message_id,
                    AIConversation.tenant_id == tenant_id
                )
            ).join(AIConversation).first()
            
            if message:
                message.feedback_rating = feedback.rating
                message.feedback_comment = feedback.comment
                db.commit()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            db.rollback()
            return False
    
    @staticmethod
    async def search_knowledge_base(
        db: Session,
        request: AISearchRequest,
        tenant_id: int
    ) -> AISearchResponse:
        """Search knowledge base"""
        try:
            start_time = time.time()
            
            query = db.query(AIKnowledgeBase).filter(
                and_(
                    AIKnowledgeBase.tenant_id == tenant_id,
                    AIKnowledgeBase.is_active == True
                )
            )
            
            if request.subject_category:
                query = query.filter(AIKnowledgeBase.subject_category == request.subject_category)
            
            if request.grade_level:
                query = query.filter(AIKnowledgeBase.grade_level == request.grade_level)
            
            # Simple text search (can be enhanced with full-text search)
            search_term = request.query.lower()
            results = []
            
            for kb in query.all():
                if (search_term in kb.title.lower() or 
                    search_term in kb.content.lower() or
                    any(search_term in tag.lower() for tag in (kb.tags or []))):
                    results.append({
                        "id": kb.id,
                        "title": kb.title,
                        "content": kb.content[:200] + "..." if len(kb.content) > 200 else kb.content,
                        "subject_category": kb.subject_category,
                        "grade_level": kb.grade_level,
                        "tags": kb.tags
                    })
            
            search_time_ms = int((time.time() - start_time) * 1000)
            
            return AISearchResponse(
                results=results[:request.limit],
                total_results=len(results),
                search_time_ms=search_time_ms
            )
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return AISearchResponse(results=[], total_results=0, search_time_ms=0)
    
    @staticmethod
    async def get_ai_analytics(
        db: Session,
        request: AIAnalyticsRequest,
        tenant_id: int
    ) -> AIAnalyticsResponse:
        """Get AI usage analytics"""
        try:
            query = db.query(AIConversation).filter(AIConversation.tenant_id == tenant_id)
            
            if request.date_from:
                query = query.filter(AIConversation.created_at >= request.date_from)
            if request.date_to:
                query = query.filter(AIConversation.created_at <= request.date_to)
            if request.assistant_id:
                query = query.filter(AIConversation.assistant_id == request.assistant_id)
            
            conversations = query.all()
            
            total_conversations = len(conversations)
            total_messages = sum(len(conv.messages) for conv in conversations)
            total_tokens_used = sum(conv.total_tokens_used for conv in conversations)
            total_cost = sum(conv.total_cost for conv in conversations)
            
            # Calculate average response time
            response_times = []
            ratings = []
            for conv in conversations:
                for msg in conv.messages:
                    if msg.response_time_ms:
                        response_times.append(msg.response_time_ms)
                    if msg.feedback_rating:
                        ratings.append(msg.feedback_rating)
            
            average_response_time_ms = sum(response_times) // len(response_times) if response_times else 0
            average_rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            # Conversations by subject
            subject_counts = {}
            for conv in conversations:
                subject = conv.subject
                subject_counts[subject] = subject_counts.get(subject, 0) + 1
            
            conversations_by_subject = [
                {"subject": subject, "count": count}
                for subject, count in subject_counts.items()
            ]
            
            # Usage trends (daily)
            usage_trends = []
            if request.date_from and request.date_to:
                current_date = request.date_from
                while current_date <= request.date_to:
                    daily_conversations = [
                        conv for conv in conversations
                        if conv.created_at.date() == current_date.date()
                    ]
                    usage_trends.append({
                        "date": current_date.date().isoformat(),
                        "conversations": len(daily_conversations),
                        "messages": sum(len(conv.messages) for conv in daily_conversations)
                    })
                    current_date += timedelta(days=1)
            
            # Top assistants
            assistant_counts = {}
            for conv in conversations:
                assistant_name = conv.assistant.name if conv.assistant else "Default"
                assistant_counts[assistant_name] = assistant_counts.get(assistant_name, 0) + 1
            
            top_assistants = [
                {"name": name, "conversations": count}
                for name, count in sorted(assistant_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            
            return AIAnalyticsResponse(
                total_conversations=total_conversations,
                total_messages=total_messages,
                total_tokens_used=total_tokens_used,
                total_cost=total_cost,
                average_response_time_ms=average_response_time_ms,
                average_rating=average_rating,
                conversations_by_subject=conversations_by_subject,
                usage_trends=usage_trends,
                top_assistants=top_assistants
            )
            
        except Exception as e:
            logger.error(f"Error getting AI analytics: {str(e)}")
            return AIAnalyticsResponse(
                total_conversations=0,
                total_messages=0,
                total_tokens_used=0,
                total_cost=0.0,
                average_response_time_ms=0,
                average_rating=0.0,
                conversations_by_subject=[],
                usage_trends=[],
                top_assistants=[]
            )
    
    @staticmethod
    async def create_default_assistants(db: Session, tenant_id: int) -> List[AIAssistant]:
        """Create default AI assistants for a tenant"""
        default_assistants = [
            {
                "name": "Math Tutor",
                "description": "Specialized in mathematics and problem-solving",
                "model_type": "mistral-7b",
                "subject_category": "mathematics",
                "system_prompt": AIService.SUBJECT_PROMPTS["mathematics"]
            },
            {
                "name": "Science Tutor",
                "description": "Specialized in science subjects",
                "model_type": "openhermes-2.5-mistral-7b",
                "subject_category": "science",
                "system_prompt": AIService.SUBJECT_PROMPTS["science"]
            },
            {
                "name": "Code Tutor",
                "description": "Specialized in programming and computer science",
                "model_type": "codellama-7b",
                "subject_category": "computer_science",
                "system_prompt": AIService.SUBJECT_PROMPTS["computer_science"]
            },
            {
                "name": "General Tutor",
                "description": "General educational assistance",
                "model_type": "mistral-7b",
                "subject_category": "general",
                "system_prompt": AIService.SUBJECT_PROMPTS["general"]
            }
        ]
        
        assistants = []
        for assistant_data in default_assistants:
            assistant = AIAssistant(
                tenant_id=tenant_id,
                name=assistant_data["name"],
                description=assistant_data["description"],
                model_type=assistant_data["model_type"],
                subject_category=assistant_data["subject_category"],
                system_prompt=assistant_data["system_prompt"],
                is_active=True,
                max_tokens=1000,
                temperature=0.7,
                rate_limit_per_minute=60,
                cost_per_token=0.0001,
                created_at=datetime.utcnow()
            )
            db.add(assistant)
            assistants.append(assistant)
        
        db.commit()
        return assistants