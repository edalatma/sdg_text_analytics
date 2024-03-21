import pandas as pd
from glob import glob
import os
import sys

sys.path.append("./scripts")
from variables import (
    PROJECTNAME_DATA_PATHS,
    SDGMODEL_DATA_PATHS,
    DOCCANO_EXPORT_DIRS,
    DOCCANO_EXPORT_FILES,
)


def check_datatype(datatype):
    """
    Checks if the provided datatype is a valid key in PROJECTNAME_DATA_PATHS.

    Parameters:
    - datatype (str): The datatype to be checked.

    Raises:
    - ValueError: If the provided datatype is not a valid key in PROJECTNAME_DATA_PATHS.
    """
    if datatype not in PROJECTNAME_DATA_PATHS:
        raise ValueError(
            f"Invalid datatype: {datatype}. Supported datatypes are {list(PROJECTNAME_DATA_PATHS.keys())}."
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


def save_data(data, datatype, project_name, sdg):
    """
    Saves the given data to the specified file path.

    Parameters:
    - data (pd.DataFrame): The Pandas DataFrame to be saved.
    - path (str): The file path where the data will be saved.
    """
    path = get_file_path(datatype, project_name, sdg)
    data.to_json(path, orient="records", lines=True)


@check_datatype_decorator
def iterdatatype_data(datatype: str, sdg: str) -> tuple[str, pd.DataFrame]:
    """
    Iterates over JSON files based on the specified datatype.

    Parameters:
    - datatype (str): The type of data to iterate over, which should be one of the keys in PROJECTNAME_DATA_PATHS.

    Options in PROJECTNAME_DATA_PATHS:
    - 'raw': Raw data files in the 'data/raw/' directory with a '*.json' extension.
    - 'test': Processed test data files in the 'data/processed/' directory ending with '__test.json'.
    - 'train': Processed training data files in the 'data/processed/' directory ending with '__train.json'.
    - 'traindev': Processed training and development data files in the 'data/processed/' directory ending with '__traindev.json'.
    - 'dev': Processed development data files in the 'data/processed/' directory ending with '__dev.json'.

    Returns:
    - Generator: Yields a tuple containing the project name and the corresponding Pandas DataFrame for each JSON file.

    Raises:
    - ValueError: If the provided datatype is not a valid key in PROJECTNAME_DATA_PATHS.

    Example:
    ```
    for project_name, data in iterdata("train"):
        # process data for the 'train' datatype
        print(f"Processing {project_name} data...")
        # Your data processing logic here
    ```
    """
    query = PROJECTNAME_DATA_PATHS[datatype](sdg=sdg)
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
    if "SDG " in project_name:
        project_sdg, project_name = project_name.split("_", maxsplit=1)

    return project_name


@check_datatype_decorator
def get_file_path(datatype: str, project_name: str, sdg=False):
    """
    Generates the file path based on the provided project name and datatype.

    Parameters:
    - project_name (str): The name of the project.
    - datatype (str): The datatype associated with the project.

    Returns:
    - str: The file path corresponding to the project and datatype.
    """

    file_path = PROJECTNAME_DATA_PATHS[datatype](sdg, project_name)
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

    for datatype, query_template in PROJECTNAME_DATA_PATHS.items():
        path = query_template(project_name)
        if os.path.exists(path):
            project_mappings[datatype] = path

    return project_mappings


def get_all_project_names(datatype: str = None):
    """
    Gets all the project names available across all files in the "data" directory.

    Returns:
    - list: A list of strings representing the project names available.
    """
    all_project_names = set()

    for dt, query_template in PROJECTNAME_DATA_PATHS.items():
        if datatype is not None and dt != datatype:
            continue
        matching_paths = glob(query_template())

        # Extract project names from the file paths
        project_names = [get_project_name(dt, path) for path in matching_paths]

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
    project_paths = glob(DOCCANO_EXPORT_DIRS)

    for project_path in project_paths:
        project_name = os.path.basename(project_path)

        dataframe_paths = glob(DOCCANO_EXPORT_FILES(project_name))
        dataframes = [load_data(path) for path in dataframe_paths]
        yield project_name, dataframes


def prepare_dirs():
    """
    Ensure the existence of directories within the 'data/' path.

    This function checks if the specified subdirectories exist within the 'data/'
    directory. If not, it creates them. The goal is to ensure that the required
    directory structure is in place for storing or organizing data.
    """
    directory = os.path.dirname(DOCCANO_EXPORT_DIRS)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for path_template in PROJECTNAME_DATA_PATHS.values():
        directory = os.path.dirname(path_template())
        if not os.path.exists(directory):
            os.makedirs(directory)

    for path_template in SDGMODEL_DATA_PATHS.values():
        directory = os.path.dirname(path_template())
        if not os.path.exists(directory):
            os.makedirs(directory)
