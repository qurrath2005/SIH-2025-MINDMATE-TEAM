from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, Mood
from datetime import datetime, timedelta
from sqlalchemy import func
from transformers import pipeline   # for NLP

app = FastAPI()

# ------------------ Database dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ Pydantic Request Model ------------------
class MoodCreate(BaseModel):
    user_id: int
    mood_score: int
    text_note: str | None = None

# ------------------ Sentiment Model + Crisis Keywords ------------------
sentiment_model = pipeline("sentiment-analysis")

CRISIS_KEYWORDS = ["suicidal", "kill myself", "hopeless", "worthless", "can't go on"]

# ------------------ Routes ------------------
@app.get("/")
def read_root():
    return {"message": "Mood Tracker API is running 🚀"}

# Add a mood entry with sentiment + crisis detection
@app.post("/mood")
def add_mood(mood: MoodCreate, db: Session = Depends(get_db)):
    # --- Sentiment + crisis detection ---
    sentiment_label = None
    crisis_flag = False

    if mood.text_note:
        # Run NLP sentiment analysis
        result = sentiment_model(mood.text_note)[0]
        sentiment_label = result["label"]  # "POSITIVE" / "NEGATIVE"

        # Crisis keyword detection
        text_lower = mood.text_note.lower()
        for word in CRISIS_KEYWORDS:
            if word in text_lower:
                crisis_flag = True
                break

        # If negative sentiment, consider it risky
        if sentiment_label == "NEGATIVE":
            crisis_flag = crisis_flag or False

    # Save entry in DB
    new_mood = Mood(
        user_id=mood.user_id,
        mood_score=mood.mood_score,
        text_note=mood.text_note,
        sentiment=sentiment_label,
        crisis_detected=crisis_flag
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)

    return {
        "message": "Mood added successfully",
        "mood": {
            "id": new_mood.id,
            "user_id": new_mood.user_id,
            "mood_score": new_mood.mood_score,
            "text_note": new_mood.text_note,
            "sentiment": new_mood.sentiment,
            "crisis_detected": new_mood.crisis_detected,
            "timestamp": new_mood.timestamp
        }
    }

# Get all moods for a user
@app.get("/mood")
def get_moods(user_id: int, db: Session = Depends(get_db)):
    moods = db.query(Mood).filter(Mood.user_id == user_id).all()
    return moods

# Weekly Mood Graph
@app.get("/mood/graph/weekly")
def weekly_graph(user_id: int, db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)

    results = (
        db.query(
            func.date(Mood.timestamp).label("day"),
            func.avg(Mood.mood_score).label("avg_mood")
        )
        .filter(Mood.user_id == user_id, Mood.timestamp >= week_ago)
        .group_by(func.date(Mood.timestamp))
        .all()
    )

    return {"weekly_graph": [{"date": str(day), "avg_mood": avg} for day, avg in results]}

# Monthly Mood Graph
@app.get("/mood/graph/monthly")
def monthly_graph(user_id: int, db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    month_ago = today - timedelta(days=30)

    results = (
        db.query(
            func.date(Mood.timestamp).label("day"),
            func.avg(Mood.mood_score).label("avg_mood")
        )
        .filter(Mood.user_id == user_id, Mood.timestamp >= month_ago)
        .group_by(func.date(Mood.timestamp))
        .all()
    )

    return {"monthly_graph": [{"date": str(day), "avg_mood": avg} for day, avg in results]}

# Crisis Alert Endpoint
@app.post("/alert")
def trigger_alert(user_id: int, db: Session = Depends(get_db)):
    # Get the latest mood entry for the user
    latest_mood = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.timestamp.desc())
        .first()
    )

    if latest_mood and latest_mood.crisis_detected:
        return {
            "alert": True,
            "message": "🚨 Crisis detected! Please reach out for help immediately.",
            "help_now": {
                "hotline": "Tele-MANAS 14416",
                "emergency_contact": "Call 112 (India’s emergency number)"
            }
        }
    else:
        return {
            "alert": False,
            "message": "No crisis detected in latest mood entry."
        }
