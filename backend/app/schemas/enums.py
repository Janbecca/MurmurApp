from enum import Enum


class ReplyType(str, Enum):
    receive = "receive"
    clarify = "clarify"
    action = "action"
    boundary = "boundary"


class MoodGuess(str, Enum):
    joy = "joy"
    sadness = "sadness"
    anxiety = "anxiety"
    anger = "anger"
    calm = "calm"
    neutral = "neutral"


class ContextGuess(str, Enum):
    work = "work"
    study = "study"
    relationship = "relationship"
    family = "family"
    health = "health"
    other = "other"
