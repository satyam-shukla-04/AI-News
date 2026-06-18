from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ScrapedArticle(BaseModel):
    source: str
    title: str
    description: str = ""
    url: str
    guid: str | None = None
    published_at: datetime | None = None
    category: str = "article"
    content: str = ""


class YouTubeVideo(BaseModel):
    title: str
    video_id: str
    url: str
    published_at: datetime | None = None
    channel: str
    transcript: str = ""


class DigestOutput(BaseModel):
    title: str
    summary: str


class RankingOutput(BaseModel):
    digest_id: int
    rank: int
    score: float = Field(ge=0, le=10)
    reasoning: str


class EmailIntroOutput(BaseModel):
    greeting: str
    introduction: str


class UserProfileData(BaseModel):
    name: str
    background: str
    expertise_level: str
    interests: list[str]
    preferences: dict[str, Any] = Field(default_factory=dict)
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ArticleCreate(BaseModel):
    source: str
    title: str
    url: HttpUrl | str
    description: str = ""
    content: str = ""
    markdown: str = ""
    published_at: datetime | None = None

