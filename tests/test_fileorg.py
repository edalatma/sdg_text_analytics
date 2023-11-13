import os
import pandas as pd
import unittest
from scripts.file_org import (
    FILENAME_OPTIONS,
    get_project_name,
    get_file_path,
    get_project_mappings,
    get_all_project_names,
)


class TestFileOrg(unittest.TestCase):
    def setUp(self):
        # Create test data
        self.project_name = lambda n: f"test_project{n}"
        self.project_0 = self.project_name(0)
        self.test_data_paths = self.create_test_files(3)

    def tearDown(self):
        for _, _, path in self.test_data_paths:
            os.remove(path)

    def create_test_files(self, num_files):
        # Create test files within the specified path template
        file_paths = []
        for datatype, path_template in FILENAME_OPTIONS.items():
            for i in range(num_files):
                project_name = self.project_name(i)
                file_path = path_template.replace("*", project_name)
                pd.DataFrame({"col1": [i], "col2": [f"a{i}"]}).to_json(
                    file_path, orient="records", lines=True
                )
                file_paths.append((datatype, project_name, file_path))
        return file_paths

    def test_get_file_path(self):
        # Assert that the result is the expected project path
        result = get_file_path("raw", self.project_0)
        expected = FILENAME_OPTIONS["raw"].replace("*", self.project_0)
        self.assertEqual(result, expected)

    def test_get_project_name(self):
        # Assert that the result is the expected project name
        for datatype, project_name, path in self.test_data_paths:
            result = get_project_name(datatype, path)
            expected = project_name
            self.assertEqual(result, expected)

    def test_get_project_mappings(self):
        # Assert that the result contains the expected project mappings
        result = get_project_mappings(self.project_0)

        # Check that all the keys appear
        self.assertTrue(set(result.keys()), set(FILENAME_OPTIONS.keys()))

        # Check that the project paths are correct
        for datatype, path in result.items():
            expected_path = FILENAME_OPTIONS[datatype].replace("*", self.project_0)
            self.assertEqual(path, expected_path)

    def test_get_all_project_names(self):
        result = get_all_project_names()
        expected = {project_name for _, project_name, _ in self.test_data_paths}
        self.assertTrue(set(result).issuperset(expected))


if __name__ == "__main__":
    unittest.main()
