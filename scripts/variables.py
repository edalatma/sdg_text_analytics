import os

#########
# PATHS #
#########

# Maps to `scripts/`
current_dir = os.path.dirname(__file__)
PREPARE_DATA_PATH = lambda ext: os.path.join(current_dir, "..", "data", ext)

# Location users place data
###########################

# Original doccano exports placed here
DOCCANO_EXPORT_FILES = lambda project_name="*": PREPARE_DATA_PATH(
    f"doccano_export/{project_name}/*.jsonl"
)
# Doccano export project dirs placed here
DOCCANO_EXPORT_DIRS = PREPARE_DATA_PATH("doccano_export/*")

# Location data is generated
############################

# Points to combined doccano export paths
RAW_TEMPLATE = lambda project_name="*": PREPARE_DATA_PATH(f"raw/{project_name}.jsonl")

# Points to train, dev, test, traindev paths
TEST_TEMPLATE = lambda project_name="*": PREPARE_DATA_PATH(
    f"processed/{project_name}__test.jsonl"
)
TRAIN_TEMPLATE = lambda project_name="*": PREPARE_DATA_PATH(
    f"processed/{project_name}__train.jsonl"
)
TRAINDEV_TEMPLATE = lambda project_name="*": PREPARE_DATA_PATH(
    f"processed/{project_name}__traindev.jsonl"
)
DEV_TEMPLATE = lambda project_name="*": PREPARE_DATA_PATH(
    f"processed/{project_name}__dev.jsonl"
)
# Paths that use "project_name"
PROJECTNAME_DATA_PATHS = {
    "raw": RAW_TEMPLATE,
    "test": TEST_TEMPLATE,
    "train": TRAIN_TEMPLATE,
    "traindev": TRAINDEV_TEMPLATE,
    "dev": DEV_TEMPLATE,
}

# Model paths
MODEL_TEMPLATE = lambda sdg="*", model_name="*": PREPARE_DATA_PATH(
    f"trained_models/{sdg}-{model_name}.dill"
)
GET_MODEL_DETAILS = lambda filename: filename.replace(".dill", "").split("-")

# Prediction paths
PREDICTIONS_TEMPLATE = (
    lambda sdg="*", model_name="*", project_name="*": PREPARE_DATA_PATH(
        f"predictions/{sdg}-{model_name}-{project_name}__predictions.jsonl"
    )
)
# Paths that use "sdg-model_name"
SDGMODEL_DATA_PATHS = {
    "models": MODEL_TEMPLATE,
    "predictions": PREDICTIONS_TEMPLATE,
}

##################
# DATA VARIABLES #
##################

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
