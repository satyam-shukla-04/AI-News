from app.agents.base import GeminiAgent
from app.schemas import DigestOutput


class DigestAgent(GeminiAgent):
    def summarize(self, title: str, content: str, article_type: str) -> DigestOutput:
        prompt = f"""
You are an expert AI news analyst.

Create a structured JSON digest for this {article_type}.

Requirements:
- Create a concise title.
- Create a 2-3 sentence summary.
- Preserve technical accuracy.
- Highlight importance.
- Explain practical impact.

Return only JSON matching:
{{"title": "...", "summary": "..."}}

Title: {title}

Content:
{content[:20000]}
"""
        return self.generate_json(prompt, DigestOutput)

