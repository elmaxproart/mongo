from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str = "user" # user, artist, admin

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True

class ArtworkBase(BaseModel):
    title: str
    description: str
    price: float
    category: str
    image_url: str
    author_id: str
    author_name: str
    is_sold: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ArtworkCreate(BaseModel):
    title: str
    description: str
    price: float
    category: str
    image_url: str

class Artwork(ArtworkBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True

class Category(BaseModel):
    name: str

class OrderCreate(BaseModel):
    artwork_id: str

class Order(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    user_username: str
    artwork_id: str
    artwork_title: str
    artwork_image_url: str
    price: float
    status: str = "pending" # pending, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

