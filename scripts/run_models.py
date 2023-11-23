import os
from scripts.variables import (
    SDG_MAP,
    MODEL_TEMPLATE,
    GET_MODEL_DETAILS,
    PREDICTIONS_TEMPLATE,
)
import importlib
import dill
from scripts.file_org import (
    get_all_project_names,
    load_data,
    get_file_path,
    iterdatatype_data,
)
from scripts.prepare_data import prepare_labels
from glob import glob
import json
import pandas as pd


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


def iterate_model_files():
    # Get the path to the models directory
    model_path = os.path.join(os.path.dirname(__file__), "..", "models")

    # Iterate over Python files in the models directory
    for filename in os.listdir(model_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            model_name = os.path.splitext(filename)[0]
            module = importlib.import_module(f"models.{model_name}")

            # Check if the module has a "predict" function
            if hasattr(module, "TextAnalyticsModel"):
                yield model_name, module.TextAnalyticsModel


def iterate_saved_models():
    for model_path in glob(MODEL_TEMPLATE()):
        model_instance = load_model(model_path)
        filename = os.path.basename(model_path)
        sdg, model_name = GET_MODEL_DETAILS(filename)
        yield sdg, model_name, model_instance


def train_models():
    """
    Train models with a particular project.
    """
    ##########
    # GET DATA
    ##########
    # Get the list of available projects and offer them as options for training
    available_projects = get_all_project_names("train")
    assert len(available_projects) > 0, "No processed datasets available."

    option_list = "\n".join(
        [
            f"\t - [{i}] {project_name}"
            for i, project_name in enumerate(available_projects)
        ]
    )

    project_index = input(
        f"Which project would you like to train the model on:\n{option_list}\n\nSelect the project for training:"
    )
    if project_index.isdigit():
        project_index = int(project_index)

    assert project_index in range(
        len(available_projects)
    ), f"Invalid selection. Please choose one of the available options, [{list(range(len(available_projects)))}]"

    selected_project = available_projects[project_index]
    data = load_data(get_file_path("train", selected_project))
    text, labels = data["text"], data["labels"]

    #############
    # TRAIN MODEL
    #############
    for sdg in SDG_MAP:
        prepared_labels = prepare_labels(labels, sdg)
        for model_name, model in iterate_model_files():
            model_instance = model(sdg)
            model_instance.train(text, prepared_labels)
            model_filepath = MODEL_TEMPLATE(sdg, model_name)
            model_instance.save(model_filepath)


def save_predictions(path, predictions):
    """Save predictions in json file in list format."""
    prediction_df = pd.DataFrame(predictions)
    prediction_df.to_json(path, orient="records", lines=True)


def predict_models(datatype):
    for project_name, data in iterdatatype_data(datatype):
        text_list = data["text"]
        for sdg, model_name, model_instance in iterate_saved_models():
            predictions = [
                dict(index=i, text=text, prediction=model_instance.predict(text))
                for i, text in text_list.items()
            ]
            prediction_path = PREDICTIONS_TEMPLATE(
                sdg, model_name, project_name, datatype
            )
            save_predictions(prediction_path, predictions)


def main():
    pass


if __name__ == "__main__":
    main()
