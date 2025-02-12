CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    dob DATE
);

CREATE TABLE IF NOT EXISTS forms_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER REFERENCES patients(id),
    form_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_name ON patients(name);
CREATE INDEX idx_patient_dob ON patients(dob);
CREATE INDEX idx_form_patient ON forms_data(patient_id); 