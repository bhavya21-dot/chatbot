from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for creating a new user account."""
    email: EmailStr = Field(..., description="User's email address, must be unique.")
    password: str = Field(min_length=8, help="Password must be at least 8 characters long.")
    username: str = Field(min_length=3, max_length=50, help="Username must be between 3 and 50 characters.")

class UserLogin(BaseModel):
    """Schema for user login credentials."""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for returning user data (sensitive fields like password are excluded)."""
    id: str = Field(alias="_id", description="MongoDB ObjectId as string")
    username: str
    email: EmailStr
    points_balance: int = 0
    join_date: datetime
    is_admin: bool = False
    model_config = {'populate_by_name': True}

class Token(BaseModel):
    """Schema for JWT access token response."""
    access_token: str
    token_type: str = "bearer"

# --- Clothing Item Schemas ---
class ClothingItemCreate(BaseModel):
    """Schema for creating a new clothing item listing."""
    title: str = Field(min_length=3, max_length=100, description="Short, descriptive title for the item.")
    description: str = Field(min_length=10, max_length=1000, description="Detailed description of the item.")
    category: str = Field(..., description="e.g., 'Tops', 'Bottoms', 'Outerwear', 'Accessories', 'Footwear'.")
    item_type: str = Field(..., description="Specific type of item, e.g., 'T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers'.")
    size: str = Field(..., description="Item size, e.g., 'S', 'M', 'L', 'XL', 'Free Size', '30x32'.")
    condition: Literal["New with Tags", "Like New", "Used - Good", "Used - Fair"] = Field(..., description="Current condition of the item.")
    tags: List[str] = Field(default_factory=list, description="Keywords for searching, e.g., ['vintage', 'cotton', 'denim'].")
    image_urls: List[str] = Field(default_factory=list, description="URLs of item images (typically uploaded to cloud storage by frontend).")

class ClothingItemResponse(ClothingItemCreate):
    """Schema for returning clothing item data, including generated fields."""
    id: str = Field(alias="_id", description="MongoDB ObjectId as string")
    user_id: str = Field(description="ID of the user who uploaded the item.")
    status: Literal["pending_approval", "available", "swapped", "redeemed", "rejected", "removed"] = "pending_approval"
    posted_date: datetime
    model_config = {'populate_by_name': True}

class ClothingItemUpdate(BaseModel):
    """Schema for updating an existing clothing item (all fields are optional)."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    item_type: Optional[str] = None
    size: Optional[str] = None
    condition: Optional[Literal["New with Tags", "Like New", "Used - Good", "Used - Fair"]] = None
    tags: Optional[List[str]] = None
    image_urls: Optional[List[str]] = None

class SwapRequestCreate(BaseModel):
    """Schema for initiating a swap request."""
    message: Optional[str] = Field(None, max_length=500, description="Optional message from the requester.")

class SwapRequestResponse(BaseModel):
    """Schema for returning swap request details."""
    id: str = Field(alias="_id")
    item_id: str = Field(description="ID of the item being requested for swap/redemption.")
    requester_id: str = Field(description="ID of the user making the request.")
    owner_id: str = Field(description="ID of the user who owns the item.")
    status: Literal["pending", "accepted", "rejected", "completed", "cancelled"] = "pending"
    request_date: datetime
    message: Optional[str] = None
    model_config = {'populate_by_name': True}

class RedeemPointsResponse(BaseModel):
    """Schema for response after a successful point redemption."""
    message: str = Field(description="Confirmation message for the redemption.")
    new_points_balance: int = Field(description="The updated points balance of the redeeming user.")

class MessageCreate(BaseModel):
    """Schema for creating a new message."""
    receiver_id: str = Field(description="ID of the user who will receive the message.")
    content: str = Field(min_length=1, max_length=1000, description="Content of the message.")
    swap_id: Optional[str] = Field(None, description="Optional ID of a related swap, if the message is part of a swap conversation.")

class MessageResponse(BaseModel):
    """Schema for returning message details."""
    id: str = Field(alias="_id")
    sender_id: str = Field(description="ID of the user who sent the message.")
    receiver_id: str = Field(description="ID of the user who received the message.")
    content: str
    timestamp: datetime
    swap_id: Optional[str] = None
    model_config = {'populate_by_name': True}

class ItemModerationAction(BaseModel):
    """Schema for admin actions on clothing items."""
    action: Literal["approve", "reject", "remove"]
    reason: Optional[str] = Field(None, description="Reason for the moderation action.")