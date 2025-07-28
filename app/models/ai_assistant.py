from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum

from app.core.database import Base


class AIModelType(str, Enum):
    """Available AI model types for different subjects"""
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    CLAUDE = "claude-3-sonnet"
    GEMINI = "gemini-pro"
    LLAMA = "llama-2-7b"
    MISTRAL = "mistral-7b"
    OPENHERMES = "openhermes-2.5-mistral-7b"
    PHI = "phi-2"
    CODELLAMA = "codellama-7b"
    MATH_SPECIALIST = "math-specialist"


class SubjectCategory(str, Enum):
    """Subject categories for AI assistance"""
    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    LITERATURE = "literature"
    HISTORY = "history"
    GEOGRAPHY = "geography"
    COMPUTER_SCIENCE = "computer_science"
    LANGUAGES = "languages"
    ARTS = "arts"
    PHYSICAL_EDUCATION = "physical_education"
    GENERAL = "general"


class ConversationStatus(str, Enum):
    """Conversation status"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


class AIAssistant(Base):
    """AI Assistant configuration for the school"""
    __tablename__ = "ai_assistants"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    model_type = Column(String(50), nullable=False, default=AIModelType.GPT_3_5)
    subject_category = Column(String(50), nullable=False, default=SubjectCategory.GENERAL)
    is_active = Column(Boolean, default=True)
    max_tokens = Column(Integer, default=1000)
    temperature = Column(Float, default=0.7)
    system_prompt = Column(Text)
    custom_instructions = Column(Text)
    api_key = Column(String(255))  # Encrypted in production
    api_endpoint = Column(String(255))
    rate_limit_per_minute = Column(Integer, default=60)
    cost_per_token = Column(Float, default=0.0001)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="ai_assistants")
    conversations = relationship("AIConversation", back_populates="assistant")


class AIConversation(Base):
    """AI conversation sessions"""
    __tablename__ = "ai_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    assistant_id = Column(Integer, ForeignKey("ai_assistants.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject = Column(String(100), nullable=False)
    topic = Column(String(200))
    status = Column(String(20), default=ConversationStatus.ACTIVE)
    total_tokens_used = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="ai_conversations")
    assistant = relationship("AIAssistant", back_populates="conversations")
    student = relationship("Student", back_populates="ai_conversations")
    teacher = relationship("Teacher", back_populates="ai_conversations")
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan")


class AIMessage(Base):
    """Individual messages in AI conversations"""
    __tablename__ = "ai_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    response_time_ms = Column(Integer)
    model_used = Column(String(50))
    confidence_score = Column(Float)
    feedback_rating = Column(Integer)  # 1-5 stars
    feedback_comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("AIConversation", back_populates="messages")


class AIKnowledgeBase(Base):
    """Knowledge base for AI assistants"""
    __tablename__ = "ai_knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    assistant_id = Column(Integer, ForeignKey("ai_assistants.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    subject_category = Column(String(50), nullable=False)
    grade_level = Column(String(20))
    tags = Column(JSON)  # Array of tags
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="ai_knowledge_base")
    assistant = relationship("AIAssistant")


class AIUsageAnalytics(Base):
    """Analytics for AI usage"""
    __tablename__ = "ai_usage_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    assistant_id = Column(Integer, ForeignKey("ai_assistants.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    total_conversations = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    average_response_time_ms = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    most_common_subjects = Column(JSON)  # Array of subject counts
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="ai_usage_analytics")
    assistant = relationship("AIAssistant")


class AIPromptTemplate(Base):
    """Prompt templates for different subjects and scenarios"""
    __tablename__ = "ai_prompt_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    subject_category = Column(String(50), nullable=False)
    grade_level = Column(String(20))
    template_content = Column(Text, nullable=False)
    variables = Column(JSON)  # Array of variable names
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tenant = relationship("Tenant", back_populates="ai_prompt_templates")