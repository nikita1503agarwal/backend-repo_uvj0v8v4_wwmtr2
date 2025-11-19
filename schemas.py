"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

class Perfume(BaseModel):
    """
    Perfumes collection schema for the perfume store
    Collection name: "perfume"
    """
    name: str = Field(..., description="Perfume name")
    description: Optional[str] = Field(None, description="Short description of the fragrance")
    price: float = Field(..., ge=0, description="Price in USD")
    notes: List[str] = Field(default_factory=list, description="Fragrance notes")
    concentration: Optional[str] = Field(None, description="e.g., Eau de Parfum, Eau de Toilette")
    volume_ml: Optional[int] = Field(None, ge=1, description="Bottle volume in ml")
    image: Optional[str] = Field(None, description="Image URL")
    in_stock: bool = Field(True, description="Availability")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
