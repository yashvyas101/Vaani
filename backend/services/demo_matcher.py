from backend.data.demo_questions import DEMO_QA, DEFAULT_ANSWER

def get_demo_answer(transcript: str) -> str:
    """
    Returns a predefined answer based on keyword matching in the transcript.
    """
    transcript_lower = transcript.lower()
    for qa in DEMO_QA:
        if any(keyword in transcript_lower for keyword in qa["keywords"]):
            return qa["answer"]
    return DEFAULT_ANSWER
