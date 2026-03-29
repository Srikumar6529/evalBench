import time
from anthropic import Anthropic
from app.config import ANTHROPIC_API_KEY, CLAUDE_MODEL

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_response(user_input: str) -> dict:
    start = time.time()

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        temperature=0.0,
        messages=[
            {"role": "user", "content": user_input}
        ],
    )

    latency = time.time() - start
    text = response.content[0].text.strip()

    return {
        "response": text,
        "latency_seconds": round(latency, 3)
    }