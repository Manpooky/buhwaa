import fitz  # PyMuPDF
from typing import Dict, List, Any, Optional, Tuple
import re
import json
import logging
from dataclasses import dataclass
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FormField:
    """Represents a form field with its properties"""
    name: str
    field_type: str
    value: Optional[str] = None
    options: Optional[List[str]] = None
    required: bool = False
    coordinates: Optional[Dict[str, float]] = None
    page_number: int = 1

class ImmigrationFormPDFParser:
    """
    Comprehensive PDF parser for immigration forms that extracts text, form fields, and metadata
    """
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
        
    def parse_immigration_form(self, file_path: str) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
        """
        Main function that parses PDF and returns data needed for ImmigrationFormPrompts
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            Tuple containing:
            - form_content (str): Complete text content of the form
            - form_fields (List[Dict]): List of form fields with their properties
            - form_metadata (Dict): Metadata about the form (pages, title, etc.)
        """
        try:
            # Validate file
            if not Path(file_path).exists():
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            if not file_path.lower().endswith('.pdf'):
                raise ValueError("File must be a PDF")
            
            # Check if file is readable
            file_size = Path(file_path).stat().st_size
            if file_size == 0:
                raise ValueError("PDF file is empty")
            
            logger.info(f"Starting to parse PDF: {file_path} (size: {file_size} bytes)")
            
            # Test if PDF can be opened
            try:
                test_doc = fitz.open(file_path)
                if test_doc.is_encrypted:
                    test_doc.close()
                    raise ValueError("PDF is encrypted and cannot be processed")
                if len(test_doc) == 0:
                    test_doc.close()
                    raise ValueError("PDF has no pages")
                test_doc.close()
                logger.info("PDF file validation successful")
            except Exception as e:
                raise ValueError(f"Invalid or corrupted PDF file: {str(e)}")
            
            # Extract form content and metadata
            logger.info("Extracting text content...")
            form_content = self._extract_text_content(file_path)
            
            logger.info("Extracting metadata...")
            form_metadata = self._extract_metadata(file_path)
            
            logger.info("Extracting form fields...")
            form_fields = self._extract_form_fields(file_path)
            
            # Enhance metadata with additional analysis
            logger.info("Analyzing form structure...")
            form_metadata.update(self._analyze_form_structure(form_content, form_fields))
            
            logger.info(f"Successfully parsed PDF with {len(form_fields)} fields and {form_metadata.get('total_pages', 0)} pages")
            
            return form_content, form_fields, form_metadata
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    def _extract_text_content(self, file_path: str) -> str:
        """
        Extract complete text content from PDF preserving structure using PyMuPDF
        """
        content_parts = []
        doc = None
        
        try:
            logger.info(f"Opening PDF document: {file_path}")
            doc = fitz.open(file_path)
            
            logger.info(f"PDF opened successfully. Pages: {len(doc)}")
            
            if len(doc) == 0:
                raise ValueError("PDF contains no pages")
            
            for page_num in range(len(doc)):
                logger.debug(f"Processing page {page_num + 1}")
                page = doc[page_num]
                content_parts.append(f"\n=== PAGE {page_num + 1} ===\n")
                
                # Extract text with layout preservation
                try:
                    text = page.get_text("layout")
                    if text and text.strip():
                        content_parts.append(text)
                        logger.debug(f"Extracted {len(text)} characters from page {page_num + 1}")
                    else:
                        # Try alternative text extraction methods
                        text = page.get_text()
                        if text and text.strip():
                            content_parts.append(text)
                            logger.debug(f"Extracted {len(text)} characters using fallback method")
                        else:
                            logger.warning(f"No text found on page {page_num + 1}")
                            content_parts.append("[No text content found on this page]")
                
                except Exception as page_error:
                    logger.warning(f"Error extracting text from page {page_num + 1}: {str(page_error)}")
                    content_parts.append(f"[Error extracting text from page {page_num + 1}]")
                
                # Extract tables if present using text blocks
                try:
                    text_dict = page.get_text("dict")
                    if "blocks" in text_dict:
                        blocks = text_dict["blocks"]
                        for block_idx, block in enumerate(blocks):
                            if "lines" in block:
                                lines = block["lines"]
                                if len(lines) > 1 and self._is_table_structure(lines):
                                    content_parts.append(f"\n--- TABLE {block_idx + 1} ---\n")
                                    for line in lines:
                                        spans = [span.get("text", "") for span in line.get("spans", [])]
                                        if spans and any(span.strip() for span in spans):
                                            content_parts.append(" | ".join(spans))
                                    content_parts.append("\n")
                except Exception as table_error:
                    logger.warning(f"Error extracting tables from page {page_num + 1}: {str(table_error)}")
            
            result = "\n".join(content_parts)
            logger.info(f"Text extraction completed. Total content length: {len(result)}")
            
            if not result.strip():
                logger.warning("No text content extracted from PDF")
                return "No text content could be extracted from this PDF."
            
            return result
            
        except Exception as e:
            logger.error(f"PyMuPDF text extraction failed: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            
            # Try a more basic extraction method as fallback
            try:
                logger.info("Attempting fallback text extraction...")
                return self._extract_text_fallback(file_path)
            except Exception as fallback_error:
                logger.error(f"Fallback extraction also failed: {str(fallback_error)}")
                raise Exception(f"All text extraction methods failed. Original error: {str(e)}, Fallback error: {str(fallback_error)}")
        
        finally:
            if doc:
                try:
                    doc.close()
                    logger.debug("PDF document closed successfully")
                except Exception as close_error:
                    logger.warning(f"Error closing PDF document: {str(close_error)}")
    
    def _is_table_structure(self, lines: List[Dict]) -> bool:
        """
        Helper method to identify if text blocks form a table structure
        """
        if len(lines) < 2:
            return False
        
        # Check if multiple lines have similar span patterns (indicating columns)
        span_counts = [len(line.get("spans", [])) for line in lines]
        avg_spans = sum(span_counts) / len(span_counts)
        
        # If most lines have similar number of spans (columns), it's likely a table
        similar_span_lines = sum(1 for count in span_counts if abs(count - avg_spans) <= 1)
        return similar_span_lines / len(lines) > 0.6
    
    def _extract_text_fallback(self, file_path: str) -> str:
        """
        Fallback text extraction using basic PyMuPDF method
        """
        content_parts = []
        doc = None
        
        try:
            logger.info("Attempting basic text extraction fallback...")
            doc = fitz.open(file_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                content_parts.append(f"\n=== PAGE {page_num + 1} ===\n")
                
                # Try different extraction methods
                methods = [
                    ("text", lambda p: p.get_text()),
                    ("html", lambda p: p.get_text("html")),
                    ("words", lambda p: " ".join([w[4] for w in p.get_text("words")])),
                ]
                
                text_extracted = False
                for method_name, method_func in methods:
                    try:
                        text = method_func(page)
                        if text and text.strip():
                            content_parts.append(f"[Extracted using {method_name} method]\n")
                            content_parts.append(text)
                            text_extracted = True
                            logger.debug(f"Successfully extracted text using {method_name} method for page {page_num + 1}")
                            break
                    except Exception as method_error:
                        logger.debug(f"{method_name} method failed for page {page_num + 1}: {str(method_error)}")
                        continue
                
                if not text_extracted:
                    content_parts.append("[No text could be extracted from this page]")
                    logger.warning(f"All extraction methods failed for page {page_num + 1}")
            
            result = "\n".join(content_parts)
            logger.info(f"Fallback extraction completed. Content length: {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Fallback text extraction failed: {str(e)}")
            raise Exception(f"Complete text extraction failure: {str(e)}")
        
        finally:
            if doc:
                try:
                    doc.close()
                except Exception as close_error:
                    logger.warning(f"Error closing PDF in fallback: {str(close_error)}")
    
    def _extract_form_fields(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract interactive form fields from PDF
        """
        form_fields = []
        doc = None
        
        try:
            logger.info("Extracting form fields...")
            doc = fitz.open(file_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get form fields (widgets) from the page
                try:
                    widgets = page.widgets()
                    logger.debug(f"Found {len(widgets)} widgets on page {page_num + 1}")
                    
                    for widget_idx, widget in enumerate(widgets):
                        try:
                            field_info = {
                                "name": widget.field_name or f"field_{len(form_fields) + 1}",
                                "field_type": self._determine_field_type(widget),
                                "value": widget.field_value or "",
                                "required": False,  # PyMuPDF doesn't always provide this
                                "page_number": page_num + 1,
                                "coordinates": {
                                    "x": widget.rect.x0,
                                    "y": widget.rect.y0,
                                    "width": widget.rect.width,
                                    "height": widget.rect.height
                                }
                            }
                            
                            # Add options for choice fields
                            if hasattr(widget, 'choice_values') and widget.choice_values:
                                field_info["options"] = widget.choice_values
                            
                            form_fields.append(field_info)
                            
                        except Exception as widget_error:
                            logger.warning(f"Error processing widget {widget_idx} on page {page_num + 1}: {str(widget_error)}")
                            continue
                            
                except Exception as page_error:
                    logger.warning(f"Error extracting widgets from page {page_num + 1}: {str(page_error)}")
                    continue
            
            logger.info(f"Extracted {len(form_fields)} interactive form fields")
            
        except Exception as e:
            logger.warning(f"PyMuPDF form field extraction failed: {str(e)}")
        
        finally:
            if doc:
                try:
                    doc.close()
                except Exception as close_error:
                    logger.warning(f"Error closing PDF in form field extraction: {str(close_error)}")
        
        # If no interactive fields found, try to detect fields from text patterns
        if not form_fields:
            logger.info("No interactive fields found, attempting text-based field detection...")
            try:
                form_fields = self._detect_fields_from_text(file_path)
                logger.info(f"Detected {len(form_fields)} fields from text patterns")
            except Exception as text_detection_error:
                logger.warning(f"Text-based field detection failed: {str(text_detection_error)}")
        
        return form_fields
    
    def _determine_field_type(self, widget) -> str:
        """
        Determine the type of form field from widget
        """
        if hasattr(widget, 'field_type'):
            field_type = widget.field_type
            type_mapping = {
                0: "text",
                1: "button", 
                2: "checkbox",
                3: "radiobutton",
                4: "dropdown",
                5: "listbox",
                6: "signature"
            }
            return type_mapping.get(field_type, "text")
        
        # Fallback based on widget properties
        if hasattr(widget, 'choice_values') and widget.choice_values:
            return "dropdown"
        elif hasattr(widget, 'button_state'):
            return "checkbox"
        else:
            return "text"
    
    def _detect_fields_from_text(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Detect potential form fields from text patterns using PyMuPDF
        """
        fields = []
        
        try:
            doc = fitz.open(file_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Common immigration form field patterns
                patterns = [
                    # Name fields
                    (r'(?i)(first\s+name|given\s+name)[\s:_\.]*([_\s\.]+)', 'text', 'first_name'),
                    (r'(?i)(last\s+name|family\s+name|surname)[\s:_\.]*([_\s\.]+)', 'text', 'last_name'),
                    (r'(?i)(middle\s+name)[\s:_\.]*([_\s\.]+)', 'text', 'middle_name'),
                    
                    # Date fields
                    (r'(?i)(date\s+of\s+birth|birth\s+date)[\s:_\.]*([_\s\.]+)', 'date', 'date_of_birth'),
                    (r'(?i)(date)[\s:_\.]*([_\s\.]+)', 'date', 'date_field'),
                    
                    # Address fields
                    (r'(?i)(address)[\s:_\.]*([_\s\.]+)', 'text', 'address'),
                    (r'(?i)(city)[\s:_\.]*([_\s\.]+)', 'text', 'city'),
                    (r'(?i)(state|province)[\s:_\.]*([_\s\.]+)', 'text', 'state'),
                    (r'(?i)(zip\s+code|postal\s+code)[\s:_\.]*([_\s\.]+)', 'text', 'postal_code'),
                    (r'(?i)(country)[\s:_\.]*([_\s\.]+)', 'text', 'country'),
                    
                    # ID fields
                    (r'(?i)(passport\s+number)[\s:_\.]*([_\s\.]+)', 'text', 'passport_number'),
                    (r'(?i)(social\s+security|ssn)[\s:_\.]*([_\s\.]+)', 'text', 'ssn'),
                    (r'(?i)(case\s+number)[\s:_\.]*([_\s\.]+)', 'text', 'case_number'),
                    
                    # Contact fields
                    (r'(?i)(phone|telephone)[\s:_\.]*([_\s\.]+)', 'text', 'phone'),
                    (r'(?i)(email)[\s:_\.]*([_\s\.]+)', 'text', 'email'),
                    
                    # Choice fields
                    (r'(?i)(gender|sex)[\s:_\.]*\s*(?:\[\s*\]\s*(male|female|m|f)|\☐\s*(male|female|m|f))', 'radio', 'gender'),
                    (r'(?i)(marital\s+status)[\s:_\.]*', 'radio', 'marital_status'),
                    
                    # Generic checkbox patterns
                    (r'(?:\[\s*\]|\☐)\s*([A-Za-z\s]+)', 'checkbox', 'checkbox_field'),
                ]
                
                for pattern, field_type, field_name in patterns:
                    matches = re.finditer(pattern, text)
                    for match_num, match in enumerate(matches):
                        field_id = f"{field_name}_{page_num + 1}_{match_num + 1}"
                        fields.append({
                            "name": field_id,
                            "field_type": field_type,
                            "label": match.group(1) if match.groups() else match.group(0),
                            "value": "",
                            "required": False,
                            "page_number": page_num + 1,
                            "coordinates": None
                        })
            
            doc.close()
        
        except Exception as e:
            logger.warning(f"Text-based field detection failed: {str(e)}")
        
        return fields
    
    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF using PyMuPDF
        """
        metadata = {
            "total_pages": 0,
            "title": "Immigration Form",
            "file_size": 0,
            "creation_date": None,
            "modification_date": None,
            "form_type": "unknown"
        }
        
        try:
            # Get file size
            metadata["file_size"] = Path(file_path).stat().st_size
            
            # Extract PDF metadata using PyMuPDF
            doc = fitz.open(file_path)
            
            metadata["total_pages"] = len(doc)
            
            # Get document metadata
            pdf_meta = doc.metadata
            if pdf_meta:
                metadata["title"] = pdf_meta.get('title', 'Immigration Form')
                metadata["author"] = pdf_meta.get('author', '')
                metadata["subject"] = pdf_meta.get('subject', '')
                metadata["creator"] = pdf_meta.get('creator', '')
                metadata["producer"] = pdf_meta.get('producer', '')
                metadata["creation_date"] = pdf_meta.get('creationDate', '')
                metadata["modification_date"] = pdf_meta.get('modDate', '')
            
            doc.close()
        
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {str(e)}")
        
        return metadata
    
    def _analyze_form_structure(self, content: str, fields: List[Dict]) -> Dict[str, Any]:
        """
        Analyze form structure and detect form type
        """
        analysis = {
            "estimated_completion_time": "15-30 minutes",
            "complexity": "medium",
            "form_type": "immigration",
            "detected_sections": [],
            "languages_detected": [],
            "field_count": len(fields)
        }
        
        # Detect form type from content
        content_lower = content.lower()
        
        form_types = {
            "i-485": ["adjustment of status", "register permanent residence"],
            "i-130": ["petition for alien relative", "immediate relative"],
            "i-765": ["employment authorization", "work permit"],
            "i-90": ["replace permanent resident card", "green card replacement"],
            "i-131": ["travel document", "advance parole"],
            "n-400": ["naturalization", "citizenship"],
            "i-751": ["remove conditions", "conditional permanent resident"]
        }
        
        for form_code, keywords in form_types.items():
            if any(keyword in content_lower for keyword in keywords):
                analysis["form_type"] = form_code
                break
        
        # Detect common sections
        sections = [
            "personal information", "biographic information", "contact information",
            "employment history", "education", "travel history", "criminal history",
            "family information", "supporting documents", "declaration", "signature"
        ]
        
        for section in sections:
            if section in content_lower:
                analysis["detected_sections"].append(section)
        
        # Estimate complexity based on field count and content
        if len(fields) < 20:
            analysis["complexity"] = "low"
            analysis["estimated_completion_time"] = "10-20 minutes"
        elif len(fields) > 50:
            analysis["complexity"] = "high"
            analysis["estimated_completion_time"] = "30-60 minutes"
        
        return analysis

    def rebuild_pdf_from_data(self, input_path: str, form_content: str, form_fields: List[Dict[str, Any]], metadata: Dict[str, Any], output_path: str):
        logger.info(f"Rebuilding PDF at {output_path}")
        doc = None
        try:
            # Open the original PDF as template
            doc = fitz.open(input_path)
            logger.info(f"Opened original PDF with {len(doc)} pages")

            # Split content into pages
            pages = form_content.split("=== PAGE ")
            logger.info(f"Split content into {len(pages)} sections")
            
            for i, page_data in enumerate(pages):
                if not page_data.strip():
                    continue

                if i >= len(doc):
                    # Create a new page if needed
                    page = doc.new_page()
                else:
                    # Use existing page
                    page = doc[i]

                # Extract actual content after marker
                content_lines = page_data.split('\n', 1)
                if len(content_lines) == 2:
                    content = content_lines[1]
                else:
                    content = page_data

                # Clear existing content
                page.draw_rect(page.rect, color=(1, 1, 1), fill=(1, 1, 1))

                # Add translated text
                page.insert_text((72, 72), content, fontsize=10)

            # Add form fields if available
            for field in form_fields:
                page_num = field.get("page_number", 1) - 1
                if page_num < len(doc):
                    page = doc[page_num]
                    coords = field.get("coordinates") or {"x": 100, "y": 100, "width": 150, "height": 20}
                    rect = fitz.Rect(coords["x"], coords["y"], coords["x"] + coords["width"], coords["y"] + coords["height"])
                    page.insert_textbox(rect, field.get("name", "Field"), fontsize=8, color=(0, 0, 1))

            # Set metadata
            doc.set_metadata({
                "title": metadata.get("title", "Immigration Form"),
                "author": metadata.get("author", "Rebuilder"),
                "subject": metadata.get("form_type", "Form Reconstruction"),
            })

            # Save and close
            doc.save(output_path)
            logger.info(f"Successfully saved translated PDF to {output_path}")

        except Exception as e:
            logger.error(f"Error rebuilding PDF: {str(e)}")
            raise
        finally:
            if doc:
                doc.close()

# Example usage function for integration with your FastAPI
def parse_pdf_for_immigration_prompt(file_path: str) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
    """
    Convenience function that returns the exact format needed for ImmigrationFormPrompts.phase1_translation_prompt
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        Tuple of (form_content, form_fields, form_metadata) ready for the prompt
    """
    parser = ImmigrationFormPDFParser()
    return parser.parse_immigration_form(file_path)
