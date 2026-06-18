from datetime import date

from app.agents.base import GeminiAgent
from app.schemas import EmailIntroOutput, UserProfileData


class EmailAgent(GeminiAgent):
    def create_intro(self, user_profile: UserProfileData, top_articles: list[dict]) -> EmailIntroOutput:
        prompt = f"""
Write a professional AI newsletter introduction.

Requirements:
- Greet the user by name.
- Mention date: {date.today().isoformat()}.
- Mention key themes from the selected articles.
- Friendly tone.
- Professional tone.

Return only JSON matching:
{{"greeting": "...", "introduction": "..."}}

User profile:
{user_profile.model_dump_json()}

Top ranked articles:
{top_articles}
"""
        return self.generate_json(prompt, EmailIntroOutput)

