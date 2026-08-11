import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-flash-latest"


def generate_fir_draft(complaint_description, location):
    """
    Ek citizen ki raw complaint leke, Gemini se formal FIR draft
    aur legal sections generate karwata hai — structured JSON
    output ke saath (response_schema se enforce kiya hai, taaki
    AI ka jawab hamesha sahi format mein aaye).
    """

    prompt = f"""You are assisting an Indian police station with drafting a formal FIR (First Information Report) from a citizen's complaint.

Citizen's complaint (in their own words): "{complaint_description}"
Location: "{location}"

Provide:
1. A formal, objective 2-4 sentence FIR description in third person, professional police-report language.
2. A short crime category label (e.g. Theft, Assault, Fraud, Cybercrime, Missing Person).
3. Likely applicable Bharatiya Nyaya Sanhita (BNS) section numbers with a brief reason each.

Note: these are AI-generated suggestions only — a police officer must verify before official registration."""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "formal_description": {"type": "STRING"},
                    "crime_category": {"type": "STRING"},
                    "suggested_sections": {"type": "STRING"},
                },
                "required": ["formal_description", "crime_category", "suggested_sections"],
            },
        ),
    )

    import json
    try:
        result = json.loads(response.text)
    except (json.JSONDecodeError, TypeError):
        result = {
            "formal_description": complaint_description,
            "crime_category": "Unspecified",
            "suggested_sections": "Could not determine — please review manually.",
        }

    return result