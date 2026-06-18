# AI News Aggregator

Production-oriented AI news aggregation pipeline using Python 3.12, PostgreSQL, SQLAlchemy, Pydantic, Feedparser, YouTube Transcript API, SMTP email, Docker, and Gemini 2.5 Flash.

## Architecture

```text
main.py
  -> app/daily_runner.py
    -> Services Layer
      -> Agents Layer
      -> Scrapers Layer
      -> Database Layer
        -> PostgreSQL
```

Scrapers collect raw data only. Services orchestrate workflows. Agents are the only modules that call Gemini. The repository owns database persistence.

## Setup

```bash
cd ai_news_aggregator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Fill in `.env`:

```env
GEMINI_API_KEY=your_key
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_news
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
DEFAULT_RECIPIENT_EMAIL=recipient@example.com
YOUTUBE_CHANNELS=UC_x5XG1OV2P6uZZ5FSM9Ttw
```

## Run With Docker

```bash
cd ai_news_aggregator/docker
docker compose up --build
```

## Run Locally

Start PostgreSQL and then:

```bash
cd ai_news_aggregator
python main.py
```

## Pipeline

1. Scrape OpenAI, Anthropic, and Hugging Face feeds.
2. Convert article pages to markdown.
3. Fetch YouTube videos and transcripts.
4. Generate Gemini-powered digests.
5. Rank articles against the user profile.
6. Generate a personalized markdown newsletter.
7. Send through SMTP.
8. Return a summary report.

## Customization

The default profile is in `app/profiles/user_profile.py`. You can seed or update profiles through `NewsRepository.upsert_user_profile`.

YouTube channels are configured as comma-separated channel IDs in `YOUTUBE_CHANNELS`.

## Deployment Notes

The app is ready for Railway, Render, AWS, or VPS deployment as a one-shot daily job. In production, schedule `python main.py` with cron, a platform scheduler, or a container job runner.

