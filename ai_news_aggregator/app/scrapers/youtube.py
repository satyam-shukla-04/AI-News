from __future__ import annotations

import feedparser
from youtube_transcript_api import YouTubeTranscriptApi

from app.config import get_settings
from app.schemas import YouTubeVideo
from app.utils.date_utils import parse_datetime, within_last_hours


def _channel_feed(channel_id: str) -> str:
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def get_transcript(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join(segment.get("text", "") for segment in transcript)


def get_latest_videos(hours: int = 24) -> list[YouTubeVideo]:
    videos: list[YouTubeVideo] = []
    for channel_id in get_settings().youtube_channels:
        parsed = feedparser.parse(_channel_feed(channel_id))
        channel = getattr(parsed.feed, "title", channel_id)
        for entry in parsed.entries:
            video_id = getattr(entry, "yt_videoid", "")
            published_at = parse_datetime(getattr(entry, "published", None))
            if not video_id or not within_last_hours(published_at, hours):
                continue
            videos.append(
                YouTubeVideo(
                    title=getattr(entry, "title", ""),
                    video_id=video_id,
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    published_at=published_at,
                    channel=channel,
                )
            )
    return videos

