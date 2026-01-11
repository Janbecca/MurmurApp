from pydantic import BaseModel, Field
from datetime import datetime
from .enums import ReplyType, MoodGuess, ContextGuess


class ThoughtCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    reply_type: ReplyType


class ThoughtAIResult(BaseModel):
    reply_text: str = Field(min_length=1, max_length=500)
    topic_guess: str = Field(min_length=1, max_length=80)
    mood_guess: MoodGuess
    mood_score: int = Field(ge=0, le=100)
    context_guess: ContextGuess


class ThoughtCreateResponse(BaseModel):
    id: str
    created_at: datetime
    reply_text: str
    topic_guess: str
    mood_guess: MoodGuess
    mood_score: int
    context_guess: ContextGuess


class ThoughtListItem(BaseModel):
    id: str
    content: str
    created_at: datetime
    reply_type: ReplyType
    reply_text: str
    topic_guess: str
    mood_guess: MoodGuess
    mood_score: int
    context_guess: ContextGuess
