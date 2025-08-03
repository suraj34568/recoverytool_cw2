# unit_testing.py

import unittest
import tempfile
import os
import shutil

# Import functions from recovery_cli.py
from recovery_cli import scan_files, recover_files

class TestSimpleFileRecoveryCLI(unittest.TestCase):

    def setUp(self):
        # Set up temporary directories
        self.scan_dir = tempfile.mkdtemp()
        self.recovery_dir = tempfile.mkdtemp()

        # Create mock files in scan_dir
        self.test_files = [
            os.path.join(self.scan_dir, "test1.txt"),
            os.path.join(self.scan_dir, "test2.deleted"),
            os.path.join(self.scan_dir, "ignore.docx")  # Should not be detected
        ]

        for file_path in self.test_files:
            with open(file_path, "w") as f:
                f.write("Mock data")

    def test_scan_files(self):
        # Scan should find only .txt and .deleted files
        results = scan_files(self.scan_dir)
        self.assertEqual(len(results), 2)
        self.assertTrue(any(f.endswith(".txt") for f in results))
        self.assertTrue(any(f.endswith(".deleted") for f in results))

    def test_recover_files(self):
        # Simulate selecting both files
        files = scan_files(self.scan_dir)
        selected_indices = [0, 1]
        recover_files(files, selected_indices, self.recovery_dir)

        # Check if files exist in recovery_dir
        recovered_files = os.listdir(self.recovery_dir)
        self.assertIn("test1.txt", recovered_files)
        self.assertIn("test2.deleted", recovered_files)
        self.assertNotIn("ignore.docx", recovered_files)

    def tearDown(self):
        # Remove all temp files and folders
        shutil.rmtree(self.scan_dir)
        shutil.rmtree(self.recovery_dir)

if __name__ == "__main__":
    unittest.main()
