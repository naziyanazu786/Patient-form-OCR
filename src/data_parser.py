import json
import re
from datetime import datetime

class DataParser:
    def __init__(self):
        self.patterns = {
            # Patient Details
            'name': r'Patient Name\s*:\s*([A-Za-z\s]+)',
            'dob': r'DOB\s*:\s*(\d{1,2}/\d{1,2}/\d{2,4})',
            
            # Treatment Details
            'injection': r'INJECTION\s*:\s*(YES|NO)',
            'exercise_therapy': r'Exercise Therapy\s*:\s*(YES|NO)',
            
            # Difficulty Ratings (0-5)
            'bending': r'Bending or Stooping:\s*([0-5])',
            'putting_on_shoes': r'Putting on shoes:\s*([0-5])',
            'sleeping': r'Sleeping:\s*([0-5])',
            'standing': r'Standing for an hour:\s*([0-5])',
            'stairs': r'Going up or down a flight of stairs:\s*([0-5])',
            'walking': r'Walking through a store:\s*([0-5])',
            'driving': r'Driving for an hour:\s*([0-5])',
            'meal_prep': r'Preparing a meal:\s*([0-5])',
            'yard_work': r'Yard work:\s*([0-5])',
            'picking_up': r'Picking up items off the floor:\s*([0-5])',
            
            # Patient Changes
            'since_last_treatment': r'Patient Changes since last treatment:\s*(.*?)(?=Patient|$)',
            'since_start': r'Patient changes since the start of treatment:\s*(.*?)(?=Describe|$)',
            'last_3_days': r'Describe any functional changes within the last three days \(good or bad\):\s*(.*?)(?=Rate|$)',
            
            # Pain Symptoms (0-10)
            'pain': r'Pain:\s*(\d{1,2})',
            'numbness': r'Numbness:\s*(\d{1,2})',
            'tingling': r'Tingling:\s*(\d{1,2})',
            'burning': r'Burning:\s*(\d{1,2})',
            'tightness': r'Tightness:\s*(\d{1,2})',
            
            # Medical Assistant Data
            'blood_pressure': r'Blood Pressure:\s*(\d{2,3}/\d{2,3})',
            'hr': r'HR:\s*(\d{2,3})',
            'weight': r'Weight:\s*(\d{2,3}(?:\.\d)?)',
            'height': r'Height:\s*(\d\'(?:\d{1,2})?\"?)',
        }

    def extract_field(self, text, pattern):
        """Extract a single field using regex pattern"""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None

    def parse_text(self, text):
        """Parse OCR text into structured data"""
        data = {
            'patient_name': self.extract_field(text, self.patterns['name']),
            'dob': self.extract_field(text, self.patterns['dob']),
            'injection': self.extract_field(text, self.patterns['injection']),
            'exercise_therapy': self.extract_field(text, self.patterns['exercise_therapy']),
            
            'difficulty_ratings': {
                'bending': self.extract_field(text, self.patterns['bending']),
                'putting_on_shoes': self.extract_field(text, self.patterns['putting_on_shoes']),
                'sleeping': self.extract_field(text, self.patterns['sleeping']),
                'standing': self.extract_field(text, self.patterns['standing']),
                'stairs': self.extract_field(text, self.patterns['stairs']),
                'walking': self.extract_field(text, self.patterns['walking']),
                'driving': self.extract_field(text, self.patterns['driving']),
                'meal_prep': self.extract_field(text, self.patterns['meal_prep']),
                'yard_work': self.extract_field(text, self.patterns['yard_work']),
                'picking_up': self.extract_field(text, self.patterns['picking_up'])
            },
            
            'patient_changes': {
                'since_last_treatment': self.extract_field(text, self.patterns['since_last_treatment']),
                'since_start_of_treatment': self.extract_field(text, self.patterns['since_start']),
                'last_3_days': self.extract_field(text, self.patterns['last_3_days'])
            },
            
            'pain_symptoms': {
                'pain': self.extract_field(text, self.patterns['pain']),
                'numbness': self.extract_field(text, self.patterns['numbness']),
                'tingling': self.extract_field(text, self.patterns['tingling']),
                'burning': self.extract_field(text, self.patterns['burning']),
                'tightness': self.extract_field(text, self.patterns['tightness'])
            },
            
            'medical_assistant_data': {
                'blood_pressure': self.extract_field(text, self.patterns['blood_pressure']),
                'hr': self.extract_field(text, self.patterns['hr']),
                'weight': self.extract_field(text, self.patterns['weight']),
                'height': self.extract_field(text, self.patterns['height'])
            }
        }
        
        return self.convert_types(data)

    def convert_types(self, data):
        """Convert string values to appropriate types"""
        # Convert difficulty ratings to integers
        for key in data['difficulty_ratings']:
            if data['difficulty_ratings'][key]:
                data['difficulty_ratings'][key] = int(data['difficulty_ratings'][key])

        # Convert pain symptoms to integers
        for key in data['pain_symptoms']:
            if data['pain_symptoms'][key]:
                data['pain_symptoms'][key] = int(data['pain_symptoms'][key])

        # Convert medical assistant numeric data
        ma_data = data['medical_assistant_data']
        if ma_data['hr']:
            ma_data['hr'] = int(ma_data['hr'])
        if ma_data['weight']:
            ma_data['weight'] = float(ma_data['weight'])
        
        return data

    def to_json(self, data):
        """Convert parsed data to JSON string"""
        return json.dumps(data, indent=4) 
