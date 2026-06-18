from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.curator_agent import CuratorAgent
from app.database.repository import NewsRepository
from app.profiles.user_profile import default_user_profile
from app.schemas import UserProfileData
from app.utils.logger import get_logger

logger = get_logger(__name__)


def process_curator(session: Session, top_n: int = 10) -> dict[str, int]:
    logger.info("Starting digest ranking")
    repo = NewsRepository(session)
    profile = repo.get_user_profile()
    profile_data = UserProfileData.model_validate(profile) if profile else default_user_profile()
    digests = repo.get_latest_digests(limit=100)
    digest_payload = [
        {
            "digest_id": digest.id,
            "title": digest.title,
            "summary": digest.summary,
            "source": digest.article.source,
            "url": digest.article.url,
        }
        for digest in digests
    ]
    rankings = CuratorAgent().rank(profile_data, digest_payload)[:top_n]
    saved = repo.save_rankings(rankings)
    logger.info("Completed digest ranking: ranked=%s", saved)
    return {"ranked": saved}

