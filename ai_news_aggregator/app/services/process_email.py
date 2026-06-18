from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.agents.email_agent import EmailAgent
from app.config import get_settings
from app.database.repository import NewsRepository
from app.profiles.user_profile import default_user_profile
from app.schemas import UserProfileData
from app.utils.email_utils import send_markdown_email
from app.utils.logger import get_logger
from app.utils.markdown_utils import markdown_newsletter

logger = get_logger(__name__)


def process_email(session: Session, top_n: int = 10, send: bool = True) -> dict[str, str | int | bool]:
    logger.info("Starting email generation")
    repo = NewsRepository(session)
    profile = repo.get_user_profile()
    profile_data = UserProfileData.model_validate(profile) if profile else default_user_profile()
    ranked = repo.get_top_ranked_articles(top_n)
    items = [
        {
            "title": item.digest.title,
            "summary": item.digest.summary,
            "url": item.digest.article.url,
            "reasoning": item.reasoning,
        }
        for item in ranked
    ]
    intro = EmailAgent().create_intro(profile_data, items)
    body = markdown_newsletter(items, intro.greeting, intro.introduction)
    recipient = profile_data.email or get_settings().default_recipient_email
    sent = False
    if send and recipient:
        send_markdown_email(recipient, f"AI News Digest - {date.today().isoformat()}", body)
        sent = True
    logger.info("Completed email generation: items=%s sent=%s", len(items), sent)
    return {"items": len(items), "sent": sent, "recipient": recipient or ""}

