from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

def verify_gemini_api_key():
    """
    Verifies that the GEMINI_API_KEY environment variable is set.
    Raises HTTPException (503 Service Unavailable) if not set.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "GEMINI_API_KEY is not set in the environment. "
                "Please configure GEMINI_API_KEY in the server environment."
            )
        )
    return api_key
