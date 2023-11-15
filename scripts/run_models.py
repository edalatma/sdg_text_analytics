import os
from scripts.variables import SDG_MAP, MODEL_TEMPLATE
import importlib
import dill
from scripts.file_org import (
    get_all_project_names,
    load_data,
    get_file_path,
)
from scripts.prepare_data import prepare_labels


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
        for model_name, model in iterate_models():
            model_instance = model(sdg)
            model_instance.train(text, prepared_labels)
            model_filepath = MODEL_TEMPLATE(sdg, model_name)
            model_instance.save(model_filepath)


def main():
    pass


if __name__ == "__main__":
    main()
