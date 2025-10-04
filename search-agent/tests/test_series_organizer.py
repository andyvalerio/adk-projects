import unittest
import os
import shutil
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from series_organizer import move_file

class TestSeriesOrganizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = "/tmp/test_tv_series"
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.test_file = os.path.join(self.test_dir, "Silicon.Valley.S06E03.avi")
        with open(self.test_file, 'w') as f:
            f.write("dummy content")
            
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_should_move_file_to_correct_series_directory(self):
        """Test that file moves to the correct series directory."""
        file_path = self.test_file
        info = {
            'series': 'Silicon Valley',
            'season': 6,
            'episode': 3
        }
        
        new_path = move_file(file_path, info)
        
        expected_path = os.path.join("/tmp/test_tv_series/Silicon.Valley", 
                                   "Silicon.Valley.S06E03.avi")
        self.assertEqual(new_path, expected_path)
        self.assertTrue(os.path.exists(new_path))

if __name__ == '__main__':
    unittest.main()