from scripts.base_model import TextAnalyticsFunctions
from sklearn.model_selection import KFold, GridSearchCV
import pandas as pd
import re


class TextAnalyticsModel(TextAnalyticsFunctions):
    def __init__(self, sdg):
        super().__init__(sdg)

        # Uncomment the one you will be creating
        # --------------------------------------
        self.model_type = "rules"
        # self.model_type = "ml"

        # Add other variables you need to persist across the model
        self.dictionary = self.load_dict()

    def load_dict(self):
        path = "./models/resources/uoft_sdg_keywords.xlsx"
        df = pd.read_excel(path)
        df["Keywords"] = df["Keywords"].apply(
            lambda s: [t.strip() for t in s.split(",")]
        )
        return dict(zip(df["SDG"], df["Keywords"]))

    def predict_rules_model(self, text):
        metadata = {"keyword_matches": []}
        prediction = 0

        # Implement rules-based prediction logic
        for keyword in self.dictionary[self.sdg]:
            match = bool(re.search(keyword, text))
            if match:
                metadata["keyword_matches"].append(keyword)
                prediction = 1
        # End of implementation

        return prediction, metadata


def main():
    pass


if __name__ == "__main__":
    main()
