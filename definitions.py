import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
TEST_OUTPUT_DIR = os.path.join(ROOT_DIR, "tests", "output")
TEST_RESOURCES = os.path.join(ROOT_DIR, "tests", "resources")
TEST_RESPONSES = os.path.join(ROOT_DIR, "tests", "resources", "responses")

# an unfortunate flag for testing purposes...
FLAG_TO_SKIP_CLOSING_OF_IN_MEMORY_TEST_FILE = "flag to skip closing of the file"
