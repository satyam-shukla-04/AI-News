from app.schemas import ScrapedArticle
from app.scrapers.common import get_feed_articles, url_to_markdown

FEEDS = {
    "blog": "https://openai.com/news/rss.xml",
    "research": "https://openai.com/research/rss.xml",
}


def get_articles(hours: int = 24) -> list[ScrapedArticle]:
    return get_feed_articles("OpenAI", FEEDS, hours)

