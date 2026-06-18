from app.schemas import ScrapedArticle
from app.scrapers.common import get_feed_articles, url_to_markdown

FEEDS = {
    "news": "https://www.anthropic.com/news/rss.xml",
    "research": "https://www.anthropic.com/research/rss.xml",
    "engineering": "https://www.anthropic.com/engineering/rss.xml",
}


AnthropicArticle = ScrapedArticle


def get_articles(hours: int = 24) -> list[AnthropicArticle]:
    return get_feed_articles("Anthropic", FEEDS, hours)

