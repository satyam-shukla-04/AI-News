from pydantic import BaseModel, Field

from app.agents.base import GeminiAgent
from app.schemas import RankingOutput, UserProfileData


class RankingList(BaseModel):
    rankings: list[RankingOutput] = Field(default_factory=list)


class CuratorAgent(GeminiAgent):
    def rank(self, user_profile: UserProfileData, digests: list[dict]) -> list[RankingOutput]:
        prompt = f"""
Rank every AI news digest for the user profile.

Ranking criteria:
1. Relevance
2. Technical depth
3. Novelty
4. Actionability
5. User expertise match

Return JSON with a "rankings" array. Each item must include:
{{"digest_id": 1, "rank": 1, "score": 9.5, "reasoning": "..."}}

User profile:
{user_profile.model_dump_json()}

Digests:
{digests}
"""
        result = self.generate_json(prompt, RankingList)
        return sorted(result.rankings, key=lambda item: item.rank)

