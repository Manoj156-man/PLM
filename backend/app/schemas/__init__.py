from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import ProductPhase, ProductStatus, TaskStatus, AlertSeverity, UserRole

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.MANAGER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    current_phase: Optional[ProductPhase] = None
    status: Optional[ProductStatus] = None

class ProductResponse(ProductBase):
    id: int
    current_phase: ProductPhase
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to_agent: str

class TaskCreate(TaskBase):
    product_id: int

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    description: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    product_id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Alert Schemas ---
class AlertBase(BaseModel):
    severity: AlertSeverity
    message: str

class AlertCreate(AlertBase):
    product_id: int

class AlertUpdate(BaseModel):
    resolved: Optional[bool] = None

class AlertResponse(AlertBase):
    id: int
    product_id: int
    resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Lifecycle Event Schemas ---
class LifecycleEventBase(BaseModel):
    phase: ProductPhase
    agent_id: str
    event_type: str
    description: str

class LifecycleEventCreate(LifecycleEventBase):
    product_id: int

class LifecycleEventResponse(LifecycleEventBase):
    id: int
    product_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Composite Schema for Dashboard ---
class ProductDetailResponse(ProductResponse):
    tasks: List[TaskResponse] = []
    alerts: List[AlertResponse] = []
    events: List[LifecycleEventResponse] = []
    
    class Config:
        from_attributes = True
