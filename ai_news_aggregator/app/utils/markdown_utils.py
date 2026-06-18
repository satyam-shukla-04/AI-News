from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from app.config import get_settings


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    article = soup.find("article") or soup.find("main") or soup.body or soup
    return md(str(article), heading_style="ATX").strip()


def url_to_markdown(url: str) -> str:
    timeout = get_settings().request_timeout_seconds
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "AI-News-Aggregator/1.0"},
    )
    response.raise_for_status()
    return html_to_markdown(response.text)


def markdown_newsletter(items: list[dict[str, str]], greeting: str, introduction: str) -> str:
    sections = [greeting.strip(), "", introduction.strip(), "", "------------------"]
    for index, item in enumerate(items, start=1):
        sections.extend(
            [
                "",
                f"Article {index}: {item['title']}",
                "",
                item["summary"],
                "",
                f"Read More: {item['url']}",
                "",
                "------------------",
            ]
        )
    return "\n".join(sections).strip()

