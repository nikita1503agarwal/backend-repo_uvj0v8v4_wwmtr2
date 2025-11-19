import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Perfume

app = FastAPI(title="Perfume Store API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Perfume Store API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Seed endpoint to add some default perfumes if collection is empty
@app.post("/api/seed")
def seed_perfumes():
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Database not configured")
        count = db["perfume"].count_documents({})
        if count > 0:
            return {"message": "Perfumes already seeded", "count": count}
        samples = [
            {
                "name": "Iridescent Muse",
                "description": "A luminous blend of pear, iris, and soft musk.",
                "price": 120.0,
                "notes": ["pear", "iris", "musk"],
                "concentration": "Eau de Parfum",
                "volume_ml": 50,
                "image": "https://images.unsplash.com/photo-1556228720-195a672e8a03?q=80&w=1200&auto=format&fit=crop",
                "in_stock": True,
                "rating": 4.7,
            },
            {
                "name": "Violet Dawn",
                "description": "Violet petals with bergamot and cashmere woods.",
                "price": 98.0,
                "notes": ["violet", "bergamot", "cashmere wood"],
                "concentration": "Eau de Toilette",
                "volume_ml": 50,
                "image": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?q=80&w=1200&auto=format&fit=crop",
                "in_stock": True,
                "rating": 4.5,
            },
            {
                "name": "Crystal Haze",
                "description": "Sparkling citrus over amber and cedar.",
                "price": 140.0,
                "notes": ["grapefruit", "amber", "cedar"],
                "concentration": "Parfum",
                "volume_ml": 75,
                "image": "https://images.unsplash.com/photo-1585386959984-a41552231656?q=80&w=1200&auto=format&fit=crop",
                "in_stock": True,
                "rating": 4.8,
            },
        ]
        for item in samples:
            create_document("perfume", item)
        new_count = db["perfume"].count_documents({})
        return {"message": "Seeded perfumes", "count": new_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public endpoint to list perfumes
@app.get("/api/perfumes")
def list_perfumes(limit: int = 50):
    try:
        docs = get_documents("perfume", {}, limit)
        # Convert ObjectId to strings
        for d in docs:
            if isinstance(d.get("_id"), ObjectId):
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple create endpoint
class CreatePerfume(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    notes: Optional[List[str]] = []
    concentration: Optional[str] = None
    volume_ml: Optional[int] = None
    image: Optional[str] = None
    in_stock: bool = True
    rating: Optional[float] = None

@app.post("/api/perfumes")
def create_perfume(body: CreatePerfume):
    try:
        perfume = Perfume(**body.model_dump())
        new_id = create_document("perfume", perfume)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
