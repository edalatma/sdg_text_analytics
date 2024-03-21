from scripts.variables import (
    GET_PREDICTION_DETAILS,
    PROJECTNAME_DATA_PATHS,
    PREDICTIONS_TEMPLATE,
    ALL_EVAL_RESULTS_PATH,
)
from scripts.file_org import load_data
import os
import numpy as np
from glob import glob
import pandas as pd


def iter_prediction_files():
    for filepath in glob(PREDICTIONS_TEMPLATE()):
        predictions = load_data(filepath)
        yield filepath, predictions


def load_original_file(prediction_path):
    filename = os.path.basename(prediction_path)
    sdg, model_name, project_name, datatype = GET_PREDICTION_DETAILS(filename)

    original_filepath = PROJECTNAME_DATA_PATHS[datatype](sdg, project_name)
    original_data = load_data(original_filepath)

    return sdg, model_name, project_name, datatype, original_data


def get_original_label(original_data, sdg, index):
    original_label = int(sdg in original_data.loc[index]["labels"])
    return original_label


def get_metrics(comparison_counts):
    TP = comparison_counts.get("TP", 0)
    FP = comparison_counts.get("FP", 0)
    TN = comparison_counts.get("TN", 0)
    FN = comparison_counts.get("FN", 0)

    if (TP + FP) == 0:
        precision = np.nan
    else:
        precision = TP / (TP + FP)

    if (TP + FN) == 0:
        recall = np.nan
    else:
        recall = TP / (TP + FN)

    if precision >= 0 or recall >= 0:
        f1 = (2 * precision * recall) / (precision + recall)
    else:
        f1 = np.nan
    return dict(precision=precision, recall=recall, f1=f1, TP=TP, FP=FP, TN=TN, FN=FN)


def compare(pred, ori):
    if pred == 1 and ori == 1:
        return "TP"
    elif pred == 1 and ori == 0:
        return "FP"
    elif pred == 0 and ori == 1:
        return "FN"
    elif pred == 0 and ori == 0:
        return "TN"


def eval_predictions():
    all_results = []
    for filepath, predictions in iter_prediction_files():
        sdg, model_name, project_name, datatype, original_data = load_original_file(
            filepath
        )

        all_comparisons = []
        original_labels = []
        for i, prediction in predictions.iterrows():
            original_label = get_original_label(original_data, sdg, prediction["index"])
            comparison = compare(prediction["prediction"]["prediction"], original_label)
            all_comparisons.append(comparison)
            original_labels.append(original_label)

        predictions["original_label"] = original_labels
        predictions["comparison"] = all_comparisons
        overall_comparisons = dict(predictions.value_counts("comparison"))
        all_results.append(
            dict(
                sdg=sdg,
                model_name=model_name,
                project_name=project_name,
                datatype=datatype,
                **get_metrics(overall_comparisons),
            )
        )

        predictions.to_json(filepath, orient="records", lines=True)
    pd.DataFrame(all_results).to_json(
        ALL_EVAL_RESULTS_PATH, orient="records", lines=True
    )
