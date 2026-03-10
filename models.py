from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class RecommendationHistory(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # User features detected
    face_shape = Column(String, nullable=True)
    skin_tone = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    style_vibe = Column(String, nullable=True)
    
    # New AI text insights
    color_advice = Column(String, nullable=True)
    occasion_suggestions = Column(String, nullable=True)

    # Generated recommendation text (JSON dumped as string)
    outfit_recommendation = Column(String, nullable=True)
