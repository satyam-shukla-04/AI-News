from __future__ import annotations

from sqlalchemy import exists, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload

from app.database.models import Article, Digest, RankedArticle, UserProfile
from app.schemas import ArticleCreate, RankingOutput, UserProfileData


class NewsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save_articles(self, articles: list[ArticleCreate]) -> int:
        saved = 0
        for item in articles:
            stmt = (
                insert(Article)
                .values(
                    source=item.source,
                    title=item.title,
                    url=str(item.url),
                    description=item.description,
                    content=item.content,
                    markdown=item.markdown,
                    published_at=item.published_at,
                )
                .on_conflict_do_nothing(index_elements=["url"])
            )
            result = self.session.execute(stmt)
            saved += result.rowcount or 0
        self.session.commit()
        return saved

    def save_digest(self, article_id: int, article_type: str, title: str, summary: str) -> Digest:
        digest = Digest(
            article_id=article_id,
            article_type=article_type,
            title=title,
            summary=summary,
        )
        self.session.add(digest)
        self.session.commit()
        self.session.refresh(digest)
        return digest

    def save_rankings(self, rankings: list[RankingOutput]) -> int:
        self.session.query(RankedArticle).delete()
        for ranking in rankings:
            self.session.add(
                RankedArticle(
                    digest_id=ranking.digest_id,
                    relevance_score=ranking.score,
                    rank=ranking.rank,
                    reasoning=ranking.reasoning,
                )
            )
        self.session.commit()
        return len(rankings)

    def get_articles_without_digest(self, limit: int = 100) -> list[Article]:
        stmt = (
            select(Article)
            .where(~exists().where(Digest.article_id == Article.id))
            .order_by(Article.published_at.desc().nullslast(), Article.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_articles_without_markdown(self, limit: int = 100) -> list[Article]:
        stmt = (
            select(Article)
            .where(Article.markdown == "")
            .order_by(Article.published_at.desc().nullslast(), Article.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_latest_digests(self, limit: int = 100) -> list[Digest]:
        stmt = (
            select(Digest)
            .options(joinedload(Digest.article))
            .order_by(Digest.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_top_ranked_articles(self, limit: int = 10) -> list[RankedArticle]:
        stmt = (
            select(RankedArticle)
            .options(joinedload(RankedArticle.digest).joinedload(Digest.article))
            .order_by(RankedArticle.rank.asc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def get_user_profile(self, email: str | None = None) -> UserProfile | None:
        stmt = select(UserProfile).order_by(UserProfile.created_at.asc())
        if email:
            stmt = stmt.where(UserProfile.email == email)
        return self.session.scalars(stmt.limit(1)).first()

    def upsert_user_profile(self, profile: UserProfileData) -> UserProfile:
        existing = self.get_user_profile(profile.email)
        if existing:
            existing.name = profile.name
            existing.background = profile.background
            existing.expertise_level = profile.expertise_level
            existing.interests = profile.interests
            existing.preferences = profile.preferences
            if profile.email:
                existing.email = profile.email
            self.session.commit()
            self.session.refresh(existing)
            return existing

        user = UserProfile(
            name=profile.name,
            background=profile.background,
            expertise_level=profile.expertise_level,
            interests=profile.interests,
            preferences=profile.preferences,
            email=profile.email or "",
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_article_markdown(self, article_id: int, markdown: str) -> None:
        article = self.session.get(Article, article_id)
        if article:
            article.markdown = markdown
            self.session.commit()

