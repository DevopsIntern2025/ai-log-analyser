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
     try:
        response = await client.post(
            GEMINI_URL,
            headers=headers,
            json=payload,
        )
     except httpx.TimeoutException as exc:
        raise RuntimeError(
            "Gemini API request timed out"
        ) from exc
     except httpx.RequestError as exc:
        raise RuntimeError(
            "Unable to connect to Gemini API"
        ) from exc

    if response.status_code != 200:
     raise RuntimeError(
        f"Gemini API request failed: "
        f"{response.status_code} - {response.text}"
     )

    data = response.json()

    try:
     return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
     raise RuntimeError(
        "Unexpected response received from Gemini API"
     ) from exc