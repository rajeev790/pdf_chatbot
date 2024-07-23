from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models import QueryRequest, QueryResponse
from app.services import process_pdf, initialize_session, get_response

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    contents = await file.read()
    text = process_pdf(contents)
    session_id = initialize_session(text)
    
    return JSONResponse(content={"message": "PDF uploaded successfully", "session_id": session_id})

@router.post("/query/")
async def query_pdf(request: QueryRequest):
    response = get_response(request.session_id, request.query)
    return QueryResponse(response=response)