from sklearn.model_selection import train_test_split, StratifiedKFold
from scripts.file_org import (
    get_doccano_export_paths,
    save_data,
    get_file_path,
    load_data,
)
import pandas as pd

SEED = 1
REQUIRED_COLS = [
    "text",
    "STRM",
    "FACULTY DESC",
    "DEPARTMENT",
    "CRSE CAREER",
    "SSR COMPONENT",
    "CRSE_ID",
    "COURSE CODE",
    "CATALOG NBR",
    "CLASS SECTION",
    "CLASS DESCR",
    "ENROLMENT",
    "LAST TERM OFFERED",
    "URL",
    "cats",
    "entities",
]

SDG_MAP = {
    "SDG 1": "1 - No Poverty",
    "SDG 2": "2 - Zero Hunger",
    "SDG 3": "3 - Good Health and Well-Being",
    "SDG 4": "4 - Quality Education",
    "SDG 5": "5 - Gender Equality",
    "SDG 6": "6 - Clean Water and Sanitation",
    "SDG 7": "7 - Affordable and Clean Energy",
    "SDG 8": "8 - Decent Work and Economic Growth",
    "SDG 9": "9 - Industry, Innovation, and Infrastructure",
    "SDG 10": "10 - Reduced Inequalities",
    "SDG 11": "11 - Sustainable Cities and Communities",
    "SDG 12": "12 - Responsible Consumption and Production",
    "SDG 13": "13 - Climate Action",
    "SDG 14": "14 - Life Below Water",
    "SDG 15": "15 - Life on Land",
    "SDG 16": "16 - Peace, Justice, and Strong Institutions",
}
REVERSE_SDG_MAP = dict(zip(SDG_MAP.values(), SDG_MAP.keys()))


def stratified_five_fold_cv_generator(df):
    """
    Generate train and dev sets for stratified five-fold cross-validation.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to be split.
    - target_column (str): The column used for stratification.
    - seed (int): Seed for reproducibility.

    Yields:
    - train_set (pd.DataFrame): Training set for the current fold.
    - dev_set (pd.DataFrame): Development set for the current fold.
    """

    # Use StratifiedKFold for stratified five-fold cross-validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    # Stratify over department because it was consistently stratify both
    # grad and undergrad courses. This is because most grad courses appear
    # under "School of Graduate Studies" rather than the undergrad faculties
    for train_index, dev_index in skf.split(df, df["DEPARTMENT"]):
        train_set = df.iloc[train_index]
        dev_set = df.iloc[dev_index]
        yield train_set, dev_set


def split_data(df):
    """
    Split a DataFrame into train, dev, test, and train+dev sets.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to be split.
    - seed (int): Seed for reproducibility.

    Returns:
    - train_set (pd.DataFrame): 60% of the input DataFrame for training.
    - dev_set (pd.DataFrame): 20% of the input DataFrame for development/validation.
    - test_set (pd.DataFrame): 20% of the input DataFrame for testing.
    - train_dev_set (pd.DataFrame): The combination of train and dev sets (80% of the input DataFrame).
    """

    # Split the data into train_dev and test sets
    train_dev_set, test_set = train_test_split(df, test_size=0.2, random_state=SEED)

    # Further split train_dev_set into train and dev sets
    # 80% * 0.25 --> 20% dev set
    train_set, dev_set = train_test_split(
        train_dev_set, test_size=0.25, random_state=SEED
    )

    return train_set, dev_set, test_set, train_dev_set


def save_splits(project_name, train_set, dev_set, test_set, train_dev_set):
    save_data(train_set, "train", project_name)
    save_data(dev_set, "dev", project_name)
    save_data(test_set, "test", project_name)
    save_data(train_dev_set, "traindev", project_name)


def check_cols(df: pd.DataFrame, cols: list):
    """
    Check if a list of columns exists in a DataFrame.

    Parameters:
    - df: pandas DataFrame
    - col_list: list of column names to check

    Raises:
    - ValueError: If any column is not found in the DataFrame
    """
    # Get the columns in the DataFrame
    dataframe_columns = df.columns

    # Check if all columns in col_list are present in the DataFrame
    if not all(col in dataframe_columns for col in cols):
        missing_cols = [col for col in cols if col not in dataframe_columns]
        raise ValueError(f"Columns not found in DataFrame: {', '.join(missing_cols)}")


def prepare_raw(project_name: str, dataframes: list[pd.DataFrame]):
    """
    Process a list of dataframes for a specific project by selecting required columns,
    remap SDG names into a simpler format and combining the dfs into a single dataframe.

    Parameters:
    - project_name (str): The name of the project.
    - dataframes (list[pd.DataFrame]): A list of pandas DataFrames to be processed.
    """
    combined_df = pd.concat(dataframes)
    combined_df = combined_df[REQUIRED_COLS]

    map_cats = lambda cats: [REVERSE_SDG_MAP[sdg] for sdg in cats]
    map_ents = lambda ents: [
        [start, stop, REVERSE_SDG_MAP[sdg]] for start, stop, sdg in ents
    ]

    combined_df["cats"] = combined_df["cats"].apply(map_cats)
    combined_df["entities"] = combined_df["entities"].apply(map_ents)

    save_data(combined_df, "raw", project_name)


def main():
    """
    Take project files from /data/doccano_export and process and split the data.
    """
    for project_name, dataframes in get_doccano_export_paths():
        prepare_raw(project_name, dataframes)
        raw_df = load_data(get_file_path("raw", project_name))
        split_dfs = split_data(raw_df)
        save_splits(project_name, *split_dfs)


if __name__ == "__main__":
    main()
