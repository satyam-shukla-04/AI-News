from sqlalchemy.orm import Session

from app.services.process_articles import process_articles


def process_digest(session: Session, limit: int = 100) -> dict[str, int]:
    return process_articles(session, limit)

