from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    customer_name: str | None = Field(default=None, max_length=120)
    source: str | None = Field(default="Manual", max_length=80)
    review_text: str = Field(min_length=5, max_length=10000)


class ReviewOut(BaseModel):
    id: int
    customer_name: str | None
    source: str | None
    review_text: str
    sentiment: str
    sentiment_score: float | None
    positive_points: list[str]
    negative_points: list[str]
    topics: list[str]
    short_summary: str
    improvement_suggestions: list[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class InsightOut(BaseModel):
    summary: str
    common_complaints: list[str]
    strengths: list[str]
    recommendations: list[str]
    reviews_analyzed: int
