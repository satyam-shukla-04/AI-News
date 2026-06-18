import sys

from app.daily_runner import run_daily_pipeline


def main() -> int:
    result = run_daily_pipeline(hours=24, top_n=10)
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())

