from datetime import UTC, datetime, timedelta

from dateutil import parser


def utc_now() -> datetime:
    return datetime.now(UTC)


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = parser.parse(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def within_last_hours(value: datetime | None, hours: int) -> bool:
    if value is None:
        return True
    return value >= utc_now() - timedelta(hours=hours)

