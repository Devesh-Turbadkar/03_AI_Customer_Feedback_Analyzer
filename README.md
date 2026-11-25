# AI Customer Feedback Analyzer

A FastAPI + PostgreSQL application that analyzes individual and CSV-uploaded customer reviews with Gemini AI and displays results in a web dashboard.

Read **guide.txt** for the complete beginner setup, project structure, workflow, endpoints, testing, limitations, and interview preparation.

Quick start:
1. Create a virtual environment and install `requirements.txt`.
2. Create a PostgreSQL database named `feedback_analyzer`.
3. Copy `.env.example` to `.env` and set `DATABASE_URL` and `GEMINI_API_KEY`.
4. Run `uvicorn app.main:app --reload`.
5. Open http://127.0.0.1:8000.
