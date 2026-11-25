import io
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Review
from app.schemas import ReviewCreate, ReviewOut
from app.services.ai_service import analyze_review

router = APIRouter(prefix="/api", tags=["Reviews"])


def _to_output(row: Review) -> dict:
    return {
        "id": row.id,
        "customer_name": row.customer_name,
        "source": row.source,
        "review_text": row.review_text,
        "sentiment": row.sentiment,
        "sentiment_score": row.sentiment_score,
        "positive_points": _split(row.positive_points),
        "negative_points": _split(row.negative_points),
        "topics": _split(row.topics),
        "short_summary": row.short_summary,
        "improvement_suggestions": _split(row.improvement_suggestions),
        "created_at": row.created_at,
    }


def _split(value: str) -> list[str]:
    return [part for part in (value or "").split("|||") if part]


def _save_review(db: Session, review_text: str, customer_name=None, source="Manual"):
    try:
        analysis = analyze_review(review_text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {exc}")
    row = Review(
        customer_name=customer_name,
        source=source,
        review_text=review_text,
        sentiment=analysis["sentiment"],
        sentiment_score=analysis["sentiment_score"],
        positive_points="|||".join(analysis["positive_points"]),
        negative_points="|||".join(analysis["negative_points"]),
        topics="|||".join(analysis["topics"]),
        short_summary=analysis["short_summary"],
        improvement_suggestions="|||".join(analysis["improvement_suggestions"]),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_output(row)


@router.post("/reviews", response_model=ReviewOut, status_code=201)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    return _save_review(db, payload.review_text, payload.customer_name, payload.source or "Manual")


@router.post("/reviews/bulk", status_code=201)
async def upload_reviews(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a .csv file.")
    content = await file.read()
    if len(content) > 2_000_000:
        raise HTTPException(status_code=400, detail="CSV must be smaller than 2 MB.")
    try:
        frame = pd.read_csv(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the CSV file.")
    if "review_text" not in frame.columns:
        raise HTTPException(status_code=400, detail="CSV must contain a review_text column.")
    if len(frame) == 0 or len(frame) > 100:
        raise HTTPException(status_code=400, detail="CSV must contain between 1 and 100 rows.")
    saved, errors = [], []
    for index, record in frame.iterrows():
        text = str(record.get("review_text", "")).strip()
        if not text or text.lower() == "nan":
            errors.append({"row": int(index) + 2, "error": "Empty review_text"})
            continue
        name = record.get("customer_name")
        source = record.get("source", "CSV")
        try:
            saved.append(_save_review(
                db, text,
                None if pd.isna(name) else str(name),
                "CSV" if pd.isna(source) else str(source)
            ))
        except HTTPException as exc:
            errors.append({"row": int(index) + 2, "error": exc.detail})
            if exc.status_code == 502:
                break
    return {"saved_count": len(saved), "error_count": len(errors), "reviews": saved, "errors": errors}


@router.get("/reviews", response_model=list[ReviewOut])
def list_reviews(
    search: str | None = None,
    sentiment: str | None = Query(default=None, pattern="^(Positive|Negative|Neutral)$"),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(Review)
    if search:
        query = query.filter(Review.review_text.ilike(f"%{search}%"))
    if sentiment:
        query = query.filter(Review.sentiment == sentiment)
    rows = query.order_by(Review.created_at.desc()).limit(limit).all()
    return [_to_output(row) for row in rows]


@router.get("/reviews/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    row = db.query(Review).filter(Review.id == review_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Review not found.")
    return _to_output(row)


@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    row = db.query(Review).filter(Review.id == review_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Review not found.")
    db.delete(row)
    db.commit()
    return {"message": "Review deleted."}
