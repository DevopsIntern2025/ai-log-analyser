class AIServiceError(Exception):
    """Base exception for AI service failures."""


class AIConnectionError(AIServiceError):
    """Gemini could not be reached."""


class AITimeoutError(AIServiceError):
    """Gemini request timed out."""


class AIRateLimitError(AIServiceError):
    """Gemini API rate limit was reached."""


class AIProviderError(AIServiceError):
    """Gemini provider returned an error."""


class AIResponseError(AIServiceError):
    """Gemini returned an invalid or unusable response."""