import os
from src.db_handler import DatabaseHandler

def setup():
    """Initialize the database and create required directories"""
    # Create directories if they don't exist
    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    # Initialize database
    db = DatabaseHandler()
    db.initialize_database()
    
    print("Setup completed successfully!")
    print("- Database initialized")
    print("- Input directory created")
    print("- Output directory created")
    print("\nYou can now:")
    print("1. Place patient assessment forms in the 'input' directory")
    print("2. Run 'python process_forms.py' to process the forms")
    print("3. Check the 'output' directory for JSON results")

if __name__ == "__main__":
    setup() 