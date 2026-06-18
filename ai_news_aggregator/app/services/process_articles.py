from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.digest_agent import DigestAgent
from app.database.repository import NewsRepository
from app.utils.logger import get_logger
from app.utils.markdown_utils import url_to_markdown

logger = get_logger(__name__)


def convert_articles_to_markdown(session: Session, limit: int = 100) -> dict[str, int]:
    logger.info("Starting article markdown conversion")
    repo = NewsRepository(session)
    articles = repo.get_articles_without_markdown(limit)
    converted = 0
    failed = 0
    for article in articles:
        try:
            repo.update_article_markdown(article.id, url_to_markdown(article.url))
            converted += 1
        except Exception as exc:
            failed += 1
            logger.warning("Failed to convert article %s: %s", article.id, exc)
    logger.info("Completed markdown conversion: converted=%s failed=%s", converted, failed)
    return {"converted": converted, "failed": failed}


def process_articles(session: Session, limit: int = 100) -> dict[str, int]:
    logger.info("Starting article digest processing")
    repo = NewsRepository(session)
    agent = DigestAgent()
    processed = 0
    failed = 0
    for article in repo.get_articles_without_digest(limit):
        try:
            content = article.markdown or article.content or article.description
            output = agent.summarize(article.title, content, "article")
            repo.save_digest(article.id, "article", output.title, output.summary)
            processed += 1
        except Exception as exc:
            failed += 1
            logger.error("Failed to process article %s: %s", article.id, exc)
    logger.info("Completed article digest processing: processed=%s failed=%s", processed, failed)
    return {"processed": processed, "failed": failed}

