import dill


class TextAnalyticsFunctions:
    def __init__(self, sdg):
        self.sdg = sdg
        self.model_type = None
        self.model = None

    def train(self, training_text, training_labels):
        """
        Train model using set of text and expected labels.

        Parameters:
            - training_text (list or array-like): Input features.
            - training_labels (list or array-like): Target labels (binary).
        """
        if self.model_type == "rules":
            self.model = "ignore"
        elif self.model_type == "ml":
            self.model = self.train_ml_model(training_text, training_labels)
        else:
            raise ValueError(
                "Invalid model type. Supported types are 'rules' and 'ml'."
            )

    def predict(self, text):
        """
        Generate SDG predictions for a piece of text using an NLP model.

        Parameters:
        - text (str): A string representing the outline or course description
            for which predictions are to be made.

        Returns:
        dict: A dictionary containing the model's prediction and additional metadata.
            The dict contains the SDG that is predicted to belong to the text and metadata
            that provides supporting details that led to the positive prediction. This
            could include a confidence score that passed a certain threshold,
            a span of text that matches a keyword associated with an SDG or other details.
            Negative predictions should not be included in the list.


        Example:
        >>> outline = "This is a sample outline for testing purposes."
        >>> prediction = main(outline)
        >>> print(prediction)
        {
            "category": "SDG-8",
            "prediction": 0,
            "metadata": {
                "confidence": 0.6,
                "spans": [[16, 34, "test"]],
                "other": {} # Other information to include
            }
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")

        if self.model_type == "rules":
            prediction, metadata = self.predict_rules_model(text)
        elif self.model_type == "ml":
            prediction, metadata = self.predict_ml_model(text)
        else:
            raise ValueError(
                "Invalid model type. Supported types are 'rules' and 'ml'."
            )

        return dict(category=self.sdg, prediction=prediction, metadata=metadata)

    def save(self, file_path):
        """
        Save the entire class to a file.

        Parameters:
            - file_path (str): File path to save the model.
        """
        with open(file_path, "wb") as file:
            dill.dump(self, file)

    def __repr__(self):
        return f"{self.sdg}__{self.model_type}__{self.model}"
