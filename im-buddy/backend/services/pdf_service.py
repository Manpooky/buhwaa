import os
import tempfile
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file using PyPDF2 for text-based PDFs
    and OCR (pytesseract) for scanned documents
    
    Args:
        pdf_file: The uploaded PDF file object
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            # Write the uploaded file contents to the temp file
            for chunk in pdf_file.chunks():
                temp_file.write(chunk)
        
        # First try to extract text directly (for text-based PDFs)
        extracted_text = extract_text_with_pypdf(temp_path)
        
        # If no text was extracted or very little text, try OCR
        if not extracted_text or len(extracted_text.strip()) < 100:
            logger.info("Minimal text extracted with PyPDF2, attempting OCR...")
            extracted_text = extract_text_with_ocr(temp_path)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        return extracted_text
    
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        # Clean up the temporary file if it exists
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        raise e

def extract_text_with_pypdf(pdf_path):
    """
    Extract text from a PDF using PyPDF2 (for text-based PDFs)
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.warning(f"Error extracting text with PyPDF2: {str(e)}")
        return ""

def extract_text_with_ocr(pdf_path):
    """
    Extract text from a PDF using OCR (for scanned documents)
    """
    text = ""
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        # Process each page
        for i, image in enumerate(images):
            # Use OCR to extract text from the image
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
            
        return text
    except Exception as e:
        logger.error(f"Error extracting text with OCR: {str(e)}")
        return ""

def create_pdf_from_text(text, filename="translated_document.pdf"):
    """
    Create a PDF document from translated text
    
    Args:
        text (str): Text to include in the PDF
        filename (str): Name of the output file
        
    Returns:
        ContentFile: Django ContentFile object containing the PDF data
    """
    try:
        # Create a buffer to hold the PDF data
        buffer = BytesIO()
        
        # Create the PDF document using reportlab
        pdf = canvas.Canvas(buffer, pagesize=letter)
        
        # Set font and size
        pdf.setFont("Helvetica", 11)
        
        # Get page dimensions
        width, height = letter
        
        # Split text into lines
        y_position = height - 50  # Start 50 points from the top
        margin = 50  # Left and right margin
        line_height = 14  # Space between lines
        
        # Process the text line by line
        for line in text.split('\n'):
            # Process long lines by wrapping them
            while line and y_position > margin:
                if len(line) > 75:  # If line is too long
                    # Find a space to break the line
                    break_point = 75
                    while break_point > 0 and line[break_point] != ' ':
                        break_point -= 1
                    
                    # If no space found, just break at the maximum length
                    if break_point == 0:
                        break_point = 75
                    
                    # Write the line segment
                    pdf.drawString(margin, y_position, line[:break_point])
                    line = line[break_point:].lstrip()
                else:
                    # Write the entire line
                    pdf.drawString(margin, y_position, line)
                    line = ""
                
                # Move down for next line
                y_position -= line_height
                
                # Check if we need a new page
                if y_position <= margin:
                    pdf.showPage()
                    y_position = height - 50
                    pdf.setFont("Helvetica", 11)  # Reset font after new page
        
        # Save the PDF
        pdf.save()
        
        # Get the PDF data from the buffer
        buffer.seek(0)
        
        # Create a ContentFile from the buffer
        pdf_file = ContentFile(buffer.getvalue())
        
        return pdf_file
        
    except Exception as e:
        logger.error(f"Error creating PDF: {str(e)}")
        raise e 