from pydantic import BaseModel, Field
from typing import List, Optional
from .enums import MoodGuess, ContextGuess


class SummaryRequest(BaseModel):
    period_start: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    period_end: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class MoodTrendPoint(BaseModel):
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    score: int = Field(ge=0, le=100)


class MoodDistributionItem(BaseModel):
    mood: MoodGuess
    count: int = Field(ge=0)


class TriggerItem(BaseModel):
    trigger: str = Field(min_length=1, max_length=40)
    count: int = Field(ge=0)


class ContextSplitItem(BaseModel):
    context: ContextGuess
    count: int = Field(ge=0)


class SuggestionItem(BaseModel):
    type: str = Field(pattern=r"^(action|boundary)$")
    text: str = Field(min_length=1, max_length=200)


class SummaryJSON(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    mood_trend: List[MoodTrendPoint] = Field(default_factory=list)
    mood_distribution: List[MoodDistributionItem] = Field(default_factory=list)
    top_triggers: List[TriggerItem] = Field(default_factory=list)
    recurring_thoughts: List[str] = Field(default_factory=list)
    context_split: List[ContextSplitItem] = Field(default_factory=list)
    insights: List[str] = Field(default_factory=list)
    suggestions: List[SuggestionItem] = Field(default_factory=list)
    persona_story: Optional[str] = ""


class SummaryResponse(BaseModel):
    period_start: str
    period_end: str
    summary: SummaryJSON
