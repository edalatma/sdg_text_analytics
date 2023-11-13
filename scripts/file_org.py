import pandas as pd
from glob import glob
import os

current_dir = os.path.dirname(__file__)

FILENAME_OPTIONS = {
    "raw": os.path.join(current_dir, "..", "data/raw/*.jsonl"),
    "test": os.path.join(current_dir, "..", "data/processed/*__test.jsonl"),
    "train": os.path.join(current_dir, "..", "data/processed/*__train.jsonl"),
    "traindev": os.path.join(current_dir, "..", "data/processed/*__traindev.jsonl"),
    "dev": os.path.join(current_dir, "..", "data/processed/*__dev.jsonl"),
    "predictions": os.path.join(
        current_dir, "..", "data/predictions/*__predictions.jsonl"
    ),
}

DOCCANO_FORMAT = os.path.join(current_dir, "..", "data/doccano_export/*")


def check_datatype(datatype):
    """
    Checks if the provided datatype is a valid key in FILENAME_OPTIONS.

    Parameters:
    - datatype (str): The datatype to be checked.

    Raises:
    - ValueError: If the provided datatype is not a valid key in FILENAME_OPTIONS.
    """
    if datatype not in FILENAME_OPTIONS:
        raise ValueError(
            f"Invalid datatype: {datatype}. Supported datatypes are {list(FILENAME_OPTIONS.keys())}."
        )


def check_datatype_decorator(func):
    """
    Decorator function to check the validity of the datatype parameter.
    """

    def wrapper(datatype, *args, **kwargs):
        check_datatype(datatype)
        return func(datatype, *args, **kwargs)

    return wrapper


def load_data(path):
    """
    Loads data from the specified file path.

    Parameters:
    - path (str): The file path to the data file.

    Returns:
    - pd.DataFrame: A Pandas DataFrame containing the loaded data.
    """
    data = pd.read_json(path, lines=True)
    return data


def save_data(data, datatype, project_name):
    """
    Saves the given data to the specified file path.

    Parameters:
    - data (pd.DataFrame): The Pandas DataFrame to be saved.
    - path (str): The file path where the data will be saved.
    """
    path = get_file_path(datatype, project_name)
    data.to_json(path, orient="records", lines=True)


@check_datatype_decorator
def iterdatatype_data(datatype: str) -> tuple[str, pd.DataFrame]:
    """
    Iterates over JSON files based on the specified datatype.

    Parameters:
    - datatype (str): The type of data to iterate over, which should be one of the keys in FILENAME_OPTIONS.

    Options in FILENAME_OPTIONS:
    - 'raw': Raw data files in the 'data/raw/' directory with a '*.json' extension.
    - 'test': Processed test data files in the 'data/processed/' directory ending with '__test.json'.
    - 'train': Processed training data files in the 'data/processed/' directory ending with '__train.json'.
    - 'traindev': Processed training and development data files in the 'data/processed/' directory ending with '__traindev.json'.
    - 'dev': Processed development data files in the 'data/processed/' directory ending with '__dev.json'.
    - 'prediction': Prediction data files in the 'data/predictions/' directory ending with '__predictions.json'.

    Returns:
    - Generator: Yields a tuple containing the project name and the corresponding Pandas DataFrame for each JSON file.

    Raises:
    - ValueError: If the provided datatype is not a valid key in FILENAME_OPTIONS.

    Example:
    ```
    for project_name, data in iterdata("train"):
        # process data for the 'train' datatype
        print(f"Processing {project_name} data...")
        # Your data processing logic here
    ```
    """
    query = FILENAME_OPTIONS[datatype]
    for path in glob(query):
        project_name = get_project_name(datatype, path)
        data = load_data(path)
        yield project_name, data


@check_datatype_decorator
def get_project_name(datatype: str, path: str) -> str:
    """
    Extracts the project name from the given path and datatype.

    Parameters:
    - path (str): The file path from which to extract the project name.
    - datatype (str): The datatype associated with the project.

    Returns:
    - str: The extracted project name.
    """
    base_name = os.path.basename(path)
    project_name = base_name.replace(f"__{datatype}", "").replace(".jsonl", "")
    return project_name


@check_datatype_decorator
def get_file_path(datatype: str, project_name: str):
    """
    Generates the file path based on the provided project name and datatype.

    Parameters:
    - project_name (str): The name of the project.
    - datatype (str): The datatype associated with the project.

    Returns:
    - str: The file path corresponding to the project and datatype.
    """

    file_path = FILENAME_OPTIONS[datatype].replace("*", project_name)
    return file_path


def get_project_mappings(project_name):
    """
    Finds all available datasources for a given project.

    Parameters:
    - project_name (str): The name of the project.

    Returns:
    - dict: A dictionary mapping datasource types to file paths for the given project.
    """
    project_mappings = {}

    for datatype, query_template in FILENAME_OPTIONS.items():
        path = query_template.replace("*", project_name)
        if os.path.exists(path):
            project_mappings[datatype] = path

    return project_mappings


def get_all_project_names():
    """
    Gets all the project names available across all files in the "data" directory.

    Returns:
    - list: A list of strings representing the project names available.
    """
    all_project_names = set()

    for datatype, query in FILENAME_OPTIONS.items():
        matching_paths = glob(query)

        # Extract project names from the file paths
        project_names = [get_project_name(datatype, path) for path in matching_paths]

        # Add the project names to the set to ensure uniqueness
        all_project_names.update(project_names)

    return list(all_project_names)


def get_doccano_export_paths():
    """
    Iterates over projects available in doccano_export.

    Returns:
    - Generator: Yields a tuple containing the project name and corresponding list of Pandas
        DataFrames for each directory
    """
    project_paths = glob(DOCCANO_FORMAT)

    for project_path in project_paths:
        project_name = os.path.basename(project_path)

        dataframe_paths = glob(
            os.path.join(
                current_dir, "..", f"data/doccano_export/{project_name}/*.jsonl"
            )
        )
        dataframes = [load_data(path) for path in dataframe_paths]
        yield project_name, dataframes


def prepare_dirs():
    directory = os.path.dirname(DOCCANO_FORMAT)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for path in FILENAME_OPTIONS.values():
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
