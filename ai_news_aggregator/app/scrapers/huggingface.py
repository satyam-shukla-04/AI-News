from app.schemas import ScrapedArticle
from app.scrapers.common import get_feed_articles

FEEDS = {
    "blog": "https://huggingface.co/blog/feed.xml",
    "research": "https://huggingface.co/papers/rss",
}


def get_articles(hours: int = 24) -> list[ScrapedArticle]:
    return get_feed_articles("HuggingFace", FEEDS, hours)

