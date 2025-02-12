from PIL import Image, ImageDraw, ImageFont
import os

def create_test_form():
    # Create a new image with white background
    img = Image.new('RGB', (800, 1000), 'white')
    draw = ImageDraw.Draw(img)
    
    # Add test data
    text_content = [
        "Patient ID: P12345",
        "Name: John Smith",
        "DOB: 05/15/1975",
        "Date: 03/20/2024",
        "Injection: Yes",
        "Exercise Therapy: No",
        "Bending: 3",
        "Putting on Shoes: 2",
        "Sleeping: 1",
        "Since Last Treatment: Better",
        "Since Start of Treatment: Better",
        "Last 3 Days: Good",
        "Pain Level: 4",
        "Numbness: 2",
        "Tingling: 3",
        "Burning: 1",
        "Tightness: 2",
        "BP: 120/80",
        "HR: 72",
        "Weight: 70.5",
        "Height: 5'10\"",
        "SpO2: 98",
        "Temperature: 98.6",
        "Blood Glucose: 95",
        "Respirations: 16"
    ]
    
    y_position = 50
    for line in text_content:
        draw.text((50, y_position), line, fill='black')
        y_position += 35
    
    # Save the test form
    os.makedirs('input', exist_ok=True)
    img.save('input/test_form.png')
    print("Test form created at input/test_form.png")

if __name__ == "__main__":
    create_test_form()