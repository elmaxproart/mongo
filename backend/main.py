from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from database import db
from models import UserCreate, User, ArtworkCreate, Artwork, Category, OrderCreate, Order
from auth import get_password_hash, verify_password, create_access_token, get_current_user, check_role
from bson import ObjectId
from typing import List
from datetime import datetime

app = FastAPI(title="E-Gallery API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "E-Gallery API is running", "docs": "/docs"}

# Auth Routes
@app.post("/auth/register")
async def register(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    result = await db.users.insert_one(user_dict)
    return {"id": str(result.inserted_id)}

@app.post("/auth/login")
async def login(credentials: dict = Body(...)):
    user = await db.users.find_one({"email": credentials.get("email")})
    if not user or not verify_password(credentials.get("password"), user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"], "username": user["username"], "_id": str(user["_id"])}

@app.get("/auth/me")
async def get_me(user: dict = Depends(get_current_user)):
    user_copy = user.copy()
    if "password" in user_copy:
        del user_copy["password"]
    return user_copy

# Artworks
@app.get("/artworks", response_model=List[Artwork])
async def get_artworks(category: str = None, search: str = None, sort_by: str = None, author_id: str = None):
    query = {}
    if category:
        query["category"] = category
    if author_id:
        query["author_id"] = author_id
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = db.artworks.find(query)
    
    if sort_by == "price_asc":
        cursor = cursor.sort("price", 1)
    elif sort_by == "price_desc":
        cursor = cursor.sort("price", -1)
    elif sort_by == "date_desc":
        cursor = cursor.sort("created_at", -1)
    else:
        cursor = cursor.sort("created_at", -1)
        
    artworks = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        artworks.append(doc)
    return artworks

@app.get("/artworks/{artwork_id}", response_model=Artwork)
async def get_artwork(artwork_id: str):
    try:
        doc = await db.artworks.find_one({"_id": ObjectId(artwork_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid artwork ID format")
    if not doc:
        raise HTTPException(status_code=404, detail="Artwork not found")
    doc["_id"] = str(doc["_id"])
    return doc

@app.post("/artworks", response_model=Artwork)
async def create_artwork(artwork: ArtworkCreate, user: dict = Depends(get_current_user)):
    await check_role(user, ["artist", "admin"])
    art_dict = artwork.dict()
    art_dict["author_id"] = str(user["_id"])
    art_dict["author_name"] = user["username"]
    art_dict["is_sold"] = False
    art_dict["created_at"] = datetime.utcnow()
    result = await db.artworks.insert_one(art_dict)
    art_dict["_id"] = str(result.inserted_id)
    return art_dict

@app.put("/artworks/{artwork_id}", response_model=Artwork)
async def update_artwork(artwork_id: str, artwork: ArtworkCreate, user: dict = Depends(get_current_user)):
    try:
        art = await db.artworks.find_one({"_id": ObjectId(artwork_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid artwork ID format")
    if not art:
        raise HTTPException(status_code=404, detail="Artwork not found")
    if user["role"] != "admin" and str(art["author_id"]) != str(user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to edit this artwork")
    
    update_data = artwork.dict()
    await db.artworks.update_one({"_id": ObjectId(artwork_id)}, {"$set": update_data})
    
    updated_doc = await db.artworks.find_one({"_id": ObjectId(artwork_id)})
    updated_doc["_id"] = str(updated_doc["_id"])
    return updated_doc

@app.delete("/artworks/{artwork_id}")
async def delete_artwork(artwork_id: str, user: dict = Depends(get_current_user)):
    try:
        art = await db.artworks.find_one({"_id": ObjectId(artwork_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid artwork ID format")
    if not art:
        raise HTTPException(status_code=404, detail="Not found")
    if user["role"] != "admin" and str(art["author_id"]) != str(user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.artworks.delete_one({"_id": ObjectId(artwork_id)})
    return {"message": "Deleted"}

# Orders
@app.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate, user: dict = Depends(get_current_user)):
    try:
        artwork = await db.artworks.find_one({"_id": ObjectId(order_data.artwork_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid artwork ID format")
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    if artwork.get("is_sold"):
        raise HTTPException(status_code=400, detail="Artwork is already sold")
    
    order_dict = {
        "user_id": str(user["_id"]),
        "user_username": user["username"],
        "artwork_id": str(artwork["_id"]),
        "artwork_title": artwork["title"],
        "artwork_image_url": artwork["image_url"],
        "price": artwork["price"],
        "status": "completed",
        "created_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(order_dict)
    order_dict["_id"] = str(result.inserted_id)
    
    await db.artworks.update_one({"_id": artwork["_id"]}, {"$set": {"is_sold": True}})
    return order_dict

@app.get("/orders", response_model=List[Order])
async def get_orders(user: dict = Depends(get_current_user)):
    query = {}
    if user["role"] == "admin":
        query = {}
    elif user["role"] == "artist":
        cursor_art = db.artworks.find({"author_id": str(user["_id"])})
        artwork_ids = [str(doc["_id"]) async for doc in cursor_art]
        query = {"artwork_id": {"$in": artwork_ids}}
    else:
        query = {"user_id": str(user["_id"])}
        
    cursor = db.orders.find(query).sort("created_at", -1)
    orders = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        orders.append(doc)
    return orders

# Admin
@app.get("/admin/users")
async def get_all_users(user: dict = Depends(get_current_user)):
    await check_role(user, ["admin"])
    cursor = db.users.find()
    users = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "password" in doc:
            del doc["password"]
        users.append(doc)
    return users

# Categories
@app.get("/categories")
async def get_categories():
    cursor = db.categories.find()
    return [doc["name"] async for doc in cursor]

@app.post("/categories")
async def add_category(cat: Category, user: dict = Depends(get_current_user)):
    await check_role(user, ["admin"])
    await db.categories.update_one({"name": cat.name}, {"$set": {"name": cat.name}}, upsert=True)
    return {"message": "Added"}

