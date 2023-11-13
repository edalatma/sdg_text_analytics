def predict(text: str) -> list[dict]:
    """
    Generate SDG predictions for a piece of text using an NLP model.

    Parameters:
    - text (str): A string representing the outline or course description
        for which predictions are to be made.

    Returns:
    list[dict]: A dictionary containing the model's predictions and additional metadata.
        Each dictionary value in the list contains the SDG that is predicted to belong
        to the text and metadata that provides supporting details that led to the positive
        prediction. This could include a confidence score that passed a certain threshold,
        a span of text that matches a keyword associated with an SDG or other details.

        Negative predictions should not be included in the list.


    Example:
    >>> outline = "This is a sample outline for testing purposes."
    >>> predictions = main(outline)
    >>> print(predictions)
    [
        {
            "category": "SDG-1",
            "metadata": {
                "confidence": 0.85,
                "spans": [[0, 10, "sample"]],
                "other": {} # Other information to include
            }
        },
        {
            "category": "SDG-8",
            "metadata": {
                "confidence": 0.6,
                "spans": [[16, 34, "test"]],
                "other": {} # Other information to include
            }
        }
    ]
    """
