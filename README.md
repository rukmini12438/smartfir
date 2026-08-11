# SmartFIR — Backend

An AI-powered FIR (First Information Report) and crime record management system. Citizens file complaints in plain language; the system uses an LLM pipeline (plain prompting → LangChain orchestration → RAG-grounded legal retrieval) to draft formal FIRs and suggest applicable legal sections, while police officers review and register cases through a role-based dashboard.

**Frontend repo:** [smartfir-frontend](https://github.com/rukmini12438/smartfir-frontend)

## Why this project

Most "AI + Django" tutorials stop at a single LLM prompt. This project was built to go one step further and demonstrate a full progression of GenAI techniques on a real, structured domain (civic/legal-tech):

1. **Plain LLM prompting** — direct calls to Gemini for FIR drafting
2. **LangChain orchestration** — the single prompt was split into a 3-step sequential chain (classify → draft → suggest sections), producing more focused, accurate output
3. **RAG (Retrieval-Augmented Generation)** — legal section suggestions are now grounded in a curated Bharatiya Nyaya Sanhita (BNS) knowledge base via FAISS similarity search, instead of relying on the model's memory alone (reduces hallucination)

## Features

- Role-based authentication (Citizen / Police) with JWT
- Citizens can file complaints and track status
- Police can review complaints and register FIRs
- AI-generated formal FIR drafts from informal complaint text
- AI-suggested BNS legal sections, grounded in retrieved legal text
- REST API built with Django REST Framework

## Tech stack

- **Backend:** Django, Django REST Framework
- **Auth:** JWT (djangorestframework-simplejwt)
- **AI:** Google Gemini (`google-genai`), LangChain (`langchain-google-genai`)
- **RAG:** FAISS vector store, Gemini embeddings
- **Database:** SQLite (dev)

## Project structure

smartfir/
├── users/ # Custom user model, auth APIs
├── stations/ # Police station & officer models
├── complaints/ # Complaint & FIR models, AI service, RAG service
│ ├── ai_service.py # LangChain pipeline (classify → draft → suggest)
│ ├── rag_service.py # FAISS-based retrieval
│ └── bns_data.py # Curated BNS sections dataset (demo/portfolio scope)
└── smartfir_backend/ # Project settings, URLs

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Create a .env file:
# GEMINI_API_KEY=your_key_here

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API overview

| Endpoint                | Method    | Description                                         |
| ----------------------- | --------- | --------------------------------------------------- |
| `/api/users/register/`  | POST      | Register (Citizen or Police)                        |
| `/api/users/login/`     | POST      | Login, returns JWT                                  |
| `/api/users/me/`        | GET       | Current user info                                   |
| `/api/complaints/`      | GET, POST | List / file complaints                              |
| `/api/complaints/firs/` | GET, POST | List / register FIRs (AI-generated draft on create) |

## Note on the legal dataset

`bns_data.py` contains a curated subset (~20 sections) of the Bharatiya Nyaya Sanhita for demonstration purposes. It is **not** a complete or authoritative legal reference — a production system would use the full official BNS text.
