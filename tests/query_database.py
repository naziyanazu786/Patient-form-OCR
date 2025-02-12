from src.db_handler import DatabaseHandler
import json

def query_test():
    db = DatabaseHandler()
    # Get forms for our test patient
    forms = db.get_patient_forms("John Smith", "05/15/1975")
    
    print("Retrieved forms:")
    for form in forms:
        print("\nForm data:")
        print(json.dumps(form, indent=2))

if __name__ == "__main__":
    query_test()