"""
Important note:
--------------------------------------------------------------------------------------------------
This model is only meant to identify courses that are have are 
sustainability-focused by identifying courses that contain the term "sustain*".

Because of how this project is set up, predictions have to be tied to one SDG, so
you'll see SDG-1 predictions tied to this project.


STARS Definition:
--------------------------------------------------------------------------------------------------
A. Sustainability-focused courses (a.k.a. “sustainability courses”)

To count as sustainability-focused, the course title or description must indicate a primary and explicit
focus on sustainability. This includes:

● Foundational courses with a primary and explicit focus on sustainability (e.g., Introduction to
    Sustainability, Sustainable Development, Sustainability Science).
● Courses with a primary and explicit focus on the application of sustainability within a field (e.g.,
    Architecture for Sustainability, Green Chemistry, Sustainable Agriculture, Sustainable Business).
    As sustainability is an interdisciplinary topic, such courses generally incorporate insights from
    multiple disciplines.
● Courses with a primary and explicit focus on a major sustainability challenge (e.g., Climate
    Change Science, Environmental Justice, Global Poverty and Development, Renewable Energy
    Policy). The focus of such courses might be on providing knowledge and understanding of the
    problems and/or the tools for solving them.

The course title or description does not have to use the term “sustainability” to count as
sustainability-focused if the primary and explicit focus of the course is on the interdependence of
ecological and social/economic systems or a major sustainability challenge. If the course title and
description do not unequivocally indicate such a focus, but it is evident from the course description or
syllabus that the course incorporates sustainability challenges, issues, and concepts in a prominent way,
the course may qualify as sustainability inclusive.
"""

from scripts.base_model import TextAnalyticsFunctions
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
        d = {"SDG 1": ["sustain*"]}

        return d

    def predict_rules_model(self, text):
        metadata = {"keyword_matches": [], "sustainability_focused": False}
        prediction = 0

        # Implement rules-based prediction logic
        for keyword in self.dictionary.get(self.sdg, []):
            query = rf"\b{keyword}"
            match = bool(re.search(query, text))
            if match:
                metadata["keyword_matches"].append(keyword)
                metadata["sustainability_focused"] = True
                prediction = 1
        # End of implementation

        return prediction, metadata


def main():
    pass


if __name__ == "__main__":
    main()
