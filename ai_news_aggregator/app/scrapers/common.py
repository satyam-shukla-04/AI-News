from __future__ import annotations

import feedparser

from app.schemas import ScrapedArticle
from app.utils.date_utils import parse_datetime, within_last_hours
from app.utils.markdown_utils import url_to_markdown


def get_feed_articles(source: str, feeds: dict[str, str], hours: int = 24) -> list[ScrapedArticle]:
    articles: list[ScrapedArticle] = []
    for category, feed_url in feeds.items():
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries:
            published_at = parse_datetime(
                getattr(entry, "published", None) or getattr(entry, "updated", None)
            )
            if not within_last_hours(published_at, hours):
                continue
            articles.append(
                ScrapedArticle(
                    source=source,
                    title=getattr(entry, "title", ""),
                    description=getattr(entry, "summary", ""),
                    url=getattr(entry, "link", ""),
                    guid=getattr(entry, "id", None),
                    published_at=published_at,
                    category=category,
                )
            )
    return articles


__all__ = ["get_feed_articles", "url_to_markdown"]

