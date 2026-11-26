from google import genai
from google.genai import errors

from app.config import settings

client = genai.Client(
    api_key=settings.gemini_api_key
)

print("Testing Gemini...")
print("Model:", settings.gemini_model)

try:
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents="Reply with only the word SUCCESS."
    )

    print("Gemini working!")
    print("Response:", response.text)

except errors.APIError as e:
    print("Gemini API Error!")
    print("Status Code:", e.code)
    print("Error Details:", repr(e))

except Exception as e:
    print("Other Error:", type(e).__name__, str(e))