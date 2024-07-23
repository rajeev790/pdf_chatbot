import openai
import os
from PyPDF2 import PdfReader
from typing import Dict
from uuid import uuid4

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# In-memory store for sessions
sessions: Dict[str, str] = {}

def process_pdf(pdf_contents: bytes) -> str:
    reader = PdfReader(pdf_contents)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def initialize_session(text: str) -> str:
    session_id = str(uuid4())
    sessions[session_id] = text
    return session_id

def get_response(session_id: str, query: str) -> str:
    if session_id not in sessions:
        return "Invalid session ID."
    
    pdf_text = sessions[session_id]
    prompt = f"PDF Content: {pdf_text}\n\nUser Query: {query}\n\nAnswer:"
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()