import unittest
import re
import sys
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from test_constants import *
from config import *

class BootAiTests(unittest.TestCase):
    def normalize_string(self, s: str) -> str:
        s = self.sort_string(s)
        return re.sub(r"file_size=\d+ bytes", "file_size=IGNORED bytes", s)
    
    def sort_string(self, s) -> str:
        str_list = s.splitlines()
        str_list.pop(0)
        return "\n".join(list(sorted(str_list)))
    
    def print_normalized_values(self, actual, expected):
        print(f"####################\n\nNormalized Results:\n{actual}\n\n-------------------\n\nNormalized Expected:\n{expected}\n\n####################")

    def get_results(self, wd, dir):
        file_info = get_files_info(wd, dir)
        if dir == ".":
            results = f"Result for current directory:\n{file_info}"
        else:
            results = f"Result for '{dir}' directory:\n{file_info}"
        return self.normalize_string(results)
    
    def print_actual_formatted(self, actual, func_name):
        header = f"######## {func_name} ########"
        print(header)
        print(actual)
        print(f"{'#' * len(header)}")
    

    def test_calculator_dir(self):
        actual = self.get_results("calculator", ".")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertAlmostEqual(actual, self.normalize_string(TEST_CALCULATOR_DIR_RESULT))

    def test_calculator_pkg(self):
        actual = self.get_results("calculator", "pkg")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertAlmostEqual(actual, self.normalize_string(TEST_CALCULATOR_PKG_EXPECTED))
    
    def test_calculator_bin(self):
        actual = self.get_results("calculator", "/bin")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        #self.print_normalized_values(actual, self.normalize_string(TEST_CALCULATOR_BIN_EXPECTED))
        self.assertEqual(actual, self.normalize_string(TEST_CALCULATOR_BIN_EXPECTED))
    
    def test_calculator_err(self):
        actual = self.get_results("calculator", "../")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertEqual(actual, self.normalize_string(TEST_CALCULATED_ERR_EXPECTED))

    def test_calculator_file(self):
        actual = self.get_results("calculator", "main.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertEqual(actual, self.normalize_string(TEST_CALCULATOR_FILE_EXPECTED))

    def test_content_lorem(self):
        actual = get_file_content("testfiles", "lorem.txt")
        self.assertNotIn("Error", actual)
        self.assertIn(f"truncated at {MAX_CHARS} characters", actual)
        self.assertIn("quis pretium arcu laoreet eu", actual)
    
    def test_content_main(self):
        actual = get_file_content("calculator", "main.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertNotIn(f"truncated at {MAX_CHARS} characters", actual)
        self.assertIn("def main():", actual)
    
    def test_content_calculator(self):
        actual = get_file_content("calculator", "pkg/calculator.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertNotIn(f"truncated at {MAX_CHARS} characters", actual)
        self.assertIn("def __init__(self):", actual)

    def test_content_bincat(self):
        actual = get_file_content("calculator", "/bin/cat")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertEqual('    Error: Cannot read "/bin/cat" as it is outside the permitted working directory', actual)

    def test_content_err(self):
        actual = get_file_content("calculator", "pkg/does_not_exist.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertTrue(actual.startswith("    Error:"))

    def test_write_calculator_lorem(self):
        actual = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertEqual(actual, 'Successfully wrote to "lorem.txt" (28 characters written)')

    def test_write_pkg_lorem(self):
        actual = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertEqual(actual, 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)')

    def test_write_err(self):
        actual = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertEqual(actual, '    Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory')

    def test_run_calc_main(self):
        actual = run_python_file("calculator", "main.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertNotIn("Error", actual)

    def test_run_calc_main_args(self):
        actual = run_python_file("calculator", "main.py", ["3 + 5"])
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertIn("8", actual)
        self.assertNotIn("Error", actual)

    def test_run_calc_tests(self):
        actual = run_python_file("calculator", "tests.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertNotIn("Error", actual)

    def test_run_calc_err(self):
        actual = run_python_file("calculator", "../main.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertIn("Error", actual)

    def test_run_calc_nonexist(self):
        actual = run_python_file("calculator", "nonexistent.py")
        self.print_actual_formatted(actual, sys._getframe().f_code.co_name)
        self.assertIn("Error", actual)

if __name__ == "__main__":
    unittest.main()