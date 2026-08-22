from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel
import logging

from backend.services.demo_matcher import get_demo_answer
from backend.services.sarvam_service import sarvam_stt, sarvam_tts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vaani Demo Backend")

class TextRequest(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/demo/text")
def demo_text(request: TextRequest):
    """Testing endpoint for text input."""
    logger.info(f"Received text request: {request.text}")
    answer = get_demo_answer(request.text)
    return {"answer": answer}

@app.post("/api/demo/voice")
async def demo_voice(audio: UploadFile = File(...)):
    """Voice demo endpoint."""
    logger.info("Received voice request")
    audio_bytes = await audio.read()
    try:
        # 1. STT
        transcript = sarvam_stt(audio_bytes)
        logger.info(f"Transcript: {transcript}")
        # 2. Demo Matcher
        answer = get_demo_answer(transcript)
        logger.info(f"Matched Answer: {answer}")
        # 3. TTS
        audio_response_bytes = sarvam_tts(answer)
    except RuntimeError as e:
        # Return a clear error response without exposing the API key
        logger.error(str(e))
        return {"error": str(e)}
    # Return audio response
    return Response(content=audio_response_bytes, media_type="audio/wav")
