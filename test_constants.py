TEST_CALCULATOR_DIR_RESULT = """Result for current directory:
 - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True"""

TEST_CALCULATOR_PKG_EXPECTED = """Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False"""

TEST_CALCULATOR_BIN_EXPECTED = """Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory"""

TEST_CALCULATED_ERR_EXPECTED = """Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory"""

TEST_CALCULATOR_FILE_EXPECTED = """Results for 'main.py' director:
    Error: "main.py" is not a directory"""