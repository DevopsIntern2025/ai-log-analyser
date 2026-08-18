import httpx
import json

from app.core.config import settings
from app.schemas.ai_schema import AIAnalysis


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

def parse_gemini_json(response_text: str) -> dict:
    cleaned_response = response_text.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = (
            cleaned_response
            .replace("```json", "", 1)
            .replace("```", "", 1)
            .strip()
        )

    try:
        return json.loads(cleaned_response)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini returned invalid JSON"
        ) from exc

def validate_ai_analysis(
    data: dict,
) -> AIAnalysis:
    try:
        return AIAnalysis.model_validate(data)

    except Exception as exc:
        raise RuntimeError(
            "Gemini response failed AIAnalysis validation"
        ) from exc

async def generate_analysis(
    prompt: str,
) -> AIAnalysis:
    response_text = await generate_text(prompt)

    data = parse_gemini_json(response_text)

    return validate_ai_analysis(data)