import json
import re
from datetime import datetime

class DataParser:
    def __init__(self):
        self.patterns = {
            # Patient Details
            'name': r'Name[:\s]*([A-Za-z\s]+)',
            'dob': r'DOB[:\s]*(\d{2}[-/]\d{2}[-/]\d{4})',
            
            # Treatment Details
            'date': r'Date[:\s]*(\d{2}[-/]\d{2}[-/]\d{4})',
            'injection': r'Injection[:\s]*(Yes|No)',
            'exercise_therapy': r'Exercise Therapy[:\s]*(Yes|No)',
            
            # Difficulty Ratings
            'bending': r'Bending[:\s]*(\d)',
            'putting_on_shoes': r'Putting on Shoes[:\s]*(\d)',
            'sleeping': r'Sleeping[:\s]*(\d)',
            
            # Patient Changes
            'since_last_treatment': r'Since Last Treatment[:\s]*(Good|Not Good|Better|Worse)',
            'since_start': r'Since Start of Treatment[:\s]*(Better|Worse|Same)',
            'last_3_days': r'Last 3 Days[:\s]*(Good|Bad)',
            
            # Pain Symptoms
            'pain': r'Pain Level[:\s]*(\d{1,2})',
            'numbness': r'Numbness[:\s]*(\d{1,2})',
            'tingling': r'Tingling[:\s]*(\d{1,2})',
            'burning': r'Burning[:\s]*(\d{1,2})',
            'tightness': r'Tightness[:\s]*(\d{1,2})',
            
            # Medical Assistant Data
            'blood_pressure': r'BP[:\s]*(\d{2,3}/\d{2,3})',
            'hr': r'HR[:\s]*(\d{2,3})',
            'weight': r'Weight[:\s]*(\d{2,3}(?:\.\d)?)',
            'height': r'Height[:\s]*(\d\'(?:\d{1,2})?\"?)',
            'spo2': r'SpO2[:\s]*(\d{2,3})',
            'temperature': r'Temperature[:\s]*((?:\d{2,3}(?:\.\d)?)|(?:\d{1,2}(?:\.\d)?))',
            'blood_glucose': r'Blood Glucose[:\s]*(\d{2,3})',
            'respirations': r'Respirations[:\s]*(\d{1,2})'
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
            'date': self.extract_field(text, self.patterns['date']),
            'injection': self.extract_field(text, self.patterns['injection']),
            'exercise_therapy': self.extract_field(text, self.patterns['exercise_therapy']),
            
            'difficulty_ratings': {
                'bending': self.extract_field(text, self.patterns['bending']),
                'putting_on_shoes': self.extract_field(text, self.patterns['putting_on_shoes']),
                'sleeping': self.extract_field(text, self.patterns['sleeping'])
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
                'height': self.extract_field(text, self.patterns['height']),
                'spo2': self.extract_field(text, self.patterns['spo2']),
                'temperature': self.extract_field(text, self.patterns['temperature']),
                'blood_glucose': self.extract_field(text, self.patterns['blood_glucose']),
                'respirations': self.extract_field(text, self.patterns['respirations'])
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
        if ma_data['spo2']:
            ma_data['spo2'] = int(ma_data['spo2'])
        if ma_data['blood_glucose']:
            ma_data['blood_glucose'] = int(ma_data['blood_glucose'])
        if ma_data['respirations']:
            ma_data['respirations'] = int(ma_data['respirations'])
        
        return data

    def to_json(self, data):
        """Convert parsed data to JSON string"""
        return json.dumps(data, indent=4) 