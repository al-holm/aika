import unittest, logging
from scripts.check_results import find_missing_files

class TestFindMissingFiles(unittest.TestCase):
    """
    tests the find_missing_files function of the check_results script
    """

    def test_no_missing_files(self):
        files = ["q1_modelA", "q2_modelA", "q3_modelA", "q1_modelB", "q2_modelB", "q3_modelB"]
        expected_missing = []
        self.assertEqual(find_missing_files(files), expected_missing)

    def test_some_missing_files(self):
        files = ["q1_modelA", "q3_modelA", "q4_modelA", "q1_modelB", "q2_modelB"]
        expected_missing = ["q2_modelA"]
        self.assertEqual(find_missing_files(files), expected_missing)

    def test_all_missing_files(self):
        files = ["q5_modelA", "q5_modelB"]
        expected_missing = ["q1_modelA", "q2_modelA", "q3_modelA", "q4_modelA", 
                            "q1_modelB", "q2_modelB", "q3_modelB", "q4_modelB"]
        self.assertEqual(find_missing_files(files), expected_missing)

    def test_non_sequential_missing_files(self):
        files = ["q1_modelA", "q4_modelA", "q7_modelA", "q1_modelB", "q3_modelB", "q5_modelB"]
        expected_missing = ["q2_modelA", "q3_modelA", "q5_modelA", "q6_modelA", "q2_modelB", "q4_modelB"]
        self.assertEqual(find_missing_files(files), expected_missing)

    def test_invalid_filenames(self):
        files = ["invalid_file", "q1-modelA", "q2_modelA", "q_modelB"]
        expected_missing = ["q1_modelA"]
        self.assertEqual(find_missing_files(files), expected_missing)
    
    def test_empty_input(self):
        files = []
        expected_missing = []
        self.assertEqual(find_missing_files(files), expected_missing)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    unittest.main()