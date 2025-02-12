import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import cv2
import numpy as np
import os

class OCRProcessor:
    def __init__(self, tesseract_path=None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def preprocess_image(self, image):
        """Apply image preprocessing techniques to improve OCR accuracy"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Noise removal
        denoised = cv2.medianBlur(thresh, 3)
        
        return denoised

    def process_image(self, image_path):
        """Process a single image file"""
        # Read image
        image = cv2.imread(image_path)
        
        # Preprocess
        processed_image = self.preprocess_image(image)
        
        # Perform OCR
        text = pytesseract.image_to_string(processed_image)
        
        return text

    def process_pdf(self, pdf_path):
        """Process a PDF file by converting to images first"""
        pages = convert_from_path(pdf_path)
        text_results = []
        
        for page in pages:
            # Convert PIL image to opencv format
            open_cv_image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
            processed_image = self.preprocess_image(open_cv_image)
            text = pytesseract.image_to_string(processed_image)
            text_results.append(text)
            
        return '\n'.join(text_results)

    def process_file(self, file_path):
        """Process either PDF or image file"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.process_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            return self.process_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}") 