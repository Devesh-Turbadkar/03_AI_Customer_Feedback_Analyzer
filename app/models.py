from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(120), nullable=True)
    source = Column(String(80), nullable=True)
    review_text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False, index=True)
    sentiment_score = Column(Float, nullable=True)
    positive_points = Column(Text, nullable=False, default="")
    negative_points = Column(Text, nullable=False, default="")
    topics = Column(Text, nullable=False, default="")
    short_summary = Column(Text, nullable=False, default="")
    improvement_suggestions = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
