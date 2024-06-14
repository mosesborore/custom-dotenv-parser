import os
import unittest
from pathlib import Path

from dotenv_parser import load_dotenv


class TestDotenvParser(unittest.TestCase):
    def setUp(self):
        # Set up temporary .env file for testing
        self.dotenv_path = Path("test.env")
        self.dotenv_path.write_text(
            """
            NAME=TestUser
            AGE=30

            # This is a comment
            LOCATION = Earth

            # Another comment
            QUOTE = "This is a quote"
            SINGLE_QUOTE = 'Single quote value'
            """
        )

    def tearDown(self):
        # Remove temporary .env file after testing
        if self.dotenv_path.exists():
            self.dotenv_path.unlink()

    def test_load_env(self):
        load_dotenv(self.dotenv_path)
        self.assertEqual(os.getenv("NAME"), "TestUser")
        self.assertEqual(os.getenv("AGE"), "30")
        self.assertEqual(os.getenv("LOCATION"), "Earth")
        self.assertEqual(os.getenv("QUOTE"), "This is a quote")
        self.assertEqual(os.getenv("SINGLE_QUOTE"), "Single quote value")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_dotenv("nonexistent.env")


if __name__ == "__main__":
    unittest.main()
