from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from ai_service import analyze_image, chat_with_assistant
from pydantic import BaseModel
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Style Recommendation API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Style Recommendation API"}

@app.post("/api/analyze")
async def analyze_style(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = await image.read()
        logger.info(f"Received image: {len(content)} bytes")
        
        # Call AI service to analyze image and get recommendations
        recommendation_data = analyze_image(content)
        
        # Save to database
        db_rec = models.RecommendationHistory(
            face_shape=recommendation_data.get("face_shape"),
            skin_tone=recommendation_data.get("skin_tone"),
            gender=recommendation_data.get("gender"),
            style_vibe=recommendation_data.get("style_vibe"),
            color_advice=recommendation_data.get("color_advice"),
            occasion_suggestions=recommendation_data.get("occasion_suggestions"),
            outfit_recommendation=json.dumps(recommendation_data.get("recommendations", {}))
        )
        db.add(db_rec)
        db.commit()
        db.refresh(db_rec)
        
        return {
            "id": db_rec.id,
            "analysis": recommendation_data
        }
    except Exception as e:
        logger.error(f"Error in analyze_style: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        reply = chat_with_assistant(request.message)
        return {"reply": reply}
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
