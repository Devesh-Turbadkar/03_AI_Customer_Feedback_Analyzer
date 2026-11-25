from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Review
from app.services.ai_service import generate_insights
from app.schemas import InsightOut

router = APIRouter(prefix="/api", tags=["Analytics"])


@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    total = db.query(func.count(Review.id)).scalar() or 0
    counts = {name: 0 for name in ["Positive", "Negative", "Neutral"]}
    for sentiment, count in db.query(Review.sentiment, func.count(Review.id)).group_by(Review.sentiment):
        counts[sentiment] = count
    return {"total_reviews": total, "sentiment_counts": counts}


@router.post("/insights", response_model=InsightOut)
def create_insights(db: Session = Depends(get_db)):
    rows = db.query(Review).order_by(Review.created_at.desc()).limit(100).all()
    if not rows:
        raise HTTPException(status_code=400, detail="Add reviews before generating insights.")
    data = [{"sentiment": r.sentiment, "review_text": r.review_text} for r in rows]
    try:
        return generate_insights(data)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not generate insights: {exc}")
