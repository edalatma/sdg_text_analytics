import unittest
import os
import importlib
from scripts.run_models import iterate_models, load_model


class TestMakePredictionFunction(unittest.TestCase):
    def setUp(self):
        # Input outline for testing
        self.outline = "This is a sample outline for testing purposes."

        # Available SDGs
        self.available_sdgs = [
            "SDG-1",
            "SDG-2",
            "SDG-3",
            "SDG-4",
            "SDG-5",
            "SDG-6",
            "SDG-7",
            "SDG-8",
            "SDG-9",
            "SDG-10",
            "SDG-11",
            "SDG-12",
            "SDG-13",
            "SDG-14",
            "SDG-15",
            "SDG-16",
        ]
        with self.subTest():
            self.test_model = self.textanalytics_class(self.available_sdgs[0])

    def test_load_models(self):
        # Make predictions using the function
        for SDG in self.available_sdgs:
            with self.subTest():
                self.sdg_model = self.textanalytics_class(SDG)

    def test_saving_and_loading(self):
        # self.test_model.save("test.dill")
        # loaded_model = load_model("test.dill")
        pass

    def test_span(self):
        pass

    def test_confidence(self):
        pass

    def test_pred_sdgs(self):
        pass


def load_tests(loader, standard_tests, pattern):
    """
    Load and return a TestSuite containing unit tests for the make_prediction function
    implemented in each Python file within the 'models' directory.

    Returns:
        unittest.TestSuite: A TestSuite containing unit tests for the make_prediction
        function in each 'models' module that has the function.

    This function dynamically discovers and creates test cases for the make_prediction
    function in each Python file within the 'models' directory. It iterates through
    the files, imports the module, and checks if the module contains a
    'make_prediction' function. If found, it creates a test case class derived from
    'TestMakePredictionFunction' and adds it to the TestSuite.
    """
    test_suite = unittest.TestSuite()

    # Iterate over Python files in the models directory
    for textanalytics_class in iterate_models():

        class TestImplementation(TestMakePredictionFunction):
            def setUp(self):
                self.textanalytics_class = textanalytics_class
                super().setUp()

        test_suite.addTest(unittest.makeSuite(TestImplementation))

    return test_suite


if __name__ == "__main__":
    unittest.main()
