from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any, List
import uuid

from pydantic import BaseModel, Field, field_validator

# Constants
MAX_TITLE_LENGTH = 200
MAX_INGREDIENTS = 50
MAX_INSTRUCTION_STEPS = 40
MAX_CUISINE_LENGTH = 120


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class _RecipeBody(BaseModel):
    title: str
    description: str
    ingredients: List[str] = Field(..., min_length=1, max_length=MAX_INGREDIENTS)
    instructions: List[str] = Field(..., min_length=1, max_length=MAX_INSTRUCTION_STEPS)
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel
    cuisine: str = Field(..., min_length=1, max_length=MAX_CUISINE_LENGTH)

    @field_validator("instructions", mode="before")
    @classmethod
    def normalize_instructions(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            text = v.strip()
            if not text:
                return []
            chunks = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            return chunks if chunks else [text]
        if isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        raise ValueError("instructions must be a list of strings or a single string")

    @field_validator("instructions")
    @classmethod
    def require_instructions(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one instruction step is required")
        return v


class Recipe(_RecipeBody):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class RecipeCreate(_RecipeBody):
    pass


class RecipeUpdate(_RecipeBody):
    pass
