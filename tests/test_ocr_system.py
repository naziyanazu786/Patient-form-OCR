import unittest
import os
from src.ocr_processor import OCRProcessor
from src.data_parser import DataParser
from src.db_handler import DatabaseHandler

class TestOCRSystem(unittest.TestCase):
    def setUp(self):
        self.ocr = OCRProcessor()
        self.parser = DataParser()
        self.db = DatabaseHandler()
        
    def test_ocr_processor_initialization(self):
        self.assertIsNotNone(self.ocr)
        
    def test_data_parser_initialization(self):
        self.assertIsNotNone(self.parser)
        
    def test_db_handler_initialization(self):
        self.assertIsNotNone(self.db)
        
    def test_directories_exist(self):
        self.assertTrue(os.path.exists('input'))
        self.assertTrue(os.path.exists('output'))
        self.assertTrue(os.path.exists('database'))

if __name__ == '__main__':
    unittest.main() 