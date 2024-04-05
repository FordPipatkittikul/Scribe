from fastapi import APIRouter, HTTPException
from models.feedback_model import Feedback, DbFeedback

feedback_router = APIRouter()

@feedback_router.post("/", status_code=201)
async def recieve_feedback(feedback:Feedback)-> dict:
    if not feedback.text or not feedback.rating:
        raise HTTPException(status_code=400, detail={"msg": "Plz fill something"})
    new_feedback = DbFeedback(text=feedback.text,rating=feedback.rating)
    await new_feedback.insert()
    return {"msg": "successfully add new feedback"} 