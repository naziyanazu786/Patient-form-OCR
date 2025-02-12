from sqlalchemy import create_engine, text
import json
import os

class DatabaseHandler:
    def __init__(self, db_path='database/forms.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        
    def initialize_database(self):
        """Initialize database with schema"""
        with open('database/schema.sql', 'r') as f:
            schema = f.read()
            
        with self.engine.connect() as conn:
            conn.execute(text(schema))
            conn.commit()

    def store_form_data(self, form_data):
        """Store processed form data in the database"""
        with self.engine.connect() as conn:
            # First, check if patient exists
            query = text("""
                SELECT id FROM patients 
                WHERE name = :name AND dob = :dob
            """)
            
            result = conn.execute(query, {
                'name': form_data['patient_name'],
                'dob': form_data['dob']
            }).first()
            
            if result:
                patient_id = result[0]
            else:
                # Insert new patient
                query = text("""
                    INSERT INTO patients (name, dob)
                    VALUES (:name, :dob)
                    RETURNING id
                """)
                
                patient_id = conn.execute(query, {
                    'name': form_data['patient_name'],
                    'dob': form_data['dob']
                }).scalar()
            
            # Store form data
            query = text("""
                INSERT INTO forms_data (patient_id, form_json)
                VALUES (:patient_id, :form_json)
            """)
            
            conn.execute(query, {
                'patient_id': patient_id,
                'form_json': json.dumps(form_data)
            })
            
            conn.commit()

    def get_patient_forms(self, patient_name, dob):
        """Retrieve all forms for a specific patient"""
        query = text("""
            SELECT f.form_json
            FROM forms_data f
            JOIN patients p ON f.patient_id = p.id
            WHERE p.name = :name AND p.dob = :dob
            ORDER BY f.created_at DESC
        """)
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {
                'name': patient_name,
                'dob': dob
            })
            return [json.loads(row[0]) for row in result] 