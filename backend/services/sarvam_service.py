import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv

# Try to load from the vaani-rag/.env file if it exists
_dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "vaani-rag", ".env")
load_dotenv(_dotenv_path)

logger = logging.getLogger(__name__)

# Environment variable name for the Sarvam API key
_SARVAM_API_KEY_ENV = "SARVAM_API_KEY"
# Base URL for Sarvam API – replace with actual endpoint if known
_SARVAM_BASE_URL = "https://api.sarvam.ai"
# Endpoints – adjust paths as needed for the real service
_STT_ENDPOINT = f"{_SARVAM_BASE_URL}/stt"
_TTS_ENDPOINT = f"{_SARVAM_BASE_URL}/tts"


def _get_api_key() -> Optional[str]:
    """Fetch the Sarvam API key from the environment.

    Returns ``None`` if the variable is not set. The key is never logged or printed.
    """
    return os.getenv(_SARVAM_API_KEY_ENV)


def sarvam_stt(audio_bytes: bytes) -> str:
    """Send audio bytes to Sarvam Speech‑to‑Text and return the transcript.

    Args:
        audio_bytes: Raw audio data (e.g., WAV bytes) submitted to the API.

    Returns:
        The transcript string returned by the service.

    Raises:
        RuntimeError: If the API key is missing or the request fails.
    """
    api_key = _get_api_key()
    if not api_key:
        logger.error("SARVAM_API_KEY environment variable is missing.")
        raise RuntimeError("SARVAM_API_KEY is not set. Unable to perform STT.")

    # Prepare multipart/form-data – typical APIs expect a file field named "audio"
    files = {"audio": ("audio.wav", audio_bytes, "audio/wav")}
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        logger.info("Calling Sarvam STT API.")
        response = requests.post(_STT_ENDPOINT, files=files, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        # Assume the JSON payload contains a field "transcript"
        transcript = data.get("transcript")
        if not transcript:
            raise RuntimeError("STT response does not contain 'transcript' field.")
        return transcript
    except Exception as exc:
        logger.exception("Sarvam STT request failed.")
        raise RuntimeError(f"Sarvam STT failed: {exc}") from exc


def sarvam_tts(text: str) -> bytes:
    """Convert text to speech using Sarvam TTS and return raw audio bytes.

    Args:
        text: The text that should be spoken.

    Returns:
        Audio data (e.g., WAV) returned by the API.

    Raises:
        RuntimeError: If the API key is missing or the request fails.
    """
    api_key = _get_api_key()
    if not api_key:
        logger.error("SARVAM_API_KEY environment variable is missing.")
        raise RuntimeError("SARVAM_API_KEY is not set. Unable to perform TTS.")

    payload = {"text": text}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        logger.info("Calling Sarvam TTS API.")
        response = requests.post(_TTS_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        # Assuming the API returns raw audio bytes with appropriate MIME type
        return response.content
    except Exception as exc:
        logger.exception("Sarvam TTS request failed.")
        raise RuntimeError(f"Sarvam TTS failed: {exc}") from exc
