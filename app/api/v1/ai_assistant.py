from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.ai_assistant import (
    AIChatRequest, AIChatResponse, AIFeedbackRequest,
    AISearchRequest, AISearchResponse, AIAnalyticsRequest, AIAnalyticsResponse,
    AIAssistantCreate, AIAssistantUpdate, AIAssistantResponse,
    AIConversationCreate, AIConversationUpdate, AIConversationResponse,
    AIConversationList, AIMessageList, AIKnowledgeBaseCreate,
    AIKnowledgeBaseUpdate, AIKnowledgeBaseResponse
)
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.post("/chat", response_model=AIChatResponse)
async def chat_with_ai(
    request: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Chat with AI assistant for doubt solving"""
    try:
        # Verify user is a student
        if current_user.role != UserRole.STUDENT:
            raise HTTPException(status_code=403, detail="Only students can use AI chat")
        
        # Get student ID from user
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")
        
        return await AIService.chat_with_ai(db, request, student.id, current_user.tenant_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations", response_model=AIConversationList)
async def get_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI conversations for the current user"""
    try:
        if current_user.role == UserRole.STUDENT:
            student = db.query(Student).filter(Student.user_id == current_user.id).first()
            if not student:
                raise HTTPException(status_code=404, detail="Student profile not found")
            conversations = await AIService.get_conversations(
                db, current_user.tenant_id, student.id, skip, limit
            )
        else:
            conversations = await AIService.get_conversations(
                db, current_user.tenant_id, None, skip, limit
            )
        
        total = len(conversations)
        pages = (total + limit - 1) // limit
        
        return AIConversationList(
            conversations=conversations,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/messages", response_model=AIMessageList)
async def get_conversation_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get messages for a specific conversation"""
    try:
        messages = await AIService.get_conversation_messages(
            db, conversation_id, current_user.tenant_id, skip, limit
        )
        
        total = len(messages)
        pages = (total + limit - 1) // limit
        
        return AIMessageList(
            messages=messages,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback")
async def submit_feedback(
    feedback: AIFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit feedback for AI response"""
    try:
        success = await AIService.submit_feedback(db, feedback, current_user.tenant_id)
        if success:
            return {"message": "Feedback submitted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Message not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=AISearchResponse)
async def search_knowledge_base(
    request: AISearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search AI knowledge base"""
    try:
        return await AIService.search_knowledge_base(db, request, current_user.tenant_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics", response_model=AIAnalyticsResponse)
async def get_ai_analytics(
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    assistant_id: Optional[int] = Query(None),
    subject_category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Get AI usage analytics (Admin/Teacher only)"""
    try:
        request = AIAnalyticsRequest(
            date_from=date_from,
            date_to=date_to,
            assistant_id=assistant_id,
            subject_category=subject_category
        )
        return await AIService.get_ai_analytics(db, request, current_user.tenant_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Admin endpoints for managing AI assistants
@router.post("/assistants", response_model=AIAssistantResponse)
async def create_ai_assistant(
    assistant: AIAssistantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Create a new AI assistant (Admin only)"""
    try:
        # Implementation for creating AI assistant
        # This would typically involve creating the assistant in the database
        return AIAssistantResponse(
            id=1,
            name=assistant.name,
            description=assistant.description,
            model_type=assistant.model_type,
            subject_category=assistant.subject_category,
            is_active=assistant.is_active,
            max_tokens=assistant.max_tokens,
            temperature=assistant.temperature,
            system_prompt=assistant.system_prompt,
            custom_instructions=assistant.custom_instructions,
            rate_limit_per_minute=assistant.rate_limit_per_minute,
            cost_per_token=assistant.cost_per_token,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assistants", response_model=List[AIAssistantResponse])
async def get_ai_assistants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all AI assistants for the tenant"""
    try:
        # Implementation for getting AI assistants
        # This would typically involve querying the database
        return []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assistants/{assistant_id}", response_model=AIAssistantResponse)
async def get_ai_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific AI assistant"""
    try:
        # Implementation for getting specific AI assistant
        # This would typically involve querying the database
        raise HTTPException(status_code=404, detail="AI Assistant not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/assistants/{assistant_id}", response_model=AIAssistantResponse)
async def update_ai_assistant(
    assistant_id: int,
    assistant: AIAssistantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Update an AI assistant (Admin only)"""
    try:
        # Implementation for updating AI assistant
        # This would typically involve updating the database
        raise HTTPException(status_code=404, detail="AI Assistant not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/assistants/{assistant_id}")
async def delete_ai_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Delete an AI assistant (Admin only)"""
    try:
        # Implementation for deleting AI assistant
        # This would typically involve soft deleting from database
        return {"message": "AI Assistant deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Knowledge base management
@router.post("/knowledge-base", response_model=AIKnowledgeBaseResponse)
async def create_knowledge_base_entry(
    entry: AIKnowledgeBaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Create a new knowledge base entry (Admin/Teacher only)"""
    try:
        # Implementation for creating knowledge base entry
        # This would typically involve creating the entry in the database
        return AIKnowledgeBaseResponse(
            id=1,
            title=entry.title,
            content=entry.content,
            subject_category=entry.subject_category,
            grade_level=entry.grade_level,
            tags=entry.tags,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-base", response_model=List[AIKnowledgeBaseResponse])
async def get_knowledge_base_entries(
    subject_category: Optional[str] = Query(None),
    grade_level: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get knowledge base entries"""
    try:
        # Implementation for getting knowledge base entries
        # This would typically involve querying the database
        return []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/knowledge-base/{entry_id}", response_model=AIKnowledgeBaseResponse)
async def update_knowledge_base_entry(
    entry_id: int,
    entry: AIKnowledgeBaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Update a knowledge base entry (Admin/Teacher only)"""
    try:
        # Implementation for updating knowledge base entry
        # This would typically involve updating the database
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/knowledge-base/{entry_id}")
async def delete_knowledge_base_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.TEACHER]))
):
    """Delete a knowledge base entry (Admin/Teacher only)"""
    try:
        # Implementation for deleting knowledge base entry
        # This would typically involve soft deleting from database
        return {"message": "Knowledge base entry deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Setup endpoints
@router.post("/setup/default-assistants")
async def setup_default_assistants(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
):
    """Setup default AI assistants for the tenant (Admin only)"""
    try:
        assistants = await AIService.create_default_assistants(db, current_user.tenant_id)
        return {
            "message": f"Created {len(assistants)} default AI assistants",
            "assistants": [assistant.name for assistant in assistants]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/available")
async def get_available_models():
    """Get list of available AI models"""
    try:
        models = [
            {
                "id": "mistral-7b",
                "name": "Mistral 7B",
                "description": "General purpose model, good for most subjects",
                "free": True,
                "max_tokens": 2048
            },
            {
                "id": "openhermes-2.5-mistral-7b",
                "name": "OpenHermes 2.5 Mistral 7B",
                "description": "Specialized in instruction following and educational content",
                "free": True,
                "max_tokens": 2048
            },
            {
                "id": "codellama-7b",
                "name": "Code Llama 7B",
                "description": "Specialized in programming and computer science",
                "free": True,
                "max_tokens": 2048
            },
            {
                "id": "llama-2-7b",
                "name": "Llama 2 7B",
                "description": "General purpose model with good reasoning",
                "free": True,
                "max_tokens": 2048
            },
            {
                "id": "phi-2",
                "name": "Phi-2",
                "description": "Small but efficient model for quick responses",
                "free": True,
                "max_tokens": 2048
            }
        ]
        return {"models": models}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subjects/available")
async def get_available_subjects():
    """Get list of available subject categories"""
    try:
        subjects = [
            {"id": "mathematics", "name": "Mathematics", "description": "Math and problem-solving"},
            {"id": "science", "name": "Science", "description": "Physics, Chemistry, Biology"},
            {"id": "literature", "name": "Literature", "description": "Language arts and writing"},
            {"id": "history", "name": "History", "description": "Historical events and analysis"},
            {"id": "geography", "name": "Geography", "description": "Geographical concepts and maps"},
            {"id": "computer_science", "name": "Computer Science", "description": "Programming and technology"},
            {"id": "languages", "name": "Languages", "description": "Language learning and grammar"},
            {"id": "arts", "name": "Arts", "description": "Creative arts and design"},
            {"id": "physical_education", "name": "Physical Education", "description": "Sports and fitness"},
            {"id": "general", "name": "General", "description": "General educational assistance"}
        ]
        return {"subjects": subjects}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))