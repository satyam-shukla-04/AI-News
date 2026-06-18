from __future__ import annotations

from datetime import UTC, datetime
from time import perf_counter
from typing import Any

from app.database.connection import SessionLocal
from app.database.create_tables import create_tables
from app.runner import run_scrapers
from app.services.process_articles import convert_articles_to_markdown
from app.services.process_curator import process_curator
from app.services.process_digest import process_digest
from app.services.process_email import process_email
from app.services.process_profiles import ensure_default_profile
from app.services.process_youtube import process_youtube
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict[str, Any]:
    started = perf_counter()
    logger.info("Starting daily AI news pipeline")
    create_tables()
    report: dict[str, Any] = {
        "success": False,
        "scraping": {},
        "processing": {},
        "ranking": {},
        "email": {},
        "duration": 0.0,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    try:
        with SessionLocal() as session:
            ensure_default_profile(session)
            report["scraping"] = run_scrapers(session, hours)
            report["processing"]["markdown"] = convert_articles_to_markdown(session)
            report["processing"]["youtube"] = process_youtube(session, hours)
            report["processing"]["digests"] = process_digest(session)
            report["ranking"] = process_curator(session, top_n)
            report["email"] = process_email(session, top_n)
        report["success"] = True
        return report
    except Exception as exc:
        logger.error("Daily pipeline failed: %s", exc)
        report["error"] = str(exc)
        return report
    finally:
        report["duration"] = round(perf_counter() - started, 2)
        logger.info("Daily AI news pipeline completed: success=%s duration=%ss", report["success"], report["duration"])

