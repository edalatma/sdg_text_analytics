import os

#########
# PATHS #
#########

# Maps to `scripts/`
current_dir = os.path.dirname(__file__)

# DATA PATHS
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

# DOCCANO EXPORT DATA DIRS
DOCCANO_DIRS_PATH = os.path.join(current_dir, "..", "data/doccano_export/*")
DOCCANO_EXPORTS_TEMPLATE = lambda project_name: os.path.join(
    current_dir, "..", f"data/doccano_export/{project_name}/*.jsonl"
)

# MODEL FILENAME
GET_MODEL_FILENAME = lambda sdg, model_name: f"{sdg}__{model_name}.dill"

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
