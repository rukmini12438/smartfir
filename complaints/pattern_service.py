import os
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


def get_embedding(text):
    """
    Kisi bhi text (complaint description) ko ek "vector"
    (numbers ki list) mein convert karta hai — jo uska
    semantic meaning represent karta hai.
    """
    return embeddings.embed_query(text)


def cosine_similarity(vec_a, vec_b):
    """
    2 vectors ke beech "kitne similar hain" ye calculate karta hai —
    result 0 (bilkul alag) se 1 (bilkul same meaning) ke beech hota hai.

    Ye simple math hai: dot product / (magnitude_a * magnitude_b)
    Isse hume EXACT words match karne ki zaroorat nahi — sirf
    MEANING match karna hai (jaise "phone chori" aur "mobile stolen"
    high similarity denge, chahe words alag hon).
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_similar_complaints(target_complaint, all_complaints, threshold=0.75):
    """
    target_complaint ke embedding ko baaki saari complaints ke
    embeddings se compare karta hai, aur jo bhi threshold se
    zyada similar hon (default 75%+), unhe return karta hai —
    similarity score ke saath, sabse zyada similar pehle.
    """
    if not target_complaint.embedding:
        return []

    similar = []
    for complaint in all_complaints:
        if complaint.id == target_complaint.id:
            continue
        if not complaint.embedding:
            continue

        score = cosine_similarity(target_complaint.embedding, complaint.embedding)
        if score >= threshold:
            similar.append({
                "complaint": complaint,
                "similarity_score": round(float(score), 3),
            })

    # Sabse zyada similar wale pehle dikhaye
    similar.sort(key=lambda x: x["similarity_score"], reverse=True)
    return similar