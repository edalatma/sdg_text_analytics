import unittest
import os
import importlib


class TestMakePredictionFunction(unittest.TestCase):
    def setUp(self):
        # Input outline for testing
        self.outline = "This is a sample outline for testing purposes."

        # Make predictions using the function
        with self.subTest():
            self.predictions = self.predict(self.outline)

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

    def test_pred_structure(self):
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

    # Get the path to the models directory
    implementations_path = os.path.join(os.path.dirname(__file__), "..", "models")

    # Iterate over Python files in the models directory
    for filename in os.listdir(implementations_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = os.path.splitext(filename)[0]
            module = importlib.import_module(f"models.{module_name}")

            # Check if the module has a "predict" function
            if hasattr(module, "predict"):

                class TestImplementation(TestMakePredictionFunction):
                    def setUp(self):
                        self.predict = module.predict
                        super().setUp()

                test_suite.addTest(unittest.makeSuite(TestImplementation))

    return test_suite


if __name__ == "__main__":
    unittest.main()
