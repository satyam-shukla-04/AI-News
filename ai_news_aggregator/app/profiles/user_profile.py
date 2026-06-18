from app.config import get_settings
from app.schemas import UserProfileData


def default_user_profile() -> UserProfileData:
    return UserProfileData(
        name="Satyam",
        background="AI & Data Science Student",
        expertise_level="Intermediate",
        interests=["LLMs", "AI Agents", "RAG", "Machine Learning", "Generative AI"],
        preferences={
            "technical_depth": "high",
            "research_focus": True,
            "industry_news": True,
        },
        email=get_settings().default_recipient_email,
    )

