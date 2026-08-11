import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

# LangChain ka LLM wrapper — humare Gemini client ki jagah lega,
# lekin LangChain ke through call hoga (chains banane ke liye zaroori)
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


# ---- STEP 1: Classification ----
# Pydantic model define karta hai ki AI ka output EXACTLY kis
# structure mein aana chahiye — LangChain isse automatically
# enforce karta hai (humein manually JSON parse nahi karna padta)
class ClassificationResult(BaseModel):
    crime_category: str = Field(description="Short category, e.g. Theft, Assault, Fraud, Cybercrime, Missing Person")


classification_prompt = ChatPromptTemplate.from_template(
    """Classify this citizen complaint into a short crime category.

Complaint: "{complaint_description}"
Location: "{location}"
"""
)

# Ye ek CHAIN hai — "|" (pipe) operator se prompt aur llm ko jodte hain.
# Matlab: prompt template mein data fill hoga, phir seedha llm ko jayega,
# aur llm ka output automatically ClassificationResult format mein aayega
classification_chain = classification_prompt | llm.with_structured_output(ClassificationResult)


# ---- STEP 2: FIR Drafting ----
class DraftResult(BaseModel):
    formal_description: str = Field(description="A formal, objective 2-4 sentence FIR description in third person, professional police-report language")


drafting_prompt = ChatPromptTemplate.from_template(
    """Write a formal FIR description for this complaint.

Complaint: "{complaint_description}"
Location: "{location}"
Crime category: "{crime_category}"
"""
)

drafting_chain = drafting_prompt | llm.with_structured_output(DraftResult)


# ---- STEP 3: Section Suggestion ----
class SectionsResult(BaseModel):
    suggested_sections: str = Field(description="Likely applicable Bharatiya Nyaya Sanhita (BNS) section numbers with a brief reason each")


sections_prompt = ChatPromptTemplate.from_template(
    """Suggest applicable Bharatiya Nyaya Sanhita (BNS) sections for this case.

Complaint: "{complaint_description}"
Crime category: "{crime_category}"

Note: these are AI-generated suggestions only — a police officer must verify before official registration.
"""
)

sections_chain = sections_prompt | llm.with_structured_output(SectionsResult)


def generate_fir_draft(complaint_description, location):
    """
    3 chains ko SEQUENCE mein chalata hai:
    1. Pehle crime category classify karo
    2. Phir usi category ke context ke saath formal description likho
    3. Phir usi category ke basis par legal sections suggest karo

    Har step ka output agle step ko context ke roop mein milta hai —
    isse single bade prompt ke bajaye, har step FOCUSED aur zyada
    accurate hota hai.
    """
    try:
        classification = classification_chain.invoke({
            "complaint_description": complaint_description,
            "location": location,
        })

        draft = drafting_chain.invoke({
            "complaint_description": complaint_description,
            "location": location,
            "crime_category": classification.crime_category,
        })

        sections = sections_chain.invoke({
            "complaint_description": complaint_description,
            "crime_category": classification.crime_category,
        })

        return {
            "formal_description": draft.formal_description,
            "crime_category": classification.crime_category,
            "suggested_sections": sections.suggested_sections,
        }

    except Exception as e:
        print(f"AI generation failed: {e}")
        return {
            "formal_description": complaint_description,
            "crime_category": "Unspecified",
            "suggested_sections": "Could not determine — please review manually.",
        }