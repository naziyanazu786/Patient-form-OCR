import os
from src.ocr_processor import OCRProcessor
from src.data_parser import DataParser
from src.db_handler import DatabaseHandler

def process_forms():
    # Initialize components
    ocr = OCRProcessor()
    parser = DataParser()
    db = DatabaseHandler()
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Process all files in input directory
    for filename in os.listdir('input'):
        if filename.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            file_path = os.path.join('input', filename)
            
            try:
                # Extract text using OCR
                text = ocr.process_file(file_path)
                
                # Parse text into structured data
                form_data = parser.parse_text(text)
                
                # Save to JSON file
                output_path = os.path.join('output', f"{filename}_output.json")
                with open(output_path, 'w') as f:
                    f.write(parser.to_json(form_data))
                
                # Store in database
                db.store_form_data(form_data)
                
                print(f"Successfully processed {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    process_forms() 