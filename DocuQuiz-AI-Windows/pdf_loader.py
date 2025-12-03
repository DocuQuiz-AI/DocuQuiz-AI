import easyocr
from PIL import Image, ImageEnhance
from fpdf import FPDF
import pytesseract
import ocrmypdf
from pdf2image import convert_from_path
import numpy as np
from PIL import Image
from pathlib import Path
from pypdf import PdfReader
import io
import os
import tkinter as tk
from tkinter import filedialog
from config import *  # This loads .env file automatically

# Fix PIL decompression bomb warning
Image.MAX_IMAGE_PIXELS = 200000000

# Try to import Google Cloud Vision (optional - better for handwriting)
try:
    from google.cloud import vision
    from google.oauth2 import service_account
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    print("Note: Google Cloud Vision API not available. Install with: pip install google-cloud-vision")
    print("      Google Vision provides much better handwriting recognition accuracy.")

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

repo_root = Path(__file__).resolve().parent
poppler_bin = str(repo_root.joinpath("poppler-25.11.0", "Library", "bin"))

def select_file_path(choose_mode):
    if choose_mode == 'pdf':
        file_path = filedialog.askopenfilename(title="Select PDF to Upload", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        print("Selected file to upload:", file_path)
        return file_path
    elif choose_mode == 'pic':
        file_path = filedialog.askopenfilename(title="Select Image File to Upload", filetypes=[("Image files", "*.png *.jpg"), ("All files", "*.*")])
        print("Selected image file to upload:", file_path)
        return file_path
    else:
        return None

def select_output_pdf_path():
    output_pdf_path = filedialog.askdirectory(title="Select output folder to save the PDF file")
    print("Selected output folder:", output_pdf_path)
    return output_pdf_path

class PDFLoader:
    def __init__(self, pdf_path, tesseract_path, output_pdf_path, pdf_or_pic, file_path, google_credentials_path=None):
        self.pdf_path = pdf_path
        self.pdf_or_pic = pdf_or_pic
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.file_path = file_path
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.output_pdf_path = output_pdf_path
        
        # Initialize Google Cloud Vision client if available
        self.vision_client = None
        if GOOGLE_VISION_AVAILABLE:
            try:
                if google_credentials_path and os.path.exists(google_credentials_path):
                    credentials = service_account.Credentials.from_service_account_file(google_credentials_path)
                    self.vision_client = vision.ImageAnnotatorClient(credentials=credentials)
                    print("Google Cloud Vision API initialized (better handwriting recognition)")
                elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                    self.vision_client = vision.ImageAnnotatorClient()
                    print("Google Cloud Vision API initialized (better handwriting recognition)")
                else:
                    print("Google Vision available but no credentials found. Set GOOGLE_APPLICATION_CREDENTIALS env var or provide credentials_path")
            except Exception as e:
                print(f"Could not initialize Google Vision: {e}")
    

    
    def extract_text_google_vision(self, img):
        """
        Extract text using Google Cloud Vision API - MUCH better for handwriting!
        This is the recommended method for handwritten documents.
        """
        if not self.vision_client:
            return None, None
        
        try:
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            if isinstance(img, Image.Image):
                img.save(img_byte_arr, format='PNG')
            else:
                Image.fromarray(img).save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Create Vision API image
            image = vision.Image(content=img_byte_arr)
            
            # Use DOCUMENT_TEXT_DETECTION for better handwriting recognition
            response = self.vision_client.document_text_detection(image=image)
            
            if response.error.message:
                print(f"Google Vision API Error: {response.error.message}")
                return None, None
            
            # Extract text
            text = response.full_text_annotation.text if response.full_text_annotation else ""
            
            # Calculate token count
            tokens_count = len(text) / 4
            
            return text, tokens_count
            
        except Exception as e:
            print(f"Google Vision API error: {e}")
            return None, None



    def extract_text_ocr(self, prefer_google_vision=True):
        """
        Extract text using OCR. Tries Google Vision first (best for handwriting),
        then falls back to EasyOCR.
        """
        if self.pdf_or_pic.lower() == 'pic':
            img = Image.open(self.pdf_path)
            
            # Try Google Vision first if available (much better for handwriting)
            if prefer_google_vision and self.vision_client:
                print("Trying Google Cloud Vision API (best for handwriting)...")
                text, tokens_count = self.extract_text_google_vision(img)
                if text and len(text.strip()) > 0:
                    print("✓ Google Vision succeeded!")
                    return text, tokens_count
                else:
                    print("Google Vision returned empty result, trying EasyOCR...")
            
            # Fallback to EasyOCR
            reader = easyocr.Reader(['en'], gpu=False)
            text = ""
            result = reader.readtext(np.array(img))
            for res in result:
                text += res[1] + "\n"
            tokens_count = len(text) / 4
            return text, tokens_count
        
        elif self.pdf_or_pic.lower() == 'pdf':
            text = ""
            
            # Convert PDF pages to images
            try:
                images = convert_from_path(self.file_path, poppler_path=poppler_bin, dpi=200)
            except Exception as e:
                print("convert_from_path failed:", e)
                return "", 0  # fallback

            # OCR each image
            for img in images:
                # Try Google Vision first if available
                if prefer_google_vision and self.vision_client:
                    page_text, _ = self.extract_text_google_vision(img)
                    if page_text:
                        text += page_text + " "
                        continue
                
                # Fallback to EasyOCR
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(np.array(img))
                for _, t, _ in results:
                    text += t + " "

            token_count = len(text.split())
            return text, token_count

    def extract_text_tesseract(self):
        text = pytesseract.image_to_string(Image.open(self.pdf_path))
        tokens_count = len(text) / 4
        return text, tokens_count
    
    def extract_text_direct(self, file_path):
        """
        Extract text directly from PDF with embedded text.
        This is much more accurate than OCR for PDFs with selectable text.
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            tokens_count = len(text) / 4
            print(text)
            return text, tokens_count
        except Exception as e:
            print(f"Error extracting text directly from PDF: {e}")
            print("Falling back to OCR method...")
            return self.extract_text_ocr()
    
    def text_to_pdf(self, text):
        pdf = FPDF()
        pdf.add_page()
        # Add Unicode font (make sure fonts/DejaVuSans.ttf exists)
        pdf.add_font('DejaVu', '', r'fonts\dejavu-sans-ttf-2.37\DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(0, 10, text)
        pdf.output(self.output_pdf_path)




