import fitz  # PyMuPDF
import json
import markdown
from weasyprint import HTML, CSS

def extract_pdf_structure(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []
    
    for page_num, page in enumerate(doc):
        # Extract text blocks with positioning and formatting
        blocks = page.get_text("dict")
        
        page_info = {
            "page_number": page_num + 1,
            "page_size": page.rect,
            "text_blocks": [],
            "images": [],
            "formatting": []
        }
        
        for block in blocks["blocks"]:
            if "lines" in block:  # Text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        page_info["text_blocks"].append({
                            "text": span["text"],
                            "bbox": span["bbox"],  # positioning
                            "font": span["font"],
                            "size": span["size"],
                            "flags": span["flags"]  # bold, italic, etc.
                        })
        
        pages_data.append(page_info)
    
    return pages_data



def rebuild_via_markdown(translation_data, output_path):
    # Get Markdown from LLM (easy to validate)
    markdown_content = get_markdown_from_llm(translation_data)
    
    # Validate markdown is safe (no HTML injection)
    if validate_markdown_safe(markdown_content):
        # Convert markdown to HTML
        html = markdown.markdown(markdown_content)
        
        # Convert to PDF
        HTML(string=html).write_pdf(output_path)

def get_markdown_from_llm(data):
    prompt = f"""
    Convert this content to clean Markdown:
    {data}
    
    Use only standard Markdown syntax:
    - # for headings
    - ** for bold
    - * for italic  
    - - for bullet points
    - | for tables
    
    No HTML tags, no links, no images.
    """
    return call_llama_api(prompt)

def validate_markdown_safe(markdown_text):
    # Check for suspicious content
    dangerous_patterns = ['<script', 'javascript:', 'data:', '<iframe']
    return not any(pattern in markdown_text.lower() for pattern in dangerous_patterns)