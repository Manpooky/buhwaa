from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import tempfile
import shutil
import os
from typing import Dict, Any
import logging
from pdf_parse import ImmigrationFormPDFParser
from llama_client import LlamaClient
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Processing API",
    description="API for processing PDF documents using LLM",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "PDF Processing API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pdf-processing-api"}


@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...), source_language: str = "English", target_language: str = "Spanish"):
    """
    Process a PDF file through LLM and return the response.
    """

     # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Check file size (10MB limit)
    file_size = 0
    temp_file_path = None

    try:
        # Create temporary file to store uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name
            
            # Read and write the file in chunks
            while chunk := await file.read(8192):
                file_size += len(chunk)
                if file_size > 10 * 1024 * 1024:  # 10MB
                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds 10MB limit"
                    )
                
                temp_file.write(chunk)

        logger.info(f"Processing PDF: {file.filename} ({file_size} bytes)")

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process PDF file")

    try:
        # Step 1: Parse PDF
        form_content, form_fields, form_metadata = ImmigrationFormPDFParser().parse_immigration_form(temp_file_path)
        logger.info("PDF parsing completed successfully")

        # Step 2: Process with LLM
        llm_response = LlamaClient().translate_pdf_content(
            form_content, form_fields, form_metadata, target_language, source_language
        )
        logger.info("LLM processing completed successfully")

        # Step 3: Put the translated text back into the PDF
        output_path = os.path.join(tempfile.gettempdir(), f"translated_{file.filename}")
        ImmigrationFormPDFParser().rebuild_pdf_from_data(temp_file_path, llm_response["translated_text"], form_fields, form_metadata, output_path)

        # Return the translated PDF file along with metadata
        return FileResponse(
            path=output_path,
            media_type="application/pdf",
            filename=f"translated_{file.filename}",
            background=None  # This ensures the file is deleted after sending
        )

    except HTTPException:
        raise  # Re-raise HTTPExceptions so FastAPI handles them correctly

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the file")

    finally:
        # Clean up temporary files
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {str(e)}")


@app.exception_handler(413)
async def request_entity_too_large_handler(request, exc):
    """Handle file too large errors"""
    return JSONResponse(
        status_code=413,
        content={"detail": "File size exceeds the maximum allowed limit"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)