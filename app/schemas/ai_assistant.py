from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

from app.models.ai_assistant import AIModelType, SubjectCategory, ConversationStatus


class AIModelTypeEnum(str, Enum):
    """Available AI model types"""
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


class SubjectCategoryEnum(str, Enum):
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


class ConversationStatusEnum(str, Enum):
    """Conversation status"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


class AIAssistantCreate(BaseModel):
    """Schema for creating an AI assistant"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    model_type: AIModelTypeEnum = AIModelTypeEnum.GPT_3_5
    subject_category: SubjectCategoryEnum = SubjectCategoryEnum.GENERAL
    max_tokens: int = Field(1000, ge=100, le=4000)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    system_prompt: Optional[str] = Field(None, max_length=2000)
    custom_instructions: Optional[str] = Field(None, max_length=1000)
    api_key: Optional[str] = Field(None, max_length=255)
    api_endpoint: Optional[str] = Field(None, max_length=255)
    rate_limit_per_minute: int = Field(60, ge=1, le=1000)
    cost_per_token: float = Field(0.0001, ge=0.0)


class AIAssistantUpdate(BaseModel):
    """Schema for updating an AI assistant"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    model_type: Optional[AIModelTypeEnum] = None
    subject_category: Optional[SubjectCategoryEnum] = None
    max_tokens: Optional[int] = Field(None, ge=100, le=4000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    system_prompt: Optional[str] = Field(None, max_length=2000)
    custom_instructions: Optional[str] = Field(None, max_length=1000)
    api_key: Optional[str] = Field(None, max_length=255)
    api_endpoint: Optional[str] = Field(None, max_length=255)
    rate_limit_per_minute: Optional[int] = Field(None, ge=1, le=1000)
    cost_per_token: Optional[float] = Field(None, ge=0.0)
    is_active: Optional[bool] = None


class AIAssistantResponse(BaseModel):
    """Schema for AI assistant response"""
    id: int
    name: str
    description: Optional[str]
    model_type: str
    subject_category: str
    is_active: bool
    max_tokens: int
    temperature: float
    system_prompt: Optional[str]
    custom_instructions: Optional[str]
    rate_limit_per_minute: int
    cost_per_token: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIConversationCreate(BaseModel):
    """Schema for creating an AI conversation"""
    subject: str = Field(..., min_length=1, max_length=100)
    topic: Optional[str] = Field(None, max_length=200)
    assistant_id: Optional[int] = None


class AIConversationUpdate(BaseModel):
    """Schema for updating an AI conversation"""
    topic: Optional[str] = Field(None, max_length=200)
    status: Optional[ConversationStatusEnum] = None


class AIConversationResponse(BaseModel):
    """Schema for AI conversation response"""
    id: int
    subject: str
    topic: Optional[str]
    status: str
    total_tokens_used: int
    total_cost: float
    started_at: datetime
    ended_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    assistant: AIAssistantResponse
    student_name: str
    teacher_name: Optional[str]

    class Config:
        from_attributes = True


class AIMessageCreate(BaseModel):
    """Schema for creating an AI message"""
    content: str = Field(..., min_length=1, max_length=4000)
    role: str = Field(..., regex="^(user|assistant|system)$")


class AIMessageResponse(BaseModel):
    """Schema for AI message response"""
    id: int
    role: str
    content: str
    tokens_used: int
    cost: float
    response_time_ms: Optional[int]
    model_used: Optional[str]
    confidence_score: Optional[float]
    feedback_rating: Optional[int]
    feedback_comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AIKnowledgeBaseCreate(BaseModel):
    """Schema for creating AI knowledge base entry"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    subject_category: SubjectCategoryEnum
    grade_level: Optional[str] = Field(None, max_length=20)
    tags: Optional[List[str]] = Field(None, max_items=10)


class AIKnowledgeBaseUpdate(BaseModel):
    """Schema for updating AI knowledge base entry"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    subject_category: Optional[SubjectCategoryEnum] = None
    grade_level: Optional[str] = Field(None, max_length=20)
    tags: Optional[List[str]] = Field(None, max_items=10)
    is_active: Optional[bool] = None


class AIKnowledgeBaseResponse(BaseModel):
    """Schema for AI knowledge base response"""
    id: int
    title: str
    content: str
    subject_category: str
    grade_level: Optional[str]
    tags: Optional[List[str]]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIPromptTemplateCreate(BaseModel):
    """Schema for creating AI prompt template"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    subject_category: SubjectCategoryEnum
    grade_level: Optional[str] = Field(None, max_length=20)
    template_content: str = Field(..., min_length=1)
    variables: Optional[List[str]] = Field(None, max_items=10)


class AIPromptTemplateUpdate(BaseModel):
    """Schema for updating AI prompt template"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    subject_category: Optional[SubjectCategoryEnum] = None
    grade_level: Optional[str] = Field(None, max_length=20)
    template_content: Optional[str] = Field(None, min_length=1)
    variables: Optional[List[str]] = Field(None, max_items=10)
    is_active: Optional[bool] = None


class AIPromptTemplateResponse(BaseModel):
    """Schema for AI prompt template response"""
    id: int
    name: str
    description: Optional[str]
    subject_category: str
    grade_level: Optional[str]
    template_content: str
    variables: Optional[List[str]]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIUsageAnalyticsResponse(BaseModel):
    """Schema for AI usage analytics response"""
    id: int
    date: datetime
    total_conversations: int
    total_messages: int
    total_tokens_used: int
    total_cost: float
    average_response_time_ms: int
    average_rating: float
    most_common_subjects: Optional[List[Dict[str, Any]]]
    created_at: datetime

    class Config:
        from_attributes = True


class AIChatRequest(BaseModel):
    """Schema for AI chat request"""
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[int] = None
    subject: Optional[str] = Field(None, max_length=100)
    topic: Optional[str] = Field(None, max_length=200)
    assistant_id: Optional[int] = None


class AIChatResponse(BaseModel):
    """Schema for AI chat response"""
    conversation_id: int
    message_id: int
    response: str
    tokens_used: int
    cost: float
    response_time_ms: int
    model_used: str
    confidence_score: Optional[float]


class AIConversationList(BaseModel):
    """Schema for paginated AI conversations"""
    conversations: List[AIConversationResponse]
    total: int
    page: int
    size: int
    pages: int


class AIMessageList(BaseModel):
    """Schema for paginated AI messages"""
    messages: List[AIMessageResponse]
    total: int
    page: int
    size: int
    pages: int


class AIFeedbackRequest(BaseModel):
    """Schema for AI feedback"""
    message_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=500)


class AISearchRequest(BaseModel):
    """Schema for AI knowledge base search"""
    query: str = Field(..., min_length=1, max_length=200)
    subject_category: Optional[SubjectCategoryEnum] = None
    grade_level: Optional[str] = None
    limit: int = Field(10, ge=1, le=50)


class AISearchResponse(BaseModel):
    """Schema for AI search response"""
    results: List[Dict[str, Any]]
    total_results: int
    search_time_ms: int


class AIAnalyticsRequest(BaseModel):
    """Schema for AI analytics request"""
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    assistant_id: Optional[int] = None
    subject_category: Optional[SubjectCategoryEnum] = None


class AIAnalyticsResponse(BaseModel):
    """Schema for AI analytics response"""
    total_conversations: int
    total_messages: int
    total_tokens_used: int
    total_cost: float
    average_response_time_ms: int
    average_rating: float
    conversations_by_subject: List[Dict[str, Any]]
    usage_trends: List[Dict[str, Any]]
    top_assistants: List[Dict[str, Any]]