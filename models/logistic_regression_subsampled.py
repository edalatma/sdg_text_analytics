import sys

sys.path.append("../scripts")
from base_model import TextAnalyticsFunctions
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import FunctionTransformer
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler


class TextAnalyticsModel(TextAnalyticsFunctions):
    def __init__(self, sdg):
        super().__init__(sdg)

        # Uncomment the one you will be creating
        # --------------------------------------
        # self.model_type = "rules"
        self.model_type = "ml"

        # Add other variables you need to persist across the model

    def preprocess_text(self, text_list):
        processed_texts = []
        for text in text_list:
            # Tokenization
            words = nltk.word_tokenize(text)

            # Remove stopwords
            stop_words = set(stopwords.words("english"))
            words = [word for word in words if word.lower() not in stop_words]

            # Stemming
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]

            processed_texts.append(" ".join(words))

        return processed_texts

    def train_ml_model(self, training_text, training_labels):
        model = None
        print(self.sdg, sum(training_labels))
        # Implement machine learning-based training logic
        pipeline = Pipeline(
            [
                ("preprocessor", FunctionTransformer(self.preprocess_text)),
                ("tfidf", TfidfVectorizer()),
                ("sampler", RandomUnderSampler(random_state=0)),
                ("classifier", LogisticRegression()),
            ]
        )

        # Define parameter grid for GridSearchCV
        hyperparameters = {
            "tfidf__max_features": [1000, 5000, 10000],
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "classifier__C": [0.1, 1, 10],
            "classifier__penalty": ["l2"],
        }

        grid_search = GridSearchCV(pipeline, hyperparameters, cv=5, n_jobs=-1)

        grid_search.fit(list(training_text), list(training_labels))
        model = grid_search.best_estimator_
        # End of implementation

        return model

    def predict_ml_model(self, text):
        metadata = {}
        prediction = 0

        # Implement machine learning-based prediction logic
        #
        predicted_probs = self.model.predict_proba([text])

        # Find the class with the highest probability
        prediction = predicted_probs.argmax(axis=1)[0]
        highest_probability = predicted_probs[0, prediction]

        metadata["confidence"] = highest_probability
        # End of implementation

        return prediction, metadata


def main():
    pass


if __name__ == "__main__":
    main()
