from sqlalchemy.orm import Session

from app.database.repository import NewsRepository
from app.profiles.user_profile import default_user_profile
from app.schemas import UserProfileData
from app.utils.logger import get_logger

logger = get_logger(__name__)


def ensure_default_profile(session: Session, profile: UserProfileData | None = None) -> dict[str, str]:
    logger.info("Ensuring user profile exists")
    data = profile or default_user_profile()
    user = NewsRepository(session).upsert_user_profile(data)
    return {"email": user.email, "name": user.name}

