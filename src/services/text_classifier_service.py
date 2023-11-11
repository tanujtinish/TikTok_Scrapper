from transformers import pipeline

class TextClassifierService:
    def __init__(self, model_name='facebook/bart-large-mnli'):
        self.classifier = pipeline('zero-shot-classification', model=model_name)

    def classify_text(self, text, labels, hypothesis_template='This text is about {}'):
        """
        Classify the given text against a list of labels.

        Args:
            text (str): The input text to classify.
            labels (list): List of labels to classify against.
            hypothesis_template (str): Template for zero-shot classification.

        Returns:
            dict: Classification results.
        """
        prediction = self.classifier(text, labels, hypothesis_template=hypothesis_template, multi_class=True)
        return prediction


#https://stackoverflow.com/questions/65262832/pre-trained-models-for-text-classification
# Example usage
if __name__ == "__main__":
    # Create an instance of the TextClassifierService
    classifier_service = TextClassifierService()

    # Define labels and text to classify
    labels = ["fasion"]
    text = "zara"

    # Perform classification
    classification_result = classifier_service.classify_text(text, labels)

    # Print the classification result
    app.logger.info(classification_result)
