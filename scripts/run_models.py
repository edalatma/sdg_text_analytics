import os
from scripts.variables import SDG_MAP
import importlib
import dill


def load_model(file_path):
    """
    Load the TextAnalyticsModel instance from a file.

    Parameters:
        - file_path (str): File path to load the model from.

    Returns:
        - TextAnalyticsModel: Loaded model instance.
    """
    with open(file_path, "rb") as file:
        loaded_model = dill.load(file)

    return loaded_model


def iterate_models():
    # Get the path to the models directory
    model_path = os.path.join(os.path.dirname(__file__), "..", "models")

    # Iterate over Python files in the models directory
    for filename in os.listdir(model_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = os.path.splitext(filename)[0]
            module = importlib.import_module(f"models.{module_name}")

            # Check if the module has a "predict" function
            if hasattr(module, "TextAnalyticsModel"):
                yield filename, module.TextAnalyticsModel


def main():
    pass


if __name__ == "__main__":
    main()
