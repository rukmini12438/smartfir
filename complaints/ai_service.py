import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .rag_service import retrieve_relevant_sections

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


# ---- STEP 1: Classification ----
class ClassificationResult(BaseModel):
    crime_category: str = Field(description="Short category, e.g. Theft, Assault, Fraud, Cybercrime, Missing Person")


classification_prompt = ChatPromptTemplate.from_template(
    """Classify this citizen complaint into a short crime category.

Complaint: "{complaint_description}"
Location: "{location}"
"""
)

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


# ---- STEP 3: Section Suggestion (RAG-grounded) ----
class SectionsResult(BaseModel):
    suggested_sections: str = Field(description="Applicable BNS section numbers with a brief reason each, based ONLY on the retrieved legal text provided")


sections_prompt = ChatPromptTemplate.from_template(
    """You are suggesting applicable Bharatiya Nyaya Sanhita (BNS) sections for this case.

Complaint: "{complaint_description}"
Crime category: "{crime_category}"

Here are the relevant BNS section texts retrieved from the legal database:
---
{retrieved_context}
---

Based ONLY on the sections provided above, suggest which ones apply and why.
Do not invent section numbers that are not in the provided text.
Note: these are AI-generated suggestions only — a police officer must verify before official registration."""
)

sections_chain = sections_prompt | llm.with_structured_output(SectionsResult)


def generate_fir_draft(complaint_description, location):
    """
    4-step pipeline:
    1. Classify crime category
    2. Draft formal FIR description
    3. RETRIEVE relevant BNS section texts (RAG)
    4. Suggest sections — GROUNDED in the retrieved real legal text,
       not just the model's memory (reduces hallucination)
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

        # RAG step: complaint ke basis par relevant BNS sections dhundo
        retrieved_context = retrieve_relevant_sections(complaint_description)

        sections = sections_chain.invoke({
            "complaint_description": complaint_description,
            "crime_category": classification.crime_category,
            "retrieved_context": retrieved_context,
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