import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
TEST_OUTPUT_DIR = os.path.join(ROOT_DIR, "tests", "output")
TEST_RESOURCES = os.path.join(ROOT_DIR, "tests", "resources")
TEST_RESPONSES = os.path.join(ROOT_DIR, "tests", "resources", "responses")