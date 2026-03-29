import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not set in the .env file.")