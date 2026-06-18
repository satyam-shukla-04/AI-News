from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.repository import NewsRepository
from app.schemas import ArticleCreate
from app.scrapers import youtube
from app.utils.logger import get_logger

logger = get_logger(__name__)


def process_youtube(session: Session, hours: int = 24) -> dict[str, int]:
    logger.info("Starting YouTube transcript processing")
    repo = NewsRepository(session)
    videos = youtube.get_latest_videos(hours)
    articles: list[ArticleCreate] = []
    failed = 0
    for video in videos:
        try:
            transcript = youtube.get_transcript(video.video_id)
            articles.append(
                ArticleCreate(
                    source=f"YouTube: {video.channel}",
                    title=video.title,
                    url=video.url,
                    description=f"YouTube video from {video.channel}",
                    content=transcript,
                    markdown=transcript,
                    published_at=video.published_at,
                )
            )
        except Exception as exc:
            failed += 1
            logger.warning("Failed to fetch transcript for %s: %s", video.video_id, exc)
    saved = repo.save_articles(articles)
    logger.info("Completed YouTube processing: videos=%s saved=%s failed=%s", len(videos), saved, failed)
    return {"videos": len(videos), "saved": saved, "failed": failed}

