from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.repository import NewsRepository
from app.schemas import ArticleCreate, ScrapedArticle
from app.scrapers import anthropic, huggingface, openai
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _to_article_create(item: ScrapedArticle) -> ArticleCreate:
    return ArticleCreate(
        source=item.source,
        title=item.title,
        url=item.url,
        description=item.description,
        content=item.content,
        published_at=item.published_at,
    )


def run_scrapers(session: Session, hours: int = 24) -> dict[str, int]:
    logger.info("Starting scrapers")
    sources = {
        "openai": openai.get_articles,
        "anthropic": anthropic.get_articles,
        "huggingface": huggingface.get_articles,
    }
    collected: list[ScrapedArticle] = []
    stats: dict[str, int] = {}
    for name, scraper in sources.items():
        try:
            articles = scraper(hours)
            collected.extend(articles)
            stats[name] = len(articles)
            logger.info("Scraper completed: source=%s count=%s", name, len(articles))
        except Exception as exc:
            stats[name] = 0
            logger.error("Scraper failed: source=%s error=%s", name, exc)
    saved = NewsRepository(session).save_articles([_to_article_create(item) for item in collected])
    stats["saved"] = saved
    logger.info("Completed scrapers: collected=%s saved=%s", len(collected), saved)
    return stats

