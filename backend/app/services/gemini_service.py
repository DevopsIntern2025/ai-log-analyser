import httpx

from app.core.config import settings


GEMINI_MODEL = "gemini-3.6-flash"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com"
    f"/v1beta/models/{GEMINI_MODEL}:generateContent"
)


async def generate_text(prompt: str) -> str:
    headers = {
        "x-goog-api-key": settings.GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(
        timeout=60.0
    ) as client:

        response = await client.post(
            GEMINI_URL,
            headers=headers,
            json=payload,
        )

    response.raise_for_status()

    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]